# --*-- conding:utf-8 --*--
# @Time : 2024/8/28 10:14
# @Author : wangchao124
# @Email : wangchao124@hikvision.com
# @File : GetPlayBackFile.py
# @Software : PyCharm
import time
from datetime import datetime
from threading import Timer
from HCNetSDK import *

Objdll = None  # 网络库


def PlayBackInitialize(loaded_Objdll, loaded_Playctrldll, loaded_cv, loaded_PlayCtrl_Port, wined):
    global Objdll
    Objdll = loaded_Objdll
    global Playctrldll
    Playctrldll = loaded_Playctrldll
    global cv
    cv = loaded_cv
    global PlayCtrl_Port
    PlayCtrl_Port = loaded_PlayCtrl_Port
    global win
    win = wined


# 查找录像文件并按文件名下载
def download_record_by_name(lUserID, iChannelNo):
    strFileName = dvr_find_file(iChannelNo, lUserID)

    # 按文件名下载
    SaveDir = "E:\\HCNetSDK\\CH-HCNetSDKV6.1.9.48_build20230410_win64_20231214151140\\CH-HCNetSDKV6.1.9.48_build20230410_win64\\Download\\" + strFileName + ".mp4"
    print(SaveDir.encode())

    FileName = Objdll.NET_DVR_GetFileByName(lUserID, strFileName.encode('utf-8'), SaveDir.encode())
    if FileName <= -1:
        print(f"下载录像失败，错误码为 {Objdll.NET_DVR_GetLastError()}")
        exit()

    # 转码3GP命令
    intP = c_int(5)
    intInlen1 = c_int(0)
    b_PlayBack = Objdll.NET_DVR_PlayBackControl_V40(FileName, 32, byref(intP), 4, None, byref(intInlen1))
    if not b_PlayBack:
        print(f"转封装失败，错误码为 {Objdll.NET_DVR_GetLastError()}")
        exit()

    intP1 = c_int(0)
    intInlen = c_int(0)
    b_PlayBackStart = Objdll.NET_DVR_PlayBackControl_V40(FileName, NET_DVR_PLAYSTART, byref(intP1), 4, None,
                                                         byref(intInlen))
    if not b_PlayBackStart:
        print(f"开始播放失败，错误码为 {Objdll.NET_DVR_GetLastError()}")
        exit()

    while True:
        Pos = Objdll.NET_DVR_GetDownloadPos(FileName)
        if Pos != 100:
            print(f"下载进度: {Pos}")
            time.sleep(5)
            continue
        else:
            break

    b_Stop = Objdll.NET_DVR_StopGetFile(FileName)
    if not b_Stop:
        print(f"停止下载失败，错误码为 {Objdll.NET_DVR_GetLastError()}")
        exit()

    print("下载成功")


