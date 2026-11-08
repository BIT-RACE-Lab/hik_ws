# --*-- conding:utf-8 --*--
# @Time : 2024/8/23 17:57
# @Author : wangchao124
# @Email : wangchao124@hikvision.com
# @File : Playback.py
# @Software : PyCharm
from HCNetSDK import *
import threading
import time

from PlayCtrl import DECCBFUNWIN

Objdll = None  # 网络库
playBackCallBack = None # 回放码流回调函数
output_stream = None
callback_playBack = 0
callback_count = 0

def playBackInitial(loaded_Objdll, loaded_Playctrldll, loaded_cv, loaded_PlayCtrl_Port, wined):
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
def DecCBFun(nPort, pBuf, nSize, pFrameInfo, nUser, nReserved2):
    global callback_count
    callback_count += 1

    if callback_count % 100 == 0:
        print("进入播放库解码回调...")
    # 解码回调函数
    if pFrameInfo.contents.nType == 3:
        sFileName = ('../../resource/pic/test_stamp[%d].jpg' % pFrameInfo.contents.nStamp)
        nWidth = pFrameInfo.contents.nWidth
        nHeight = pFrameInfo.contents.nHeight
        nType = pFrameInfo.contents.nType
        dwFrameNum = pFrameInfo.contents.dwFrameNum
        nStamp = pFrameInfo.contents.nStamp
        # print(nWidth, nHeight, nType, dwFrameNum, nStamp, sFileName)    # 帧信息

        lRet = Playctrldll.PlayM4_ConvertToJpegFile(pBuf, nSize, nWidth, nHeight, nType,
                                                    c_char_p(sFileName.encode()))
        if lRet == 0:
            print('PlayM4_ConvertToJpegFile fail, error code is:', Playctrldll.PlayM4_GetLastError(nPort))
        else:
            print('PlayM4_ConvertToJpegFile success')
def PlayDataCallBackWin(lPlayHandle, dwDataType, pBuffer, dwBufSize, pUser):
    global callback_playBack
    callback_playBack += 1

    if callback_playBack % 100 == 0:
        print("回放码流回调")
    if dwDataType == NET_DVR_SYSHEAD:
        Playctrldll.PlayM4_SetStreamOpenMode(PlayCtrl_Port, 0)
        if Playctrldll.PlayM4_OpenStream(PlayCtrl_Port, pBuffer, dwBufSize, 40960 * 1024):
            global FuncDecCB
            FuncDecCB = DECCBFUNWIN(DecCBFun)
            Playctrldll.PlayM4_SetDecCallBackExMend(PlayCtrl_Port, FuncDecCB, None, 0, None)
            print("播放窗口句柄：", cv.winfo_id())
            if Playctrldll.PlayM4_Play(PlayCtrl_Port, cv.winfo_id()):
                print(u'播放库播放成功')
            else:
                print(u'播放库播放失败')
        else:
            print(u'播放库打开流失败')
    elif dwDataType == NET_DVR_STREAMDATA:
        if not Playctrldll.PlayM4_InputData(PlayCtrl_Port, pBuffer, dwBufSize):
            print('数据输入失败，缓冲区大小不足？')

    else:
        print(u'其他数据,长度:', dwBufSize)


def PlayDataCallBackFile(lPlayHandle, dwDataType, pBuffer, dwBufSize, pUser):
    print("回放码流回调...")
    offset = 0
    bytes_data = bytes(pBuffer[offset:offset + dwBufSize])
    output_path = '../../resource/video/video.mp4'
    try:
        with open(output_path, 'ab') as output_stream:  # 使用 'ab' 模式以追加二进制文件
            output_stream.write(bytes_data)
    except IOError as e:
        print(f"Error writing to file: {e}")


