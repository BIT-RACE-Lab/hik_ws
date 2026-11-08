# --*-- conding:utf-8 --*--
# @Time : 2024/5/11 15:06
# @Author : wangchao124
# @Email : wangchao124@hikvision.com
# @File : ParameterConfigurator.py
# @Software : PyCharm
import os
import platform
import time
from HCNetSDK import *
import re

# 系统环境标识
WINDOWS_FLAG = True


def GetPlatform():
    """
    获取当前系统环境
    @return:
    """
    sysstr = platform.system()
    print('' + sysstr)
    if sysstr != "Windows":
        global WINDOWS_FLAG
        WINDOWS_FLAG = False


def SetSDKInitCfg():
    """
    设置SDK初始化依赖库路径
    @return:
    """
    # print(os.getcwd())
    if WINDOWS_FLAG:
        strPath = os.getcwd().encode('gbk')
        sdk_ComPath = NET_DVR_LOCAL_SDK_PATH()
        sdk_ComPath.sPath = strPath
        sdk.NET_DVR_SetSDKInitCfg(2, byref(sdk_ComPath))
        sdk.NET_DVR_SetSDKInitCfg(3, create_string_buffer(strPath + b'\\libcrypto-1_1-x64.dll'))
        sdk.NET_DVR_SetSDKInitCfg(4, create_string_buffer(strPath + b'\\libssl-1_1-x64.dll'))
    else:
        strPath = os.getcwd().encode('utf-8')
        sdk_ComPath = NET_DVR_LOCAL_SDK_PATH()
        sdk_ComPath.sPath = strPath
        sdk.NET_DVR_SetSDKInitCfg(2, byref(sdk_ComPath))
        sdk.NET_DVR_SetSDKInitCfg(3, create_string_buffer(strPath + b'/libcrypto.so.1.1'))
        sdk.NET_DVR_SetSDKInitCfg(4, create_string_buffer(strPath + b'/libssl.so.1.1'))


def login_v40(ip, port, username, password):
    """
    设备登录V40 与V30功能一致
    @param ip:
    @param port:
    @param username:
    @param password:
    @return:
    """
    # 用户注册设备
    # c++传递进去的是byte型数据，需要转成byte型传进去，否则会乱码
    # 登录参数，包括设备地址、登录用户、密码等
    struLoginInfo = NET_DVR_USER_LOGIN_INFO()
    struLoginInfo.bUseAsynLogin = 0  # 同步登录方式 0- 否，1- 是
    struLoginInfo.sDeviceAddress = bytes(ip, "ascii")  # 设备IP地址
    struLoginInfo.wPort = port  # 设备服务端口
    struLoginInfo.sUserName = bytes(username, "ascii")  # 设备登录用户名
    struLoginInfo.sPassword = bytes(password, "ascii")  # 设备登录密码
    struLoginInfo.byLoginMode = 0

    # 设备信息, 输出参数
    struDeviceInfoV40 = NET_DVR_DEVICEINFO_V40()

    UserID = sdk.NET_DVR_Login_V40(byref(struLoginInfo), byref(struDeviceInfoV40))
    if UserID < 0:
        print("Login failed, error code: %d" % sdk.NET_DVR_GetLastError())
        sdk.NET_DVR_Cleanup()
    else:
        print(ip + '登录成功，设备序列号：%s' % str(struDeviceInfoV40.struDeviceV30.sSerialNumber, encoding="utf8"))
    return UserID


def get_device_status(UserId):
    """
    获取设备在线状态
    @param UserId:
    @return:
    """
    devStatus = sdk.NET_DVR_RemoteControl(UserId, NET_DVR_CHECK_USER_STATUS, None, 0)
    if devStatus:
        print("设备在线")
    else:
        print("设备不在线")


def get_ip():
    """
    获取服务器网卡信息
    @return:
    """
    # 假设每个IP地址最多为64个字符
    struByteArray = create_string_buffer(16 * 64)
    pInt = c_int(0)
    pEnableBind = c_bool(False)

    if not sdk.NET_DVR_GetLocalIP(byref(struByteArray), byref(pInt), pEnableBind):
        print("NET_DVR_GetLocalIP失败，错误号:", sdk.NET_DVR_GetLastError())
    else:
        inum = pInt.value
        num = 0
        for i in range(inum):
            # 解码字节数组为字符串
            ip_address = struByteArray.raw[i * 64: (i + 1) * 64].decode('utf-8')
            # 按空格分割字符串，获取每个IP地址
            ip_addresses = ip_address.split()
            for ip in enumerate(ip_addresses):
                ip_addresses = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', ip_address)
            for ip in ip_addresses:
                print("网卡序号:", num, ", 网卡IP:", ip)
                num += 1
            # 选择需要绑定的网卡
            if ip == "10.19.36.24":
                sdk.NET_DVR_SetValidIP(i, True)


