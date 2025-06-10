from TLib import *
from TLib.T_imports import *
import TLib.T_LW3T


class LW3T(T_Process.TProcess):
    def Run(self, master: 'Termination4.Termination'):
        self.master=master
        self.desc="Thread Web & Local Time Task Table"
        self.L3T=T_LW3T.L3T(self.master)
        self.scheduler = TLib.T_LW3T.TaskScheduler(self.ExecuteCallBack)
        try:
            self.__init_scheduler__()
            self._stop_event.wait()
        finally:
            self.scheduler.shutdown()
    def __init_scheduler__(self):
        L3T=self.L3T.read()
        for i in L3T:
            if self.scheduler.add_task(L3T[i]):
                print(f"Task {L3T[i]['TaskUUID']} Add Successful")
        print("Task List:")
        for TaskID, TaskINFO in self.scheduler.list_tasks().items():
            print(f"ID: {TaskID}, Name: {TaskINFO['TaskName']}")

    def get(self):
        return self.L3T.read()
    def insert(self, TaskUUID, TaskDict):
        if self.L3T.Is(TaskUUID):
            return False
        if not self.L3T.writekc(TaskUUID, TaskDict):
            return False
        if not self.scheduler.add_task(TaskDict):
            return False
        return True
    def remove(self, TaskUUID):
        self.scheduler.remove_task(TaskUUID)
        return self.L3T.remove(TaskUUID)
    def change(self, TaskUUID, TaskDict):
        self.remove(TaskUUID)
        self.insert(TaskUUID, TaskDict)
        return False
    def ExecuteCallBack(self, task: dict, _code: str, _type: str):
        EBUF=LW3TExecuteCallBack(self.master, task, _code, _type)
        self.master.TProcessManager.AddThread(EBUF)
        EBUF.start()



class LW3TExecuteCallBack(T_Process.TProcess):
    def Run(self, master: 'Termination4.Termination', task: dict, _code: str, _type: str):
        self.master=master
        self.desc=f"Thread [{task["TaskName"]}] [{task["TaskUUID"]}]"
        if _type == "1":
            exec(_code, self.master.WorkENV)
        if _type == "2":
            for i in _code.split("\n"):
                subprocess.Popen(i, shell=True).wait()