def OpenPlayback(lUserId, lChannel, command):
    net_dvr_vod_para = NET_DVR_VOD_PARA()
    net_dvr_vod_para.dwSize = sizeof(net_dvr_vod_para)
    net_dvr_vod_para.struIDInfo.dwChannel = lChannel  # 通道号
    # 开始时间
    net_dvr_vod_para.struBeginTime.dwYear = 2025
    net_dvr_vod_para.struBeginTime.dwMonth = 6
    net_dvr_vod_para.struBeginTime.dwDay = 17
    net_dvr_vod_para.struBeginTime.dwHour = 0
    net_dvr_vod_para.struBeginTime.dwMinute = 0
    net_dvr_vod_para.struBeginTime.dwSecond = 0
    # 停止时间
    net_dvr_vod_para.struEndTime.dwYear = 2025
    net_dvr_vod_para.struEndTime.dwMonth = 6
    net_dvr_vod_para.struEndTime.dwDay = 17
    net_dvr_vod_para.struEndTime.dwHour = 0
    net_dvr_vod_para.struEndTime.dwMinute = 10
    net_dvr_vod_para.struEndTime.dwSecond = 0
    net_dvr_vod_para.hWnd = 1  # 回放的窗口句柄，若置为空，SDK仍能收到码流数据，但不解码显示

    iPlayBack = Objdll.NET_DVR_PlayBackByTime_V40(lUserId, byref(net_dvr_vod_para))
    if iPlayBack <= -1:
        print("按时间回放失败，错误码为：%d" % Objdll.NET_DVR_GetLastError())
    else:
        print("按时间回放成功，回放句柄：%d" % iPlayBack)
    bCtrl = Objdll.NET_DVR_PlayBackControl_V40(iPlayBack, NET_DVR_PLAYSTART, None, 0, None)
    if bCtrl == False:
        print("NET_DVR_PlayBackControl_V40失败，错误码为：%d" % Objdll.NET_DVR_GetLastError())
    else:
        print("NET_DVR_PlayBackControl_V40成功，返回值：%d" % bCtrl)

    if command == "win":
        playBackCallBack = PLAYBACKCALLBACK(PlayDataCallBackWin)  # 窗口回调
        Objdll.NET_DVR_SetPlayDataCallBack_V40(iPlayBack, playBackCallBack, None)
        win.mainloop()
    else:
        playBackCallBack = PLAYBACKCALLBACK(PlayDataCallBackFile)  # 下载回调
        Objdll.NET_DVR_SetPlayDataCallBack_V40(iPlayBack, playBackCallBack, None)
        nPos = byref(c_int(0))  # 模拟IntByReference
        # 在回放进度为100后return iPlayBack，否则继续等待
        while True:
            bret = Objdll.NET_DVR_PlayBackControl(iPlayBack, NET_DVR_PLAYGETPOS, 0, nPos)
            if bret:
                print("回放进度", nPos._obj.value)
            else:
                print("获取回放进度失败，错误码为：%d" % Objdll.NET_DVR_GetLastError())

            if nPos._obj.value > 100:
                Objdll.NET_DVR_StopPlayBack(iPlayBack)
                if output_stream:
                    try:
                        output_stream.close()
                    except IOError as e:
                        print("关闭输出流时出错:", e)
                palybackFlay = True
                print("由于网络原因或DVR忙,回放异常终止!")
                return

            if nPos._obj.value == 100:
                Objdll.NET_DVR_StopPlayBack(iPlayBack)
                if output_stream:
                    try:
                        output_stream.close()
                    except IOError as e:
                        print("关闭输出流时出错:", e)
                palybackFlay = True
                print("按时间回放结束")
                return iPlayBack

            time.sleep(5)
    return iPlayBack


def CleanPlayBackUp(Objdll, Playctrldll, iPlayBack):
    Objdll.NET_DVR_StopRealPlay(iPlayBack)
    if PlayCtrl_Port.value > -1:
        Playctrldll.PlayM4_Stop(PlayCtrl_Port)
        Playctrldll.PlayM4_CloseStream(PlayCtrl_Port)
        Playctrldll.PlayM4_FreePort(PlayCtrl_Port)