def circle_get_pic(UserID):
    """
    设备抓图
    @param UserID:
    @return:
    """
    sdf = '%Y%m%d%H%M%S'
    result = False
    count = 0
    while not result:
        try:
            time.sleep(1)  # 设置暂停的时间 1 秒
            cur_time0 = time.strftime(sdf, time.localtime())
            count += 1
            filename = f"E:\\PIC\\{cur_time0}{count}.jpg"
            file_byte = filename.encode("utf-8")
            str_jpeg_parm = NET_DVR_JPEGPARA()
            str_jpeg_parm.wPicSize = 2
            str_jpeg_parm.wPicQuality = 0
            b_cap = sdk.NET_DVR_CaptureJPEGPicture(UserID, 34, byref(str_jpeg_parm), file_byte)
            if not b_cap:
                print("抓图失败,错误码为:", sdk.NET_DVR_GetLastError())
                return
            # 解析为日期对象
            date_object = time.strptime(time.strftime(sdf, time.localtime()), "%Y%m%d%H%M%S")

            # 格式化为标准日期格式
            formatted_date = time.strftime("%Y-%m-%d %H:%M:%S", date_object)
            print(formatted_date + f"--循环执行第{count}次")
            if count == 3:
                result = True
                break
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(e)


def bind_port():
    """
    端口绑定
    @return:
    """
    str_local_tcp_bind = NET_DVR_LOCAL_TCP_PORT_BIND_CFG()
    str_local_tcp_bind.wLocalBindTcpMinPort = 30000
    str_local_tcp_bind.wLocalBindTcpMaxPort = 30200

    if not sdk.NET_DVR_SetSDKLocalCfg(0, byref(str_local_tcp_bind)):
        print("绑定失败，错误码为", sdk.NET_DVR_GetLastError())
        return

    print("绑定成功")


def get_cfg(UserID):
    """
    获取设备的基本参数
    @param UserID:
    @return:
    """
    m_str_device_cfg = NET_DVR_DEVICECFG_V40()
    m_str_device_cfg.dwSize = sizeof(m_str_device_cfg)

    p_int = c_int(0)

    b_get_cfg = sdk.NET_DVR_GetDVRConfig(UserID, NET_DVR_GET_DEVICECFG_V40,
                                         0xFFFFFFFF, byref(m_str_device_cfg), sizeof(m_str_device_cfg), byref(p_int))
    if not b_get_cfg:
        print("获取参数失败  错误码：", sdk.NET_DVR_GetLastError())
        return

    print("获取参数成功")

    dvr_name = bytes(m_str_device_cfg.sDVRName).decode('gbk', 'ignore').strip('\x00')
    serial_number = bytes(m_str_device_cfg.sSerialNumber).decode('utf-8').strip('\x00')

    print("设备名称:", dvr_name, "设备序列号:", serial_number)
    print("模拟通道个数:", m_str_device_cfg.byChanNum)

    parse_version(m_str_device_cfg.dwSoftwareVersion)
    parse_build_time(m_str_device_cfg.dwSoftwareBuildDate, "软件")
    parse_build_time(m_str_device_cfg.dwDSPSoftwareBuildDate, "DSP")


def parse_version(version):
    """
    解析软件版本
    @param version:
    @return:
    """
    major = (version >> 24) & 0xFF
    minor = (version >> 16) & 0xFF
    build = version & 0xFFFF
    print("软件版本:" + str(major) + "." + str(minor) + "." + str(build))


def parse_build_time(build_time, format_str):
    """
    解析软件或DSP构建版本
    @param build_time: 构建日期
    @param format_str: 软件 or DSP
    @return:
    """
    year = (build_time >> 16) & 0xFFFF
    month = (build_time >> 8) & 0xFF
    day = build_time & 0xFF
    print(format_str + "构建日期:", year, "年", month, "月", day, "日")


def get_dev_time(UserID):
    """
    获取设备时间参数
    @param UserID:
    @return:
    """
    m_time = NET_DVR_TIME()

    p_time = byref(m_time)
    p_int = c_int(0)

    b_get_time = sdk.NET_DVR_GetDVRConfig(UserID, NET_DVR_GET_TIMECFG, 0xFFFFFFFF, p_time, sizeof(m_time), byref(p_int))
    if not b_get_time:
        print("获取时间参数失败，错误码：", sdk.NET_DVR_GetLastError())
        return
    print("年:", m_time.dwYear, "\n月:", m_time.dwMonth, "\n日:", m_time.dwDay, "\n时:", m_time.dwHour,
          "\n分:", m_time.dwMinute, "\n秒:", m_time.dwSecond)


