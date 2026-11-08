# coding=utf-8

import os
import platform
import time
import ctypes
import tkinter
from tkinter import *

from HCNetSDK import *
from module.Playback import OpenPlayback, playBackInitial, CleanPlayBackUp
from module import GetPlayBackFile
from module.Preview import OpenPreview, RealDataCallBack_V30, InitializeGlobals, CleanRealUp

# 登录的设备信息
DEV_IP = ctypes.create_string_buffer(b'10.10.138.111')
DEV_PORT = 8000
DEV_USER_NAME = ctypes.create_string_buffer(b'admin')
DEV_PASSWORD = ctypes.create_string_buffer(b'')

PlayCtrl_Port = ctypes.c_long(-1)  # 播放句柄
WINDOWS_FLAG = True


def SetSDKInitCfg(Objdll, strPath, WINDOWS_FLAG):
    sdk_ComPath = NET_DVR_LOCAL_SDK_PATH()
    sdk_ComPath.sPath = strPath
    Objdll.NET_DVR_SetSDKInitCfg(2, ctypes.byref(sdk_ComPath))

    if WINDOWS_FLAG:
        Objdll.NET_DVR_SetSDKInitCfg(3, ctypes.create_string_buffer(strPath + b'\\libcrypto-1_1-x64.dll'))
        Objdll.NET_DVR_SetSDKInitCfg(4, ctypes.create_string_buffer(strPath + b'\\libssl-1_1-x64.dll'))
    else:
        Objdll.NET_DVR_SetSDKInitCfg(3, ctypes.create_string_buffer(strPath + b'/libcrypto.so.1.1'))
        Objdll.NET_DVR_SetSDKInitCfg(4, ctypes.create_string_buffer(strPath + b'/libssl.so.1.1'))


def LoginDev(Objdll, DEV_IP, DEV_PORT, DEV_USER_NAME, DEV_PASSWORD):
    # 登录注册设备
    device_info = NET_DVR_DEVICEINFO_V30()
    lUserId = Objdll.NET_DVR_Login_V30(DEV_IP, DEV_PORT, DEV_USER_NAME, DEV_PASSWORD, ctypes.byref(device_info))
    return (lUserId, device_info)


def Initialize(Objdll, Playctrldll):
    # 初始化DLL
    Objdll.NET_DVR_Init()
    Objdll.NET_DVR_SetLogToFile(3, bytes('./SdkLog_Python/', encoding="utf-8"), False)

    # 获取一个播放句柄
    if not Playctrldll.PlayM4_GetPort(ctypes.byref(PlayCtrl_Port)):
        print(u'获取播放库句柄失败')


def GetPlatform():
    sysstr = platform.system()
    if sysstr != "Windows":
        global WINDOWS_FLAG
        WINDOWS_FLAG = False


# 获取IP接入配置参数
def get_ip_channel_info(user_id):
    ibr_bytes_returned = c_int(0)  # 获取返回字节数
    m_str_ippara_cfg = NET_DVR_IPPARACFG_V40()
    memset(byref(m_str_ippara_cfg), 0, sizeof(m_str_ippara_cfg))  # 清空结构体

    # lpIpParaConfig 接收数据的缓冲指针
    lp_ip_para_config = cast(pointer(m_str_ippara_cfg), POINTER(NET_DVR_IPPARACFG_V40))

    # 假设你已经定义了 hCNetSDK 和相应的方法
    b_ret = Objdll.NET_DVR_GetDVRConfig(user_id, NET_DVR_GET_IPPARACFG_V40, 0, lp_ip_para_config,
                                        sizeof(m_str_ippara_cfg), byref(ibr_bytes_returned))

    if b_ret:
        print("起始数字通道号：", m_str_ippara_cfg.dwStartDChan)

        for i_channel_num in range(m_str_ippara_cfg.dwDChanNum):
            channel_num = i_channel_num + m_str_ippara_cfg.dwStartDChan
            stream_mode = m_str_ippara_cfg.struStreamMode[i_channel_num]

            if stream_mode.uGetStream.struChanInfo.byEnable == 1:
                print("IP通道", channel_num, "在线")
            else:
                print("IP通道", channel_num, "不在线")
    else:
        print("获取通道信息失败")


def set_window_transparent(hwnd):
    GWL_EXSTYLE = -20
    WS_EX_LAYERED = 0x00080000
    WS_EX_TRANSPARENT = 0x00000020
    LWA_ALPHA = 0x2
    user32 = ctypes.windll.user32
    SetWindowLong = user32.SetWindowLongW
    GetWindowLong = user32.GetWindowLongW
    SetLayeredWindowAttributes = ctypes.windll.user32.SetLayeredWindowAttributes
    style = GetWindowLong(hwnd, GWL_EXSTYLE)
    SetWindowLong(hwnd, GWL_EXSTYLE, style | WS_EX_LAYERED)
    SetLayeredWindowAttributes(hwnd, 0, 240, LWA_ALPHA)


# 拖动窗口函数
def start_move(event):
    win.x = event.x
    win.y = event.y


def on_motion(event):
    deltax = event.x - win.x
    deltay = event.y - win.y
    x = win.winfo_x() + deltax
    y = win.winfo_y() + deltay
    win.geometry(f"+{x}+{y}")


