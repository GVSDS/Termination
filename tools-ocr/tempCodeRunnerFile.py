class DLL(ctypes.CDLL):
    def __init__(self, DLL_Path, mode=ctypes.DEFAULT_MODE, handle=None,
                 use_errno=False,
                 use_last_error=False,
                 winmode=None):
        super().__init__(DLL_Path, mode=mode, handle=handle,
                         use_errno=use_errno,
                         use_last_error=use_last_error,
                         winmode=winmode)