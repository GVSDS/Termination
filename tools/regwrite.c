#include <windows.h>
#include <stdio.h>

// 解析注册表根键
HKEY parseRootKey(const char* rootKeyStr) {
    if (strcmp(rootKeyStr, "HKEY_CLASSES_ROOT") == 0) {
        return HKEY_CLASSES_ROOT;
    } else if (strcmp(rootKeyStr, "HKEY_CURRENT_USER") == 0) {
        return HKEY_CURRENT_USER;
    } else if (strcmp(rootKeyStr, "HKEY_LOCAL_MACHINE") == 0) {
        return HKEY_LOCAL_MACHINE;
    } else if (strcmp(rootKeyStr, "HKEY_USERS") == 0) {
        return HKEY_USERS;
    } else if (strcmp(rootKeyStr, "HKEY_CURRENT_CONFIG") == 0) {
        return HKEY_CURRENT_CONFIG;
    }
    return NULL;
}

int main(int argc, char* argv[]) {
    if (argc != 4) {
        printf("Usage: %s <RegistryPath> <KeyName> <KeyValue>\n", argv[0]);
        return 1;
    }

    // 解析注册表根键
    char* rootKeyStr = strtok(argv[1], "\\");
    HKEY hRootKey = parseRootKey(rootKeyStr);
    if (hRootKey == NULL) {
        printf("Invalid root key.\n");
        return 1;
    }

    // 获取剩余的注册表路径
    char* subKey = strtok(NULL, "");
    if (subKey == NULL) {
        printf("Invalid registry path.\n");
        return 1;
    }

    // 打开或创建注册表项
    HKEY hKey;
    LONG lResult = RegCreateKeyEx(hRootKey, subKey, 0, NULL, REG_OPTION_NON_VOLATILE, KEY_ALL_ACCESS, NULL, &hKey, NULL);
    if (lResult != ERROR_SUCCESS) {
        printf("Failed to create or open registry key. Error code: %ld\n", lResult);
        return 1;
    }

    // 设置注册表键值
    lResult = RegSetValueEx(hKey, argv[2], 0, REG_SZ, (const BYTE*)argv[3], strlen(argv[3]));
    if (lResult != ERROR_SUCCESS) {
        printf("Failed to set registry value. Error code: %ld\n", lResult);
        RegCloseKey(hKey);
        return 1;
    }

    // 关闭注册表项
    RegCloseKey(hKey);

    printf("Registry value set successfully.\n");

    return 0;
}