import ctypes

SECONDS_TO_UNIX_EPOCH = 11644473600

class FILETIME(ctypes.Structure):
    _fields_ = [("dwLowDateTime", ctypes.c_uint),
                ("dwHighDateTime", ctypes.c_uint)]

def time():
    """Accurate version of time.time() for windows, return UTC time in term of seconds since 01/01/1601
"""
    file_time = FILETIME()
    ctypes.windll.kernel32.GetSystemTimePreciseAsFileTime(ctypes.byref(file_time))
    return ((file_time.dwLowDateTime + (file_time.dwHighDateTime << 32)) / 1.0e7) - SECONDS_TO_UNIX_EPOCH