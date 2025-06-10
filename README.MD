<p align="center">
  <img src="./icon.png" width="270px" />
  <p align="center">Termination 4.1.0</p>
  <p align="center">黯 - 傀儡系统 4.1.0</p>
</p>

![GitHub Followers](https://img.shields.io/badge/dynamic/json?color=green&label=GitHub%20Followers&query=%24.data.totalSubs&url=https%3A%2F%2Fapi.spencerwoo.com%2Fsubstats%2F%3Fsource%3Dgithub%26queryKey%3DGVSADS)
![Total Repos](https://img.shields.io/badge/dynamic/json?color=orange&label=Total%20Repos&query=%24.total_count&url=https%3A%2F%2Fapi.github.com%2Fsearch%2Frepositories%3Fq%3Duser%3AGVSADS)
![GitHub Stars](https://img.shields.io/github/stars/GVSADS/EMSTC?style=flat&label=Github%20Stars)
[![YangCun No. 8 Middle School](https://img.shields.io/badge/YangCun%20No.%208%20Middle%20School-114514-00a8f3)](https://baike.baidu.com/item/%E5%A4%A9%E6%B4%A5%E5%B8%82%E6%AD%A6%E6%B8%85%E5%8C%BA%E6%9D%A8%E6%9D%91%E7%AC%AC%E5%85%AB%E4%B8%AD%E5%AD%A6/62290383)

> 注意：本项目仅为技术分享，仅为客户端代码，无服务端代码，T_Lib.TWNT经过处理编译后的程序无法运行

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![C](https://img.shields.io/badge/C-A8B9CC?style=for-the-badge&logo=c&logoColor=black)
![C++](https://img.shields.io/badge/C%2B%2B-00599C?style=for-the-badge&logo=c%2B%2B&logoColor=white)
![HTML](https://img.shields.io/badge/HTML-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![CSS](https://img.shields.io/badge/CSS-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![Operating System](https://img.shields.io/badge/Operating%20System-000000?style=for-the-badge&logo=linux&logoColor=white)
![Investment](https://img.shields.io/badge/Investment-FFA500?style=for-the-badge&logo=bitcoin&logoColor=white)
![Mining](https://img.shields.io/badge/Mining-000000?style=for-the-badge&logo=ethereum&logoColor=white)
![Server](https://img.shields.io/badge/Server-000000?style=for-the-badge&logo=serverless&logoColor=white)
![Networking](https://img.shields.io/badge/Networking-000000?style=for-the-badge&logo=cisco&logoColor=white)

# 项目介绍

## 一、项目概述
本项目是一个功能全面且复杂的系统，主要围绕系统自动化运行、硬件资源监控、网络通信、任务调度以及特定场景下的感染处理等多个核心功能展开。通过多线程和模块化的设计理念，项目具备高度的可扩展性和灵活性，旨在满足不同用户在系统管理和监控方面的多样化需求。

## 二、主要模块详细介绍

### （一）自动化运行模块（Thread_AutoRun.py）
#### 1. 功能概述
该模块主要负责系统的自动化运行设置，确保系统在合适的环境下以正确的方式启动和运行。具体包括检查运行模式、安装和启动服务等操作，同时还能处理服务的停止和状态检查。
#### 2. 主要类及方法
- **AutoRunSetup类**：
    - `Setup`方法：初始化主对象，为后续操作提供基础。
    - `Run`方法：首先检查运行模式是否符合要求，若不符合则返回错误码；接着检查相关配置是否存在，若不存在也返回错误码；然后检查服务是否已安装，若未安装则进行安装；若服务已安装但路径不一致，则进行重新安装；最后尝试启动服务。
    - `stop`方法：停止正在运行的服务，若停止失败则输出错误信息。
    - `iswork`方法：检查服务是否正在运行，返回布尔值。

### （二）锁机制模块（T_Lock.py）
#### 1. 功能概述
该模块实现了锁机制，确保同一时间只有一个实例在运行，避免多个实例之间的冲突和干扰。
#### 2. 主要类及方法
- **LockMe类**：
    - `__init__`方法：初始化锁对象，设置相关参数，如锁的名称、临时目录等。
    - `IsOtherLock`方法：检查是否存在其他锁，若存在则表示有其他实例正在运行。
    - `lock`方法：加锁操作，若发现有其他锁则终止当前实例的运行。
    - `unlock`方法：解锁操作，释放当前实例持有的锁。

### （三）网络传输与监控模块（Thread_TWNTWork.py）
#### 1. 功能概述
该模块集成了网络传输、硬件监控、键盘鼠标监听、进程同步、屏幕截图上传等多种功能，实现了系统与服务器之间的数据交互和实时监控。
#### 2. 主要类及功能
- **MonitorWorker类**：监控硬件资源使用情况，包括CPU使用率、核心数、内存使用率、网络收发流量等，并将这些信息加密后发送到服务器。
- **ListenKMWorker类**：监听键盘和鼠标事件，记录用户的操作信息，并在满足一定条件时将记录加密后发送到服务器。
- **TWNTProcessSynchronousWorker类**：定期同步进程信息到服务器，让服务器了解系统中各个进程的运行状态。
- **TWNTCoverScreen类**：定期上传屏幕截图到服务器，实现屏幕的定期覆盖更新。
- **TWNTRealTimeScreen类**：实时上传屏幕截图到服务器，满足对屏幕实时监控的需求。
- **TWNESynchronousTProcess类**：定期告知服务器自己处于活跃状态，保持与服务器的心跳连接。
- **TWNToast类**：处理消息通知，根据不同的消息级别（如错误、信息、成功等）将消息加密后发送到服务器。
- **TWNETProcess类**：根据服务器发送的命令执行相应的操作，如重新获取系统信息、执行Python命令、执行Cmd命令等。

### （四）任务调度模块（Thread_LW3T.py 和 T_LW3T.py）
#### 1. 功能概述
该模块实现了任务的调度和管理，支持多种任务类型和时间触发方式，确保任务能够按照预定的时间和规则执行。
#### 2. 主要类及功能
- **LW3T类**：负责读取任务列表并添加到调度器，同时提供任务的插入、删除、修改等操作接口。
- **LW3TExecuteCallBack类**：任务执行回调，当任务触发时，执行相应的代码或命令。
- **L3T类**：管理本地时间任务表，实现任务的读取、写入和删除等操作。
- **Task类**：封装任务属性和行为，包括任务的唯一标识、名称、生效时间、触发时间、执行代码等，并提供任务有效性检查和触发器创建等方法。
- **TaskScheduler类**：任务调度器，管理所有任务的调度，包括任务的添加、删除和执行。

### （五）文件读取工具模块（T_Tools.py）
#### 1. 功能概述
该模块提供了文件读取功能，特别是支持从文件末尾读取指定范围的行，方便用户获取文件的最新信息。
#### 2. 主要函数
- `ReadFileRangeFromEnd`函数：实现从文件末尾读取指定范围的行。

### （六）网络传输模块（Thread_TWNT.py）
#### 1. 功能概述
该模块负责实现系统与服务器之间的网络连接、文件获取、消息处理等功能，确保数据的可靠传输。
#### 2. 主要类及方法
- **TWNetworkTransit类**：
    - `Run`方法：启动网络传输循环，包括初始化参数、连接服务器等操作。
    - `__init_values__`方法：初始化网络传输相关参数，如密钥、版本号、服务器地址、SSL上下文等。
    - `ServerLoop`方法：循环尝试连接服务器，若连接失败则进行重试，并在一定条件下检查更新。
    - `SocketIOregirst`方法：注册SocketIO事件，处理连接、断开连接和命令接收等事件。

### （七）感染处理模块（Thread_InfectionWorker.py）（未完成）
#### 1. 功能概述
该模块主要用于检测USB驱动器的插入，并对其进行感染处理，确保系统在特定场景下的安全性。
#### 2. 主要类及功能
- **InfectionWorker类**：检测USB驱动器的插入事件。
- **InfectionInstallWorker类**：对插入的USB驱动器进行感染处理。

## 三、项目依赖
### （一）系统库
项目使用了多个Python系统库，包括但不限于：
- `os`：用于操作系统相关的操作，如文件路径处理、进程管理等。
- `time`：用于时间处理，如获取当前时间、延时操作等。
- `threading`：用于多线程编程，实现并发执行。
- `subprocess`：用于创建新的进程，执行外部命令。
- `shlex`：用于解析命令行字符串。
- `re`：用于正则表达式匹配，处理字符串。
- `json`：用于JSON数据的编码和解码。
- `datetime`：用于日期和时间的处理。
- `ssl`：用于SSL/TLS加密通信。
- `ftplib`：用于FTP文件传输。
- `sys`：用于访问Python解释器的相关信息。

### （二）第三方库
项目还依赖了一些第三方库，需要用户手动安装：
- `psutil`：用于获取系统硬件信息，如CPU、内存、网络等。
- `pynput`：用于监听键盘和鼠标事件。
- `socketio`：用于实现WebSocket通信。
- `requests`：用于发送HTTP请求。
- `ast`：用于抽象语法树处理。
- `typing`：用于类型注解。
- `pytz`：用于处理时区信息。
- `APScheduler`：用于任务调度。

## 四、安装与使用
### （一）安装依赖
在使用项目之前，需要确保已经安装了所有的第三方库。可以使用以下命令进行安装：
```bash
pip install psutil pywin32 python-socketio requests websocket-client pyinstaller pillow pynput playsound cryptography apscheduler pytz setproctitle playsound
```

### （二）使用方法
1. 将项目代码下载到本地。
2. 根据客户端代码反推服务器代码。
3. 根据需要修改配置文件和参数，如服务器地址。
4. 运行主程序，并在服务器控制。

## 五、贡献指南的后续事项
### （一）事项
我们愿意倾听您的任何建议，您可以随时提交工单和Pr，但我们可能会对您的Pr进行修改，因为本项目一直在更新，但新版本不会再同步至GitHub，具体做法由开发者决定。

### （二）提交代码
1. 提交代码前，请确保代码通过了单元测试，避免引入新的错误。
2. 提交代码时，请提供详细的提交说明，描述所做的更改和目的。提交说明应包括以下内容：
    - 更改的功能模块。
    - 具体的更改内容。
    - 更改的原因和目的。

### （三）问题反馈
如果发现任何问题或有改进建议，请在项目的Issues页面提交问题。问题描述应包括以下内容：
- 问题的详细描述，包括复现步骤。
- 预期的行为和实际的行为。
- 相关的错误信息或日志。

## 六、许可证
本项目采用 [GPL] 许可证，详情请参阅LICENSE文件。该许可证规定了项目的使用、修改和分发的相关条款和条件，请在使用项目前仔细阅读。

## 七、联系信息
如果您有任何问题或建议，请联系 [GVSDS.TermiNexus]。我们将尽快回复您的问题，并认真考虑您的建议。