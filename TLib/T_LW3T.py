from .T_imports import *
from .T_FIO import FIO


class L3T:
    def __init__(self, master: 'Termination4.Termination'):
        self.master=master
        self.__init_values__()
    def __init_values__(self):
        if hasattr(self.master.PDir, "__need_L3T__"):
            self.__need_L3T__=self.master.PDir.__need_L3T__
            self.L3T: dict=ast.literal_eval(self.master.GodKeys.decrypt(FIO.openr(self.__need_L3T__, 2)))["LocalTimeTaskTable"]
            print(f"L3T: {self.L3T}")
        else:
            print("L3T: __need_L3T__ not in PDir")
    def write(self, j):
        try: FIO.openw(self.__need_L3T__, self.master.GodKeys.encrypt(str({"LocalTimeTaskTable": j})), 2)
        except:
            print(traceback.format_exc())
            return False
        return True
    def save(self):
        return self.write(self.L3T)
    def get(self, key):
        if key in self.L3T: return self.L3T[key]
        return False
    def writek(self, key, value):
        if key in self.L3T:
            return False
        self.L3T[key]=value
        return self.save()
    def writekc(self, key, value):
        self.L3T[key]=value
        return self.save()
    def remove(self, key):
        if key not in self.L3T:
            return False
        self.L3T.pop(key)
        return self.save()
    def Is(self, key):
        return key in self.L3T
    def read(self):
        return self.L3T


class Task:
    """Task Type, Encapsulating Task Attributes And Behaviors."""
    
    def __init__(self, task_data: typing.Dict):
        """
        初始化任务
        :param task_data: 任务数据字典
        """
        self.task_data=task_data
        self.uuid = task_data.get('TaskUUID', GUUID())
        self.name = task_data.get('TaskName', 'Unnamed Task')
        self.e_time_type = task_data.get('ETimeType')
        self.e_time = task_data.get('ETime')
        self.r_time_type = task_data.get('RTimeType')
        self.r_time = task_data.get('RTime')
        self.r_code = task_data.get('RCode')
        self.r_type = task_data.get('RType')
        
        # 验证必要字段
        if not all([self.e_time_type, self.r_time_type, self.r_code]):
            raise ValueError("Missing Necessary Task Parameters")

    def is_effective(self) -> bool:
        """检查任务是否在生效时间内"""
        now = datetime.now(pytz.timezone('Asia/Shanghai'))
        
        try:
            if self.e_time_type == '1':  # 具体时间
                effective_time = datetime.strptime(self.e_time, '%Y-%m-%d %H:%M:%S')
                effective_time = pytz.timezone('Asia/Shanghai').localize(effective_time)
                return now >= effective_time
            
            elif self.e_time_type == '2':  # 每日执行时间
                hour, minute, second = map(int, self.e_time.split(':'))
                effective_time = now.replace(hour=hour, minute=minute, second=second)
                return now >= effective_time
            
            # 其他类型默认返回True
            return True
        except Exception as e:
            print(f"Failed To Check The Effective Time Of Task {self.uuid}: {e}")
            return False

    def create_trigger(self) -> typing.Optional[typing.Union[DateTrigger, CronTrigger, IntervalTrigger]]:
        """根据时间类型创建对应的触发器"""
        try:
            if self.r_time_type == '1':  # 具体时间
                return DateTrigger(run_date=datetime.strptime(self.r_time, '%Y-%m-%d %H:%M:%S'))
            
            elif self.r_time_type == '2':  # 每日执行时间
                hour, minute, second = map(int, self.r_time.split(':'))
                return CronTrigger(hour=hour, minute=minute, second=second)
            
            elif self.r_time_type == '3':  # 每周循环时间
                parts = self.r_time.split()
                day_of_week = parts[0]  # 1-7，1=周一
                hour, minute, second = map(int, parts[1].split(':'))
                return CronTrigger(day_of_week=day_of_week, hour=hour, minute=minute, second=second)
            
            elif self.r_time_type == '4':  # 月循环时间
                parts = self.r_time.split()
                day = parts[0]  # 1-31
                hour, minute, second = map(int, parts[1].split(':'))
                return CronTrigger(day=day, hour=hour, minute=minute, second=second)
            
            elif self.r_time_type == '5':  # 间隔时间
                hour, minute, second = map(int, self.r_time.split(':'))
                return IntervalTrigger(hours=hour, minutes=minute, seconds=second)
            
            elif self.r_time_type == '6':  # 开机时执行
                return None  # 已在调度器中特殊处理
            
            return None
        except Exception as e:
            print(f"Failed To Create Scheduler For Task {self.uuid} : {e}")
            return None


