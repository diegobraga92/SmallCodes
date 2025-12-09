import ctypes

libc = ctypes.CDLL(None)
printf = libc.printf
printf(b"hello %d\n", 123)