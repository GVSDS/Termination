from .T_imports import *
from . import T_FIO


class TProcess(threading.Thread):
    """
    Thread Process
    """
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.Args = args
        self.Kwargs = kwargs
        self._stop_event = threading.Event()
        self._manager = None
        self.desc=""
        self.progress=0
    
    def set_manager(self, manager):
        """设置线程管理器"""
        self._manager = manager
    
    def Run(self):
        """线程主函数，由子类实现"""
        raise NotImplementedError("Subclasses must implement Run method")
    
    def run(self):
        """重写Thread的run方法"""
        try:
            # Notify manager that thread is starting
            if self._manager:
                self._manager._on_thread_start(self.name)
            self.Run(*self.Args, **self.Kwargs)
        except SystemExit:
            pass
        except:
            traceback.print_exc()
        finally:
            # 线程结束时自动从管理器中移除
            if self._manager:
                self._manager._on_thread_end(self.name)
                self._manager.RemoveThread(self.name)
    
    def join(self, timeout=None):
        """重写join方法，确保线程结束后从管理器中移除"""
        super().join(timeout)
        if self._manager and not self.is_alive():
            self._manager._on_thread_end(self.name)
            self._manager.RemoveThread(self.name)
    
    def Stop(self):
        """线程自杀方法"""
        self._stop_event.set()
        self.join()  # 等待线程结束
    
    def ShouldStop(self) -> bool:
        """检查是否应该停止线程"""
        return self._stop_event.is_set()

class TProcessManager:
    """
    Thread Process Manager
    """
    def __init__(self):
        self._threads: typing.Dict[str, TProcess] = {}
        self._lock = threading.Lock()
        self._start_callbacks = {}
        self._end_callbacks = {}
        self._callback_id_counter = 0
    
    def _on_thread_start(self, thread_name: str):
        """内部方法：线程启动时调用"""
        with self._lock:
            for callback in self._start_callbacks.values():
                try:
                    callback(thread_name)
                except:
                    traceback.print_exc()
    
    def _on_thread_end(self, thread_name: str):
        """内部方法：线程结束时调用"""
        with self._lock:
            for callback in self._end_callbacks.values():
                try:
                    callback(thread_name)
                except:
                    traceback.print_exc()
    
    def add_start_callback(self, callback: typing.Callable[[str], None]) -> int:
        """
        添加线程启动回调
        :param callback: 回调函数，接受线程名称作为参数
        :return: 回调ID，可用于移除回调
        """
        with self._lock:
            self._callback_id_counter += 1
            callback_id = self._callback_id_counter
            self._start_callbacks[callback_id] = callback
            return callback_id

    def add_end_callback(self, callback: typing.Callable[[str], None]) -> int:
        """
        添加线程结束回调
        :param callback: 回调函数，接受线程名称作为参数
        :return: 回调ID，可用于移除回调
        """
        with self._lock:
            self._callback_id_counter += 1
            callback_id = self._callback_id_counter
            self._end_callbacks[callback_id] = callback
            return callback_id
    
    def remove_start_callback(self, callback_id: int) -> bool:
        """
        移除线程启动回调
        :param callback_id: 回调ID
        :return: 是否移除成功
        """
        with self._lock:
            if callback_id in self._start_callbacks:
                del self._start_callbacks[callback_id]
                return True
            return False
    
    def remove_end_callback(self, callback_id: int) -> bool:
        """
        移除线程结束回调
        :param callback_id: 回调ID
        :return: 是否移除成功
        """
        with self._lock:
            if callback_id in self._end_callbacks:
                del self._end_callbacks[callback_id]
                return True
            return False
    
    def clear_start_callbacks(self):
        """清除所有线程启动回调"""
        with self._lock:
            self._start_callbacks.clear()
    
    def clear_end_callbacks(self):
        """清除所有线程结束回调"""
        with self._lock:
            self._end_callbacks.clear()
    
    def AddThread(self, thread: TProcess, name: typing.Optional[str] = None) -> bool:
        """
        添加线程到管理器
        :param thread: 线程对象
        :param name: 线程名称，如果不指定则使用线程默认名称
        :return: 是否添加成功
        """
        with self._lock:
            thread_name = name if name else thread.name
            if thread_name in self._threads:
                return False
            thread.name = thread_name  # 确保线程名称设置正确
            thread.set_manager(self)  # 设置管理器引用
            self._threads[thread_name] = thread
            return True
    
    def RemoveThread(self, name: str) -> bool:
        """
        从管理器移除线程
        :param name: 线程名称
        :return: 是否移除成功
        """
        with self._lock:
            if name not in self._threads:
                return False
            # 清除线程的管理器引用
            if self._threads[name]._manager == self:
                self._threads[name]._manager = None
            del self._threads[name]
            return True
    
    def GetThread(self, name: str) -> typing.Optional[TProcess]:
        """
        获取指定名称的线程
        :param name: 线程名称
        :return: 线程对象或None
        """
        with self._lock:
            return self._threads.get(name)
    
    def GetAllThreads(self) -> typing.Dict[str, TProcess]:
        """
        获取所有线程
        :return: 线程字典
        """
        with self._lock:
            return self._threads.copy()
    
    def StopThread(self, name: str) -> bool:
        """
        优雅停止线程（通过设置停止标志）
        :param name: 线程名称
        :return: 是否停止成功
        """
        thread = self.GetThread(name)
        if thread:
            thread.Stop()
            return True
        return False

    def KillThread(self, name: str) -> bool:
        """
        强制杀死线程（通过ctypes API）
        :param name: 线程名称
        :return: 是否杀死成功
        """
        thread = self.GetThread(name)

        if not thread:
            return False
        
        thread._stop_event.set()

        self._on_thread_end(name)

        if not thread.is_alive():
            self.RemoveThread(name)
            return True
        
        thread_id = thread.ident
        if not thread_id:
            return False
        
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
            ctypes.c_long(thread_id), 
            ctypes.py_object(SystemExit))
        
        if res == 0:
            return False
        elif res != 1:
            # 如果返回值大于1，需要重置状态
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, None)
            return False
        
        # 等待线程实际结束
        #thread.join()
        self.RemoveThread(name)
        return True
    
    def StopAllThreads(self) -> None:
        """优雅停止所有线程"""
        threads = self.GetAllThreads()
        for name in list(threads.keys()):  # 使用keys的副本避免修改问题
            self.StopThread(name)
    
    def KillAllThreads(self) -> None:
        """强制杀死所有线程"""
        threads = self.GetAllThreads()
        for name in list(threads.keys()):  # 使用keys的副本避免修改问题
            try: self.KillThread(name)
            except: print(f"EKill: [{name}]")