def dvr_find_file(iChannelNo, lUserID):
    strFileName = ""
    net_dvr_filecond = NET_DVR_FILECOND_V50()
    net_dvr_filecond.struStreamID.dwChannel = iChannelNo  # 通道号
    # NVR设备路数小于32路的起始通道号从33开始，依次增加
    net_dvr_filecond.dwFileType = 0
    net_dvr_filecond.byFindType = 0
    # 起始时间
    net_dvr_filecond.struStartTime.wYear = 2025
    net_dvr_filecond.struStartTime.byMonth = 6
    net_dvr_filecond.struStartTime.byDay = 17
    net_dvr_filecond.struStartTime.byHour = 0
    net_dvr_filecond.struStartTime.byMinute = 0
    net_dvr_filecond.struStartTime.bySecond = 0
    # 停止时间
    net_dvr_filecond.struStopTime.wYear = 2025
    net_dvr_filecond.struStopTime.byMonth = 6
    net_dvr_filecond.struStopTime.byDay = 17
    net_dvr_filecond.struStopTime.byHour = 1
    net_dvr_filecond.struStopTime.byMinute = 0
    net_dvr_filecond.struStopTime.bySecond = 0
    find_file_handle = Objdll.NET_DVR_FindFile_V50(lUserID, byref(net_dvr_filecond))
    if find_file_handle < 0:
        print("查找建立失败，错误码为" + Objdll.NET_DVR_GetLastError())
    else:
        print("查找建立成功")
    while True:
        # Call the FindNextFile function
        struFindData = NET_DVR_FINDDATA_V50()
        State = Objdll.NET_DVR_FindNextFile_V50(find_file_handle, byref(struFindData))

        if State <= -1:
            print(f"查找失败，错误码为 {Objdll.NET_DVR_GetLastError()}")
            break

        elif State == 1000:  # 获取文件信息成功
            fileName = struFindData.sFileName.decode('utf-8').strip()
            strFileName = fileName
            print(f"文件名称：{fileName}")
            print(f"文件大小: {struFindData.dwFileSize}")
            print("获取文件成功")
            break

        elif State == 1001:  # 未查找到文件
            print("未查找到文件")
            break

        elif State == 1002:  # 正在查找请等待
            print("正在查找，请等待")
            continue

        elif State == 1003:  # 没有更多的文件，查找结束
            print("没有更多的文件，查找结束")
            break

        elif State == 1004:  # 查找文件时异常
            print("查找文件时异常，查找结束")
            break

        elif State == 1005:  # 查找文件超时
            print("查找文件超时，查找结束")
            break
    # Close the file handle
    b_CloseHandle = Objdll.NET_DVR_FindClose_V30(find_file_handle)
    if not b_CloseHandle:
        print(f"关闭失败，错误码为 {Objdll.NET_DVR_GetLastError()}")
    else:
        print("NET_DVR_FindClose_V30成功")
    return strFileName


# 按时间下载录像
def download_record_by_time(userID):
    # 创建条件结构体
    net_dvr_playcond = NET_DVR_PLAYCOND()
    net_dvr_playcond.dwChannel = 36  # 通道号

    # 开始时间
    net_dvr_playcond.struStartTime.dwYear = 2025
    net_dvr_playcond.struStartTime.dwMonth = 6
    net_dvr_playcond.struStartTime.dwDay = 4
    net_dvr_playcond.struStartTime.dwHour = 0
    net_dvr_playcond.struStartTime.dwMinute = 10
    net_dvr_playcond.struStartTime.dwSecond = 0

    # 停止时间
    net_dvr_playcond.struStopTime.dwYear = 2025
    net_dvr_playcond.struStopTime.dwMonth = 6
    net_dvr_playcond.struStopTime.dwDay = 4
    net_dvr_playcond.struStopTime.dwHour = 1
    net_dvr_playcond.struStopTime.dwMinute = 0
    net_dvr_playcond.struStopTime.dwSecond = 0

    # 文件名
    sFileName = f"E:\\HCNetSDK\\CH-HCNetSDKV6.1.9.48_build20230410_win64_20231214151140\\CH-HCNetSDKV6.1.9.48_build20230410_win64\\Download\\{int(time.time() * 1000)}.mp4"
    print(sFileName)

    # 按时间下载
    m_lLoadHandle = Objdll.NET_DVR_GetFileByTime_V40(userID, sFileName.encode('utf-8'), byref(net_dvr_playcond))
    if m_lLoadHandle >= 0:
        # 开始下载
        Objdll.NET_DVR_PlayBackControl(m_lLoadHandle, NET_DVR_PLAYSTART, 0, None)
        nPos = byref(c_int(0))
        while True:
            bret = Objdll.NET_DVR_PlayBackControl(m_lLoadHandle, NET_DVR_PLAYGETPOS, 0, nPos)
            if bret:
                print("回放进度", nPos._obj.value)
            else:
                print("获取回放进度失败，错误码为：%d" % Objdll.NET_DVR_GetLastError())

            if nPos._obj.value > 100:
                Objdll.NET_DVR_StopPlayBack(m_lLoadHandle)
                print("由于网络原因或DVR忙,回放异常终止!")
                return

            if nPos._obj.value == 100:
                Objdll.NET_DVR_StopGetFile(m_lLoadHandle)
                print("按时间回放结束")
                return
            time.sleep(5)
    else:
        print("按时间下载失败")
        print("last error", Objdll.NET_DVR_GetLastError())