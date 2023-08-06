"""
MicroPython Remote - Interaction and automation tool for MicroPython
MIT license; Copyright (c) 2019-2021 Damien P. George

This program provides a set of utilities to interact with and automate a
MicroPython device over a serial connection.  Commands supported are:

    mpremote                         -- auto-detect, connect and enter REPL

    mpremote <device-shortcut>       -- connect to given device
    mpremote connect <device>        -- connect to given device
    mpremote mount <local-dir>       -- mount local directory on device

    mpremote eval <string>           -- evaluate and print the string
    mpremote exec <string>           -- execute the string
    mpremote fs <command> <args...>  -- execute filesystem commands on the device
    mpremote repl                    -- enter REPL
    mpremote run <script>            -- run the given local script

Multiple commands can be specified and they will be run sequentially.  The
serial device will be automatically detected if not specified.  If no action
is specified then the REPL will be entered.

Examples:
    mpremote
    mpremote a1
    mpremote connect /dev/ttyUSB0 repl
    mpremote ls
    mpremote a1 ls
    mpremote exec "import micropython; micropython.mem_info()"
    mpremote eval 1/2 eval 3/4
    mpremote mount .
    mpremote mount . exec "import local_script"
    mpremote ls
    mpremote cat boot.py
"""

import os, select, sys, time
import serial.tools.list_ports

from . import pyboardextended as pyboard
from .console import Console, ConsolePosix

_PROG = "mpremote"

device_shortcuts = {
    "a0": "/dev/ttyACM0",
    "a1": "/dev/ttyACM1",
    "a2": "/dev/ttyACM2",
    "a3": "/dev/ttyACM3",
    "u0": "/dev/ttyUSB0",
    "u1": "/dev/ttyUSB1",
    "u2": "/dev/ttyUSB2",
    "u3": "/dev/ttyUSB3",
    "c0": "COM0",
    "c1": "COM1",
    "c2": "COM2",
    "c3": "COM3",
}

_BUILTIN_COMMAND_EXPANSIONS = {
    "cat": "fs cat",
    "ls": "fs ls",
    "cp": "fs cp",
    "rm": "fs rm",
    "mkdir": "fs mkdir",
    "rmdir": "fs rmdir",
    "df": [
        "exec",
        "import uos\nprint('mount \\tsize \\tused \\tavail \\tuse%')\nfor _m in [''] + uos.listdir('/'):\n _s = uos.stat('/' + _m)\n if not _s[0] & 1 << 14: continue\n _s = uos.statvfs(_m)\n if _s[0]:\n  _size = _s[0] * _s[2]; _free = _s[0] * _s[3]; print(_m, _size, _size - _free, _free, int(100 * (_size - _free) / _size), sep='\\t')",
    ],

    "reset t_ms=100": [
        "exec",
        "--no-follow",
        "import utime, umachine; utime.sleep_ms(t_ms); umachine.reset()",
    ],
    "bootloader t_ms=100": [
        "exec",
        "--no-follow",
        "import utime, umachine; utime.sleep_ms(t_ms); umachine.bootloader()",
    ],
    "setrtc": [
        "exec",
        "import machine; machine.RTC().datetime((2020, 1, 1, 0, 10, 0, 0, 0))"
    ],
}

def load_user_config():
    # Create empty config object.
    config = __build_class__(lambda:None, "Config")()
    config.commands = {}

    # Get config file name.
    path = os.getenv("XDG_CONFIG_HOME")
    if path is None:
        path = os.getenv("HOME")
        if path is None:
            return config
        path = os.path.join(path, ".config")
    path = os.path.join(path, _PROG)
    config_file = os.path.join(path, "config.py")

    # Check if config file exists.
    if not os.path.exists(config_file):
        return config

    # Exec the config file in its directory.
    with open(config_file) as f:
        config_data = f.read()
    prev_cwd = os.getcwd()
    os.chdir(path)
    exec(config_data, config.__dict__)
    os.chdir(prev_cwd)

    return config


def prepare_command_expansions(config):
    global _command_expansions

    _command_expansions = {}

    for command_set in (_BUILTIN_COMMAND_EXPANSIONS, config.commands):
        for cmd, sub in command_set.items():
            cmd = cmd.split()
            if len(cmd) == 1:
                args = ()
            else:
                args = tuple(c.split("=") for c in cmd[1:])
            if isinstance(sub, str):
                sub = sub.split()
            _command_expansions[cmd[0]] = (args, sub)


