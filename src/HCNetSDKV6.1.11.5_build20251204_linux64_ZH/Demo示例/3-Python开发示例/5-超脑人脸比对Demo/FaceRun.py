# coding=utf-8
import os
import platform



# 系统环境标识
from module.Face.FacePicManage import FacePicManage
from module.common.TransIsapi import TransIsapi
from HCNetSDK import *

WINDOWS_FLAG = True

# 报警信息列表，报一次在回调中加1次记录
alarm_info = []


# 获取当前系统环境
def GetPlatform():
    sysstr = platform.system()
    print('' + sysstr)
    if sysstr != "Windows":
        global WINDOWS_FLAG
        WINDOWS_FLAG = False


# 设置SDK初始化依赖库路径
def SetSDKInitCfg():
    # 设置HCNetSDKCom组件库和SSL库加载路径
    # print(os.getcwd())
    if WINDOWS_FLAG:
        strPath = os.getcwd().encode('gbk')
        sdk_ComPath = NET_DVR_LOCAL_SDK_PATH()
        sdk_ComPath.sPath = strPath
        sdk.NET_DVR_SetSDKInitCfg(2, byref(sdk_ComPath))
        sdk.NET_DVR_SetSDKInitCfg(3, create_string_buffer(strPath + b'\libcrypto-1_1-x64.dll'))
        sdk.NET_DVR_SetSDKInitCfg(4, create_string_buffer(strPath + b'\libssl-1_1-x64.dll'))
    else:
        strPath = os.getcwd().encode('utf-8')
        sdk_ComPath = NET_DVR_LOCAL_SDK_PATH()
        sdk_ComPath.sPath = strPath
        sdk.NET_DVR_SetSDKInitCfg(2, byref(sdk_ComPath))
        sdk.NET_DVR_SetSDKInitCfg(3, create_string_buffer(strPath + b'/libcrypto.so.1.1'))
        sdk.NET_DVR_SetSDKInitCfg(4, create_string_buffer(strPath + b'/libssl.so.1.1'))


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
    sdk.NET_DVR_SetLogToFile(3, bytes(r'./sdklog', encoding="utf-8"), False)
    # 通用参数配置
    sdkCfg = NET_DVR_LOCAL_GENERAL_CFG()
    sdkCfg.byAlarmJsonPictureSeparate = 1
    sdk.NET_DVR_SetSDKLocalCfg(17, byref(sdkCfg))

    # 初始化用户id, 在调用正常是程序一般返回正数，故初始化一个负数
    UserID = c_long(-1)

    # 用户注册设备
    # c++传递进去的是byte型数据，需要转成byte型传进去，否则会乱码
    # 登录参数，包括设备地址、登录用户、密码等
    struLoginInfo = NET_DVR_USER_LOGIN_INFO()
    struLoginInfo.bUseAsynLogin = 0  # 同步登录方式
    struLoginInfo.sDeviceAddress = bytes("10.9.137.190", "ascii")  # 设备IP地址
    struLoginInfo.wPort = 8000  # 设备服务端口
    struLoginInfo.sUserName = bytes("admin", "ascii")  # 设备登录用户名
    struLoginInfo.sPassword = bytes("hik12345", "ascii")  # 设备登录密码
    struLoginInfo.byLoginMode = 0

    # 设备信息, 输出参数
    struDeviceInfoV40 = NET_DVR_DEVICEINFO_V40()
    UserID = sdk.NET_DVR_Login_V40(byref(struLoginInfo), byref(struDeviceInfoV40))
    if UserID < 0:
        print("Login failed, error code: %d" % sdk.NET_DVR_GetLastError())
        sdk.NET_DVR_Cleanup()
    else:
        print('登录成功，设备序列号：%s' % str(struDeviceInfoV40.struDeviceV30.sSerialNumber, encoding="utf8"))

    FDID = "DAE062F76837411C9DBEF948C82B98E1"  # 人脸库ID
    PID = "217E59A7C7F741A69047CBA157E53DF5"  # 人脸图片ID，可以通过POST / ISAPI / Intelligent / FDLib / FDSearch查询指定人脸库的人脸图片，其中包含ID
    FacePicManage.get_all_face_lib(UserID, sdk)   # 获取所有人脸库信息
    # FacePicManage.get_face_lib(UserID, FDID, sdk)   # 获取指定人脸库信息
    # FacePicManage.create_face_lib(UserID, "13", "faceContrast1", sdk) # 创建人脸库
    # FacePicManage.delete_face_lib(UserID, FDID, sdk)  # 删除一个人脸库
    # FacePicManage.upload_pic(UserID, FDID, sdk)  # 上传人脸图片到人脸库
    # HumanName = "testName"  # 人员姓名
    # FacePicManage.get_facelib_faceinfo(UserID, FDID, HumanName, sdk)    # 查询指定人脸库的人脸信息
    
    # 获取人脸对比库图片数据附加信息
    # requestUrl = "GET /ISAPI/Intelligent/FDLib/" + FDID + "/picture/" + PID
    # strOutXML = TransIsapi.put_isapi(UserID, requestUrl, "", sdk)
    # print(strOutXML)

    # 删除人脸比对库图片数据(包含附加信息)
    # requestUrl = "DELETE /ISAPI/Intelligent/FDLib/" + FDID + "/picture/" + PID
    # strOutXML = TransIsapi.put_isapi(UserID, requestUrl, "", sdk)
    # print(strOutXML)


    #按照图片搜索
    # ModeDataStr = TransIsapi.put_isapi(UserID, "POST /ISAPI/Intelligent/analysisImage/face", "", sdk, "..//..//resource//pic//FDLib.jpg")
    # ModeData = TransIsapi.convert_str_to_xml(ModeDataStr)
    # 使用模型数据检索人脸库
    # FacePicManage.FDSearch(UserID, FDID, ModeData, sdk)

    # 查询设备中存储的人脸比对结果信息
#    FacePicManage.FCSearch(UserID, FDID, sdk)


    # 注销用户，退出程序时调用
    flag = sdk.NET_DVR_Logout(UserID)
    print(sdk.NET_DVR_Logout(UserID))
    if UserID >= 0:
        if flag:
            print("设备注销成功")
        else:
            print("设备注销失败，错误码为：" + sdk.NET_DVR_GetLastError())
    # 释放SDK资源，退出程序时调用
    sdk.NET_DVR_Cleanup()