def get_pic_cfg(UserID):
    """
    获取设备的图像参数-移动侦测高亮显示
    @param UserID:
    @return:
    """
    str_pic_cfg = NET_DVR_PICCFG_V40()
    str_pic_cfg.dwSize = sizeof(str_pic_cfg)

    p_str_pic_cfg = byref(str_pic_cfg)
    l_channel = c_int(1)
    p_int = c_int(0)

    b_get_pic_cfg = sdk.NET_DVR_GetDVRConfig(UserID, NET_DVR_GET_PICCFG_V40, l_channel.value,
                                             p_str_pic_cfg, sizeof(str_pic_cfg), byref(p_int))
    if not b_get_pic_cfg:
        print("获取图像参数失败，错误码：", sdk.NET_DVR_GetLastError())
        return

    print("通道号:", l_channel.value)
    print("通道名称:", bytes(str_pic_cfg.sChanName).decode('gbk').strip('\x00'))
    print("预览的图像是否显示OSD:", str_pic_cfg.dwShowOsd)
    enable_display = str_pic_cfg.struMotion.byEnableDisplay

    print("移动侦测高亮显示是否开启:", enable_display)

    # 修改移动侦测高亮显示参数
    str_pic_cfg.dwShowOsd = 0
    str_pic_cfg.struMotion.byEnableDisplay = 1

    b_set_pic_cfg = sdk.NET_DVR_SetDVRConfig(UserID, NET_DVR_SET_PICCFG_V40, l_channel.value,
                                             p_str_pic_cfg, sizeof(str_pic_cfg))
    if not b_set_pic_cfg:
        print("设置图像参数移动侦测高亮参数失败，错误码：", sdk.NET_DVR_GetLastError())
    else:
        print("设置移动侦测高亮参数成功")


def get_usr_cfg(UserID):
    """
    获取用户参数
    @param UserID:
    @return:
    """
    usercfg = NET_DVR_USER_V30()
    usercfg.dwSize = sizeof(usercfg)
    lChannel = c_long(1)
    pInt = ctypes.pointer(ctypes.c_int(0))

    b_GetUserCfg = sdk.NET_DVR_GetDVRConfig(
        UserID,
        NET_DVR_GET_USERCFG_V30,
        lChannel,
        byref(usercfg),
        sizeof(usercfg),
        pInt
    )

    if not b_GetUserCfg:
        error_code = sdk.NET_DVR_GetLastError()
        print(f"获取用户参数失败，错误码：{error_code}")
        return
    user_name = bytes(usercfg.struUser[0].sUserName).decode('utf8').strip('\x00')
    user_password = bytes(usercfg.struUser[0].sPassword).decode('utf8').strip('\x00')
    print(f"name： {user_name}")
    print(f"password： {user_password}")


# 定义回调函数类型
FLOWTESTCALLBACK = CFUNCTYPE(None, c_int, POINTER(NET_DVR_FLOW_INFO), c_void_p)


# 定义回调函数
def flowTestCallback(lFlowHandle, pFlowInfo, pUser):
    pFlowInfo = pFlowInfo.contents
    print("发送的流量数据：" + str(pFlowInfo.dwSendFlowSize))
    print("接收的流量数据：" + str(pFlowInfo.dwRecvFlowSize))


def netFlowDec(UserID):
    """
    网络流量检测
    @param UserID:
    @return:
    """
    struFlowPam = NET_DVR_FLOW_TEST_PARAM()
    struFlowPam.dwSize = sizeof(NET_DVR_FLOW_TEST_PARAM)
    struFlowPam.lCardIndex = 0
    struFlowPam.dwInterval = 1
    flowcallback = FLOWTESTCALLBACK(flowTestCallback)
    FlowHandle = sdk.NET_DVR_StartNetworkFlowTest(UserID, byref(struFlowPam), flowcallback, None)
    if FlowHandle <= -1:
        print("开启流量检测失败，错误码：" + str(sdk.NET_DVR_GetLastError()))
    else:
        print("开启流量检测成功")

    # 等待 20 秒
    time.sleep(20)

    # 停止流量检测
    sdk.NET_DVR_StopNetworkFlowTest(FlowHandle)


def search_record_time(UserID):
    """
    录像起止时间查询
    @param UserID:
    @return:
    """
    stru_rec_inq = NET_DVR_RECORD_TIME_SPAN_INQUIRY()
    stru_rec_inq.dwSize = sizeof(stru_rec_inq)
    stru_rec_inq.byType = 0
    stru_rec_span = NET_DVR_RECORD_TIME_SPAN()
    # 通道号说明：一般IPC / IPD通道号为1，32路以及以下路数的NVR的IP通道通道号从33开始，64路及以上路数的NVR的IP通道通道号从1开始。
    if not sdk.NET_DVR_InquiryRecordTimeSpan(UserID, 35, byref(stru_rec_inq), byref(stru_rec_span)):
        print("录像起止时间查询失败，错误码：", sdk.NET_DVR_GetLastError())
    else:
        print("录像起止时间查询成功")
        print("开启时间： 年：", stru_rec_span.strBeginTime.dwYear)
        print("开启时间： 月：", stru_rec_span.strBeginTime.dwMonth)
        print("开启时间： 日：", stru_rec_span.strBeginTime.dwDay)
        print("开启时间： 时：", stru_rec_span.strBeginTime.dwHour)
        print("停止时间： 年：", stru_rec_span.strEndTime.dwYear)
        print("停止时间： 月：", stru_rec_span.strEndTime.dwMonth)
        print("停止时间： 日：", stru_rec_span.strEndTime.dwDay)
        print("停止时间： 时：", stru_rec_span.strEndTime.dwHour)