def do_command_expansion(args):
    def usage_error(cmd, exp_args, msg):
        print(f"Command {cmd} {msg}; signature is:")
        print("   ", cmd, " ".join("=".join(a) for a in exp_args))
        sys.exit(1)

    last_arg_idx = len(args)
    pre = []
    while args and args[0] in _command_expansions:
        cmd = args.pop(0)
        exp_args, exp_sub = _command_expansions[cmd]
        for exp_arg in exp_args:
            exp_arg_name = exp_arg[0]
            if args and "=" not in args[0]:
                # Argument given without a name.
                value = args.pop(0)
            elif args and args[0].startswith(exp_arg_name + "="):
                # Argument given with correct name.
                value = args.pop(0).split("=", 1)[1]
            else:
                # No argument given, or argument given with a different name.
                if len(exp_arg) == 1:
                    # Required argument (it has no default).
                    usage_error(cmd, exp_args, f"missing argument {exp_arg_name}")
                else:
                    # Optional argument with a default.
                    value = exp_arg[1]
            pre.append(f"{exp_arg_name}={value}")

        args[0:0] = exp_sub
        last_arg_idx = len(exp_sub)

    if last_arg_idx < len(args) and "=" in args[last_arg_idx]:
        # Extra unknown arguments given.
        arg = args[last_arg_idx].split("=", 1)[0]
        usage_error(cmd, exp_args, f"given unexpected argument {arg}")
        sys.exit(1)

    # Insert expansion with optional setting of arguments.
    if pre:
        args[0:0] = ["exec", ";".join(pre)]

def do_connect(args):
    try:
        if args and (args[0] == "connect" or args[0] in device_shortcuts):
            if args[0] == "connect":
                args.pop(0)
            dev = args.pop(0)
            dev = device_shortcuts.get(dev, dev)
            return pyboard.PyboardExtended(dev, baudrate=115200)
        else:
            # auto-detect and auto-connect
            ports = serial.tools.list_ports.comports()
            for dev in device_shortcuts.values():
                if any(p.device == dev for p in ports):
                    try:
                        return pyboard.PyboardExtended(dev, baudrate=115200)
                    except pyboard.PyboardError as er:
                        if not er.args[0].startswith("failed to access"):
                            raise er
            raise pyboard.PyboardError("no device found")
    except pyboard.PyboardError as er:
        msg = er.args[0]
        if msg.startswith("failed to access"):
            msg += " (it may be in use by another program)"
        print(msg)
        sys.exit(1)


def do_filesystem(pyb, args):
    def _list_recursive(files, path):
        if os.path.isdir(path):
            for entry in os.listdir(path):
                _list_recursive(files, os.path.join(path, entry))
        else:
            files.append(os.path.split(path))

    if args[0] == "cp" and args[1] == "-r":
        args.pop(0)
        args.pop(0)
        assert args[-1] == ":"
        args.pop()
        src_files = []
        for path in args:
            _list_recursive(src_files, path)
        known_dirs = {""}
        pyb.exec_("import uos")
        for dir, file in src_files:
            dir_parts = dir.split("/")
            for i in range(len(dir_parts)):
                d = "/".join(dir_parts[: i + 1])
                if d not in known_dirs:
                    pyb.exec_("try:\n uos.mkdir('%s')\nexcept OSError as e:\n print(e)" % d)
                    known_dirs.add(d)
            pyboard.filesystem_command(pyb, ["cp", os.path.join(dir, file), ":" + dir + "/"])
    else:
        pyboard.filesystem_command(pyb, args)
    args.clear()


def do_repl_main_loop(pyb, console_in, console_out_write, file_to_inject):
    while True:
        if isinstance(console_in, ConsolePosix):
            # TODO pyb.serial might not have fd
            select.select([console_in.infd, pyb.serial.fd], [], [])
        else:
            while not (console_in.inWaiting() or pyb.serial.inWaiting()):
                time.sleep(0.01)
        c = console_in.readchar()
        if c:
            if c == b"\x1d":  # ctrl-], quit
                break
            elif c == b"\x04":  # ctrl-D
                # do a soft reset and reload the filesystem hook
                pyb.soft_reset_with_mount(console_out_write)
            elif c == b"\x0a":  # ctrl-j, inject code
                pyb.serial.write(b"print('test')-----------------------------------aaaaa")
            elif c == b"\x0b":  # ctrl-k, inject script
                console_out_write(bytes("Injecting %s\r\n" % file_to_inject, "utf8"))
                pyb.enter_raw_repl_without_soft_reset()
                with open(file_to_inject, "rb") as f:
                    pyfile = f.read()
                try:
                    pyb.exec_raw_no_follow(pyfile)
                except pyboard.PyboardError as er:
                    console_out_write(b"Error:\r\n")
                    console_out_write(er)
                pyb.exit_raw_repl()
            else:
                pyb.serial.write(c)

        try:
            n = pyb.serial.inWaiting()
        except OSError as er:
            if er.args[0] == 5:  # IO error, device disappeared
                print("device disconnected")
                break

        if n > 0:
            c = pyb.serial.read(1)
            if c is not None:
                # pass character through to the console
                oc = ord(c)
                if oc in (8, 9, 10, 13, 27) or 32 <= oc <= 126:
                    console_out_write(c)
                else:
                    console_out_write(b"[%02x]" % ord(c))


