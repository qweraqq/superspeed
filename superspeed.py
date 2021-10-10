#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""使用python实现superspeed
原脚本网址: https://github.com/ernisn/superspeed

"""
import shutil
import subprocess
from sys import platform

china_telecom_servers = [3633, 29071, 17145, 27575, 5396, 7509, 28225]
china_unicom_servers = [24447, 5505, 27154, 26180, 26678, 13704, 4884]
china_mobile_servers = [25637, 30293, 25858, 17184, 26940, 31815, 26938, 26850, 17320, 4647,28491, 17584, 26656]

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def check_os():
    if platform == "linux" or platform == "linux2":
        return "linux"
    elif platform == "darwin":
        return "macos"
    elif platform == "win32":
        return "windows"


def check_speedtestcli() -> bool:
    """[summary]
    https://www.speedtest.net/apps
    https://www.speedtest.net/apps/cli
    Returns:
        bool: [description]
    """    
    command = 'speedtest'
    return shutil.which(command) is not None


def run_speedtest():
    print("测速类型:") 
    print("1. 三网测速")
    print("2. 电信节点")
    print("3. 联通节点")
    print("4. 移动节点")
    choice = int(input(f"{bcolors.HEADER}请输入数字选择测速类型:{bcolors.ENDC}"))
    servers = []
    if choice == 1:
        servers = china_mobile_servers + china_telecom_servers + china_unicom_servers
    elif choice == 2:
        servers = china_telecom_servers
    elif choice == 3:
        servers = china_unicom_servers
    elif choice == 4:
        servers = china_mobile_servers
    else:
        exit(0)
    template = "{SERVER:50}|{UPLOAD:15}|{DOWNLOAD:15}|{LATENCY:15}" # same, but named
    print(template.format(SERVER="SERVER", UPLOAD="UPLOAD", DOWNLOAD="DOWNLOAD",LATENCY="LATENCY"))

    for server in servers:
        result = {}
        # result["ID"] = f"{server}"
        output = subprocess.run(["speedtest", "-p", "no", "--accept-license", "-s", f"{server}"], capture_output=True, text=True)
        if output.returncode != 0:
            continue

        for line in output.stdout.splitlines():
            if "Server" in line:
                result["SERVER"] = line.split(":")[1].split("(")[0].strip()
            if "Latency" in line:
                result["LATENCY"] = line.split(":")[1].split("(")[0].strip()
            if "Upload" in line:
                result["UPLOAD"] = line.split(":")[1].split("(")[0].strip()
            if "Download" in line:
                result["DOWNLOAD"] = line.split(":")[1].split("(")[0].strip()

        print(template.format(**result))

if __name__ == "__main__":
    print(f"检测到操作系统:{bcolors.OKGREEN}{check_os()}{bcolors.ENDC}")
    if not check_speedtestcli():
        print("""
请访问
https://www.speedtest.net/apps
https://www.speedtest.net/apps/cli
安装官方版speedtest命令行工具
""")
        exit(0)
    run_speedtest()