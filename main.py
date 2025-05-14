import tkinter as tk
import subprocess as sp
import random
from tkinter.ttk import Separator
from setproctitle import setproctitle
import psutil as ps
from pyperclip import copy
import winreg
import tkinter.messagebox
from tkinter import ttk
import webbrowser
import win32gui
import win32con
import win32api
Letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")

def OpenLuoguLink(event=None):
    webbrowser.open("https://www.luogu.com.cn/user/731196")

def EnumChildProc(hwnd, lParam):
    hMenu = win32gui.GetMenu(hwnd)
    if hMenu and win32api.LOWORD(hMenu) == 1004:
        if not win32gui.IsWindowEnabled(hwnd):
            win32gui.EnableWindow(hwnd, True)
        else:
            win32gui.EnableWindow(hwnd, False)
        return False  # 停止遍历
    return True

def ToggleFullscreenButton():
    hwnd_parent = win32gui.FindWindow(None, "屏幕广播")  # 假设“广播”为窗口标题
    if hwnd_parent:
        win32gui.EnumChildWindows(hwnd_parent, EnumChildProc, None)
    else:
        tk.messagebox.showwarning("提示", "未找到极域广播窗口")

def SuspendJiYu():
    global SuspendJiYuButton
    global ResumeJiYuButton
    for name in ps.process_iter(["pid" , "name"]):
        if name.info["name"] == "StudentMain.exe":
            name.suspend()
    SuspendJiYuButton.place_forget()
    ResumeJiYuButton.place(x=270 , y=100)
    tk.messagebox.showinfo("提示" , "已挂起")
def ResumeJiYu():
    global SuspendJiYuButton
    for name in ps.process_iter(["pid" , "name"]):
        if name.info["name"] == "StudentMain.exe":
            name.resume()
    ResumeJiYuButton.place_forget()
    SuspendJiYuButton.place(x=270 , y=100)
    tk.messagebox.showinfo("提示" , "已恢复")
def GetJiYuPassword():
    try:
        # 打开注册表键
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                            r"SOFTWARE\TopDomain\e-Learning Class\Student",
                            0,
                            winreg.KEY_READ | winreg.KEY_WOW64_32KEY) as key:
            # 读取名为 'knock1' 的值
            value, regtype = winreg.QueryValueEx(key, "knock1")
            if regtype != winreg.REG_BINARY:
                print("注册表项 'knock1' 的类型不是 REG_BINARY。")
                return None
    except FileNotFoundError:
        print("注册表项未找到。")
        tk.messagebox.showerror("错误" , "注册表项未找到。")
        return None
    except OSError as e:
        print(f"读取注册表时发生错误: {e}")
        tk.messagebox.showerror("错误" , f"读取注册表时发生错误: {e}")
        return None
    decoded_bytes = bytearray(value)
    for i in range(0, len(decoded_bytes), 4):
        if i + 3 >= len(decoded_bytes):
            break
        decoded_bytes[i] ^= 0x50 ^ 0x45
        decoded_bytes[i + 1] ^= 0x43 ^ 0x4C
        decoded_bytes[i + 2] ^= 0x4C ^ 0x43
        decoded_bytes[i + 3] ^= 0x45 ^ 0x50

    # 提取 ASCII 字符
    password_chars = []
    for i in range(0, len(decoded_bytes), 2):
        if i + 1 >= len(decoded_bytes):
            break
        if decoded_bytes[i + 1] == 0:
            if decoded_bytes[i] == 0:
                break
            password_chars.append(chr(decoded_bytes[i]))
    return ''.join(password_chars)

def CopyPassword():
    copy(GetJiYuPassword())
    tk.messagebox.showinfo("提示" , "已复制到剪切板")

def TopmostWindow():
    if TopmostVar.get():
        main.attributes("-topmost" , True)
    else:
        main.attributes("-topmost" , False)

def find(n):
    for name in ps.process_iter(attrs=["name"]):
        if name.info["name"] == n:
            return True
    return False
def findJiYu():
        global KillJiYuButton
        global StartJiYuButton
        if find("StudentMain.exe"):
            KillJiYuButton = tk.Button(main, text="杀死极域", command=KillJiYu, width=30, height=3, state="active")
            StartJiYuButton = tk.Button(main , text="极域已启动" , command=StartJiYu , width=30 , height=3 , state="disabled")
        else:
            KillJiYuButton = tk.Button(main, text="未找到极域", command=KillJiYu, width=30, height=3, state="disabled")
            StartJiYuButton = tk.Button(main, text="开启极域", command=StartJiYu, width=30, height=3, state="disabled")

def KillJiYu():
    sp.run("taskkill /im StudentMain.exe /f")
    findJiYu()