if __name__ == '__main__':
    win = tkinter.Tk()
    win.overrideredirect(True)
    win.attributes('-topmost', True)

    # 拖动绑定
    win.bind("<ButtonPress-1>", start_move)
    win.bind("<B1-Motion>", on_motion)

    # 窗口大小与居中
    ww, wh = 1024, 768
    sw, sh = win.winfo_screenwidth(), win.winfo_screenheight()
    x, y = int((sw - ww) / 2), int((sh - wh) / 2)
    win.geometry(f"{ww}x{wh}+{x}+{y}")

    # 设置透明窗体（仅 Windows）
    if WINDOWS_FLAG:
        hwnd = ctypes.windll.user32.GetParent(win.winfo_id())
        set_window_transparent(hwnd)

    # 美观界面
    frame = Frame(win, bg='#2e2e2e')
    frame.pack(fill=BOTH, expand=YES)

    # 视频Canvas
    cv = Canvas(frame, bg='black', width=ww, height=wh)
    cv.pack()

    # 退出按钮
    b = Button(frame, text='退出', command=win.quit, bg='red', fg='white')
    b.place(x=ww - 60, y=10, width=50, height=25)
    GetPlatform()

    if WINDOWS_FLAG:
        os.chdir(r'./lib/win')
        Objdll = ctypes.CDLL(r'./HCNetSDK.dll')
        Playctrldll = ctypes.CDLL(r'./PlayCtrl.dll')
    else:
        os.chdir(r'./lib/linux')
        Objdll = ctypes.cdll.LoadLibrary(r'./libhcnetsdk.so')
        Playctrldll = ctypes.cdll.LoadLibrary(r'./libPlayCtrl.so')

    SetSDKInitCfg(Objdll, os.getcwd().encode('gbk') if WINDOWS_FLAG else os.getcwd().encode('utf-8'), WINDOWS_FLAG)

    Initialize(Objdll, Playctrldll)
    net_dvr_local_general_cfg = NET_DVR_LOCAL_GENERAL_CFG()
    net_dvr_local_general_cfg.byNotSplitRecordFile = 1
    Objdll.NET_DVR_SetSDKLocalCfg(17, byref(net_dvr_local_general_cfg))

    (lUserId, device_info) = LoginDev(Objdll, DEV_IP, DEV_PORT, DEV_USER_NAME, DEV_PASSWORD)
    if lUserId < 0:
        print('Login device fail, error code is: %d' % Objdll.NET_DVR_GetLastError())
        Objdll.NET_DVR_Cleanup()
        exit()
    else:
        print("NET_DVR_Login_V30登录成功！！！")
    while True:
        str_input = input("请输入您想要执行的demo实例! （退出请输入yes）\n").strip().lower()
        if str_input == "yes":
            break
        elif str_input == "1":
            print("获取IP接入配置参数")
            get_ip_channel_info(lUserId)
        elif str_input == "2":
            print("预览窗口调用示例、播放库回调抓图")
            # 初始化预览全局变量
            # InitializeGlobals(Objdll, Playctrldll, cv, PlayCtrl_Port, win)  # 带窗口
            InitializeGlobals(Objdll, Playctrldll, PlayCtrl_Port)     # 不带窗口
            global funcRealDataCallBack_V30
            funcRealDataCallBack_V30 = REALDATACALLBACK(RealDataCallBack_V30)
            lRealPlayHandle = OpenPreview(lUserId, funcRealDataCallBack_V30)
            if lRealPlayHandle < 0:
                print('开始预览失败, 错误码: %d' % Objdll.NET_DVR_GetLastError())
                Objdll.NET_DVR_Logout(lUserId)
                Objdll.NET_DVR_Cleanup()
                exit()
            else:
                print("NET_DVR_RealPlay_V40接口调用成功！！！")
            time.sleep(20)
            # win.mainloop()
            # 停止预览，释放播放库资源
            CleanRealUp(Objdll, Playctrldll, lRealPlayHandle)
        elif str_input == "3":
            print("按时间回放窗口")
            # 初始化回放全局变量
            playBackInitial(Objdll, Playctrldll, cv, PlayCtrl_Port, win)
            iPlayBack = OpenPlayback(lUserId, 34, "win")
            if iPlayBack < 0:
                print('开始回放失败, 错误码: %d' % Objdll.NET_DVR_GetLastError())
                Objdll.NET_DVR_Logout(lUserId)
                Objdll.NET_DVR_Cleanup()
                exit()
            else:
                print("开始回放成功")
            # 停止回放，释放播放库资源
            CleanPlayBackUp(Objdll, Playctrldll, iPlayBack)
        elif str_input == "4":
            print("取回放流保存文件调用示例")
            # 初始化回放全局变量
            playBackInitial(Objdll, Playctrldll, cv, PlayCtrl_Port, win)
            iPlayBack = OpenPlayback(lUserId, 34, "file")
            if iPlayBack < 0:
                print('开始回放失败, 错误码: %d' % Objdll.NET_DVR_GetLastError())
                Objdll.NET_DVR_Logout(lUserId)
                Objdll.NET_DVR_Cleanup()
                exit()
            else:
                print("开始回放成功")
            # 停止回放，释放播放库资源
            CleanPlayBackUp(Objdll, Playctrldll, iPlayBack)
        elif str_input == "5":
            print("查找录像文件并按文件名下载")
            GetPlayBackFile.PlayBackInitialize(Objdll, Playctrldll, cv, PlayCtrl_Port, win)
            GetPlayBackFile.download_record_by_name(lUserId, 34)
        elif str_input == "6":
            print("查找录像文件并按时间下载")
            GetPlayBackFile.PlayBackInitialize(Objdll, Playctrldll, cv, PlayCtrl_Port, win)
            # 按时间下载
            GetPlayBackFile.download_record_by_time(lUserId)
        else:
            print("未知的指令操作!请重新输入!\n")
    """
    释放sdk资源
    """
    Objdll.NET_DVR_Logout(lUserId)
    Objdll.NET_DVR_Cleanup()