def get_rec_month(UserID):
    """
    月历录像查询
    @param UserID:
    @return:
    """
    # 初始化查询参数结构体
    stru_mrd_sea_param = NET_DVR_MRD_SEARCH_PARAM()
    stru_mrd_sea_param.dwSize = sizeof(stru_mrd_sea_param)
    stru_mrd_sea_param.wYear = 2024
    stru_mrd_sea_param.byMonth = 4
    stru_mrd_sea_param.struStreamInfo.dwChannel = 33  # 假设直接赋值通道号

    # 初始化查询结果结构体
    stru_mrd_sea_resu = NET_DVR_MRD_SEARCH_RESULT()
    stru_mrd_sea_resu.dwSize = sizeof(stru_mrd_sea_resu)

    # 调用查询函数
    list_ref = c_int(0)
    b_get_result = sdk.NET_DVR_GetDeviceConfig(UserID, NET_DVR_GET_MONTHLY_RECORD_DISTRIBUTION, 0,
                                               byref(stru_mrd_sea_param), sizeof(NET_DVR_MRD_SEARCH_PARAM),
                                               byref(list_ref),
                                               byref(stru_mrd_sea_resu),
                                               sizeof(NET_DVR_MRD_SEARCH_RESULT)
                                               )

    if not b_get_result:
        print("月历录像查询失败，错误码：", sdk.NET_DVR_GetLastError())
    else:
        for i in range(31):
            day = i + 1
            print(f"{day}号是否有录像文件: {stru_mrd_sea_resu.byRecordDistribution[i]}")


def get_gis_info(UserID):
    """
    球机GIS信息获取
    @param UserID:
    @return:
    """
    # 创建结构体实例
    stru_std_cfg = NET_DVR_STD_CONFIG()
    stru_gis_info = NET_DVR_GIS_INFO()

    # 设置条件缓冲区和输出缓冲区
    lchannel = c_int(1)
    stru_std_cfg.lpCondBuffer = addressof(lchannel)
    stru_std_cfg.dwCondSize = 4
    stru_std_cfg.lpOutBuffer = addressof(stru_gis_info)
    stru_std_cfg.dwOutSize = sizeof(stru_gis_info)

    # 假设 hcnetsdk 是加载的HCNetSDK库
    get_std_config = sdk.NET_DVR_GetSTDConfig(UserID, NET_DVR_GET_GISINFO, byref(stru_std_cfg))

    if not get_std_config:
        print("查询GIS信息失败，错误码：", sdk.NET_DVR_GetLastError())
    else:
        print("查询成功")
        print(stru_gis_info.struPtzPos.fPanPos)
        print(stru_gis_info.struPtzPos.fTiltPos)
        print(stru_gis_info.struPtzPos.fZoomPos)
        print(stru_gis_info.fHorizontalValue)
        print(stru_gis_info.fVerticalValue)


def setPTZcfg(UserID):
    """
    球机PTZ参数获取设置
    @param UserID:
    @return:
    """
    struPtTZPos = NET_DVR_PTZPOS()
    pUsers = c_int(1)

    # 获取PTZ坐标信息
    b_GetPTZ = sdk.NET_DVR_GetDVRConfig(UserID, NET_DVR_GET_PTZPOS, 1, byref(struPtTZPos), sizeof(struPtTZPos),
                                        byref(pUsers))

    if not b_GetPTZ:
        print("获取PTZ坐标信息失败，错误码：", sdk.NET_DVR_GetLastError())
    else:
        wPanPos = int(hex(struPtTZPos.wPanPos).replace('0x', ''), 16)
        WPanPos = wPanPos * 0.1
        wTiltPos = int(hex(struPtTZPos.wTiltPos).replace('0x', ''), 16)
        WTiltPos = wTiltPos * 0.1
        wZoomPos = int(hex(struPtTZPos.wZoomPos).replace('0x', ''), 16)
        WZoomPos = wZoomPos * 0.1

        print("P参数：", WPanPos)
        print("T参数：", WTiltPos)
        print("Z参数：", WZoomPos)

    # 设置PTZ坐标信息（取消注释下面的代码来启用设置功能）
    # struPtTZPos.wAction = 2
    # pHex = "13669"
    # pInter = int(pHex)
    # struPtTZPos.wPanPos = c_short(pInter)
    # b_SetPTZ = sdk.NET_DVR_SetDVRConfig(UserID, NET_DVR_SET_PTZPOS, 1, byref(struPtTZPos), sizeof(struPtTZPos))
    #
    # if not b_SetPTZ:
    #     print("设置PTZ坐标信息失败，错误码：", sdk.NET_DVR_GetLastError())
    # else:
    #     print("设置PTZ成功")


