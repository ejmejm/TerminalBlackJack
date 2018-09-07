# https://stackoverflow.com/questions/1394956/how-to-do-hit-any-key-in-python
try:
    # Win32
    from msvcrt import getch
except ImportError:
    # UNIX
    def getch():
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
