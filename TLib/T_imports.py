# pip install psutil pywin32 python-socketio requests websocket-client pyinstaller pillow pynput# flask playsound cryptography apscheduler pytz setproctitle playsound
# Libraries
import ctypes.wintypes
import subprocess
class ast:
    from ast import literal_eval
class atexit:
    from atexit import register
class threading:
    from threading import Thread, Lock, Event, enumerate, active_count, excepthook, Semaphore
class re:
    from re import match, compile, fullmatch
#psutil:
    # NoSuchProcess,
    # pid_exists,
    # Process,
    # users,
    # boot_time,
    # net_io_counters,
    # disk_io_counters,
    # disk_usage,
    # swap_memory,
    # virtual_memory,
    # cpu_count,
    # cpu_percent,
    # AccessDenied,
    # ZombieProcess,
    # process_iter,
    # win_service_get
import psutil
class uuid:
    from uuid import uuid3, uuid1, NAMESPACE_DNS
class random:
    from random import randint, choice, random, uniform
class time:
    from time import sleep, localtime, strftime, time, ctime, strptime, mktime
#class winreg:
#    from winreg import HKEY_CURRENT_USER, REG_DWORD, REG_SZ, HKEY_LOCAL_MACHINE
#    from winreg import CreateKey, CloseKey, SetValueEx, OpenKey, QueryValueEx
import winreg
class struct:
    from struct import pack, unpack
class ftplib:
    from ftplib import FTP, _SSLSocket
class socket:
    from socket import gethostbyname, gethostname, getfqdn
import win32serviceutil
import pywintypes
import win32gui
import win32api
import win32con
import win32ui
import win32security
import ntsecuritycon
import win32file
from PIL import Image, ImageTk, ImageDraw, ImageFont, ImageGrab
class base64:
    from base64 import b64encode, b64decode
class json:
    from json import loads, dumps
class pickle:
    from pickle import loads, dumps, HIGHEST_PROTOCOL
class socketio:
    from socketio import Client
#import colorama
class platform:
    from platform import system, node, release, version, version, machine, processor, win32_ver, python_build, python_compiler, python_branch, python_implementation, python_revision, python_version, python_version_tuple
class requests:
    from requests import get, post, Request, Response, Session, adapters
import ctypes
class copy:
    from copy import copy, deepcopy
class typing:
    from typing import Optional, Callable, Tuple, Dict, Any, TYPE_CHECKING, Union
class string:
    from string import ascii_uppercase
class ssl:
    from ssl import create_default_context, Purpose, TLSVersion, PROTOCOL_TLSv1_2, CERT_REQUIRED
class X_ctypes:
    from _ctypes import FreeLibrary
class colorama:
    class Fore:
        RED = '\033[31m'
        GREEN = '\033[32m'
        YELLOW = '\033[33m'
        WHITE = '\033[37m'
        LIGHTYELLOW_EX = '\033[93m'
        RESET = '\033[39m'
    class Style:
        RESET_ALL = '\033[0m'
class configparser:
    from configparser import ConfigParser
class urllib3:
    from urllib3 import disable_warnings
    class exceptions:
        from urllib3.exceptions import InsecureRequestWarning
class traceback:
    from traceback import format_exc, print_exc
class io:
    from io import BytesIO, UnsupportedOperation, TextIOBase, TextIOWrapper
class pynput:
    from pynput import keyboard, mouse
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import shlex
import multiprocessing
class queue:
    from queue import Queue
class hashlib:
    from hashlib import sha256


import tkinter
import tkinter.font
import tkinter.messagebox
import setproctitle
import playsound
import inspect
import math
import sys
import os

from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
import pytz
import logging


def GUUID():
    return str(uuid.uuid3(uuid.NAMESPACE_DNS, str(random.randint(0, 10000000000000000000))))
def GMAC():
    return '-'.join([uuid.uuid1().hex[-12:].upper()[i:i+2] for i in range(0, 11, 2)])
def asyncs(f):
    def wrapper(*args, **kwargs):
        thr = threading.Thread(target = f, args = args, kwargs = kwargs)
        thr.start()
    return wrapper

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

if typing.TYPE_CHECKING:
    import Termination4