def setPTZLOCKCFG(UserID):
    """
    设置云台锁定信息
    @param UserID:
    @return:
    """
    # 初始化NET_DVR_PTZ_LOCKCFG结构体
    struPtzLockCfg = NET_DVR_PTZ_LOCKCFG()
    struPtzLockCfg.dwSize = sizeof(struPtzLockCfg)

    # 定义指针和其他变量
    lChannel = c_int(1)
    pInt = c_int(0)

    # 获取云台锁定信息
    b_GetPtzLockCfg = sdk.NET_DVR_GetDVRConfig(UserID, NET_DVR_GET_PTZLOCKCFG, lChannel, byref(struPtzLockCfg),
                                               sizeof(struPtzLockCfg), byref(pInt))

    if not b_GetPtzLockCfg:
        print(f"获取云台锁定信息失败，错误码：{sdk.NET_DVR_GetLastError()}")
        return

    print(f"通道号：{lChannel.value}")
    print(f"云台锁定控制状态为：{struPtzLockCfg.byWorkMode}")

    # 设置云台锁定信息
    struPtzLockCfg.byWorkMode = 0  # 0- 解锁，1- 锁定

    b_SetPtzLockCfg = sdk.NET_DVR_SetDVRConfig(UserID, NET_DVR_SET_PTZLOCKCFG, lChannel, byref(struPtzLockCfg),
                                               sizeof(struPtzLockCfg))

    if not b_SetPtzLockCfg:
        print(f"设置云台锁定信息失败，错误码：{sdk.NET_DVR_GetLastError()}")
    else:
        print("设置云台锁定信息成功")
        print(f"云台锁定控制状态当前为：{struPtzLockCfg.byWorkMode}")


def PTZControlOther(UserID):
    """
    云台控制
    @param UserID:
    @return:
    """
    # 调用云台控制函数
    b_ptzcontrol = sdk.NET_DVR_PTZControl_Other(UserID, 1, TILT_UP, 0)

    if not b_ptzcontrol:
        print(f"云台向上转动失败，错误码：{sdk.NET_DVR_GetLastError()}")
    else:
        print("设置向上转动成功")


def get_camera_para(UserID):
    """
    获取(设置)前端参数(扩展)
    @param UserID:
    @return:
    """
    struCameraParam = NET_DVR_CAMERAPARAMCFG_EX()
    struCameraParam.dwSize = sizeof(struCameraParam)
    lChannel = c_int(1)
    pInt = c_int(0)
    b_GetCameraParam = sdk.NET_DVR_GetDVRConfig(UserID, NET_DVR_GET_CCDPARAMCFG_EX, lChannel, byref(struCameraParam),
                                                sizeof(struCameraParam), byref(pInt))
    if not b_GetCameraParam:
        print("获取前端参数失败，错误码：" + str(sdk.NET_DVR_GetLastError()))
        return

    print("是否开启旋转：" + str(struCameraParam.struCorridorMode.byEnableCorridorMode))

    struCameraParam.struCorridorMode.byEnableCorridorMode = 1
    b_SetCameraParam = sdk.NET_DVR_SetDVRConfig(
        UserID, NET_DVR_SET_CCDPARAMCFG_EX, 1, byref(struCameraParam), sizeof(struCameraParam))
    if not b_SetCameraParam:
        print("设置前端参数失败，错误码：" + str(sdk.NET_DVR_GetLastError()))
        return
    print("设置成功")


def getFocusMode(UserID):
    """
    获取快球聚焦模式信息
    @param UserID:
    @return:
    """
    struFocusMode = NET_DVR_FOCUSMODE_CFG()
    struFocusMode.dwSize = sizeof(struFocusMode)
    pInt = c_int(0)
    b_GetCameraParam = sdk.NET_DVR_GetDVRConfig(UserID, NET_DVR_GET_FOCUSMODECFG, 1, byref(struFocusMode),
                                                sizeof(struFocusMode), byref(pInt))
    if not b_GetCameraParam:
        print("获取快球聚焦模式失败，错误码：", sdk.NET_DVR_GetLastError())
        return

    print("聚焦模式：", struFocusMode.byFocusMode)

    # 修改聚焦模式配置
    struFocusMode.byFocusMode = 2
    struFocusMode.byFocusDefinitionDisplay = 1
    struFocusMode.byFocusSpeedLevel = 3

    b_SetCameraParam = sdk.NET_DVR_SetDVRConfig(UserID, NET_DVR_SET_FOCUSMODECFG, 1, byref(struFocusMode),
                                                sizeof(struFocusMode))
    if not b_SetCameraParam:
        print("设置快球聚焦模式失败，错误码：", sdk.NET_DVR_GetLastError())
        return

    print("设置成功")