def GetJiYuInstallationPath():
    try:
        # 打开注册表键
        with winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\WOW6432Node\TopDomain\e-Learning Class Standard\1.00",
                0,
                winreg.KEY_READ | winreg.KEY_WOW64_32KEY
        ) as key:
            # 查询名为 'TargetDirectory' 的值
            value, regtype = winreg.QueryValueEx(key, "TargetDirectory")
            if regtype in (winreg.REG_SZ, winreg.REG_EXPAND_SZ):
                # 将单反斜杠替换为双反斜杠
                return value.replace("\\", "\\\\")
            else:
                print("注册表项 'TargetDirectory' 的类型不是字符串。")
                return None
    except FileNotFoundError:
        print("注册表项未找到。")
        tk.messagebox.showerror("错误", "注册表项未找到。")
        return None
    except OSError as e:
        print(f"读取注册表时发生错误: {e}")
        tk.messagebox.showerror("错误", f"读取注册表时发生错误: {e}")
        return None

# def ResumeImageFileExecutionOptions():
#     try:
#         with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE ,
#                             r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\a.exe" ,
#                             0 , winreg.KEY_WRITE) as key:
#             winreg.DeleteKey("Debugger" , r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\a.exe")
#             print("删除成功")
#     except FileNotFoundError:
#         print("注册表项未找到。")
#         tk.messagebox.showerror("错误", "注册表项未找到。")
#         return None
#     except OSError as e:
#         print(f"读取注册表时发生错误: {e}")
#         tk.messagebox.showerror("错误", f"读取注册表时发生错误: {e}")
#         return None
#
# ResumeImageFileExecutionOptions()

def Exit():
    exit(0)

def StartJiYu():
    InstallationPath = GetJiYuInstallationPath()
    sp.run([InstallationPath])
    findJiYu()

def CopyUniversalPassword():
    copy("mythware_super_password")
    tk.messagebox.showinfo("提示", "已复制到剪切板")

main = tk.Tk()
main.geometry("600x170")
name = ""
for i in range(random.randint(7 , 12)):
    str = random.choice(Letters)
    name += str
main.title(name)
setproctitle(name)
main.resizable(False , False)
width = 600
height = 170
TopmostVar = tk.IntVar()
TopmostCB = tk.Checkbutton(main , text="置顶窗口" , variable=TopmostVar , onvalue=1 , offvalue=0 , command=TopmostWindow)
TopmostCB.place(x=0 , y=140)
Separator1 = tk.Frame(main , height=2 , borderwidth=1 , relief="groove")
Separator1.place(x=0, y=135, relwidth=1)
OpenLuoguLabel = tk.Label(main , text="洛谷博客" , fg="blue" , cursor="hand2" , font=("黑体", 17, "underline"))
OpenLuoguLabel.place(x=210 , y=0)
OpenLuoguLabel.bind("<Button-1>" , OpenLuoguLink)
ToggleFullscreenButtonBtn = tk.Button(main, text="切换全屏按钮", command=ToggleFullscreenButton)
ToggleFullscreenButtonBtn.place(x=180, y=100)

SuspendJiYuButton = tk.Button(main , text="挂起极域" , command=SuspendJiYu)
SuspendJiYuButton.place(x=270 , y=100)
ResumeJiYuButton = tk.Button(main , text="恢复极域" , command=ResumeJiYu)
ResumeJiYuButton.place(x=270 , y=100)
ResumeJiYuButton.place_forget()
# ResumeImageFileExecutionOptionsButton = tk.Button(main , text="恢复映像劫持注册表项" , command=ResumeImageFileExecutionOptions)
# ResumeImageFileExecutionOptionsButton.place(x=340,y=100)
ExitButton = tk.Button(main , text="退出" , command=Exit , state="disabled")
ExitButton.place(x=340 , y=100)

Title = tk.Label(main , text="欢迎使用极域杀手!" , font=("黑体" , 17))
Title.place(x=0 , y=0)
KillJiYuButton = tk.Button(main , text="杀死极域" , command=KillJiYu , width=30 , height=3)
findJiYu()
KillJiYuButton.place(x=0 , y=32)
CopyUniversalPasswordButton = tk.Button(main , text="复制万能密码" , command=CopyUniversalPassword)
CopyUniversalPasswordButton.place(x = 0 , y = 100)
GetJiYuPasswordButton = tk.Button(main , text="获取极域密码" , command=GetJiYuPassword)
GetJiYuPasswordButton.place(x = 90 , y = 100)
StartJiYuButton = tk.Button(main , text="开启极域" , command=StartJiYu , width=30 , height=3)
StartJiYuButton.place(x=230 , y=32)

main.mainloop()