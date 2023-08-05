class _GetchUnix:
    def __call__(self):
        import sys, tty, termios

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


getch = None
try:
    import msvcrt

    # MS Windows
    getch = msvcrt.getch()

except ImportError:
    getch = _GetchUnix()