class TaskScheduler:
    """任务调度器类，管理所有任务的调度"""
    
    def __init__(self, ExecuteCallBack=lambda x, y, z: exec(y)):
        self.ExecuteCallBack=ExecuteCallBack
        """初始化调度器"""
        # 初始化调度器，使用上海时区
        self.scheduler = BackgroundScheduler(timezone=pytz.timezone('Asia/Shanghai'))
        self.scheduler.start()
        
        # 存储任务对象
        self.tasks: typing.Dict[str, Task] = {}
        
        # 添加事件监听
        self.scheduler.add_listener(self._job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    
    def _job_listener(self, event):
        """Task Execution Event Listener"""
        if event.code == EVENT_JOB_EXECUTED:
            print(f"Task {event.job_id} Executed Successfully")
        elif event.code == EVENT_JOB_ERROR:
            print(f"Task {event.job_id} Execution Failed: {event.exception}")

    def add_task(self, task_data: typing.Dict) -> bool:
        """
        Add Tasks To The Scheduler
        :param task_data: Task Data Dictionary
        :return: Was It Added Successfully?
        """
        try:
            task = Task(task_data)
            
            # 检查生效时间是否已过
            if not task.is_effective():
                print(f"Task {task.uuid} The Effective Date Has Passed.")
                return False
            
            # 处理开机执行的任务
            if task.r_time_type == '6':
                print(f"Immediately Execute The StartUp Task: {task.name}")
                self._execute_code(task_data, task.r_code, task.r_type)
                return True
            
            # 创建触发器
            trigger = task.create_trigger()
            if not trigger:
                print(f"Unable To Create A Trigger For Task: {task.uuid}")
                return False
            
            # 添加任务到调度器
            self.scheduler.add_job(
                self._execute_code,
                trigger=trigger,
                args=[task_data, task.r_code, task.r_type],
                id=task.uuid,
                name=task.name,
                misfire_grace_time=60,  # 允许60秒的延迟执行
            )
            
            # 存储任务对象
            self.tasks[task.uuid] = task
            print(f"Task {task.uuid} Has Been Added.")
            return True
            
        except Exception as e:
            print(f"Failed To Add Task: {e}")
            return False
    
    def remove_task(self, task_uuid: str) -> bool:
        """
        移除任务
        :param task_uuid: 任务UUID
        :return: 是否移除成功
        """
        if task_uuid not in self.tasks:
            print(f"任务 {task_uuid} 不存在")
            return False

        try:
            # 从调度器中移除
            try:
                self.scheduler.remove_job(task_uuid)
            except:
                pass

            # 从任务字典中移除
            del self.tasks[task_uuid]
            
            print(f"Task {task_uuid} Has Been Removed")
            return True
        except Exception as e:
            print(traceback.format_exc())
            print(f"Failed To Remove Task {task_uuid}: {e}")
            return False
    
    def get_task(self, task_uuid: str) -> typing.Optional[typing.Dict]:
        """
        获取任务信息
        :param task_uuid: 任务UUID
        :return: 任务信息字典或None
        """
        task = self.tasks.get(task_uuid)
        if not task:
            return None
        
        return {
            'TaskUUID': task.uuid,
            'TaskName': task.name,
            'ETimeType': task.e_time_type,
            'ETime': task.e_time,
            'RTimeType': task.r_time_type,
            'RTime': task.r_time,
            'RCode': task.r_code,
            'RType': task.r_type
        }
    
    def list_tasks(self) -> typing.Dict[str, typing.Dict]:
        """Get All Task Information"""
        return {uuid: self.get_task(uuid) for uuid in self.tasks}
    
    def _execute_code(self, task: dict, _code: str, _type: str):
        self.ExecuteCallBack(task, _code, _type)
    
    def shutdown(self):
        """关闭调度器"""
        self.scheduler.shutdown()
        print("Task Scheduler Has Been Closed.")