def getIPChannelInfo(UserID):
    """
    获取IP通道
    @param UserID:
    @return:
    """
    pInt = c_int(0)  # 获取IP接入配置参数
    m_strIpparaCfg = NET_DVR_IPPARACFG_V40()
    m_strIpparaCfg.dwSize = sizeof(m_strIpparaCfg)

    lpIpParaConfig = byref(m_strIpparaCfg)
    bRet = sdk.NET_DVR_GetDVRConfig(UserID, NET_DVR_GET_IPPARACFG_V40, 0, lpIpParaConfig, sizeof(m_strIpparaCfg),
                                    byref(pInt))
    if not bRet:
        print("获取IP接入配置参数失败，错误码：", sdk.NET_DVR_GetLastError())
        return
    print("起始数字通道号：", m_strIpparaCfg.dwStartDChan)

    for iChannum in range(m_strIpparaCfg.dwDChanNum):
        channum = iChannum + m_strIpparaCfg.dwStartDChan
        strPicCfg = NET_DVR_PICCFG_V40()
        strPicCfg.dwSize = sizeof(NET_DVR_PICCFG_V40)
        pStrPicCfg = byref(strPicCfg)
        lChannel = channum
        pInt = c_int(0)

        b_GetPicCfg = sdk.NET_DVR_GetDVRConfig(UserID, NET_DVR_GET_PICCFG_V40, lChannel, pStrPicCfg, sizeof(strPicCfg),
                                               byref(pInt))
        # if not b_GetPicCfg:
        #     print("获取图像参数失败，错误码：", sdk.NET_DVR_GetLastError())
        #     continue

        if m_strIpparaCfg.struStreamMode[iChannum].byGetStreamType == 0:
            print("--------------第", iChannum + 1, "个通道------------------")
            channel = m_strIpparaCfg.struStreamMode[iChannum].uGetStream.struChanInfo.byIPID + (
                    m_strIpparaCfg.struStreamMode[iChannum].uGetStream.struChanInfo.byIPIDHigh * 256)
            print("channel:", channel)
            if channel > 0:
                ip_addr = bytes(m_strIpparaCfg.struIPDevInfo[channel - 1].struIP.sIpV4).decode('utf8').strip('\x00')
                print("ip：", ip_addr)
                name = bytes(strPicCfg.sChanName).decode('utf8').strip('\x00')
                print("name：", name)

            if m_strIpparaCfg.struStreamMode[iChannum].uGetStream.struChanInfo.byEnable == 1:
                print("IP通道", channum, "在线")
            else:
                print("IP通道", channum, "不在线")


def DevWorkStateCB(pUserdata, UserID, lpWorkState):
    print(f"设备状态: {lpWorkState.dwDeviceStatic}")
    for i in range(MAX_CHANNUM_V40):
        channel = i + 1
        print(f"第{channel}通道是否在录像: {lpWorkState.struChanStatic[i].byRecordStatic}")
    return True


setdvrwork_state_callback_func = DEV_WORK_STATE_CB(DevWorkStateCB)


def regular_inspection():
    struCheckStatus = NET_DVR_CHECK_DEV_STATE()
    struCheckStatus.dwTimeout = 30000  # 定时检测设备工作状态，单位：ms，0表示使用默认值(30000)，最小值为1000
    struCheckStatus.fnStateCB = setdvrwork_state_callback_func
    b_state = sdk.NET_DVR_StartGetDevState(struCheckStatus)
    if not b_state:
        print(f"定时巡检设备状态失败: {sdk.NET_DVR_GetLastError()}")


def getPTZAbsoluteEx(UserID):
    """
    获取高精度PTZ绝对位置配置,一般热成像设备支持
    @param UserID:
    @return:
    """
    struSTDcfg = NET_DVR_STD_CONFIG()
    lchannel = c_int(1)
    struSTDcfg.lpCondBuffer = addressof(lchannel)
    struSTDcfg.dwCondSize = sizeof(c_int)
    struPTZ = NET_DVR_PTZABSOLUTEEX_CFG()
    struSTDcfg.lpOutBuffer = addressof(struPTZ)
    struSTDcfg.dwOutSize = sizeof(struPTZ)

    bGetPTZ = sdk.NET_DVR_GetSTDConfig(UserID, NET_DVR_GET_PTZABSOLUTEEX, byref(struSTDcfg))
    if not bGetPTZ:
        print("获取PTZ参数错误, 错误码：", sdk.NET_DVR_GetLastError())
        return

    print("焦距范围：", struPTZ.dwFocalLen)
    print("聚焦参数：", struPTZ.struPTZCtrl.dwFocus)


