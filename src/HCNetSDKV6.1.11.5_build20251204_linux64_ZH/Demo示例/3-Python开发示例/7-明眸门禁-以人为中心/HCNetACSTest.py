# coding=utf-8
import os
import platform

from ACS import ACSUserManager
from ACS.CardManager import CardManage
from ACS.FaceManage import FaceManage
from ACS.ACSManage import ACSManage
from HCNetSDK import *

# 系统环境标识
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
    struLoginInfo.sDeviceAddress = bytes("10.10.138.12", "ascii")  # 设备IP地址
    struLoginInfo.wPort = 8000  # 设备服务端口
    struLoginInfo.sUserName = bytes("admin", "ascii")  # 设备登录用户名
    struLoginInfo.sPassword = bytes("", "ascii")  # 设备登录密码
    struLoginInfo.byLoginMode = 0

    # 设备信息, 输出参数
    struDeviceInfoV40 = NET_DVR_DEVICEINFO_V40()
    UserID = sdk.NET_DVR_Login_V40(byref(struLoginInfo), byref(struDeviceInfoV40))
    if UserID < 0:
        print("Login failed, error code: %d" % sdk.NET_DVR_GetLastError())
        sdk.NET_DVR_Cleanup()
    else:
        print('登录成功，设备序列号：%s' % str(struDeviceInfoV40.struDeviceV30.sSerialNumber, encoding="utf8"))

    while True:
        str_input = input("请输入您想要执行的demo实例! （退出请输入yes）\n").strip().lower()
        if str_input == "yes":
            break
        # 人员工号管理
        elif str_input == "1":
            print("查询人员")
            ACSUserManager.UserManage().search_user_info(UserID, sdk)
        elif str_input == "2":
            print("添加修改人员")
            ACSUserManager.UserManage().add_user_info(UserID, 'employeeNo1', sdk)
        elif str_input == "3":
            print("删除人员")
            ACSUserManager.UserManage().delete_user_info(UserID, sdk)
        # 卡号管理
        elif str_input == "4":
            print("查询卡号")
            CardManage.search_card_info(UserID, "employeeNo1", sdk)
        elif str_input == "5":
            print("添加卡号")
            CardManage.add_card_info(UserID, "123456", sdk)
        elif str_input == "6":
            print("查询所有卡号")
            CardManage.search_all_card_info(UserID, sdk)
        elif str_input == "7":
            print("删除指定工号下人员的所有工卡")
            CardManage.delete_card_info(UserID, "employeeNo1", sdk)
        elif str_input == "8":
            print("删除所有人员工卡，谨慎使用")
            CardManage.delete_all_card_info(UserID, sdk)
        elif str_input == "9":
            print("获取所有下发卡的数量")
            CardManage.get_all_card_number(UserID, sdk)
        # 人脸管理
        elif str_input == "10":
            print("人脸查询")
            FaceManage.search_face_info(UserID, "employeeNo1", sdk)
        elif str_input == "11":
            print("二进制下发人脸")
            FaceManage.add_face_by_binary(UserID, "employeeNo1", sdk)
        elif str_input == "12":
            print("url下发人脸")
            FaceManage.add_face_by_url(UserID, "employeeNo1", sdk)
        elif str_input == "13":
            print("删除人脸")
            FaceManage.delete_face_info(UserID, "employeeNo1", sdk)
        elif str_input == "14":
            print("人脸采集")
            FaceManage.capture_face_info(UserID, sdk)
        # 门禁主机管理
        elif str_input == "15":
            print("获取(设置)门禁主机参数")
            ACSManage.acs_cfg(UserID, sdk)
        elif str_input == "16":
            print("获取门禁主机工作状态")
            ACSManage.get_acs_status(UserID, sdk)
        elif str_input == "17":
            print("远程控门")
            ACSManage.remote_control_gate(UserID, sdk)
        else:
            print("未知的指令操作!请重新输入!\n")
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
