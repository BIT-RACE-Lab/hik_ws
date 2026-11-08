# coding=utf-8

import time

from HCNetSDK import *


class devClass(object):
    def __init__(self):
        self.hikSDK = self.LoadSDK()  # 加载sdk库
        self.iUserID = -1  # 登录句柄
        self.alarmHandle = -1  # 布防句柄
        self.listenHandle = -1  # 监听句柄
        self.basePath = ''  # 基础路径
        self.msg_callback_func = MSGCallBack_V31(self.g_fMessageCallBack_Alarm)  # 注册回调函数实现

    def LoadSDK(self):
        hikSDK = None
        try:
            print("netsdkdllpath: ", netsdkdllpath)
            hikSDK = load_library(netsdkdllpath)
        except OSError as e:
            print('动态库加载失败', e)
        return hikSDK

    # 报警信息回调函数实现代码
    def g_fMessageCallBack_Alarm(self, lCommand, pAlarmer, pAlarmInfo, dwBufLen, pUser):
        """
        解析报警信息
        """
        pAlarmer = pAlarmer.contents
        sDeviceIP = str(pAlarmer.sDeviceIP, encoding="utf8").rstrip('\x00')
        sSerialNumber = str(pAlarmer.sSerialNumber, encoding="utf8").rstrip('\x00')
        print(f"lUserID: {pAlarmer.lUserID}, sDeviceIP: {sDeviceIP}, sSerialNumber: {sSerialNumber}")

        # 移动侦测、视频丢失、遮挡、IO信号量等报警信息(V3.0以上版本支持的设备)
        if lCommand == ALARM_LCOMMAND_ENUM.COMM_ALARM_V30.value:
            print('移动侦测')
            Alarm_struct = cast(pAlarmInfo,
                                LPNET_DVR_ALARMINFO_V30).contents  # 当lCommand是COMM_ALARM时将pAlarmInfo强制转换为NET_DVR_ALARMINFO类型的指针再取值
            print(
                f'dwAlarmType: {hex(Alarm_struct.dwAlarmType)}, '
                f'byAlarmOutputNumber: {Alarm_struct.byAlarmOutputNumber[0]}, '
                f'byChannel: {Alarm_struct.byChannel[0]}'
            )

        # 门禁报警事件
        if lCommand == ALARM_LCOMMAND_ENUM.COMM_ALARM_ACS.value:
            Alarm_struct = cast(pAlarmInfo,
                                LPNET_DVR_ACS_ALARM_INFO).contents  # 当lCommand是0x5002时将pAlarmInfo强制转换为NET_DVR_ACS_ALARM_INFO类型的指针再取值
            byCardNo = str(Alarm_struct.struAcsEventInfo.byCardNo, encoding="utf-8").rstrip('\x00')
            byCardType = Alarm_struct.struAcsEventInfo.byCardType
            dwMajor = hex(Alarm_struct.dwMajor)
            dwMinor = hex(Alarm_struct.dwMinor)
            dwEmployeeNo = Alarm_struct.struAcsEventInfo.dwEmployeeNo
            print(
                f'【门禁主机报警信息】卡号：{byCardNo}, '
                f'卡类型: {byCardType}, '
                f'报警主类型: {dwMajor}, '
                f'报警次类型: {dwMinor}, '
                f'工号1: {dwEmployeeNo}, '
            )
            if Alarm_struct.byAcsEventInfoExtend == 1:
                pAcsEventInfoExtend = cast(Alarm_struct.pAcsEventInfoExtend, LPNET_DVR_ACS_EVENT_INFO_EXTEND).contents
                byEmployeeNo = str(pAcsEventInfoExtend.byEmployeeNo, encoding="gbk").rstrip('\x00')
                if byEmployeeNo > '':
                    print(f'工号2: {byEmployeeNo}, ')
            # 报警时间
            struTime = Alarm_struct.struTime
            SwipeTime = f'{struTime.dwYear}/{struTime.dwMonth}/{struTime.dwDay}_{struTime.dwHour}:{struTime.dwMinute}:{struTime.dwSecond}'
            print(f'事件触发时间,SwipeTime: {SwipeTime}')
            # 抓拍图片
            PicDataLen = Alarm_struct.dwPicDataLen
            if PicDataLen > 0:
                from datetime import datetime
                # 获取当前时间的datetime对象
                current_time = datetime.now()
                timestamp_str = current_time.strftime('%Y%m%d_%H%M%S')

                buff1 = string_at(Alarm_struct.pPicData, PicDataLen)
                with open(f'./pic/Acs_Capturetest{timestamp_str}.jpg', 'wb') as fp:
                    fp.write(buff1)

        if lCommand == ALARM_LCOMMAND_ENUM.COMM_ID_INFO_ALARM.value:
            print('身份证刷卡事件上传')
            Alarm_struct = cast(pAlarmInfo, LPNET_DVR_ID_CARD_INFO_ALARM).contents

            print(
                f'dwSize: {Alarm_struct.dwSize}, '
                f'dwMajor: {hex(Alarm_struct.dwMajor)}, '
                f'dwMinor: {hex(Alarm_struct.dwMinor)}, '
                f'dwPicDataLen: {Alarm_struct.dwPicDataLen}, '
                f'localtime: {time.asctime(time.localtime(time.time()))}, '
            )

            # 抓拍图片
            DataLen = Alarm_struct.dwCapturePicDataLen
            if DataLen != 0:
                from datetime import datetime
                # 获取当前时间的datetime对象
                current_time = datetime.now()
                timestamp_str = current_time.strftime('%Y%m%d_%H%M%S')
                buff1 = string_at(Alarm_struct.pCapturePicData, DataLen)
                with open(f'./pic/IDInfo_Capturetest{timestamp_str}.jpg', 'wb') as fp1:
                    fp1.write(buff1)
            # 身份证图片
            CardPicLen = Alarm_struct.dwPicDataLen
            if DataLen > 0:
                from datetime import datetime
                # 获取当前时间的datetime对象
                current_time = datetime.now()
                timestamp_str = current_time.strftime('%Y%m%d_%H%M%S')
                buff2 = string_at(Alarm_struct.pPicData, CardPicLen)
                with open(f'./pic/IDInfo_IDPicTest{timestamp_str}.jpg', 'wb') as fp2:
                    fp2.write(buff2)

        # 人脸抓拍报警信息
        if lCommand == ALARM_LCOMMAND_ENUM.COMM_UPLOAD_FACESNAP_RESULT.value:
            struFaceSnap = cast(pAlarmInfo,
                                LPNET_VCA_FACESNAP_RESULT).contents

            # 事件时间
            dwYear = (struFaceSnap.dwAbsTime >> 26) + 2000
            dwMonth = (struFaceSnap.dwAbsTime >> 22) & 15
            dwDay = (struFaceSnap.dwAbsTime >> 17) & 31
            dwHour = (struFaceSnap.dwAbsTime >> 12) & 31
            dwMinute = (struFaceSnap.dwAbsTime >> 6) & 63
            dwSecond = (struFaceSnap.dwAbsTime >> 0) & 63
            strAbsTime = f"{dwYear}_{dwMonth}_{dwDay}_{dwHour}_{dwMinute}_{dwSecond}"

            # 人脸属性信息
            sFaceAlarmInfo = "Abs时间:" + strAbsTime + ",是否戴口罩：" + str(
                struFaceSnap.struFeature.byMask) + ",是否微笑：" + str(
                struFaceSnap.struFeature.bySmile)
            print(sFaceAlarmInfo)

            from datetime import datetime
            # 获取当前时间戳
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            # 创建文件名
            filename1 = f'image_{timestamp}_1.jpg'
            filename2 = f'image_{timestamp}_2.jpg'

            # 指定保存图片的完整路径（包括文件名）
            filepath1 = os.path.join(os.getcwd(), filename1)
            filepath2 = os.path.join(os.getcwd(), filename2)
            if struFaceSnap.dwFacePicLen > 0:
                buff1 = string_at(struFaceSnap.pBuffer1, struFaceSnap.dwFacePicLen)
                with open(filepath1, 'wb') as fp:
                    fp.write(buff1)

            if struFaceSnap.dwBackgroundPicLen > 0:
                buff2 = string_at(struFaceSnap.pBuffer2, struFaceSnap.dwBackgroundPicLen)
                with open(filepath2, 'wb') as fp:
                    fp.write(buff2)

        # 人脸对比数据上报
        if lCommand == ALARM_LCOMMAND_ENUM.COMM_SNAP_MATCH_ALARM.value:
            print("*********************************************************")
            print("对比数据")
            p_cont_device = cast(pAlarmInfo, POINTER(NET_VCA_FACESNAP_MATCH_ALARM))
            contents = p_cont_device.contents

            print("相似度: ", contents.fSimilarity)
            print("dwsize:", contents.dwSize)
            print("byMatchPicNum:", contents.byMatchPicNum)

            print("设备识别抓拍图片指针 : ", contents.pSnapPicBuffer)
            print("设备识别抓拍图片长度: ", contents.dwSnapPicLen)
            print("图片数据传输方式: ", contents.byPicTransType)

            # 事件时间
            dwYear = (contents.struSnapInfo.dwAbsTime >> 26) + 2000
            dwMonth = (contents.struSnapInfo.dwAbsTime >> 22) & 15
            dwDay = (contents.struSnapInfo.dwAbsTime >> 17) & 31
            dwHour = (contents.struSnapInfo.dwAbsTime >> 12) & 31
            dwMinute = (contents.struSnapInfo.dwAbsTime >> 6) & 63
            dwSecond = (contents.struSnapInfo.dwAbsTime >> 0) & 63
            strAbsTime = f"{dwYear}_{dwMonth}_{dwDay}_{dwHour}_{dwMinute}_{dwSecond}"
            print("contents.struSnapInfo.dwAbsTime: ", contents.struSnapInfo.dwAbsTime)
            # 人脸抓拍
            print("绝对时标: ", strAbsTime)
            print("性别:", contents.struSnapInfo.bySex)
            print("是否带眼镜:", contents.struSnapInfo.byGlasses)
            print("年龄段 : ", contents.struSnapInfo.byAgeGroup)
            print("抓拍人脸子图的长度 : ", contents.struSnapInfo.dwSnapFacePicLen)
            print("抓拍人脸子图的图片数据:", contents.struSnapInfo.pBuffer1)
            print("sIpV4:", contents.struSnapInfo.struDevInfo.struDevIP.sIpV4)

            # 对比
            # print("非授权名单人脸子图的长度:", contents.struBlockListInfo.dwBlockListPicLen)
            # print("非授权名单人脸子图的图片数据: ", contents.struBlockListInfo.pBuffer1)
            # print("结构体大小: ", contents.struBlockListInfo.struBlockListInfo.dwSize)
            # print("非授权名单等级: ", contents.struBlockListInfo.struBlockListInfo.byLevel)
            # print("性别: ", contents.struBlockListInfo.struBlockListInfo.struAttribute.bySex)
            # print("姓名 : ", contents.struBlockListInfo.struBlockListInfo.struAttribute.byName)
            print("*********************************************************")

        # ISAPI协议报警信息
        if lCommand == ALARM_LCOMMAND_ENUM.COMM_ISAPI_ALARM.value:
            print('ISAPI协议报警信息上传')
            Alarm_struct = cast(pAlarmInfo, LPNET_DVR_ALARM_ISAPI_INFO).contents

            print(
                f'byDataType: {Alarm_struct.byDataType}, '
                f'byPicturesNumber: {Alarm_struct.byPicturesNumber}, '
            )

            # 报警信息XML或者JSON数据
            DataLen = Alarm_struct.dwAlarmDataLen
            if DataLen != 0:
                from datetime import datetime
                # 获取当前时间的datetime对象
                current_time = datetime.now()
                timestamp_str = current_time.strftime('%Y%m%d_%H%M%S')

                buffInfo = string_at(Alarm_struct.pAlarmData, DataLen)
                with open(f'./pic/ISAPIInfo_{timestamp_str}.txt', 'wb') as fpInfo:
                    fpInfo.write(buffInfo)

            # 报警信息图片数据
            pNum = Alarm_struct.byPicturesNumber
            if pNum > 0:
                print('报警图片数量：', pNum)
                STRUCT = NET_DVR_ALARM_ISAPI_PICDATA * pNum
                PicStruct = cast(Alarm_struct.pPicPackData, POINTER(STRUCT)).contents
                for nPicIndex in range(pNum):
                    nSize = PicStruct[nPicIndex].dwPicLen
                    if nSize != 0:
                        from datetime import datetime
                        # 获取当前时间的datetime对象
                        current_time = datetime.now()
                        timestamp_str = current_time.strftime('%Y%m%d_%H%M%S')

                        buffInfo = string_at(PicStruct[nPicIndex].pPicData, nSize)
                        # strName = str(PicStruct[nPicIndex].szFilename)
                        sFileName = (f'./pic/ISAPI_Pic[{nPicIndex}]_{timestamp_str}.jpg')
                        with open(sFileName, 'wb') as fpPic:
                            fpPic.write(buffInfo)

        return True

    # 设置SDK初始化依赖库路径
    def SetSDKInitCfg(self):
        # 设置HCNetSDKCom组件库和SSL库加载路径
        if sys_platform == 'windows':
            basePath = os.getcwd().encode('gbk')
            strPath = basePath + b'\lib'
            sdk_ComPath = NET_DVR_LOCAL_SDK_PATH()
            sdk_ComPath.sPath = strPath
            print('strPath: ', strPath)
            if self.hikSDK.NET_DVR_SetSDKInitCfg(NET_SDK_INIT_CFG_TYPE.NET_SDK_INIT_CFG_SDK_PATH.value,
                                                 byref(sdk_ComPath)):
                print('NET_DVR_SetSDKInitCfg: 2 Succ')
            if self.hikSDK.NET_DVR_SetSDKInitCfg(NET_SDK_INIT_CFG_TYPE.NET_SDK_INIT_CFG_LIBEAY_PATH.value,
                                                 create_string_buffer(strPath + b'\libcrypto-1_1-x64.dll')):
                print('NET_DVR_SetSDKInitCfg: 3 Succ')
            if self.hikSDK.NET_DVR_SetSDKInitCfg(NET_SDK_INIT_CFG_TYPE.NET_SDK_INIT_CFG_SSLEAY_PATH.value,
                                                 create_string_buffer(strPath + b'\libssl-1_1-x64.dll')):
                print('NET_DVR_SetSDKInitCfg: 4 Succ')
        else:
            basePath = os.getcwd().encode('utf-8')
            strPath = basePath + b'\lib'
            sdk_ComPath = NET_DVR_LOCAL_SDK_PATH()
            sdk_ComPath.sPath = strPath
            if self.hikSDK.NET_DVR_SetSDKInitCfg(NET_SDK_INIT_CFG_TYPE.NET_SDK_INIT_CFG_SDK_PATH.value,
                                                 byref(sdk_ComPath)):
                print('NET_DVR_SetSDKInitCfg: 2 Succ')
            if self.hikSDK.NET_DVR_SetSDKInitCfg(NET_SDK_INIT_CFG_TYPE.NET_SDK_INIT_CFG_LIBEAY_PATH.value,
                                                 create_string_buffer(strPath + b'/libcrypto.so.1.1')):
                print('NET_DVR_SetSDKInitCfg: 3 Succ')
            if self.hikSDK.NET_DVR_SetSDKInitCfg(NET_SDK_INIT_CFG_TYPE.NET_SDK_INIT_CFG_SSLEAY_PATH.value,
                                                 create_string_buffer(strPath + b'/libssl.so.1.1')):
                print('NET_DVR_SetSDKInitCfg: 4 Succ')
        self.basePath = basePath

    # 通用设置，日志/回调事件类型等
    def GeneralSetting(self):

        # 日志的等级（默认为0）：0-表示关闭日志，1-表示只输出ERROR错误日志，2-输出ERROR错误信息和DEBUG调试信息，3-输出ERROR错误信息、DEBUG调试信息和INFO普通信息等所有信息
        self.hikSDK.NET_DVR_SetLogToFile(3, b'./SdkLog_Python/', False)

        # 通用参数配置
        sdkCfg = NET_DVR_LOCAL_GENERAL_CFG()
        sdkCfg.byAlarmJsonPictureSeparate = 1  # 控制JSON透传报警数据和图片是否分离，0-不分离，1-分离（分离后走COMM_ISAPI_ALARM回调返回）
        self.hikSDK.NET_DVR_SetSDKLocalCfg(NET_SDK_LOCAL_CFG_TYPE.NET_DVR_LOCAL_CFG_TYPE_GENERAL.value, byref(sdkCfg))

        # 设置报警回调函数
        self.hikSDK.NET_DVR_SetDVRMessageCallBack_V31(self.msg_callback_func, None)

    # 登录设备
    def LoginDev(self, ip, username, pwd):
        # 登录参数，包括设备地址、登录用户、密码等
        struLoginInfo = NET_DVR_USER_LOGIN_INFO()
        struLoginInfo.bUseAsynLogin = 0  # 同步登录方式
        struLoginInfo.sDeviceAddress = ip  # 设备IP地址
        struLoginInfo.wPort = 8000  # 设备服务端口
        struLoginInfo.sUserName = username  # 设备登录用户名
        struLoginInfo.sPassword = pwd  # 设备登录密码
        struLoginInfo.byLoginMode = 0

        # 设备信息, 输出参数
        struDeviceInfoV40 = NET_DVR_DEVICEINFO_V40()

        self.iUserID = self.hikSDK.NET_DVR_Login_V40(byref(struLoginInfo), byref(struDeviceInfoV40))
        if self.iUserID < 0:
            print("Login failed, error code: %d" % self.hikSDK.NET_DVR_GetLastError())
            self.hikSDK.NET_DVR_Cleanup()
        else:
            print('登录成功，设备序列号：%s' % str(struDeviceInfoV40.struDeviceV30.sSerialNumber, encoding="utf8").rstrip('\x00'))

    # 开启监听
    def StartListen(self, listenIp, listenPort):
        # 启动报警监听并且设置回调函数接收事件
        self.listenHandle = self.hikSDK.NET_DVR_StartListen_V30(listenIp, listenPort, self.msg_callback_func, None)
        print('self.listenHandle: ', self.listenHandle)
        if self.listenHandle < 0:
            print("NET_DVR_StartListen_V30失败, error code: %d" % self.hikSDK.NET_DVR_GetLastError())
            self.hikSDK.NET_DVR_Cleanup()
            exit()

    # 停止监听
    def StopListen(self):
        if self.listenHandle > -1:
            # 停止监听
            self.hikSDK.NET_DVR_StopListen_V30(self.listenHandle)

    # 登出设备
    def LogoutDev(self):
        if self.iUserID > -1:
            # 撤销布防，退出程序时调用
            self.hikSDK.NET_DVR_Logout(self.iUserID)

    # 设置网络参数
    def SetNetCFG(self):
        NETCFG_V50 = self.GetNetCFG()
        NETCFG_V50.struAlarmHostIpAddr.sIpV4 = b'10.9.137.19'
        NETCFG_V50.wAlarmHostIpPort = 7200
        if self.hikSDK.NET_DVR_SetDVRConfig(self.iUserID, NET_DVR_SET_NETCFG_V50, None, byref(NETCFG_V50),
                                            NETCFG_V50.dwSize):
            print('NET_DVR_SetDVRConfig Succ!!')

    # 获取网络参数
    def GetNetCFG(self):
        outBuffer = NET_DVR_NETCFG_V50()
        outBuffer.dwSize = sizeof(outBuffer)
        lpBytesReturned = C_LPDWORD(c_uint(1))
        if self.hikSDK.NET_DVR_GetDVRConfig(self.iUserID, NET_DVR_GET_NETCFG_V50, None, byref(outBuffer),
                                            outBuffer.dwSize, lpBytesReturned):
            struAlarmHostIpAddr = str(outBuffer.struAlarmHostIpAddr.sIpV4, encoding="utf8").rstrip('\x00')
            wAlarmHostIpPort = outBuffer.wAlarmHostIpPort
            print(f"告警管理主机地址: {struAlarmHostIpAddr}, 端口：{wAlarmHostIpPort}")

        else:
            print("NET_DVR_GetDVRConfig failed, error code: %d" % self.hikSDK.NET_DVR_GetLastError())
        return outBuffer


if __name__ == '__main__':
    dev = devClass()
    dev.SetSDKInitCfg()  # 设置SDK初始化依赖库路径
    dev.hikSDK.NET_DVR_Init()  # 初始化sdk
    dev.GeneralSetting()  # 通用设置，日志，回调函数等

    '''
    说明：这里包含布防和监听两种方式，其中，布防方式接收事件需要先布防，监听方式不需要布防，两种方式二选一即可。
    '''
    dev.LoginDev(ip=b'10.9.137.118', username=b"admin", pwd=b"hik12345")  # 登录设备
    dev.StartListen(listenIp=b'0.0.0.0', listenPort=7200)  # 开启监听，这里的ip为本地服务器的内网IP，监听之后需要

    # SetNetCFG设置监听参数，需要下发服务端的监听信息。
    dev.SetNetCFG()
    while True:
        user_input = input("请输入一个字符 (输入 Y 退出): ").strip().upper()
        if user_input == 'Y':
            break
    dev.StopListen()  # 停止监听
    dev.LogoutDev()  # 登出设备
    dev.hikSDK.NET_DVR_Cleanup()  # 反初始化sdk