def get_GB28181_info(UserID):
    """
    获取GB28181参数
    @param UserID:
    @return:
    """
    stream_info = NET_DVR_STREAM_INFO()
    stream_info.dwSize = sizeof(stream_info)  # 设置结构体大小
    stream_info.dwChannel = 1  # 设置通道

    gbt28181_chaninfo_cfg = NET_DVR_GBT28181_CHANINFO_CFG()
    gbt28181_chaninfo_cfg.dwSize = sizeof(gbt28181_chaninfo_cfg)

    lpInBuffer = byref(stream_info)
    lpOutBuffer = byref(gbt28181_chaninfo_cfg)
    lpBytesReturned = pointer(c_int(0))

    # 3251对应它的宏定义
    bRet = sdk.NET_DVR_GetDeviceConfig(UserID, 3251, 1, lpInBuffer,
                                       sizeof(stream_info), lpBytesReturned, lpOutBuffer, sizeof(gbt28181_chaninfo_cfg))

    if not bRet:
        print("获取失败,错误码：", sdk.NET_DVR_GetLastError())
        return
    print(bytes(gbt28181_chaninfo_cfg.szVideoChannelNumID).decode('utf8').strip('\x00'))


def get_aes_info(UserID):
    """
    获取码流加密信息
    @param UserID:
    @return:
    """
    net_dvr_aes_key_info = NET_DVR_AES_KEY_INFO()
    pnet_dvr_aes_key_info = pointer(net_dvr_aes_key_info)
    pInt = c_int(0)

    # 假设pyhikvision提供了类似的方法
    b_GetCfg = sdk.NET_DVR_GetDVRConfig(UserID, NET_DVR_GET_AES_KEY, 0xFFFFFFFF, pnet_dvr_aes_key_info,
                                        sizeof(net_dvr_aes_key_info), byref(pInt))

    if not b_GetCfg:
        print("获取码流加密失败  错误码：", sdk.NET_DVR_GetLastError())
    else:
        print("获取码流加密信息成功")


def getCruisePoint(UserID):
    """
    设置球机预置点
    @param UserID:
    @return:
    """
    # 初始化NET_DVR_CRUISEPOINT_COND结构
    struCruisepointCond = NET_DVR_CRUISEPOINT_COND()
    struCruisepointCond.dwSize = sizeof(struCruisepointCond)
    struCruisepointCond.dwChan = 1
    struCruisepointCond.wRouteNo = 1

    # 初始化NET_DVR_CRUISEPOINT_V50结构
    struCruisepointV40 = NET_DVR_CRUISEPOINT_V50()
    struCruisepointV40.dwSize = sizeof(struCruisepointV40)

    # 错误信息列表
    pInt = c_int(0)
    lpStatusList = pointer(pInt)

    # 调用SDK的NET_DVR_GetDeviceConfig方法
    flag = sdk.NET_DVR_GetDeviceConfig(UserID, 6714, 1, byref(struCruisepointCond), sizeof(struCruisepointCond),
                                       lpStatusList, byref(struCruisepointV40), sizeof(struCruisepointV40)
                                       )

    if not flag:
        iErr = sdk.NET_DVR_GetLastError()
        print("NET_DVR_STDXMLConfig失败，错误号：", iErr)
        return


def getPictoPointer(UserID):
    """
    抓图保存到缓冲区、文件
    @param UserID: 用户ID
    @return: None
    """
    # 初始化NET_DVR_JPEGPARA结构
    jpegpara = NET_DVR_JPEGPARA()
    jpegpara.wPicSize = 255
    jpegpara.wPicQuality = 0

    M1 = 8 * 1024 * 1024  # 8 MB 缓冲区
    buff1 = (c_ubyte * M1)()  # 创建缓冲区
    byte_array = cast(buff1, POINTER(c_ubyte))  # 获取缓冲区指针
    ret = c_int(0)

    # 调用SDK的NET_DVR_CaptureJPEGPicture_NEW方法
    b = sdk.NET_DVR_CaptureJPEGPicture_NEW(UserID, 1, byref(jpegpara), byte_array, M1, byref(ret))

    if not b:
        err = sdk.NET_DVR_GetLastError()
        print("抓图失败：", err)
        return

    print("抓图成功")
    # 从缓冲区中获取图像数据大小
    image_size = ret.value
    filename = "captured_image.jpg"
    # 将缓冲区中的数据保存为JPEG文件
    with open(filename, 'wb') as f:
        f.write(bytearray(buff1)[:image_size])

    print(f"图像已保存为 {filename}")