def do_repl(pyb, args):
    if len(args) and args[0] == "--capture":
        args.pop(0)
        capture_file = args.pop(0)
    else:
        capture_file = None

    file_to_inject = args.pop(0) if len(args) else None

    print("Connected to MicroPython at %s" % pyb.device_name)
    print("Use Ctrl-] to exit this shell")
    if capture_file is not None:
        print('Capturing session to file "%s"' % capture_file)
        capture_file = open(capture_file, "wb")
    if file_to_inject is not None:
        print('Use Ctrl-K to inject file "%s"' % file_to_inject)

    console = Console()
    console.enter()

    def console_out_write(b):
        console.write(b)
        if capture_file is not None:
            capture_file.write(b)
            capture_file.flush()

    try:
        do_repl_main_loop(pyb, console, console_out_write, file_to_inject)
    finally:
        console.exit()
        if capture_file is not None:
            capture_file.close()


def execbuffer(pyb, buf, follow):
    ret_val = 0
    try:
        pyb.exec_raw_no_follow(buf)
        if follow:
            ret, ret_err = pyb.follow(timeout=None, data_consumer=pyboard.stdout_write_bytes)
            if ret_err:
                pyboard.stdout_write_bytes(ret_err)
                ret_val = 1
    except pyboard.PyboardError as er:
        print(er)
        ret_val = 1
    except KeyboardInterrupt:
        ret_val = 1
    return ret_val


def main():
    config = load_user_config()
    prepare_command_expansions(config)

    args = sys.argv[1:]
    pyb = do_connect(args)
    in_raw_repl = False
    did_action = False

    try:
        while args:
            do_command_expansion(args)

            cmds = {
                "mount": (True, False, 1),
                "repl": (False, True, 0),
                "eval": (True, True, 1),
                "exec": (True, True, 1),
                "run": (True, True, 1),
                "fs": (True, True, 1),
            }
            cmd = args.pop(0)
            try:
                need_raw_repl, is_action, num_args_min = cmds[cmd]
            except KeyError:
                print(f"{_PROG}: '{cmd}' is not a command")
                return 1

            if need_raw_repl:
                if not in_raw_repl:
                    pyb.enter_raw_repl()
                    in_raw_repl = True
            else:
                if in_raw_repl:
                    pyb.exit_raw_repl()
                    in_raw_repl = False
            if is_action:
                did_action = True
            if len(args) < num_args_min:
                print(f"{_PROG}: '{cmd}' neads at least {num_args_min} argument(s)")

            if cmd == "mount":
                path = args.pop(0)
                pyb.mount_local(path)
                print(f"Local directory {path} is mounted at /remote")
            elif cmd in ("exec", "eval", "run"):
                follow = True
                if args[0] == "--no-follow":
                    args.pop(0)
                    follow = False
                if cmd == "exec":
                    buf = args.pop(0)
                elif cmd == "eval":
                    buf = "print(" + args.pop(0) + ")"
                else:
                    filename = args.pop(0)
                    try:
                        with open(filename, "rb") as f:
                            buf = f.read()
                    except OSError:
                        print(f"{_PROG}: could not read file '{filename}'")
                        return 1
                ret = execbuffer(pyb, buf, follow)
                if ret:
                    return ret
            elif cmd == "fs":
                do_filesystem(pyb, args)
            elif cmd == "repl":
                do_repl(pyb, args)

        if not did_action:
            if in_raw_repl:
                pyb.exit_raw_repl()
                in_raw_repl = False
            do_repl(pyb, args)
    finally:
        if pyb is not None:
            if pyb.mounted:
                if not in_raw_repl:
                    pyb.enter_raw_repl_without_soft_reset()
                    in_raw_repl = True
                pyb.umount_local()
            if in_raw_repl:
                try:
                    pyb.exit_raw_repl()
                except:
                    # pyboard.filesystem_command will close the connecton on error
                    pass
            pyb.close()