def getRs485Cfg(lUserID):
    """
    获取报警主机RS485参数
    @param lUserID: 用户ID
    @return: None
    """
    rs485CFG = NET_DVR_ALARM_RS485CFG()
    rs485CFG.dwSize = sizeof(rs485CFG)
    pointer = byref(rs485CFG)
    pInt1 = c_int(0)
    # 调用SDK的NET_DVR_GetDVRConfig方法
    bGetRs485 = sdk.NET_DVR_GetDVRConfig(lUserID, NET_DVR_GET_ALARM_RS485CFG, 1, pointer, rs485CFG.dwSize,
                                         byref(pInt1))
    if not bGetRs485:
        err = sdk.NET_DVR_GetLastError()
        print("获取报警主机RS485参数失败！错误号：", err)
        return
    else:
        print("前端设备名称：", bytes(rs485CFG.sDeviceName).decode('utf8').strip('\x00'))
    return


def getRs485SlotInfo(UserID):
    """
    获取报警主机RS485槽位参数
    """
    strRs485SlotCFG = NET_DVR_ALARMHOST_RS485_SLOT_CFG()
    strRs485SlotCFG.dwSize = sizeof(strRs485SlotCFG)
    pRs485SlotCFG = pointer(strRs485SlotCFG)
    pInt1 = pointer(c_int(0))
    Schannel = "0000000100000001"  # 高2字节表示485通道号，低2字节表示槽位号，都从1开始
    channel = int(Schannel, 2)
    bRs485Slot = sdk.NET_DVR_GetDVRConfig(UserID, NET_DVR_GET_ALARMHOST_RS485_SLOT_CFG, channel,
                                          pRs485SlotCFG, strRs485SlotCFG.dwSize, pInt1)
    if not bRs485Slot:
        print("获取报警主机RS485槽位参数失败！错误号：", sdk.NET_DVR_GetLastError())
        return
    print(pRs485SlotCFG.contents)


if __name__ == '__main__':

    # 获取系统平台
    GetPlatform()

    # 加载库,先加载依赖库
    if WINDOWS_FLAG:
        os.chdir(r'./lib/win')
        sdk = ctypes.CDLL(r'./HCNetSDK.dll')
    else:
        os.chdir(r'./lib/linux')
        sdk = cdll.LoadLibrary(r'./libhcnetsdk.so')

    SetSDKInitCfg()  # 设置组件库和SSL库加载路径

    # 初始化
    sdk.NET_DVR_Init()
    # 启用SDK写日志
    sdk.NET_DVR_SetLogToFile(3, bytes('./SdkLog_Python/', encoding="utf-8"), False)

    # 通用参数配置
    sdkCfg = NET_DVR_LOCAL_GENERAL_CFG()
    sdkCfg.byAlarmJsonPictureSeparate = 1
    sdk.NET_DVR_SetSDKLocalCfg(17, byref(sdkCfg))

    # 登录设备
    UserID = login_v40("10.9.137.15", 8000, "admin", "hik12345")
    get_device_status(UserID)   # 获取设备在线状态
    # get_ip()  # 获取服务器网卡信息
    # circle_get_pic(UserID)  # 设备抓图
    # bind_port()  # 端口绑定
    # get_cfg(UserID)  # 获取设备的基本参数
    # get_dev_time(UserID)  # 获取设备时间参数
    # get_pic_cfg(UserID)  # 获取设备的图像参数-移动侦测高亮显示
    # get_usr_cfg(UserID)  # 获取用户参数
    # netFlowDec(UserID)  # 网络流量检测
    # search_record_time(UserID)  # 录像起止时间查询
    # get_rec_month(UserID)  # 月历录像查询
    # get_gis_info(UserID)  # 球机GIS信息获取
    # setPTZcfg(UserID)  # 球机PTZ参数获取设置
    # setPTZLOCKCFG(UserID)  # 设置云台锁定信息
    # PTZControlOther(UserID)  # 云台控制
    # get_camera_para(UserID)  # 获取(设置)前端参数(扩展)
    # getFocusMode(UserID)  # 获取快球聚焦模式信息
    # getIPChannelInfo(UserID)  # 获取IP通道
    # regular_inspection()  # 定时巡检设备
    # getPTZAbsoluteEx(UserID)  # 获取高精度PTZ绝对位置配置,一般热成像设备支持
    # get_GB28181_info(UserID)  # 获取GB28181参数
    # get_aes_info(UserID)  # 获取码流加密信息
    # getCruisePoint(UserID)  # 设置球机预置点
    # getPictoPointer(UserID)  # 抓图保存到缓冲区、文件
    # getRs485Cfg(UserID)  # 获取报警主机RS485参数
    # getRs485SlotInfo(UserID)  # 获取报警主机RS485槽位参数

    # 注销用户，退出程序时调用
    if sdk.NET_DVR_Logout(UserID):
        print("注销成功")

    # 释放SDK资源，退出程序时调用
    sdk.NET_DVR_Cleanup()
