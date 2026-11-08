# coding=utf-8

import ctypes
import sys
from ctypes import *

# 回调函数类型定义

if 'linux' in sys.platform:
    fun_ctype = CFUNCTYPE
else:
    fun_ctype = WINFUNCTYPE

# 云台控制命令
LIGHT_PWRON = 2  # 接通灯光电源
WIPER_PWRON = 3  # 接通雨刷开关
FAN_PWRON = 4  # 接通风扇开关
HEATER_PWRON = 5  # 接通加热器开关
AUX_PWRON1 = 6  # 接通辅助设备开关
AUX_PWRON2 = 7  # 接通辅助设备开关
ZOOM_IN = 11  # 焦距变大(倍率变大)
ZOOM_OUT = 12  # 焦距变小(倍率变小)
FOCUS_NEAR = 13  # 焦点前调
FOCUS_FAR = 14  # 焦点后调
IRIS_OPEN = 15  # 光圈扩大
IRIS_CLOSE = 16  # 光圈缩小
TILT_UP = 21  # 云台上仰
TILT_DOWN = 22  # 云台下俯
PAN_LEFT = 23  # 云台左转
PAN_RIGHT = 24  # 云台右转
UP_LEFT = 25  # 云台上仰和左转
UP_RIGHT = 26  # 云台上仰和右转
DOWN_LEFT = 27  # 云台下俯和左转
DOWN_RIGHT = 28  # 云台下俯和右转
PAN_AUTO = 29  # 云台左右自动扫描
TILT_DOWN_ZOOM_IN = 58  # 云台下俯和焦距变大(倍率变大)
TILT_DOWN_ZOOM_OUT = 59  # 云台下俯和焦距变小(倍率变小)
PAN_LEFT_ZOOM_IN = 60  # 云台左转和焦距变大(倍率变大)
PAN_LEFT_ZOOM_OUT = 61  # 云台左转和焦距变小(倍率变小)
PAN_RIGHT_ZOOM_IN = 62  # 云台右转和焦距变大(倍率变大)
PAN_RIGHT_ZOOM_OUT = 63  # 云台右转和焦距变小(倍率变小)
UP_LEFT_ZOOM_IN = 64  # 云台上仰和左转和焦距变大(倍率变大)
UP_LEFT_ZOOM_OUT = 65  # 云台上仰和左转和焦距变小(倍率变小)
UP_RIGHT_ZOOM_IN = 66  # 云台上仰和右转和焦距变大(倍率变大)
UP_RIGHT_ZOOM_OUT = 67  # 云台上仰和右转和焦距变小(倍率变小)
DOWN_LEFT_ZOOM_IN = 68  # 云台下俯和左转和焦距变大(倍率变大)
DOWN_LEFT_ZOOM_OUT = 69  # 云台下俯和左转和焦距变小(倍率变小)
DOWN_RIGHT_ZOOM_IN = 70  # 云台下俯和右转和焦距变大(倍率变大)
DOWN_RIGHT_ZOOM_OUT = 71  # 云台下俯和右转和焦距变小(倍率变小)
TILT_UP_ZOOM_IN = 72  # 云台上仰和焦距变大(倍率变大)
TILT_UP_ZOOM_OUT = 73  # 云台上仰和焦距变小(倍率变小)

# 码流回调数据类型
NET_DVR_SYSHEAD = 1
NET_DVR_STREAMDATA = 2
NET_DVR_AUDIOSTREAMDATA = 3
NET_DVR_PRIVATE_DATA = 112

# 参数获取与配置
NET_DVR_CHECK_USER_STATUS = 20005  # 检测设备是否在线
NAME_LEN = 32  # 用户名长度
SERIALNO_LEN = 48  # 序列号长度
DEV_TYPE_NAME_LEN = 24  # 设备类型名称长度
NET_DVR_GET_DEVICECFG_V40 = 1100  # 获取扩展设备参数
NET_DVR_SET_DEVICECFG_V40 = 1101  # 设置扩展设备参数
NET_DVR_GET_TIMECFG = 118  # 获取DVR时间
NET_DVR_SET_TIMECFG = 119  # 设置DVR时间
MAX_TIMESEGMENT_V30 = 8  # 9000设备最大时间段数
MAX_SHELTERNUM = 4  # 8000设备最大遮挡区域数
MAX_DAYS = 7  # 每周天数

# 9000 IPC接入
MAX_ANALOG_CHANNUM = 32  # 最大32个模拟通道
MAX_ANALOG_ALARMOUT = 32  # 最大32路模拟报警输出
MAX_ANALOG_ALARMIN = 32  # 最大32路模拟报警输入
MAX_IP_ALARMIN_V40 = 4096  # 允许加入的最多报警输入数
MAX_IP_ALARMOUT_V40 = 4096  # 允许加入的最多报警输出数
MAX_ALARMOUT_V40 = MAX_IP_ALARMOUT_V40 + MAX_ANALOG_ALARMOUT  # 4128
MAX_ALARMIN_V40 = MAX_IP_ALARMIN_V40 + MAX_ANALOG_ALARMIN  # 4128
MAX_CHANNUM_V40 = 512
MAX_IP_DEVICE = 32  # 允许接入的最大IP设备数
MAX_IP_CHANNEL = 32  # 允许加入的最多IP通道数
MAX_IP_ALARMIN = 128  # 允许加入的最多报警输入数
MAX_IP_ALARMOUT = 64  # 允许加入的最多报警输出数

# 网络(NET_DVR_NETCFG_V30结构)
NET_DVR_GET_NETCFG_V30 = 1000  # 获取网络参数
NET_DVR_SET_NETCFG_V30 = 1001  # 设置网络参数

# 图象(NET_DVR_PICCFG_V30结构)
NET_DVR_GET_PICCFG_V30 = 1002  # 获取图象参数
NET_DVR_SET_PICCFG_V30 = 1003  # 设置图象参数
NET_DVR_GET_PICCFG_V40 = 6179  # 获取图象参数
NET_DVR_SET_PICCFG_V40 = 6180  # 设置图象参数
NET_DVR_GET_AES_KEY = 6113  # 获取设备AES加密密钥

MAX_NAMELEN = 16  # DVR本地登陆名
MAX_RIGHT = 32  # 设备支持的权限（1-12表示本地权限，13-32表示远程权限）
NAME_LEN = 32  # 用户名长度
PASSWD_LEN = 16  # 密码长度
SERIALNO_LEN = 48  # 序列号长度
MACADDR_LEN = 6  # mac地址长度
MAX_ETHERNET = 2  # 设备可配以太网络
PATHNAME_LEN = 128  # 路径长度
MAX_TIMESEGMENT_V30 = 8  # 9000设备最大时间段数
MAX_TIMESEGMENT = 4  # 8000设备最大时间段数
MAX_SHELTERNUM = 4  # 8000设备最大遮挡区域数
MAX_DAYS = 7  # 每周天数
PHONENUMBER_LEN = 32  # pppoe拨号号码最大长度
MAX_DISKNUM_V30 = 33  # 9000设备最大硬盘数
# 最多33个硬盘(包括16个内置SATA硬盘、1个eSATA硬盘和16个NFS盘)
MAX_DISKNUM = 16  # 8000设备最大硬盘数
MAX_DISKNUM_V10 = 8  # 1.2版本之前版本
MAX_WINDOW_V30 = 32  # 9000设备本地显示最大播放窗口数
MAX_WINDOW = 16  # 8000设备最大硬盘数
MAX_VGA_V30 = 4  # 9000设备最大可接VGA数
MAX_VGA = 1  # 8000设备最大可接VGA数
MAX_USERNUM_V30 = 32  # 9000设备最大用户数
MAX_USERNUM = 16  # 8000设备最大用户数
MAX_EXCEPTIONNUM_V30 = 32  # 9000设备最大异常处理数
MAX_EXCEPTIONNUM = 16  # 8000设备最大异常处理数
MAX_LINK = 6  # 8000设备单通道最大视频流连接数
MAX_DECPOOLNUM = 4  # 单路解码器每个解码通道最大可循环解码数
MAX_DECNUM = 4  # 单路解码器的最大解码通道数（实际只有一个，其他三个保留）
MAX_TRANSPARENTNUM = 2  # 单路解码器可配置最大透明通道数
MAX_CYCLE_CHAN = 16  # 单路解码器最大轮循通道数
MAX_DIRNAME_LENGTH = 80  # 最大目录长度
MAX_STRINGNUM_V30 = 8  # 9000设备最大OSD字符行数数
MAX_STRINGNUM = 4  # 8000设备最大OSD字符行数数
MAX_STRINGNUM_EX = 8  # 8000定制扩展
MAX_AUXOUT_V30 = 16  # 9000设备最大辅助输出数
MAX_AUXOUT = 4  # 8000设备最大辅助输出数
MAX_HD_GROUP = 16  # 9000设备最大硬盘组数
MAX_NFS_DISK = 8  # 8000设备最大NFS硬盘数
IW_ESSID_MAX_SIZE = 32  # WIFI的SSID号长度
IW_ENCODING_TOKEN_MAX = 32  # WIFI密锁最大字节数
MAX_SERIAL_NUM = 64  # 最多支持的透明通道路数
MAX_DDNS_NUMS = 10  # 9000设备最大可配ddns数
MAX_DOMAIN_NAME = 64  # 最大域名长度

MAX_EMAIL_ADDR_LEN = 48  # 最大email地址长度
MAX_EMAIL_PWD_LEN = 32  # 最大email密码长度
MAXPROGRESS = 100  # 回放时的最大百分率
MAX_SERIALNUM = 2  # 8000设备支持的串口数 1-232， 2-485
CARDNUM_LEN = 20  # 卡号长度
MAX_VIDEOOUT_V30 = 4  # 9000设备的视频输出数
MAX_VIDEOOUT = 2  # 8000设备的视频输出数
MAX_PRESET_V30 = 256  # 9000设备支持的云台预置点数
MAX_TRACK_V30 = 256  # 9000设备支持的云台数
MAX_CRUISE_V30 = 256  # 9000设备支持的云台巡航数
MAX_PRESET = 128  # 8000设备支持的云台预置点数
MAX_TRACK = 128  # 8000设备支持的云台数
MAX_CRUISE = 128  # 8000设备支持的云台巡航数
CRUISE_MAX_PRESET_NUMS = 32  # 一条巡航最多的巡航点
MAX_SERIAL_PORT = 8  # 9000设备支持232串口数
MAX_PREVIEW_MODE = 8  # 设备支持最大预览模式数目 1画面,4画面,9画面,16画面....
MAX_MATRIXOUT = 16  # 最大模拟矩阵输出个数
LOG_INFO_LEN = 11840  # 日志附加信息
DESC_LEN = 16  # 云台描述字符串长度
PTZ_PROTOCOL_NUM = 200  # 9000最大支持的云台协议数
MAX_AUDIO = 1  # 8000语音对讲通道数
MAX_AUDIO_V30 = 2  # 9000语音对讲通道数
MAX_CHANNUM = 16  # 8000设备最大通道数
MAX_ALARMIN = 16  # 8000设备最大报警输入数
MAX_ALARMOUT = 4  # 8000设备最大报警输出数

# 最大支持的通道数 最大模拟加上最大IP支持
MAX_CHANNUM_V30 = MAX_ANALOG_CHANNUM + MAX_IP_CHANNEL  # 64
MAX_ALARMOUT_V30 = MAX_ANALOG_ALARMOUT + MAX_IP_ALARMOUT  # 96
MAX_ALARMIN_V30 = MAX_ANALOG_ALARMIN + MAX_IP_ALARMIN  # 160
MAX_IP_DEVICE_V40 = 64
STREAM_ID_LEN = 32

# 用户(NET_DVR_USER_V30结构)
NET_DVR_GET_USERCFG_V30 = 1006  # 获取用户参数
NET_DVR_SET_USERCFG_V30 = 1007  # 设置用户参数

NET_DVR_GET_MONTHLY_RECORD_DISTRIBUTION = 6164  # 获取月历录像分布

# 对应NET_DVR_EMAILCFG结构
NET_DVR_GET_EMAILPARACFG = 250  # Get EMAIL parameters
NET_DVR_SET_EMAILPARACFG = 251  # Setup EMAIL parameters
NET_DVR_GET_DDNSCFG_EX = 274  # 获取扩展DDNS参数
NET_DVR_SET_DDNSCFG_EX = 275  # 设置扩展DDNS参数
NET_DVR_SET_PTZPOS = 292  # 云台设置PTZ位置
NET_DVR_GET_PTZPOS = 293  # 云台获取PTZ位置
NET_DVR_GET_PTZSCOPE = 294  # 云台获取PTZ范围
NET_DVR_GET_PTZLOCKCFG = 3287  # 获取云台锁定信息
NET_DVR_SET_PTZLOCKCFG = 3288  # 设置云台锁定信息

# 云台控制命令
LIGHT_PWRON = 2  # 接通灯光电源
WIPER_PWRON = 3  # 接通雨刷开关
FAN_PWRON = 4  # 接通风扇开关
HEATER_PWRON = 5  # 接通加热器开关
AUX_PWRON1 = 6  # 接通辅助设备开关
AUX_PWRON2 = 7  # 接通辅助设备开关
SET_PRESET = 8  # 设置预置点
CLE_PRESET = 9  # 清除预置点
ZOOM_IN = 11  # 焦距以速度SS变大(倍率变大)
ZOOM_OUT = 12  # 焦距以速度SS变小(倍率变小)
FOCUS_NEAR = 13  # 焦点以速度SS前调
FOCUS_FAR = 14  # 焦点以速度SS后调
IRIS_OPEN = 15  # 光圈以速度SS扩大
IRIS_CLOSE = 16  # 光圈以速度SS缩小
TILT_UP = 21  # 云台以SS的速度上仰
TILT_DOWN = 22  # 云台以SS的速度下俯
PAN_LEFT = 23  # 云台以SS的速度左转
PAN_RIGHT = 24  # 云台以SS的速度右转
UP_LEFT = 25  # 云台以SS的速度上仰和左转
UP_RIGHT = 26  # 云台以SS的速度上仰和右转
DOWN_LEFT = 27  # 云台以SS的速度下俯和左转
DOWN_RIGHT = 28  # 云台以SS的速度下俯和右转
PAN_AUTO = 29  # 云台以SS的速度左右自动扫描
FILL_PRE_SEQ = 30  # 将预置点加入巡航序列
SET_SEQ_DWELL = 31  # 设置巡航点停顿时间
SET_SEQ_SPEED = 32  # 设置巡航速度
CLE_PRE_SEQ = 33  # 将预置点从巡航序列中删除
STA_MEM_CRUISE = 34  # 开始记录
STO_MEM_CRUISE = 35  # 停止记录
RUN_CRUISE = 36  # 开始
RUN_SEQ = 37  # 开始巡航
STOP_SEQ = 38  # 停止巡航
GOTO_PRESET = 39  # 快球转到预置点
NET_DVR_GET_CCDPARAMCFG_EX = 3368  # 获取前端参数(扩展)
NET_DVR_SET_CCDPARAMCFG_EX = 3369  # 设置前端参数(扩展)
NET_DVR_GET_FOCUSMODECFG = 3305  # 获取快球聚焦模式信息
NET_DVR_SET_FOCUSMODECFG = 3306  # 设置快球聚焦模式信息
# DS9000新增命令(_V30) begin

# 网络 (NET_DVR_NETCFG_V30结构)
NET_DVR_GET_NETCFG_V30 = 1000  # 获取网络参数
NET_DVR_SET_NETCFG_V30 = 1001  # 设置网络参数

# 图像 (NET_DVR_PICCFG_V30结构)
NET_DVR_GET_PICCFG_V30 = 1002  # 获取图像参数
NET_DVR_SET_PICCFG_V30 = 1003  # 设置图像参数
NET_DVR_GET_PICCFG_V40 = 6179  # 获取图像参数
NET_DVR_SET_PICCFG_V40 = 6180  # 设置图像参数
NET_DVR_GET_AES_KEY = 6113  # 获取设备AES加密密钥

# 录像时间 (NET_DVR_RECORD_V30结构)
NET_DVR_GET_RECORDCFG_V30 = 1004  # 获取录像参数
NET_DVR_SET_RECORDCFG_V30 = 1005  # 设置录像参数

# 用户 (NET_DVR_USER_V30结构)
NET_DVR_GET_USERCFG_V30 = 1006  # 获取用户参数
NET_DVR_SET_USERCFG_V30 = 1007  # 设置用户参数

# 9000DDNS参数配置 (NET_DVR_DDNSPARA_V30结构)
NET_DVR_GET_DDNSCFG_V30 = 1010  # 获取DDNS(9000扩展)
NET_DVR_SET_DDNSCFG_V30 = 1011  # 设置DDNS(9000扩展)

# EMAIL功能 (NET_DVR_EMAILCFG_V30结构)
NET_DVR_GET_EMAILCFG_V30 = 1012  # 获取EMAIL参数
NET_DVR_SET_EMAILCFG_V30 = 1013  # 设置EMAIL参数

# 巡航参数 (NET_DVR_CRUISE_PARA结构)
NET_DVR_GET_CRUISE = 1020  # 获取巡航参数
NET_DVR_SET_CRUISE = 1021  # 设置巡航参数

# 报警输入结构参数 (NET_DVR_ALARMINCFG_V30结构)
NET_DVR_GET_ALARMINCFG_V30 = 1024  # 获取报警输入结构参数
NET_DVR_SET_ALARMINCFG_V30 = 1025  # 设置报警输入结构参数

# 报警输出结构参数 (NET_DVR_ALARMOUTCFG_V30结构)
NET_DVR_GET_ALARMOUTCFG_V30 = 1026  # 获取报警输出结构参数
NET_DVR_SET_ALARMOUTCFG_V30 = 1027  # 设置报警输出结构参数

# 视频输出结构参数 (NET_DVR_VIDEOOUT_V30结构)
NET_DVR_GET_VIDEOOUTCFG_V30 = 1028  # 获取视频输出结构参数
NET_DVR_SET_VIDEOOUTCFG_V30 = 1029  # 设置视频输出结构参数

# 叠加字符结构参数 (NET_DVR_SHOWSTRING_V30结构)
NET_DVR_GET_SHOWSTRING_V30 = 1030  # 获取叠加字符结构参数
NET_DVR_SET_SHOWSTRING_V30 = 1031  # 设置叠加字符结构参数

# 异常结构参数 (NET_DVR_EXCEPTION_V30结构)
NET_DVR_GET_EXCEPTIONCFG_V30 = 1034  # 获取异常结构参数
NET_DVR_SET_EXCEPTIONCFG_V30 = 1035  # 设置异常结构参数

# 串口232结构参数 (NET_DVR_RS232CFG_V30结构)
NET_DVR_GET_RS232CFG_V30 = 1036  # 获取串口232结构参数
NET_DVR_SET_RS232CFG_V30 = 1037  # 设置串口232结构参数

# 压缩参数 (NET_DVR_COMPRESSIONCFG_V30结构)
NET_DVR_GET_COMPRESSCFG_V30 = 1040  # 获取压缩参数
NET_DVR_SET_COMPRESSCFG_V30 = 1041  # 设置压缩参数

# 获取485解码器参数 (NET_DVR_DECODERCFG_V30结构)
NET_DVR_GET_DECODERCFG_V30 = 1042  # 获取解码器参数
NET_DVR_SET_DECODERCFG_V30 = 1043  # 设置解码器参数

# 获取预览参数 (NET_DVR_PREVIEWCFG_V30结构)
NET_DVR_GET_PREVIEWCFG_V30 = 1044  # 获取预览参数
NET_DVR_SET_PREVIEWCFG_V30 = 1045  # 设置预览参数

# 辅助预览参数 (NET_DVR_PREVIEWCFG_AUX_V30结构)
NET_DVR_GET_PREVIEWCFG_AUX_V30 = 1046  # 获取辅助预览参数
NET_DVR_SET_PREVIEWCFG_AUX_V30 = 1047  # 设置辅助预览参数

# IP接入配置参数 (NET_DVR_IPPARACFG结构)
NET_DVR_GET_IPPARACFG = 1048  # 获取IP接入配置信息
NET_DVR_SET_IPPARACFG = 1049  # 设置IP接入配置信息

# IP接入配置参数V40 (NET_DVR_IPPARACFG_V40结构)
NET_DVR_GET_IPPARACFG_V40 = 1062  # 获取IP接入配置信息
NET_DVR_SET_IPPARACFG_V40 = 1063  # 设置IP接入配置信息

# IP报警输入接入配置参数 (NET_DVR_IPALARMINCFG结构)
NET_DVR_GET_IPALARMINCFG = 1050  # 获取IP报警输入接入配置信息
NET_DVR_SET_IPALARMINCFG = 1051  # 设置IP报警输入接入配置信息

# IP报警输出接入配置参数 (NET_DVR_IPALARMOUTCFG结构)
NET_DVR_GET_IPALARMOUTCFG = 1052  # 获取IP报警输出接入配置信息
NET_DVR_SET_IPALARMOUTCFG = 1053  # 设置IP报警输出接入配置信息

# 硬盘管理的参数获取 (NET_DVR_HDCFG结构)
NET_DVR_GET_HDCFG = 1054  # 获取硬盘管理配置参数
NET_DVR_SET_HDCFG = 1055  # 设置硬盘管理配置参数

# 盘组管理的参数获取 (NET_DVR_HDGROUP_CFG结构)
NET_DVR_GET_HDGROUP_CFG = 1056  # 获取盘组管理配置参数
NET_DVR_SET_HDGROUP_CFG = 1057  # 设置盘组管理配置参数

# 设备编码类型配置 (NET_DVR_COMPRESSION_AUDIO结构)
NET_DVR_GET_COMPRESSCFG_AUD = 1058  # 获取设备语音对讲编码参数
NET_DVR_SET_COMPRESSCFG_AUD = 1059  # 设置设备语音对讲编码参数

# 慧影科技智慧医疗
NET_SDK_FINDMEDICALFILE = 3954  # 慧影科技智慧医疗查找录像文件
NET_SDK_FINDMEDICALPICTURE = 3955  # 慧影科技智慧医疗查找图片文件

# 快速运动侦测配置
NET_DVR_GET_RAPIDMOVE_DETECTION = 3539  # 获取快速运动侦测配置
NET_DVR_SET_RAPIDMOVE_DETECTION = 3540  # 设置快速运动侦测配置

# 快速运动联动配置
NET_DVR_GET_RAPIDMOVE_TRIGGER = 3543  # 获取快速运动联动配置
NET_DVR_SET_RAPIDMOVE_TRIGGER = 3544  # 设置快速运动联动配置

# 快速运动布防时间配置
NET_DVR_GET_RAPIDMOVE_SCHEDULE = 3545  # 获取快速运动的布防时间配置
NET_DVR_SET_RAPIDMOVE_SCHEDULE = 3546  # 设置快速运动的布防时间配置

# 预置点名称
NET_DVR_GET_PRESET_NAME = 3383  # 获取预置点名称
NET_DVR_SET_PRESET_NAME = 3382  # 设置预置点名称

# 异常行为检测参数 (NET_VCA_RULECFG_V42)
NET_DVR_GET_RULECFG_V42 = 5049  # 获取异常行为检测参数(支持16条规则扩展)
NET_DVR_SET_RULECFG_V42 = 5050  # 设置异常行为检测参数(支持16条规则扩展)

# 车牌识别 (NET_VCA_PLATE_CFG)
NET_DVR_SET_PLATECFG = 150  # 设置车牌识别参数
NET_DVR_GET_PLATECFG = 151  # 获取车牌识别参数

# 异常行为检测规则 (NET_VCA_RULECFG)
NET_DVR_SET_RULECFG = 152  # 设置异常行为检测规则
NET_DVR_GET_RULECFG = 153  # 获取异常行为检测规则

# 双摄像机标定参数 (NET_DVR_LF_CFG)
NET_DVR_SET_LF_CFG = 160  # 设置双摄像机的配置参数
NET_DVR_GET_LF_CFG = 161  # 获取双摄像机的配置参数

# 智能分析仪取流配置结构
NET_DVR_SET_IVMS_STREAMCFG = 162  # 设置智能分析仪取流参数

# DS9000新增命令(_V30) begin
# 网络(NET_DVR_NETCFG_V30结构)
NET_DVR_GET_NETCFG_V30 = 1000  # 获取网络参数
NET_DVR_SET_NETCFG_V30 = 1001  # 设置网络参数

# 图象(NET_DVR_PICCFG_V30结构)
NET_DVR_GET_PICCFG_V30 = 1002  # 获取图象参数
NET_DVR_SET_PICCFG_V30 = 1003  # 设置图象参数
NET_DVR_GET_PICCFG_V40 = 6179  # 获取图象参数
NET_DVR_SET_PICCFG_V40 = 6180  # 设置图象参数
NET_DVR_GET_AES_KEY = 6113  # 获取设备AES加密密钥

# 录像时间(NET_DVR_RECORD_V30结构)
NET_DVR_GET_RECORDCFG_V30 = 1004  # 获取录像参数
NET_DVR_SET_RECORDCFG_V30 = 1005  # 设置录像参数

# 用户(NET_DVR_USER_V30结构)
NET_DVR_GET_USERCFG_V30 = 1006  # 获取用户参数
NET_DVR_SET_USERCFG_V30 = 1007  # 设置用户参数

# 9000DDNS参数配置(NET_DVR_DDNSPARA_V30结构)
NET_DVR_GET_DDNSCFG_V30 = 1010  # 获取DDNS(9000扩展)
NET_DVR_SET_DDNSCFG_V30 = 1011  # 设置DDNS(9000扩展)

# EMAIL功能(NET_DVR_EMAILCFG_V30结构)
NET_DVR_GET_EMAILCFG_V30 = 1012  # 获取EMAIL参数
NET_DVR_SET_EMAILCFG_V30 = 1013  # 设置EMAIL参数

# 巡航参数 (NET_DVR_CRUISE_PARA结构)
NET_DVR_GET_CRUISE = 1020
NET_DVR_SET_CRUISE = 1021

# 报警输入结构参数 (NET_DVR_ALARMINCFG_V30结构)
NET_DVR_GET_ALARMINCFG_V30 = 1024
NET_DVR_SET_ALARMINCFG_V30 = 1025

# 报警输出结构参数 (NET_DVR_ALARMOUTCFG_V30结构)
NET_DVR_GET_ALARMOUTCFG_V30 = 1026
NET_DVR_SET_ALARMOUTCFG_V30 = 1027

# 视频输出结构参数 (NET_DVR_VIDEOOUT_V30结构)
NET_DVR_GET_VIDEOOUTCFG_V30 = 1028
NET_DVR_SET_VIDEOOUTCFG_V30 = 1029

# 叠加字符结构参数 (NET_DVR_SHOWSTRING_V30结构)
NET_DVR_GET_SHOWSTRING_V30 = 1030
NET_DVR_SET_SHOWSTRING_V30 = 1031

# 异常结构参数 (NET_DVR_EXCEPTION_V30结构)
NET_DVR_GET_EXCEPTIONCFG_V30 = 1034
NET_DVR_SET_EXCEPTIONCFG_V30 = 1035

# 串口232结构参数 (NET_DVR_RS232CFG_V30结构)
NET_DVR_GET_RS232CFG_V30 = 1036
NET_DVR_SET_RS232CFG_V30 = 1037

# 压缩参数 (NET_DVR_COMPRESSIONCFG_V30结构)
NET_DVR_GET_COMPRESSCFG_V30 = 1040
NET_DVR_SET_COMPRESSCFG_V30 = 1041

# 获取485解码器参数 (NET_DVR_DECODERCFG_V30结构)
NET_DVR_GET_DECODERCFG_V30 = 1042  # 获取解码器参数
NET_DVR_SET_DECODERCFG_V30 = 1043  # 设置解码器参数

# 获取预览参数 (NET_DVR_PREVIEWCFG_V30结构)
NET_DVR_GET_PREVIEWCFG_V30 = 1044  # 获取预览参数
NET_DVR_SET_PREVIEWCFG_V30 = 1045  # 设置预览参数

# 辅助预览参数 (NET_DVR_PREVIEWCFG_AUX_V30结构)
NET_DVR_GET_PREVIEWCFG_AUX_V30 = 1046  # 获取辅助预览参数
NET_DVR_SET_PREVIEWCFG_AUX_V30 = 1047  # 设置辅助预览参数

# IP接入配置参数 （NET_DVR_IPPARACFG结构）
NET_DVR_GET_IPPARACFG = 1048  # 获取IP接入配置信息
NET_DVR_SET_IPPARACFG = 1049  # 设置IP接入配置信息

# IP接入配置参数V40 （NET_DVR_IPPARACFG_V40结构）
NET_DVR_GET_IPPARACFG_V40 = 1062  # 获取IP接入配置信息
NET_DVR_SET_IPPARACFG_V40 = 1063  # 设置IP接入配置信息

# IP报警输入接入配置参数 （NET_DVR_IPALARMINCFG结构）
NET_DVR_GET_IPALARMINCFG = 1050  # 获取IP报警输入接入配置信息
NET_DVR_SET_IPALARMINCFG = 1051  # 设置IP报警输入接入配置信息

# IP报警输出接入配置参数 （NET_DVR_IPALARMOUTCFG结构）
NET_DVR_GET_IPALARMOUTCFG = 1052  # 获取IP报警输出接入配置信息
NET_DVR_SET_IPALARMOUTCFG = 1053  # 设置IP报警输出接入配置信息

# 硬盘管理的参数获取 (NET_DVR_HDCFG结构)
NET_DVR_GET_HDCFG = 1054  # 获取硬盘管理配置参数
NET_DVR_SET_HDCFG = 1055  # 设置硬盘管理配置参数

# 盘组管理的参数获取 (NET_DVR_HDGROUP_CFG结构)
NET_DVR_GET_HDGROUP_CFG = 1056  # 获取盘组管理配置参数
NET_DVR_SET_HDGROUP_CFG = 1057  # 设置盘组管理配置参数

# 设备编码类型配置(NET_DVR_COMPRESSION_AUDIO结构)
NET_DVR_GET_COMPRESSCFG_AUD = 1058  # 获取设备语音对讲编码参数
NET_DVR_SET_COMPRESSCFG_AUD = 1059  # 设置设备语音对讲编码参数

NET_SDK_FINDMEDICALFILE = 3954  # 慧影科技智慧医疗查找录像文件
NET_SDK_FINDMEDICALPICTURE = 3955  # 慧影科技智慧医疗查找图片文件

NET_DVR_GET_RAPIDMOVE_DETECTION = 3539  # 获取快速运动侦测配置
NET_DVR_SET_RAPIDMOVE_DETECTION = 3540  # 设置快速运动侦测配置

NET_DVR_GET_RAPIDMOVE_TRIGGER = 3543  # 获取快速运动联动配置
NET_DVR_SET_RAPIDMOVE_TRIGGER = 3544  # 设置快速运动联动配置
NET_DVR_GET_RAPIDMOVE_SCHEDULE = 3545  # 获取快速运动的布防时间配置
NET_DVR_SET_RAPIDMOVE_SCHEDULE = 3546  # 设置快速运动的布防时间配置

NET_DVR_GET_PRESET_NAME = 3383  # 获取预置点名称
NET_DVR_SET_PRESET_NAME = 3382  # 设置预置点名称
NET_DVR_GET_RULECFG_V42 = 5049  # 获取异常行为检测参数(支持16条规则扩展)
NET_DVR_SET_RULECFG_V42 = 5050  # 设置异常行为检测参数(支持16条规则扩展)

# 车牌识别（NET_VCA_PLATE_CFG）
NET_DVR_SET_PLATECFG = 150  # 设置车牌识别参数
NET_DVR_GET_PLATECFG = 151  # 获取车牌识别参数

# 行为对应（NET_VCA_RULECFG）
NET_DVR_SET_RULECFG = 152  # 设置异常行为检测规则
NET_DVR_GET_RULECFG = 153  # 获取异常行为检测规则

# 双摄像机标定参数（NET_DVR_LF_CFG）
NET_DVR_SET_LF_CFG = 160  # 设置双摄像机的配置参数
NET_DVR_GET_LF_CFG = 161  # 获取双摄像机的配置参数

# 智能分析仪取流配置结构
NET_DVR_SET_IVMS_STREAMCFG = 162  # 设置智能分析仪取流参数
NET_DVR_GET_IVMS_STREAMCFG = 163  # 获取智能分析仪取流参数

# 智能控制参数结构
NET_DVR_SET_VCA_CTRLCFG = 164  # 设置智能控制参数
NET_DVR_GET_VCA_CTRLCFG = 165  # 获取智能控制参数

# 屏蔽区域NET_VCA_MASK_REGION_LIST
NET_DVR_SET_VCA_MASK_REGION = 166  # 设置屏蔽区域参数
NET_DVR_GET_VCA_MASK_REGION = 167  # 获取屏蔽区域参数

# ATM进入区域 NET_VCA_ENTER_REGION
NET_DVR_SET_VCA_ENTER_REGION = 168  # 设置进入区域参数
NET_DVR_GET_VCA_ENTER_REGION = 169  # 获取进入区域参数

# 标定线配置NET_VCA_LINE_SEGMENT_LIST
NET_DVR_SET_VCA_LINE_SEGMENT = 170  # 设置标定线
NET_DVR_GET_VCA_LINE_SEGMENT = 171  # 获取标定线

# ivms屏蔽区域NET_IVMS_MASK_REGION_LIST
NET_DVR_SET_IVMS_MASK_REGION = 172  # 设置IVMS屏蔽区域参数
NET_DVR_GET_IVMS_MASK_REGION = 173  # 获取IVMS屏蔽区域参数

# ivms进入检测区域NET_IVMS_ENTER_REGION
NET_DVR_SET_IVMS_ENTER_REGION = 174  # 设置IVMS进入区域参数
NET_DVR_GET_IVMS_ENTER_REGION = 175  # 获取IVMS进入区域参数

NET_DVR_SET_IVMS_BEHAVIORCFG = 176  # 设置智能分析仪行为规则参数
NET_DVR_GET_IVMS_BEHAVIORCFG = 177  # 获取智能分析仪行为规则参数

NET_DVR_GET_TRAVERSE_PLANE_DETECTION = 3360  # 获取越界侦测配置
NET_DVR_SET_TRAVERSE_PLANE_DETECTION = 3361
NET_DVR_GET_FIELD_DETECTION = 3362  # 获取区域侦测配置
NET_DVR_SET_FIELD_DETECTION = 3363  # 设置区域侦测配置

NET_DVR_GET_STREAM_INFO = 6023  # 获取已添加流ID信息
NET_DVR_GET_STREAM_RECORD_STATUS = 6021  # 获取流状态信息

NET_DVR_GET_ALL_VEHICLE_CONTROL_LIST = 3124  # 获取所有车辆禁止和允许名单信息
NET_DVR_VEHICLELIST_CTRL_START = 3133  # 设置车辆禁止和允许名单信息(批量)
ENUM_SENDDATA = 0x0  # 发送数据

NET_DVR_GET_LEDDISPLAY_CFG = 3673
NET_DVR_SET_LEDDISPLAY_CFG = 3672
NET_DVR_SET_VOICEBROADCAST_CFG = 3675
NET_DVR_SET_CHARGE_ACCOUNTINFO = 3662

NET_DVR_GET_TRAFFIC_DATA = 3141  # 长连接获取交通数据
NET_DVR_GET_TRAFFIC_FLOW = 3142  # 长连接获取交通流量

NET_DVR_GET_CCDPARAMCFG_EX = 3368  # 获取前端参数(扩展)
NET_DVR_SET_CCDPARAMCFG_EX = 3369  # 设置前端参数(扩展)
NET_DVR_GET_FOCUSMODECFG = 3305  # 获取快球聚焦模式信息
NET_DVR_SET_FOCUSMODECFG = 3306  # 设置快球聚焦模式信息

NET_DVR_GET_SUPPLEMENTLIGHT = 3728  # 获取内置补光灯配置协议
NET_DVR_SET_SUPPLEMENTLIGHT = 3729  # 设置内置补光灯配置协议

NET_DVR_GET_FACECONTRAST_TRIGGER = 3965  # 获取人脸比对联动配置
NET_DVR_SET_FACECONTRAST_TRIGGER = 3966  # 设置人脸比对联动配置

NET_DVR_GET_FACECONTRAST_SCHEDULE = 3968  # 获取人脸比对布防时间配置
NET_DVR_SET_FACECONTRAST_SCHEDULE = 3969  # 设置人脸比对布防时间配置

NET_DVR_INQUEST_GET_CDW_STATUS = 6350  # 获取审讯机刻录状态-长连接

NET_DVR_GET_REALTIME_THERMOMETRY = 3629  # 实时温度检测
NET_DVR_GET_MANUALTHERM_INFO = 6706  # 手动测温实时获取
NET_DVR_GET_THERMOMETRY_MODE = 6765  # 获取测温模式参数
NET_DVR_SET_THERMOMETRY_MODE = 6766  # 设置测温模式参数
NET_DVR_GET_PTZABSOLUTEEX = 6696
NET_DVR_GET_THERMOMETRY_PRESETINFO = 3624  # 获取测温预置点关联配置参数
NET_DVR_SET_THERMOMETRY_PRESETINFO = 3625  # 设置测温预置点关联配置参数
NET_DVR_GET_THERMOMETRYRULE_TEMPERATURE_INFO = 23001  # 手动获取测温规则温度信息
NET_DVR_SET_DEVSERVER_CFG = 3258  # 设置模块服务配置

NET_DVR_GET_PHY_DISK_INFO = 6306  # 获取物理磁盘信息
NET_DVR_GET_WORK_STATUS = 6189  # 获取设备工作状态
NET_DVR_GET_MONTHLY_RECORD_DISTRIBUTION = 6164  # 获取月历录像分布

NET_DVR_GET_CURTRIGGERMODE = 3130  # 获取设备当前触发模式
NET_ITC_GET_TRIGGERCFG = 3003  # 获取触发参数
NET_ITC_SET_TRIGGERCFG = 3004  # 设置触发参数
NET_ITC_GET_VIDEO_TRIGGERCFG = 3017  # 获取视频电警触发参数
NET_ITC_SET_VIDEO_TRIGGERCFG = 3018  # 设置视频电警触发参数

NET_DVR_GET_MULTI_STREAM_COMPRESSIONCFG = 3216  # 远程获取多码流压缩参数
NET_DVR_SET_MULTI_STREAM_COMPRESSIONCFG = 3217  # 远程设置多码流压缩参数

NET_DVR_GET_CMS_CFG = 2070
NET_DVR_SET_CMS_CFG = 2071

NET_DVR_GET_ALARM_INFO = 4193  # 获取报警事件数据

NET_DVR_SET_SENSOR_CFG = 1180  # 设置模拟量参数
NET_DVR_GET_SENSOR_CFG = 1181  # 获取模拟量参数
NET_DVR_SET_ALARMIN_PARAM = 1182  # 设置报警输入参数
NET_DVR_GET_ALARMIN_PARAM = 1183  # 获取报警输入参数
NET_DVR_SET_ALARMOUT_PARAM = 1184  # 设置报警输出参数
NET_DVR_GET_ALARMOUT_PARAM = 1185  # 获取报警输出参数
NET_DVR_SET_SIREN_PARAM = 1186  # 设置警号参数
NET_DVR_GET_SIREN_PARAM = 1187  # 获取警号参数
NET_DVR_SET_ALARM_RS485CFG = 1188  # 设置报警主机485参数
NET_DVR_GET_ALARM_RS485CFG = 1189  # 获取报警主机485参数
NET_DVR_GET_ALARMHOST_MAIN_STATUS = 1190  # 获取报警主机主要状态
NET_DVR_GET_ALARMHOST_OTHER_STATUS = 1191  # 获取报警主机其他状态
NET_DVR_SET_ALARMHOST_ENABLECFG = 1192  # 设置报警主机使能状态
NET_DVR_GET_ALARMHOST_ENABLECFG = 1193  # 获取报警主机使能状态
NET_DVR_SET_ALARM_CAMCFG = 1194  # 设置视频综合平台报警触发CAM操作配置
NET_DVR_GET_ALARM_CAMCFG = 1195  # 设置视频综合平台报警触发CAM操作配置
NET_DVR_SET_ALARMHOST_RS485_SLOT_CFG = 2055  # 设置报警主机485槽位参数
NET_DVR_GET_ALARMHOST_RS485_SLOT_CFG = 2056  # 获取报警主机485槽位参数
NET_DVR_SET_VIDEOWALLDISPLAYMODE = 1730  # 设置电视墙拼接模式
NET_DVR_GET_VIDEOWALLDISPLAYMODE = 1731  # 获取电视墙拼接模式
NET_DVR_GET_VIDEOWALLDISPLAYNO = 1732  # 获取设备显示输出号
NET_DVR_SET_VIDEOWALLDISPLAYPOSITION = 1733  # 设置显示输出位置参数
NET_DVR_GET_VIDEOWALLDISPLAYPOSITION = 1734  # 获取显示输出位置参数
NET_DVR_GET_VIDEOWALLWINDOWPOSITION = 1735  # 获取电视墙窗口参数
NET_DVR_SET_VIDEOWALLWINDOWPOSITION = 1736  # 设置电视墙窗口参数
NET_DVR_VIDEOWALLWINDOW_CLOSEALL = 1737  # 电视墙关闭所有窗口
NET_DVR_SET_VIRTUALLED = 1738  # 虚拟LED设置
NET_DVR_GET_VIRTUALLED = 1739  # 虚拟LED获取
NET_DVR_GET_IMAGE_CUT_MODE = 1740  # 获取图像切割模式
NET_DVR_SET_IMAGE_CUT_MODE = 1741  # 设置图像切割模式
NET_DVR_GET_USING_SERIALPORT = 1742  # 获取当前使用串口
NET_DVR_SET_USING_SERIALPORT = 1743  # 设置当前使用串口
NET_DVR_SCENE_CONTROL = 1744  # 场景控制
NET_DVR_GET_CURRENT_SCENE = 1745  # 获取当前场景号
NET_DVR_GET_VW_SCENE_PARAM = 1746  # 获取电视墙场景模式参数
NET_DVR_SET_VW_SCENE_PARAM = 1747  # 设置电视墙场景模式参数
NET_DVR_DISPLAY_CHANNO_CONTROL = 1748  # 电视墙显示编号控制
NET_DVR_GET_WIN_DEC_INFO = 1749  # 获取窗口解码信息（批量）
NET_DVR_RESET_VIDEOWALLDISPLAYPOSITION = 1750  # 解除电视墙输出接口绑定
NET_DVR_SET_VW_AUDIO_CFG = 1752  # 设置音频切换参数
NET_DVR_GET_VW_AUDIO_CFG = 1753  # 获取音频切换参数
NET_DVR_GET_GBT28181_DECCHANINFO_CFG = 1754  # 获取GBT28181协议接入设备的解码通道信息
NET_DVR_SET_GBT28181_DECCHANINFO_CFG = 1755  # 设置GBT28181协议接入设备的解码通道信息
NET_DVR_SET_MAINBOARD_SERIAL = 1756  # 设置主控板串口参数
NET_DVR_GET_MAINBOARD_SERIAL = 1757  # 获取主控板串口参数
NET_DVR_GET_SUBBOARD_INFO = 1758  # 获取子板信息
NET_DVR_GET_SUBBOARD_EXCEPTION = 1759  # 获取异常子板异常信息


# 设备参数结构体 V30
class NET_DVR_DEVICEINFO_V30(ctypes.Structure):
    _fields_ = [
        ("sSerialNumber", c_byte * 48),  # 序列号
        ("byAlarmInPortNum", c_byte),  # 模拟报警输入个数
        ("byAlarmOutPortNum", c_byte),  # 模拟报警输出个数
        ("byDiskNum", c_byte),  # 硬盘个数
        ("byDVRType", c_byte),  # 设备类型
        ("byChanNum", c_byte),  # 设备模拟通道个数，数字（IP）通道最大个数为byIPChanNum + byHighDChanNum*256
        ("byStartChan", c_byte),  # 模拟通道的起始通道号，从1开始。数字通道的起始通道号见下面参数byStartDChan
        ("byAudioChanNum", c_byte),  # 设备语音对讲通道数
        ("byIPChanNum", c_byte),  # 设备最大数字通道个数，低8位，高8位见byHighDChanNum
        ("byZeroChanNum", c_byte),  # 零通道编码个数
        ("byMainProto", c_byte),  # 主码流传输协议类型：0- private，1- rtsp，2- 同时支持私有协议和rtsp协议取流（默认采用私有协议取流）
        ("bySubProto", c_byte),  # 子码流传输协议类型：0- private，1- rtsp，2- 同时支持私有协议和rtsp协议取流（默认采用私有协议取流）
        ("bySupport", c_byte),  # 能力，位与结果为0表示不支持，1表示支持
        # bySupport & 0x1，表示是否支持智能搜索
        # bySupport & 0x2，表示是否支持备份
        # bySupport & 0x4，表示是否支持压缩参数能力获取
        # bySupport & 0x8, 表示是否支持双网卡
        # bySupport & 0x10, 表示支持远程SADP
        # bySupport & 0x20, 表示支持Raid卡功能
        # bySupport & 0x40, 表示支持IPSAN目录查找
        # bySupport & 0x80, 表示支持rtp over rtsp
        ("bySupport1", c_byte),  # 能力集扩充，位与结果为0表示不支持，1表示支持
        # bySupport1 & 0x1, 表示是否支持snmp v30
        # bySupport1 & 0x2, 表示是否支持区分回放和下载
        # bySupport1 & 0x4, 表示是否支持布防优先级
        # bySupport1 & 0x8, 表示智能设备是否支持布防时间段扩展
        # bySupport1 & 0x10,表示是否支持多磁盘数（超过33个）
        # bySupport1 & 0x20,表示是否支持rtsp over http
        # bySupport1 & 0x80,表示是否支持车牌新报警信息，且还表示是否支持NET_DVR_IPPARACFG_V40配置
        ("bySupport2", c_byte),  # 能力集扩充，位与结果为0表示不支持，1表示支持
        # bySupport2 & 0x1, 表示解码器是否支持通过URL取流解码
        # bySupport2 & 0x2, 表示是否支持FTPV40
        # bySupport2 & 0x4, 表示是否支持ANR(断网录像)
        # bySupport2 & 0x20, 表示是否支持单独获取设备状态子项
        # bySupport2 & 0x40, 表示是否是码流加密设备
        ("wDevType", c_uint16),  # 设备型号，详见下文列表
        ("bySupport3", c_byte),  # 能力集扩展，位与结果：0- 不支持，1- 支持
        # bySupport3 & 0x1, 表示是否支持多码流
        # bySupport3 & 0x4, 表示是否支持按组配置，具体包含通道图像参数、报警输入参数、IP报警输入/输出接入参数、用户参数、设备工作状态、JPEG抓图、定时和时间抓图、硬盘盘组管理等
        # bySupport3 & 0x20, 表示是否支持通过DDNS域名解析取流
        ("byMultiStreamProto", c_byte),  # 是否支持多码流，按位表示，位与结果：0-不支持，1-支持
        # byMultiStreamProto & 0x1, 表示是否支持码流3
        # byMultiStreamProto & 0x2, 表示是否支持码流4
        # byMultiStreamProto & 0x40,表示是否支持主码流
        # byMultiStreamProto & 0x80,表示是否支持子码流
        ("byStartDChan", c_byte),  # 起始数字通道号，0表示无数字通道，比如DVR或IPC
        ("byStartDTalkChan", c_byte),  # 起始数字对讲通道号，区别于模拟对讲通道号，0表示无数字对讲通道
        ("byHighDChanNum", c_byte),  # 数字通道个数，高8位
        ("bySupport4", c_byte),  # 能力集扩展，按位表示，位与结果：0- 不支持，1- 支持
        # bySupport4 & 0x01, 表示是否所有码流类型同时支持RTSP和私有协议
        # bySupport4 & 0x10, 表示是否支持域名方式挂载网络硬盘
        ("byLanguageType", c_byte),  # 支持语种能力，按位表示，位与结果：0- 不支持，1- 支持
        # byLanguageType ==0，表示老设备，不支持该字段
        # byLanguageType & 0x1，表示是否支持中文
        # byLanguageType & 0x2，表示是否支持英文
        ("byVoiceInChanNum", c_byte),  # 音频输入通道数
        ("byStartVoiceInChanNo", c_byte),  # 音频输入起始通道号，0表示无效
        ("bySupport5", c_byte),  # 按位表示,0-不支持,1-支持,bit0-支持多码流
        ("bySupport6", c_byte),  # 按位表示,0-不支持,1-支持
        # bySupport6 & 0x1  表示设备是否支持压缩
        # bySupport6 & 0x2  表示是否支持流ID方式配置流来源扩展命令，DVR_SET_STREAM_SRC_INFO_V40
        # bySupport6 & 0x4  表示是否支持事件搜索V40接口
        # bySupport6 & 0x8  表示是否支持扩展智能侦测配置命令
        # bySupport6 & 0x40 表示图片查询结果V40扩展
        ("byMirrorChanNum", c_byte),  # 镜像通道个数，录播主机中用于表示导播通道
        ("wStartMirrorChanNo", c_uint16),  # 起始镜像通道号
        ("bySupport7", c_byte),  # 能力,按位表示,0-不支持,1-支持
        # bySupport7 & 0x1  表示设备是否支持NET_VCA_RULECFG_V42扩展
        # bySupport7 & 0x2  表示设备是否支持IPC HVT 模式扩展
        # bySupport7 & 0x04 表示设备是否支持返回锁定时间
        # bySupport7 & 0x08 表示设置云台PTZ位置时，是否支持带通道号
        # bySupport7 & 0x10 表示设备是否支持双系统升级备份
        # bySupport7 & 0x20 表示设备是否支持OSD字符叠加V50
        # bySupport7 & 0x40 表示设备是否支持主从（从摄像机）
        # bySupport7 & 0x80 表示设备是否支持报文加密
        ("byRes2", c_byte)]  # 保留，置为0


LPNET_DVR_DEVICEINFO_V30 = POINTER(NET_DVR_DEVICEINFO_V30)


# 设备参数结构体 V40
class NET_DVR_DEVICEINFO_V40(ctypes.Structure):
    _fields_ = [
        ('struDeviceV30', NET_DVR_DEVICEINFO_V30),  # 设备信息
        ('bySupportLock', c_byte),  # 设备支持锁定功能，该字段由SDK根据设备返回值来赋值的。bySupportLock为1时，dwSurplusLockTime和byRetryLoginTime有效
        ('byRetryLoginTime', c_byte),  # 剩余可尝试登陆的次数，用户名，密码错误时，此参数有效
        ('byPasswordLevel', c_byte),  # admin密码安全等级
        ('byProxyType', c_byte),  # 代理类型，0-不使用代理, 1-使用socks5代理, 2-使用EHome代理
        ('dwSurplusLockTime', c_uint32),  # 剩余时间，单位秒，用户锁定时，此参数有效
        ('byCharEncodeType', c_byte),  # 字符编码类型
        ('bySupportDev5', c_byte),  # 支持v50版本的设备参数获取，设备名称和设备类型名称长度扩展为64字节
        ('bySupport', c_byte),  # 能力集扩展，位与结果：0- 不支持，1- 支持
        ('byLoginMode', c_byte),  # 登录模式:0- Private登录，1- ISAPI登录
        ('dwOEMCode', c_uint32),  # OEM Code
        ('iResidualValidity', c_uint32),  # 该用户密码剩余有效天数，单位：天，返回负值，表示密码已经超期使用，例如“-3表示密码已经超期使用3天”
        ('byResidualValidity', c_byte),  # iResidualValidity字段是否有效，0-无效，1-有效
        ('bySingleStartDTalkChan', c_byte),  # 独立音轨接入的设备，起始接入通道号，0-为保留字节，无实际含义，音轨通道号不能从0开始
        ('bySingleDTalkChanNums', c_byte),  # 独立音轨接入的设备的通道总数，0-表示不支持
        ('byPassWordResetLevel', c_byte),  # 0-无效，
        # 1- 管理员创建一个非管理员用户为其设置密码，该非管理员用户正确登录设备后要提示“请修改初始登录密码”，未修改的情况下，用户每次登入都会进行提醒；
        # 2- 当非管理员用户的密码被管理员修改，该非管理员用户再次正确登录设备后，需要提示“请重新设置登录密码”，未修改的情况下，用户每次登入都会进行提醒。
        ('bySupportStreamEncrypt', c_byte),  # 能力集扩展，位与结果：0- 不支持，1- 支持
        # bySupportStreamEncrypt & 0x1 表示是否支持RTP/TLS取流
        # bySupportStreamEncrypt & 0x2 表示是否支持SRTP/UDP取流
        # bySupportStreamEncrypt & 0x4 表示是否支持SRTP/MULTICAST取流
        ('byMarketType', c_byte),  # 0-无效（未知类型）,1-经销型，2-行业型
        ('byRes2', c_byte * 238)  # 保留，置为0
    ]


LPNET_DVR_DEVICEINFO_V40 = POINTER(NET_DVR_DEVICEINFO_V40)

# 异步登录回调函数
fLoginResultCallBack = CFUNCTYPE(None, c_uint32, c_uint32, LPNET_DVR_DEVICEINFO_V30, c_void_p)


# NET_DVR_Login_V40()参数
class NET_DVR_USER_LOGIN_INFO(Structure):
    _fields_ = [
        ("sDeviceAddress", c_char * 129),  # 设备地址，IP 或者普通域名
        ("byUseTransport", c_byte),  # 是否启用能力集透传：0- 不启用透传，默认；1- 启用透传
        ("wPort", c_uint16),  # 设备端口号，例如：8000
        ("sUserName", c_char * 64),  # 登录用户名，例如：admin
        ("sPassword", c_char * 64),  # 登录密码，例如：12345
        ("cbLoginResult", fLoginResultCallBack),  # 登录状态回调函数，bUseAsynLogin 为1时有效
        ("pUser", c_void_p),  # 用户数据
        ("bUseAsynLogin", c_uint32),  # 是否异步登录：0- 否，1- 是
        ("byProxyType", c_byte),  # 0:不使用代理，1：使用标准代理，2：使用EHome代理
        ("byUseUTCTime", c_byte),
        # 0-不进行转换，默认,1-接口上输入输出全部使用UTC时间,SDK完成UTC时间与设备时区的转换,2-接口上输入输出全部使用平台本地时间，SDK完成平台本地时间与设备时区的转换
        ("byLoginMode", c_byte),  # 0-Private 1-ISAPI 2-自适应
        ("byHttps", c_byte),  # 0-不适用tls，1-使用tls 2-自适应
        ("iProxyID", c_uint32),  # 代理服务器序号，添加代理服务器信息时，相对应的服务器数组下表值
        ("byVerifyMode", c_byte),  # 认证方式，0-不认证，1-双向认证，2-单向认证；认证仅在使用TLS的时候生效;
        ("byRes2", c_byte * 119)]


LPNET_DVR_USER_LOGIN_INFO = POINTER(NET_DVR_USER_LOGIN_INFO)


# 组件库加载路径信息
class NET_DVR_LOCAL_SDK_PATH(Structure):
    pass


LPNET_DVR_LOCAL_SDK_PATH = POINTER(NET_DVR_LOCAL_SDK_PATH)
NET_DVR_LOCAL_SDK_PATH._fields_ = [
    ('sPath', c_char * 256),  # 组件库地址
    ('byRes', c_byte * 128),
]


# 定义预览参数结构体
class NET_DVR_PREVIEWINFO(Structure):
    pass


LPNET_DVR_PREVIEWINFO = POINTER(NET_DVR_PREVIEWINFO)
NET_DVR_PREVIEWINFO._fields_ = [
    ('lChannel', c_uint32),  # 通道号
    ('dwStreamType', c_uint32),  # 码流类型，0-主码流，1-子码流，2-码流3，3-码流4, 4-码流5,5-码流6,7-码流7,8-码流8,9-码流9,10-码流10
    ('dwLinkMode', c_uint32),  # 0：TCP方式,1：UDP方式,2：多播方式,3 - RTP方式，4-RTP/RTSP,5-RSTP/HTTP ,6- HRUDP（可靠传输） ,7-RTSP/HTTPS
    ('hPlayWnd', c_void_p),  # 播放窗口的句柄,为NULL表示不播放图象
    ('bBlocked', c_uint32),  # 0-非阻塞取流, 1-阻塞取流, 如果阻塞SDK内部connect失败将会有5s的超时才能够返回,不适合于轮询取流操作
    ('bPassbackRecord', c_uint32),  # 0-不启用录像回传,1启用录像回传
    ('byPreviewMode', c_ubyte),  # 预览模式，0-正常预览，1-延迟预览
    ('byStreamID', c_ubyte * 32),  # 流ID，lChannel为0xffffffff时启用此参数
    ('byProtoType', c_ubyte),  # 应用层取流协议，0-私有协议，1-RTSP协议,
    # 2-SRTP码流加密（对应此结构体中dwLinkMode 字段，支持如下方式, 为1，表示udp传输方式，信令走TLS加密，码流走SRTP加密，为2，表示多播传输方式，信令走TLS加密，码流走SRTP加密）
    ('byRes1', c_ubyte),
    ('byVideoCodingType', c_ubyte),  # 码流数据编解码类型 0-通用编码数据 1-热成像探测器产生的原始数据
    ('dwDisplayBufNum', c_uint32),  # 播放库播放缓冲区最大缓冲帧数，范围1-50，置0时默认为1
    ('byNPQMode', c_ubyte),  # NPQ是直连模式，还是过流媒体：0-直连 1-过流媒体
    ('byRecvMetaData', c_ubyte),  # 是否接收metadata数据
    # 设备是否支持该功能通过GET /ISAPI/System/capabilities 中DeviceCap.SysCap.isSupportMetadata是否存在且为true
    ('byDataType', c_ubyte),  # 数据类型，0-码流数据，1-音频数据
    ('byRes', c_ubyte * 213),
]


# 定义JPEG图像信息结构体
class NET_DVR_JPEGPARA(Structure):
    pass


LPNET_DVR_JPEGPARA = POINTER(NET_DVR_JPEGPARA)
NET_DVR_JPEGPARA._fields_ = [
    ('wPicSize', c_ushort),
    ('wPicQuality', c_ushort),
]


# 叠加字符
class NET_DVR_SHOWSTRINGINFO(Structure):
    pass


LPNET_DVR_SHOWSTRINGINFO = POINTER(NET_DVR_SHOWSTRINGINFO)
NET_DVR_SHOWSTRINGINFO._fields_ = [
    ('wShowString', c_ushort),
    ('wStringSize', c_ushort),
    ('wShowStringTopLeftX', c_ushort),
    ('wShowStringTopLeftY', c_ushort),
    ('sString', c_ubyte * 44),
]


# 叠加字符
class NET_DVR_SHOWSTRING_V30(Structure):
    pass


LPNET_DVR_SHOWSTRING_V30 = POINTER(NET_DVR_SHOWSTRING_V30)
NET_DVR_SHOWSTRING_V30._fields_ = [
    ('dwSize', c_uint32),
    ('struStringInfo', NET_DVR_SHOWSTRINGINFO * 8),
]


# 透传接口输出参数结构体
class NET_DVR_XML_CONFIG_OUTPUT(Structure):
    pass


LPNET_DVR_XML_CONFIG_OUTPUT = POINTER(NET_DVR_XML_CONFIG_OUTPUT)
NET_DVR_XML_CONFIG_OUTPUT._fields_ = [
    ('dwSize', c_uint32),
    ('lpOutBuffer', c_void_p),
    ('dwOutBufferSize', c_uint32),
    ('dwReturnedXMLSize', c_uint32),
    ('lpStatusBuffer', c_void_p),
    ('dwStatusSize', c_uint32),
    ('byRes', c_ubyte * 32)
]


# 透传接口输入参数结构体
class NET_DVR_XML_CONFIG_INPUT(Structure):
    pass


LPNET_DVR_XML_CONFIG_INPUT = POINTER(NET_DVR_XML_CONFIG_INPUT)
NET_DVR_XML_CONFIG_INPUT._fields_ = [
    ('dwSize', c_uint32),
    ('lpRequestUrl', c_void_p),
    ('dwRequestUrlLen', c_uint32),
    ('lpInBuffer', c_void_p),
    ('dwInBufferSize', c_uint32),
    ('dwRecvTimeOut', c_uint32),
    ('byForceEncrpt', c_ubyte),
    ('byNumOfMultiPart', c_ubyte),
    ('byRes', c_ubyte * 30)
]


# 报警设备信息结构体
class NET_DVR_ALARMER(Structure):
    _fields_ = [
        ("byUserIDValid", c_byte),  # UserID是否有效 0-无效，1-有效
        ("bySerialValid", c_byte),  # 序列号是否有效 0-无效，1-有效
        ("byVersionValid", c_byte),  # 版本号是否有效 0-无效，1-有效
        ("byDeviceNameValid", c_byte),  # 设备名字是否有效 0-无效，1-有效
        ("byMacAddrValid", c_byte),  # MAC地址是否有效 0-无效，1-有效
        ("byLinkPortValid", c_byte),  # login端口是否有效 0-无效，1-有效
        ("byDeviceIPValid", c_byte),  # 设备IP是否有效 0-无效，1-有效
        ("bySocketIPValid", c_byte),  # socket ip是否有效 0-无效，1-有效
        ("lUserID", c_uint32),  # NET_DVR_Login()返回值, 布防时有效
        ("sSerialNumber", c_byte * 48),  # 序列号
        ("dwDeviceVersion", c_uint32),  # 版本信息 高16位表示主版本，低16位表示次版本
        ("sDeviceName", c_byte * 32),  # 设备名字
        ("byMacAddr", c_byte * 6),  # MAC地址
        ("wLinkPort", c_uint16),  # link port
        ("sDeviceIP", c_byte * 128),  # IP地址
        ("sSocketIP", c_byte * 128),  # 报警主动上传时的socket IP地址
        ("byIpProtocol", c_byte),  # Ip协议 0-IPV4, 1-IPV6
        ("byRes2", c_byte * 11)]


LPNET_DVR_ALARMER = POINTER(NET_DVR_ALARMER)


# 报警布防参数结构体
class NET_DVR_SETUPALARM_PARAM(Structure):
    _fields_ = [
        ("dwSize", c_uint32),  # 结构体大小
        ("byLevel", c_byte),  # 布防优先级：0- 一等级（高），1- 二等级（中），2- 三等级（低）
        ("byAlarmInfoType", c_byte),
        # 上传报警信息类型（抓拍机支持），0-老报警信息（NET_DVR_PLATE_RESULT），1-新报警信息(NET_ITS_PLATE_RESULT)2012-9-28
        ("byRetAlarmTypeV40", c_byte),
        # 0- 返回NET_DVR_ALARMINFO_V30或NET_DVR_ALARMINFO,
        # 1- 设备支持NET_DVR_ALARMINFO_V40则返回NET_DVR_ALARMINFO_V40，不支持则返回NET_DVR_ALARMINFO_V30或NET_DVR_ALARMINFO
        ("byRetDevInfoVersion", c_byte),  # CVR上传报警信息回调结构体版本号 0-COMM_ALARM_DEVICE， 1-COMM_ALARM_DEVICE_V40
        ("byRetVQDAlarmType", c_byte),  # VQD报警上传类型，0-上传报报警NET_DVR_VQD_DIAGNOSE_INFO，1-上传报警NET_DVR_VQD_ALARM
        ("byFaceAlarmDetection", c_byte),
        ("bySupport", c_byte),
        ("byBrokenNetHttp", c_byte),
        ("wTaskNo", c_uint16),
        # 任务处理号 和 (上传数据NET_DVR_VEHICLE_RECOG_RESULT中的字段dwTaskNo对应 同时 下发任务结构 NET_DVR_VEHICLE_RECOG_COND中的字段dwTaskNo对应)
        ("byDeployType", c_byte),  # 布防类型：0-客户端布防，1-实时布防
        ("byRes1", c_byte * 3),
        ("byAlarmTypeURL", c_byte),
        # bit0-表示人脸抓拍报警上传
        # 0-表示二进制传输，1-表示URL传输（设备支持的情况下，设备支持能力根据具体报警能力集判断,同时设备需要支持URL的相关服务，当前是”云存储“）
        ("byCustomCtrl", c_byte)]  # Bit0- 表示支持副驾驶人脸子图上传: 0-不上传,1-上传


LPNET_DVR_SETUPALARM_PARAM = POINTER(NET_DVR_SETUPALARM_PARAM)


# 上传的报警信息结构体。
class NET_DVR_ALARMINFO_V30(Structure):
    _fields_ = [
        ("dwAlarmType", c_uint32),  # 报警类型
        ("dwAlarmInputNumber", c_uint32),  # 报警输入端口，当报警类型为0、23时有效
        ("byAlarmOutputNumber", c_byte * 96),
        # 触发的报警输出端口，值为1表示该报警端口输出，如byAlarmOutputNumber[0]=1表示触发第1个报警输出口输出，byAlarmOutputNumber[1]=1表示触发第2个报警输出口，依次类推
        ("byAlarmRelateChannel", c_byte * 64),  # 触发的录像通道，值为1表示该通道录像，如byAlarmRelateChannel[0]=1表示触发第1个通道录像
        ("byChannel", c_byte * 64),  # 发生报警的通道。当报警类型为2、3、6、9、10、11、13、15、16时有效，如byChannel[0]=1表示第1个通道报警
        ("byDiskNumber", c_byte * 33)]  # 发生报警的硬盘。当报警类型为1，4，5时有效，byDiskNumber[0]=1表示1号硬盘异常


LPNET_DVR_ALARMINFO_V30 = POINTER(NET_DVR_ALARMINFO_V30)


# 报警布防参数结构体
class NET_DVR_SETUPALARM_PARAM(Structure):
    _fields_ = [
        ("dwSize", c_uint32),  # 结构体大小
        ("byLevel", c_byte),  # 布防优先级：0- 一等级（高），1- 二等级（中），2- 三等级（低）
        ("byAlarmInfoType", c_byte),
        # 上传报警信息类型（抓拍机支持），0-老报警信息（NET_DVR_PLATE_RESULT），1-新报警信息(NET_ITS_PLATE_RESULT)2012-9-28
        ("byRetAlarmTypeV40", c_byte),
        # 0- 返回NET_DVR_ALARMINFO_V30或NET_DVR_ALARMINFO,
        # 1- 设备支持NET_DVR_ALARMINFO_V40则返回NET_DVR_ALARMINFO_V40，不支持则返回NET_DVR_ALARMINFO_V30或NET_DVR_ALARMINFO
        ("byRetDevInfoVersion", c_byte),  # CVR上传报警信息回调结构体版本号 0-COMM_ALARM_DEVICE， 1-COMM_ALARM_DEVICE_V40
        ("byRetVQDAlarmType", c_byte),  # VQD报警上传类型，0-上传报报警NET_DVR_VQD_DIAGNOSE_INFO，1-上传报警NET_DVR_VQD_ALARM
        ("byFaceAlarmDetection", c_byte),
        ("bySupport", c_byte),
        ("byBrokenNetHttp", c_byte),
        ("wTaskNo", c_uint16),
        # 任务处理号 和 (上传数据NET_DVR_VEHICLE_RECOG_RESULT中的字段dwTaskNo对应 同时 下发任务结构 NET_DVR_VEHICLE_RECOG_COND中的字段dwTaskNo对应)
        ("byDeployType", c_byte),  # 布防类型：0-客户端布防，1-实时布防
        ("byRes1", c_byte * 3),
        ("byAlarmTypeURL", c_byte),
        # bit0-表示人脸抓拍报警上传
        # 0- 表示二进制传输，1- 表示URL传输（设备支持的情况下，设备支持能力根据具体报警能力集判断,同时设备需要支持URL的相关服务，当前是”云存储“）
        ("byCustomCtrl", c_byte)]  # Bit0- 表示支持副驾驶人脸子图上传: 0-不上传,1-上传,(注：只在公司内部8600/8200等平台开放)


LPNET_DVR_SETUPALARM_PARAM = POINTER(NET_DVR_SETUPALARM_PARAM)


# 时间参数结构体
class NET_DVR_TIME(Structure):
    _fields_ = [
        ("dwYear", c_uint32),  # 年
        ("dwMonth", c_uint32),  # 月
        ("dwDay", c_uint32),  # 日
        ("dwHour", c_uint32),  # 时
        ("dwMinute", c_uint32),  # 分
        ("dwSecond", c_uint32)]  # 秒


LPNET_DVR_TIME = POINTER(NET_DVR_TIME)


# IP地址结构体
class NET_DVR_IPADDR(Structure):
    _fields_ = [
        ("sIpV4", c_byte * 16),  # 设备IPv4地址
        ("sIpV6", c_byte * 128)]  # 设备IPv6地址


LPNET_DVR_IPADDR = POINTER(NET_DVR_IPADDR)


# 门禁主机事件信息
class NET_DVR_ACS_EVENT_INFO(Structure):
    _fields_ = [
        ("dwSize", c_uint32),  # 结构体大小
        ("byCardNo", c_byte * 32),  # 卡号
        ("byCardType", c_byte),  # 卡类型：1- 普通卡，3- 非授权名单卡，4- 巡更卡，5- 胁迫卡，6- 超级卡，7- 来宾卡，8- 解除卡，为0表示无效
        ("byAllowListNo", c_byte),  # 授权名单单号，取值范围：1~8，0表示无效
        ("byReportChannel", c_byte),  # 报告上传通道：1- 布防上传，2- 中心组1上传，3- 中心组2上传，0表示无效
        ("byCardReaderKind", c_byte),  # 读卡器类型：0- 无效，1- IC读卡器，2- 身份证读卡器，3- 二维码读卡器，4- 指纹头
        ("dwCardReaderNo", c_uint32),  # 读卡器编号，为0表示无效
        ("dwDoorNo", c_uint32),  # 门编号（或者梯控的楼层编号），为0表示无效（当接的设备为人员通道设备时，门1为进方向，门2为出方向）
        ("dwVerifyNo", c_uint32),  # 多重卡认证序号，为0表示无效
        ("dwAlarmInNo", c_uint32),  # 报警输入号，为0表示无效
        ("dwAlarmOutNo", c_uint32),  # 报警输出号，为0表示无效
        ("dwCaseSensorNo", c_uint32),  # 事件触发器编号
        ("dwRs485No", c_uint32),  # RS485通道号，为0表示无效
        ("dwMultiCardGroupNo", c_uint32),  # 群组编号
        ("wAccessChannel", c_uint16),  # 人员通道号
        ("byDeviceNo", c_byte),  # 设备编号，为0表示无效
        ("byDistractControlNo", c_byte),  # 分控器编号，为0表示无效
        ("dwEmployeeNo", c_uint32),  # 工号，为0无效
        ("wLocalControllerID", c_uint16),  # 就地控制器编号，0-门禁主机，1-255代表就地控制器
        ("byInternetAccess", c_byte),  # 网口ID：（1-上行网口1,2-上行网口2,3-下行网口1）
        ("byType", c_byte),
        # 防区类型，0:即时防区,1-24小时防区,2-延时防区,3-内部防区,4-钥匙防区,5-火警防区,6-周界防区,7-24小时无声防区,
        # 8-24小时辅助防区,9-24小时震动防区,10-门禁紧急开门防区,11-门禁紧急关门防区，0xff-无
        ("byMACAddr", c_byte * 6),  # 物理地址，为0无效
        ("bySwipeCardType", c_byte),  # 刷卡类型，0-无效，1-二维码
        ("byMask", c_byte),  # 是否带口罩：0-保留，1-未知，2-不戴口罩，3-戴口罩
        ("dwSerialNo", c_uint32),  # 事件流水号，为0无效
        ("byChannelControllerID", c_byte),  # 通道控制器ID，为0无效，1-主通道控制器，2-从通道控制器
        ("byChannelControllerLampID", c_byte),  # 通道控制器灯板ID，为0无效（有效范围1-255）
        ("byChannelControllerIRAdaptorID", c_byte),  # 通道控制器红外转接板ID，为0无效（有效范围1-255）
        ("byChannelControllerIREmitterID", c_byte),  # 通道控制器红外对射ID，为0无效（有效范围1-255）
        ("byHelmet", c_byte),  # 可选，是否戴安全帽：0-保留，1-未知，2-不戴安全, 3-戴安全帽
        ("byRes", c_byte * 3)]  # 保留，置为0


LPNET_DVR_ACS_EVENT_INFO = POINTER(NET_DVR_ACS_EVENT_INFO)


# 门禁主机报警信息结构体
class NET_DVR_ACS_ALARM_INFO(Structure):
    _fields_ = [
        ("dwSize", c_uint32),  # 结构体大小
        ("dwMajor", c_uint32),  # 报警主类型，具体定义见“Remarks”说明
        ("dwMinor", c_uint32),  # 报警次类型，次类型含义根据主类型不同而不同，具体定义见“Remarks”说明
        ("struTime", NET_DVR_TIME),  # 报警时间
        ("sNetUser", c_byte * 16),  # 网络操作的用户名
        ("struRemoteHostAddr", NET_DVR_IPADDR),  # 远程主机地址
        ("struAcsEventInfo", NET_DVR_ACS_EVENT_INFO),  # 报警信息详细参数
        ("dwPicDataLen", c_uint32),  # 图片数据大小，不为0是表示后面带数据
        ("pPicData", c_void_p),  # 图片数据缓冲区
        ("wInductiveEventType", c_uint16),  # 归纳事件类型，0-无效，客户端判断该值为非0值后，报警类型通过归纳事件类型区分，否则通过原有报警主次类型（dwMajor、dwMinor）区分
        ("byPicTransType", c_byte),  # 图片数据传输方式: 0-二进制；1-url
        ("byRes1", c_byte),  # 保留，置为0
        ("dwIOTChannelNo", c_uint32),  # IOT通道号
        ("pAcsEventInfoExtend", c_void_p),  # byAcsEventInfoExtend为1时，表示指向一个NET_DVR_ACS_EVENT_INFO_EXTEND结构体
        ("byAcsEventInfoExtend", c_byte),  # pAcsEventInfoExtend是否有效：0-无效，1-有效
        ("byTimeType", c_byte),  # 时间类型：0-设备本地时间，1-UTC时间（struTime的时间）
        ("byRes2", c_byte),  # 保留，置为0
        ("byAcsEventInfoExtendV20", c_byte),  # pAcsEventInfoExtendV20是否有效：0-无效，1-有效
        ("pAcsEventInfoExtendV20", c_void_p),  # byAcsEventInfoExtendV20为1时，表示指向一个NET_DVR_ACS_EVENT_INFO_EXTEND_V20结构体
        ("byRes", c_byte * 4)]  # 保留，置为0


LPNET_DVR_ACS_ALARM_INFO = POINTER(NET_DVR_ACS_ALARM_INFO)


# 点坐标参数结构体
class NET_VCA_POINT(Structure):
    _fields_ = [
        ("fX", c_float),
        ("fY", c_float)
    ]


# 身份证刷卡信息扩展参数
class NET_DVR_ID_CARD_INFO_EXTEND(Structure):
    _fields_ = [
        ("byRemoteCheck", c_ubyte),
        ("byThermometryUnit", c_ubyte),
        ("byIsAbnomalTemperature", c_ubyte),
        ("byRes2", c_ubyte),
        ("fCurrTemperature", c_float),
        ("struRegionCoordinates", NET_VCA_POINT),
        ("dwQRCodeInfoLen", c_uint32),
        ("dwVisibleLightDataLen", c_uint32),
        ("dwThermalDataLen", c_uint32),
        ("pQRCodeInfo", POINTER(c_byte)),
        ("pVisibleLightData", POINTER(c_byte)),
        ("pThermalData", POINTER(c_byte)),
        ("byRes", c_ubyte * 1024)
    ]


# 日期信息结构体
class NET_DVR_DATE(Structure):
    _fields_ = [
        ('wYear', c_ushort),
        ('byMonth', c_ubyte),
        ('byDay', c_ubyte)
    ]


# 身份证信息结构体
class NET_DVR_ID_CARD_INFO(Structure):
    _fields_ = [
        ("dwSize", c_uint),
        ("byName", c_ubyte * 128),
        ("struBirth", NET_DVR_DATE),
        ("byAddr", c_ubyte * 280),
        ("byIDNum", c_ubyte * 32),
        ("byIssuingAuthority", c_ubyte * 128),
        ("struStartDate", NET_DVR_DATE),
        ("struEndDate", NET_DVR_DATE),
        ("byTermOfValidity", c_ubyte),
        ("bySex", c_ubyte),
        ("byNation", c_ubyte),
        ("byRes", c_ubyte * 101)
    ]


# 时间参数结构体
class NET_DVR_TIME(Structure):
    _fields_ = [
        ("dwYear", c_uint32),
        ("dwMonth", c_uint32),
        ("dwDay", c_uint32),
        ("dwHour", c_uint32),
        ("dwMinute", c_uint32),
        ("dwSecond", c_uint32)
    ]


# 时间参数结构体
class NET_DVR_TIME_V30(Structure):
    _fields_ = [
        ('wYear', c_ushort),
        ('byMonth', c_ubyte),
        ('byDay', c_ubyte),
        ('byHour', c_ubyte),
        ('byMinute', c_ubyte),
        ('bySecond', c_ubyte),
        ('byISO8601', c_ubyte),
        ('wMilliSec', c_ushort),
        ('cTimeDifferenceH', c_ubyte),
        ('cTimeDifferenceM', c_ubyte),
    ]


# IP地址结构体
class NET_DVR_IPADDR(Structure):
    _fields_ = [
        ("sIpV4", c_ubyte * 16),
        ("byIPv6", c_ubyte * 128)]


# 身份证刷卡信息上传结构体
class NET_DVR_ID_CARD_INFO_ALARM(Structure):
    _fields_ = [
        ("dwSize", c_uint32),  # 结构长度
        ("struIDCardCfg", NET_DVR_ID_CARD_INFO),  # 身份证信息
        ("dwMajor", c_uint32),  # 报警主类型，参考宏定义
        ("dwMinor", c_uint32),  # 报警次类型，参考宏定义
        ("struSwipeTime", NET_DVR_TIME_V30),  # 刷卡时间
        ("byNetUser", c_ubyte * 16),  # 网络操作的用户名
        ("struRemoteHostAddr", NET_DVR_IPADDR),  # 远程主机地址
        ("dwCardReaderNo", c_uint32),  # 读卡器编号，为0无效
        ("dwDoorNo", c_uint32),  # 门编号，为0无效
        ("dwPicDataLen", c_uint32),  # 图片数据大小，不为0是表示后面带数据
        ("pPicData", c_void_p),  # 身份证图片数据缓冲区，dwPicDataLen不为0时缓冲区里面存放身份证头像的图片数据
        ("byCardType", c_ubyte),  # 卡类型，1-普通卡，3-非授权名单卡，4-巡更卡，5-胁迫卡，6-超级卡，7-来宾卡，8-解除卡，为0无效
        ("byDeviceNo", c_ubyte),  # 设备编号，为0时无效（有效范围1-255）
        ("byMask", c_ubyte),  # 是否带口罩：0-保留，1-未知，2-不戴口罩，3-戴口罩
        ("byRes2", c_ubyte),  # 保留，置为0
        ("dwFingerPrintDataLen", c_uint32),  # 指纹数据大小，不为0是表示后面带数据
        ("pFingerPrintData", c_void_p),  # 指纹数据缓冲区，dwFingerPrintDataLen不为0时缓冲区里面存放指纹数据
        ("dwCapturePicDataLen", c_uint32),  # 抓拍图片数据大小，不为0是表示后面带数据
        ("pCapturePicData", c_void_p),  # 抓拍图片数据缓冲区，dwCapturePicDataLen不为0时缓冲区里面存放设备上摄像机抓拍上传的图片数据
        ("dwCertificatePicDataLen", c_uint32),  # 证件抓拍图片数据大小，不为0是表示后面带数据
        ("pCertificatePicData", c_void_p),  # 证件抓拍图片数据缓冲区，dwCertificatePicDataLen不为0时缓冲区里面存放设备上摄像机抓拍上传的证件抓拍图片数据
        ("byCardReaderKind", c_ubyte),  # 读卡器属于哪一类：0-无效，1-IC读卡器，2-身份证读卡器，3-二维码读卡器，4-指纹头
        ("byRes3", c_ubyte * 2),  # 保留，置为0
        ("byIDCardInfoExtend", c_ubyte),  # pIDCardInfoExtend是否有效：0-无效，1-有效
        ("pIDCardInfoExtend", POINTER(NET_DVR_ID_CARD_INFO_EXTEND)),  # 身份证刷卡扩展事件信息
        ("byRes", c_ubyte * 172)  # 身份证刷卡扩展事件信息
    ]


LPNET_DVR_ID_CARD_INFO_ALARM = POINTER(NET_DVR_ID_CARD_INFO_ALARM)


class NET_DVR_ALARM_ISAPI_PICDATA(Structure):
    _fields_ = [
        ("dwPicLen", c_uint32),  # 图片数据长度
        ("byPicType", c_ubyte),  # 图片格式: 1- jpg
        ("byRes", c_ubyte * 3),  #
        ("szFilename", c_ubyte * 256),  # 图片名称
        ("pPicData", c_void_p),  # 图片数据
    ]


LPNET_DVR_ALARM_ISAPI_PICDATA = POINTER(NET_DVR_ALARM_ISAPI_PICDATA)


class NET_DVR_ALARM_ISAPI_INFO(Structure):
    _fields_ = [
        ("pAlarmData", c_void_p),  # 报警数据
        ("dwAlarmDataLen", c_uint32),  # 报警数据长度
        ("byDataType", c_ubyte),  # 0-invalid,1-xml,2-json
        ("byPicturesNumber", c_ubyte),  # 图片数量
        ("byRes[2]", c_ubyte * 2),  # 保留字节
        ("pPicPackData", c_void_p),  # 图片变长部分
        ("byRes1[32]", c_ubyte * 32),  # 保留字节
    ]


LPNET_DVR_ALARM_ISAPI_INFO = POINTER(NET_DVR_ALARM_ISAPI_INFO)


class NET_DVR_LOCAL_GENERAL_CFG(Structure):
    _fields_ = [
        ("byExceptionCbDirectly", c_ubyte),  # 0-通过线程池异常回调，1-直接异常回调给上层
        ("byNotSplitRecordFile", c_ubyte),  # 回放和预览中保存到本地录像文件不切片 0-默认切片，1-不切片
        ("byResumeUpgradeEnable", c_ubyte),  # 断网续传升级使能，0-关闭（默认），1-开启
        ("byAlarmJsonPictureSeparate", c_ubyte),  # 控制JSON透传报警数据和图片是否分离，0-不分离，1-分离（分离后走COMM_ISAPI_ALARM回调返回）
        ("byRes", c_ubyte * 4),  # 保留
        ("i64FileSize", c_uint64),  # 单位：Byte
        ("dwResumeUpgradeTimeout", c_uint32),  # 断网续传重连超时时间，单位毫秒
        ("byAlarmReconnectMode", c_ubyte),  # 0-独立线程重连（默认） 1-线程池重连
        ("byStdXmlBufferSize", c_ubyte),  # 设置ISAPI透传接收缓冲区大小，1-1M 其他-默认
        ("byMultiplexing", c_ubyte),  # 0-普通链接（非TLS链接）关闭多路复用，1-普通链接（非TLS链接）开启多路复用
        ("byFastUpgrade", c_ubyte),  # 0-正常升级，1-快速升级
        ("byRes1", c_ubyte * 232),  # 预留
    ]


class NET_DVR_LOCAL_TCP_PORT_BIND_CFG(Structure):
    _fields_ = [
        ("wLocalBindTcpMinPort", c_ushort),
        ("wLocalBindTcpMaxPort", c_ushort),
        ("byRes", c_byte * 60),
    ]


class NET_DVR_DEVICECFG_V40(Structure):
    _fields_ = [("dwSize", c_int),
                ("sDVRName", c_byte * NAME_LEN),
                ("dwDVRID", c_int),
                ("dwRecycleRecord", c_int),
                ("sSerialNumber", c_byte * SERIALNO_LEN),
                ("dwSoftwareVersion", c_int),
                ("dwSoftwareBuildDate", c_int),
                ("dwDSPSoftwareVersion", c_int),
                ("dwDSPSoftwareBuildDate", c_int),
                ("dwPanelVersion", c_int),
                ("dwHardwareVersion", c_int),
                ("byAlarmInPortNum", c_byte),
                ("byAlarmOutPortNum", c_byte),
                ("byRS232Num", c_byte),
                ("byRS485Num", c_byte),
                ("byNetworkPortNum", c_byte),
                ("byDiskCtrlNum", c_byte),
                ("byDiskNum", c_byte),
                ("byDVRType", c_byte),
                ("byChanNum", c_byte),
                ("byStartChan", c_byte),
                ("byDecordChans", c_byte),
                ("byVGANum", c_byte),
                ("byUSBNum", c_byte),
                ("byAuxoutNum", c_byte),
                ("byAudioNum", c_byte),
                ("byIPChanNum", c_byte),
                ("byZeroChanNum", c_byte),
                ("bySupport", c_byte),
                ("byEsataUseage", c_byte),
                ("byIPCPlug", c_byte),
                ("byStorageMode", c_byte),
                ("bySupport1", c_byte),
                ("wDevType", c_ushort),
                ("byDevTypeName", c_byte * DEV_TYPE_NAME_LEN),
                ("bySupport2", c_byte),
                ("byAnalogAlarmInPortNum", c_byte),
                ("byStartAlarmInNo", c_byte),
                ("byStartAlarmOutNo", c_byte),
                ("byStartIPAlarmInNo", c_byte),
                ("byStartIPAlarmOutNo", c_byte),
                ("byHighIPChanNum", c_byte),
                ("byEnableRemotePowerOn", c_byte),
                ("wDevClass", c_short),
                ("byRes2", c_byte * 6),
                ]


LPNET_DVR_LOCAL_GENERAL_CFG = POINTER(NET_DVR_LOCAL_GENERAL_CFG)


class NET_DVR_COLOR(Structure):
    _fields_ = [
        ("byBrightness", c_byte),  # 亮度,0-255
        ("byContrast", c_byte),  # 对比度,0-255
        ("bySaturation", c_byte),  # 饱和度,0-255
        ("byHue", c_byte),  # 色调,0-255
    ]


class NET_DVR_SCHEDTIME(Structure):
    _fields_ = [
        ("byStartHour", c_byte),  # 开始时间
        ("byStartMin", c_byte),
        ("byStopHour", c_byte),  # 结束时间
        ("byStopMin", c_byte),
    ]


class NET_DVR_VICOLOR(Structure):
    _fields_ = [
        ("struColor", NET_DVR_COLOR * MAX_TIMESEGMENT_V30),  # 图像参数(第一个有效，其他三个保留)
        ("struHandleTime", NET_DVR_SCHEDTIME * MAX_TIMESEGMENT_V30)  # 处理时间段(保留)
    ]


class NET_DVR_SHELTER(Structure):
    _fields_ = [
        ("wHideAreaTopLeftX", c_uint16),  # 遮挡区域的x坐标
        ("wHideAreaTopLeftY", c_uint16),  # 遮挡区域的y坐标
        ("wHideAreaWidth", c_uint16),  # 遮挡区域的宽
        ("wHideAreaHeight", c_uint16),  # 遮挡区域的高
    ]


class NET_DVR_SCHEDTIMEWEEK(Structure):
    _fields_ = [
        ("struAlarmTime", NET_DVR_SCHEDTIME * 8),
    ]


class NET_DVR_VILOST_V40(Structure):
    _fields_ = [
        ("dwEnableVILostAlarm", c_int32),  # 是否启动信号丢失报警,0-否,1-是
        ("dwHandleType", c_int32),  # 异常处理，异常处理方式的"或"结果
        # 0x00 无响应
        # 0x01 布防器上警告
        # 0x02 声音警告
        # 0x04 上传中心
        # 0x08 触发报警输出
        # 0x10 触发JPRG抓图并上传Email
        # 0x20 无线声光报警器联动
        # 0x40 联动电子地图(目前只有PCNVR支持)
        # 0x200 抓图并上传FTP
        # 0x1000 抓图上传到云
        ("dwMaxRelAlarmOutChanNum", c_int32),  # 触发的报警输出通道数(只读)最大支持数量
        ("dwRelAlarmOut", c_int32 * MAX_ALARMOUT_V40),
        ("struAlarmTime", NET_DVR_SCHEDTIMEWEEK * MAX_DAYS),
        ("byVILostAlarmThreshold", c_byte),
        ("byRes", c_byte * 63)
    ]


class NET_DVR_MOTION_SINGLE_AREA(Structure):
    _fields_ = [
        ("byMotionScope", c_byte * (64 * 96)),  # 侦测区域，0-96位，表示64行，共有96*64个小宏块，目前有效的是22*18，为1表示是移动侦测区域，0-表示不是
        ("byMotionSensitive", c_byte),  # 移动侦测灵敏度，0 - 5，越高越灵敏，0xff关闭
        ("byRes", c_byte * 3)  # 保留字段
    ]


class NET_DVR_DAYTIME(Structure):
    _fields_ = [
        ("byHour", c_byte),  # 0~24
        ("byMinute", c_byte),  # 0~60
        ("bySecond", c_byte),  # 0~60
        ("byRes", c_byte),
        ("wMilliSecond", c_uint16),  # 0~1000
        ("byRes1", c_byte * 2)
    ]


class NET_DVR_SCHEDULE_DAYTIME(Structure):
    _fields_ = [
        ("struStartTime", NET_DVR_DAYTIME),  # 开始时间
        ("struStopTime", NET_DVR_DAYTIME)  # 结束时间
    ]


class NET_VCA_RECT(Structure):
    _fields_ = [
        ("fX", c_float),
        ("fY", c_float),
        ("fWidth", c_float),
        ("fHeight", c_float)
    ]


class NET_DVR_DNMODE(Structure):
    _fields_ = [
        ("byObjectSize", c_byte),  # 占比参数(0~100)
        ("byMotionSensitive", c_byte),  # 移动侦测灵敏度, 0 - 5,越高越灵敏,0xff关闭
        ("byRes", c_byte * 6)
    ]


class NET_DVR_MOTION_MULTI_AREAPARAM(Structure):
    _fields_ = [
        ("byAreaNo", c_byte),  # 区域编号(IPC- 1~8)
        ("byRes", c_byte * 3),  # 保留字段
        ("struRect", NET_VCA_RECT),  # 单个区域的坐标信息(矩形)
        ("struDayNightDisable", NET_DVR_DNMODE),  # 关闭模式
        ("struDayModeParam", NET_DVR_DNMODE),  # 白天模式
        ("struNightModeParam", NET_DVR_DNMODE),  # 夜晚模式
        ("byRes1", c_byte * 8)
    ]


MAX_MULTI_AREA_NUM = 24


class NET_DVR_MOTION_MULTI_AREA(Structure):
    _fields_ = [
        ("byDayNightCtrl", c_byte),  # 日夜控制 0~关闭,1~自动切换,2~定时切换(默认关闭)
        ("byAllMotionSensitive", c_byte),  # 移动侦测灵敏度, 0 - 5,越高越灵敏,0xff关闭，全部区域的灵敏度范围
        ("byRes", c_byte * 2),  # 保留字段
        ("struScheduleTime", NET_DVR_SCHEDULE_DAYTIME),  # 切换时间
        ("struMotionMultiAreaParam", NET_DVR_MOTION_MULTI_AREAPARAM * MAX_MULTI_AREA_NUM),  # 最大支持24个区域
        ("byRes1", c_byte * 60)
    ]


class NET_DVR_MOTION_MODE_PARAM(Structure):
    _fields_ = [
        ("struMotionSingleArea", NET_DVR_MOTION_SINGLE_AREA),
        ("struMotionMultiArea", NET_DVR_MOTION_MULTI_AREA),
    ]


class NET_DVR_MOTION_V40(Structure):
    _fields_ = [
        ("struMotionMode", NET_DVR_MOTION_MODE_PARAM),  # (5.1.0新增)
        ("byEnableHandleMotion", c_byte),  # 是否处理移动侦测 0－否 1－是
        ("byEnableDisplay", c_byte),  # 启用移动侦测高亮显示，0-否，1-是
        ("byConfigurationMode", c_byte),  # 0~普通,1~专家(5.1.0新增)
        ("byKeyingEnable", c_byte),  # 启用键控移动侦测 0-不启用，1-启用
        ("dwHandleType", c_uint32),  # 异常处理方式
        ("dwMaxRelAlarmOutChanNum", c_uint32),  # 触发的报警输出通道数（只读）最大支持数量
        ("dwRelAlarmOut", c_uint32 * MAX_ALARMOUT_V40),  # 实际触发的报警输出号
        ("struAlarmTime", NET_DVR_SCHEDTIMEWEEK * MAX_DAYS),  # 布防时间
        ("dwMaxRecordChanNum", c_uint32),  # 设备支持的最大关联录像通道数-只读
        ("dwRelRecordChan", c_uint32 * MAX_CHANNUM_V40),  # 实际触发录像通道
        ("byDiscardFalseAlarm", c_byte),  # 启用去误报 0-无效，1-不启用，2-启用
        ("byRes", c_byte * 127)  # 保留字节
    ]


class NET_DVR_HIDEALARM_V40(Structure):
    _fields_ = [
        ("dwEnableHideAlarm", c_int32),  # 是否启动遮挡报警，0-否，1-低灵敏度，2-中灵敏度，3-高灵敏度
        ("wHideAlarmAreaTopLeftX", c_int16),  # 遮挡区域的x坐标
        ("wHideAlarmAreaTopLeftY", c_int16),  # 遮挡区域的y坐标
        ("wHideAlarmAreaWidth", c_int16),  # 遮挡区域的宽
        ("wHideAlarmAreaHeight", c_int16),  # 遮挡区域的高
        ("dwHandleType", c_int32),  # 异常处理方式的"或"结果
        ("dwMaxRelAlarmOutChanNum", c_int32),  # 触发的报警输出通道数（只读）最大支持数量
        ("dwRelAlarmOut", c_int32 * MAX_ALARMOUT_V40),
        # 触发报警输出号，按值表示,采用紧凑型排列，从下标0 - dwRelAlarmOut -1有效，如果中间遇到0xffffffff,则后续无效
        ("struAlarmTime", NET_DVR_SCHEDTIMEWEEK * MAX_DAYS),  # 布防时间
        ("byRes", c_byte * 64)  # 保留
    ]


class NET_DVR_RGB_COLOR(Structure):
    _fields_ = [
        ("byRed", c_byte),  # RGB颜色三分量中的红色
        ("byGreen", c_byte),  # RGB颜色三分量中的绿色
        ("byBlue", c_byte),  # RGB颜色三分量中的蓝色
        ("byRes", c_byte)  # 保留
    ]


class NET_DVR_PICCFG_V40(Structure):
    _fields_ = [
        ("dwSize", c_uint32),  # 结构体大小
        ("sChanName", c_byte * NAME_LEN),  # 通道名称
        ("dwVideoFormat", c_uint32),  # 视频制式
        ("struViColor", NET_DVR_VICOLOR),  # 图像参数
        ("dwShowChanName", c_uint32),  # 是否显示通道名称
        ("wShowNameTopLeftX", c_uint16),  # 通道名称显示位置的x坐标
        ("wShowNameTopLeftY", c_uint16),  # 通道名称显示位置的y坐标
        ("dwEnableHide", c_uint32),  # 是否启用隐私遮挡
        ("struShelter", NET_DVR_SHELTER * MAX_SHELTERNUM),  # 遮挡区域
        ("dwShowOsd", c_uint32),  # 是否显示OSD
        ("wOSDTopLeftX", c_uint16),  # OSD的x坐标
        ("wOSDTopLeftY", c_uint16),  # OSD的y坐标
        ("byOSDType", c_byte),  # OSD类型
        ("byDispWeek", c_byte),  # 是否显示星期
        ("byOSDAttrib", c_byte),  # OSD属性
        ("byHourOSDType", c_byte),  # OSD小时制
        ("byFontSize", c_byte),  # OSD字体大小
        ("byOSDColorType", c_byte),  # OSD颜色类型
        ("byAlignment", c_byte),  # OSD对齐方式
        ("byOSDMilliSecondEnable", c_byte),  # 视频叠加时间支持毫秒
        ("struVILost", NET_DVR_VILOST_V40),  # 视频信号丢失报警
        ("struAULost", NET_DVR_VILOST_V40),  # 音频信号丢失报警（支持组）
        ("struMotion", NET_DVR_MOTION_V40),  # 移动侦测报警（支持组）
        ("struHideAlarm", NET_DVR_HIDEALARM_V40),  # 遮挡报警（支持组）
        ("struOsdColor", NET_DVR_RGB_COLOR),  # OSD颜色
        ("dwBoundary", c_uint32),  # 边界值，左对齐，右对齐以及国标模式的边界值，0-表示默认值，单位：像素;在国标模式下，单位修改为字符个数（范围是，0,1,2）
        ("struOsdBkColor", NET_DVR_RGB_COLOR),  # 自定义OSD背景色
        ("byOSDBkColorMode", c_byte),  # OSD背景色模式，0-默认，1-自定义OSD背景色
        ("byUpDownBoundary", c_byte),
        # 上下最小边界值选项，单位为字符个数（范围是，0,1,2）,国标模式下无效。byAlignment=3该字段无效，通过dwBoundary进行边界配置，.byAlignment不等于3的情况下， byUpDownBoundary/byLeftRightBoundary配置成功后，dwBoundary值将不生效
        ("byLeftRightBoundary", c_byte),
        # 左右最小边界值选项，单位为字符个数（范围是，0,1,2）, 国标模式下无效。byAlignment=3该字段无效，通过dwBoundary进行边界配置，.byAlignment不等于3的情况下， byUpDownBoundary/byLeftRightBoundary配置成功后，dwBoundary值将不生效
        ("byAngleEnabled", c_byte),  # OSD是否叠加俯仰角信息.0-不叠加,1-叠加
        ("wTiltAngleTopLeftX", c_uint16),  # 俯仰角信息显示位置的x坐标
        ("wTiltAngleTopLeftY", c_uint16),  # 俯仰角信息显示位置的y坐标
        ("byRes", c_byte * 108)
    ]


class NET_DVR_USER_INFO_V30(Structure):
    _fields_ = [
        # 用户名
        ("sUserName", c_byte * NAME_LEN),
        # 密码
        ("sPassword", c_byte * PASSWD_LEN),
        # 本地权限
        ("byLocalRight", c_byte * MAX_RIGHT),
        # 远程权限
        ("byRemoteRight", c_byte * MAX_RIGHT),
        # 远程可以预览的通道 0-有权限，1-无权限
        ("byNetPreviewRight", c_byte * MAX_CHANNUM_V30),
        # 本地可以回放的通道 0-有权限，1-无权限
        ("byLocalPlaybackRight", c_byte * MAX_CHANNUM_V30),
        # 远程可以回放的通道 0-有权限，1-无权限
        ("byNetPlaybackRight", c_byte * MAX_CHANNUM_V30),
        # 本地可以录像的通道 0-有权限，1-无权限
        ("byLocalRecordRight", c_byte * MAX_CHANNUM_V30),
        # 远程可以录像的通道 0-有权限，1-无权限
        ("byNetRecordRight", c_byte * MAX_CHANNUM_V30),
        # 本地可以PTZ的通道 0-有权限，1-无权限
        ("byLocalPTZRight", c_byte * MAX_CHANNUM_V30),
        # 远程可以PTZ的通道 0-有权限，1-无权限
        ("byNetPTZRight", c_byte * MAX_CHANNUM_V30),
        # 本地备份权限通道 0-有权限，1-无权限
        ("byLocalBackupRight", c_byte * MAX_CHANNUM_V30),
        # 用户IP地址(为0时表示允许任何地址)
        ("struUserIP", NET_DVR_IPADDR),
        # 物理地址
        ("byMACAddr", c_byte * MACADDR_LEN),
        # 优先级，0xff-无，0--低，1--中，2--高
        ("byPriority", c_byte),
        # 保留
        ("byRes", ctypes.c_byte * 17)
    ]


class NET_DVR_USER_V30(Structure):
    _fields_ = [
        ("dwSize", c_uint32),
        ("struUser", NET_DVR_USER_INFO_V30 * MAX_USERNUM_V30)
    ]


class NET_DVR_FLOW_TEST_PARAM(Structure):
    _fields_ = [
        ("dwSize", c_uint32),  # 结构大小
        ("lCardIndex", c_uint32),  # 网卡索引
        ("dwInterval", c_uint32),  # 设备上传流量时间间隔, 单位:100ms
        ("byRes", c_byte * 8)  # 保留字节
    ]


class NET_DVR_FLOW_INFO(ctypes.Structure):
    _fields_ = [
        ("dwSize", c_uint32),  # 结构大小
        ("dwSendFlowSize", c_uint32),  # 发送流量大小, 单位kbps
        ("dwRecvFlowSize", c_uint32),  # 接收流量大小, 单位kbps
        ("byRes", c_byte * 20)  # 保留
    ]


class NET_DVR_RECORD_TIME_SPAN_INQUIRY(Structure):
    _fields_ = [
        ("dwSize", c_uint32),  # 结构体大小
        ("byType", c_byte),  # 0 正常音视频录像, 1图片通道录像, 2ANR通道录像, 3抽帧通道录像
        ("byRes", c_byte * 63)  # 保留字节
    ]


class NET_DVR_RECORD_TIME_SPAN(Structure):
    _fields_ = [
        ("dwSize", c_uint32),  # 结构体大小
        ("strBeginTime", NET_DVR_TIME),  # 开始时间
        ("strEndTime", NET_DVR_TIME),  # 结束时间
        ("byType", c_byte),  # 录像类型
        ("byRes", c_byte * 35)  # 保留
    ]


class NET_DVR_STREAM_INFO(Structure):
    _fields_ = [
        ("dwSize", c_uint32),  # 结构体大小
        ("byID", c_byte * 32),  # ID数组
        ("dwChannel", c_uint32),  # 通道号
        ("byRes", c_byte * 32)  # 保留
    ]


class NET_DVR_MRD_SEARCH_PARAM(Structure):
    _fields_ = [
        ("dwSize", c_uint32),  # 结构体大小
        ("struStreamInfo", NET_DVR_STREAM_INFO),  # 布防点
        ("wYear", c_uint16),  # 年
        ("byMonth", c_byte),  # 月
        ("byDrawFrame", c_byte),  # 0-不抽帧 1-抽帧
        ("byStreamType", c_byte),  # 0-主码流 1-子码流
        ("byLocalOrUTC", c_byte),  # 0-设备本地时区  1-UTC
        ("byRes", c_byte * 30)  # 保留
    ]


# 月历录像分布查询结果结构体
class NET_DVR_MRD_SEARCH_RESULT(Structure):
    _fields_ = [
        ("dwSize", c_uint32),  # 结构体大小
        ("byRecordDistribution", c_byte * 32),
        # 录像分布，byRecordDistribution[0]=1表示1日存在录像，byRecordDistribution[0]=0表示没有录像，byRecordDistribution[1]表示2日，以此类推
        ("byHasEventRecode", c_byte * 31),  # 事件录像 0-无事件录像，1-有事件录像
        ("byRes", c_byte)  # 保留
    ]


class NET_DVR_STD_CONFIG(Structure):
    _fields_ = [
        ("lpCondBuffer", c_void_p),  # [in]条件参数(结构体格式),例如通道号等.可以为NULL
        ("dwCondSize", c_uint32),  # [in] lpCondBuffer指向的内存大小
        ("lpInBuffer", c_void_p),  # [in]输入参数(结构体格式),设置时不为NULL，获取时为NULL
        ("dwInSize", c_uint32),  # [in] lpInBuffer指向的内存大小
        ("lpOutBuffer", c_void_p),  # [out]输出参数(结构体格式),获取时不为NULL,设置时为NULL
        ("dwOutSize", c_uint32),  # [in] lpOutBuffer指向的内存大小
        ("lpStatusBuffer", c_void_p),  # [out]返回的状态参数(XML格式),获取成功时不会赋值,如果不需要,可以置NULL
        ("dwStatusSize", c_uint32),  # [in] lpStatusBuffer指向的内存大小
        ("lpXmlBuffer", c_void_p),  # [in/out]byDataType = 1时有效,xml格式数据
        ("dwXmlSize", c_uint32),  # [in/out]lpXmlBuffer指向的内存大小,获取时同时作为输入和输出参数，获取成功后会修改为实际长度，设置时表示实际长度，而不是整个内存大小
        ("byDataType", c_byte),  # [in]输入/输出参数类型,0-使用结构体类型lpInBuffer/lpOutBuffer有效,1-使用XML类型lpXmlBuffer有效
        ("byRes", c_byte * 23)  # 保留
    ]


class NET_DVR_LLI_PARAM(Structure):
    _fields_ = [
        ("fSec", c_float),  # 秒[0.000000,60.000000]
        ("byDegree", c_byte),  # 度:纬度[0,90] 经度[0,180]
        ("byMinute", c_byte),  # 分[0,59]
        ("byRes", c_byte * 6)  # 保留
    ]


class NET_DVR_PTZPOS_PARAM(Structure):
    _fields_ = [
        ("fPanPos", c_float),  # 水平参数，精确到小数点后1位
        ("fTiltPos", c_float),  # 垂直参数，精确到小数点后1位
        ("fZoomPos", c_float),  # 变倍参数，精确到小数点后1位
        ("byRes", c_byte * 16)  # 保留
    ]


class NET_DVR_SENSOR_PARAM(Structure):
    _fields_ = [
        ("bySensorType", c_byte),  # SensorType: 0-CCD, 1-CMOS
        ("byRes", c_byte * 31),  # 保留
        ("fHorWidth", c_float),  # 水平宽度，精确到小数点后两位 *10000
        ("fVerWidth", c_float),  # 垂直宽度，精确到小数点后两位 *10000
        ("fFold", c_float)  # zoom=1没变时的焦距，精确到小数点后两位 *100
    ]


class NET_PTZ_INFO(Structure):
    _fields_ = [
        ("fPan", c_float),  # 水平参数
        ("fTilt", c_float),  # 垂直参数
        ("fZoom", c_float),  # 变焦参数
        ("dwFocus", c_uint32),  # 聚焦参数，聚焦范围：归一化0-100000
        ("byRes", c_byte * 4)  # 保留
    ]


# GIS信息
NET_DVR_GET_GISINFO = 3711


class NET_DVR_GIS_INFO(Structure):
    _fields_ = [
        ("dwSize", c_uint32),  # 结构体大小
        ("fAzimuth", c_float),  # 方位角
        ("fHorizontalValue", c_float),  # 水平值
        ("fVerticalValue", c_float),  # 垂直值
        ("fVisibleRadius", c_float),  # 可见半径
        ("fMaxViewRadius", c_float),  # 最大视距
        ("byLatitudeType", c_byte),  # 纬度类型
        ("byLongitudeType", c_byte),  # 经度类型
        ("byPTZPosExEnable", c_byte),  # PTZ位置扩展使能
        ("byRes1", c_byte),  # 保留
        ("struLatitude", NET_DVR_LLI_PARAM),  # 纬度参数
        ("struLongitude", NET_DVR_LLI_PARAM),  # 经度参数
        ("struPtzPos", NET_DVR_PTZPOS_PARAM),  # PTZ位置参数
        ("struSensorParam", NET_DVR_SENSOR_PARAM),  # 传感器参数
        ("struPtzPosEx", NET_PTZ_INFO),  # PTZ位置扩展
        ("fMinHorizontalValue", c_float),  # 最小水平值
        ("fMaxHorizontalValue", c_float),  # 最大水平值
        ("fMinVerticalValue", c_float),  # 最小垂直值
        ("fMaxVerticalValue", c_float),  # 最大垂直值
        ("byRes", c_byte * 220)  # 保留
    ]


class NET_DVR_PTZPOS(Structure):
    _fields_ = [
        ("wAction", c_uint16),  # 获取时该字段无效
        ("wPanPos", c_uint16),  # 水平参数
        ("wTiltPos", c_uint16),  # 垂直参数
        ("wZoomPos", c_uint16)  # 变倍参数
    ]


# 云台锁定配置结构体
class NET_DVR_PTZ_LOCKCFG(Structure):
    _fields_ = [
        ("dwSize", c_uint32),  # 结构体大小
        ("byWorkMode", c_byte),  # 云台锁定控制：0- 解锁，1- 锁定
        ("byRes", c_byte * 123)  # 保留未使用的字段
    ]


class NET_DVR_VIDEOEFFECT(Structure):
    _fields_ = [
        ("byBrightnessLevel", c_byte),  # 亮度级别 [0-100]
        ("byContrastLevel", c_byte),  # 对比度级别 [0-100]
        ("bySharpnessLevel", c_byte),  # 锐度级别 [0-100]
        ("bySaturationLevel", c_byte),  # 饱和度级别 [0-100]
        ("byHueLevel", c_byte),  # 色调级别 [0-100,（保留）]
        ("byEnableFunc", c_byte),  # 使能，按位表示，bit0-SMART IR(防过曝)，bit1-低照度,bit2-强光抑制使能，0-否，1-是
        ("byLightInhibitLevel", c_byte),  # 强光抑制等级，[1-3]表示等级
        ("byGrayLevel", c_byte)  # 灰度值域，0-[0-255]，1-[16-235]
    ]


class NET_DVR_GAIN(Structure):
    _fields_ = [
        ("byGainLevel", c_byte),  # 增益级别 [0-100]
        ("byGainUserSet", c_byte),  # 用户自定义增益 [0-100]，对于抓拍机，是CCD模式下的抓拍增益
        ("byRes", c_byte * 2),  # 保留字段
        ("dwMaxGainValue", c_uint32)  # 最大增益值，单位dB
    ]


class NET_DVR_WHITEBALANCE(Structure):
    _fields_ = [
        ("byWhiteBalanceMode", c_byte),  # 0-手动白平衡（MWB）, 1-自动白平衡1（AWB1）, 2-自动白平衡2 (AWB2),
        # 3-自动控制改名为锁定白平衡(Locked WB), 4-室外(Indoor), 5-室内(Outdoor),
        # 6-日光灯(Fluorescent Lamp), 7-钠灯(Sodium Lamp), 8-自动(Auto-Track),
        # 9-一次白平衡(One Push), 10-室外自动(Auto-Outdoor), 11-钠灯自动 (Auto-Sodiumlight),
        # 12-水银灯(Mercury Lamp), 13-自动白平衡(Auto), 14-白炽灯 (Incandescent Lamp),
        # 15-暖光灯(Warm Light Lamp), 16-自然光(Natural Light)
        ("byWhiteBalanceModeRGain", c_byte),  # 手动白平衡时有效，手动白平衡 R增益
        ("byWhiteBalanceModeBGain", c_byte),  # 手动白平衡时有效，手动白平衡 B增益
        ("byRes", c_byte * 5)  # 保留字段
    ]


class NET_DVR_EXPOSURE(Structure):
    _fields_ = [
        ("byExposureMode", c_byte),  # 0 手动曝光, 1 自动曝光
        ("byAutoApertureLevel", c_byte),  # 自动光圈灵敏度, 0-10
        ("byRes", c_byte * 2),  # 保留字段
        ("dwVideoExposureSet", c_uint32),  # 自定义视频曝光时间（单位us）注:自动曝光时该值为曝光最慢值 新增20-1s(1000000us)
        ("dwExposureUserSet", c_uint32),  # 自定义曝光时间, 在抓拍机上应用时，CCD模式时是抓拍快门速度
        ("dwRes", c_uint32)  # 保留字段
    ]


class NET_DVR_GAMMACORRECT(Structure):
    _fields_ = [
        ("byGammaCorrectionEnabled", c_byte),  # 0 dsibale  1 enable
        ("byGammaCorrectionLevel", c_byte),  # 0-100
        ("byRes", c_byte * 6)  # 保留字段
    ]


class NET_DVR_WDR(Structure):
    _fields_ = [
        ("byWDREnabled", c_byte),  # 宽动态：0 dsibale  1 enable 2 auto
        ("byWDRLevel1", c_byte),  # 0-F
        ("byWDRLevel2", c_byte),  # 0-F
        ("byWDRContrastLevel", c_byte),  # 0-100
        ("byRes", c_byte * 16)  # 保留字段
    ]


class NET_DVR_DAYNIGHT(Structure):
    _fields_ = [
        ("byDayNightFilterType", c_byte),  # 日夜切换：0-白天，1-夜晚，2-自动，3-定时，4-报警输入触发, 5-自动模式2（无光敏）,6-黑光，7-黑光自动，8-黑光定时
        ("bySwitchScheduleEnabled", c_byte),  # 0 dsibale  1 enable,(保留)
        # 定时模式参数
        ("byBeginTime", c_byte),  # 开始时间（小时），0-23
        ("byEndTime", c_byte),  # 结束时间（小时），0-23
        # 模式2
        ("byDayToNightFilterLevel", c_byte),  # 0-7
        ("byNightToDayFilterLevel", c_byte),  # 0-7
        ("byDayNightFilterTime", c_byte),  # (60秒)
        # 定时模式参数
        ("byBeginTimeMin", c_byte),  # 开始时间（分），0-59
        ("byBeginTimeSec", c_byte),  # 开始时间（秒），0-59
        ("byEndTimeMin", c_byte),  # 结束时间（分），0-59
        ("byEndTimeSec", c_byte),  # 结束时间（秒），0-59
        # 报警输入触发模式参数
        ("byAlarmTrigState", c_byte)  # 报警输入触发状态，0-白天，1-夜晚
    ]


class NET_DVR_BACKLIGHT(Structure):
    _fields_ = [
        ("byBacklightMode", c_byte),  # 背光补偿:0 off 1 UP、2 DOWN、3 LEFT、4 RIGHT、5MIDDLE、6自定义，10-开，11-自动，12-多区域背光补偿
        ("byBacklightLevel", c_byte),  # 0x0-0xF
        ("byRes1", c_byte * 2),
        ("dwPositionX1", c_uint32),  # （X坐标1）
        ("dwPositionY1", c_uint32),  # （Y坐标1）
        ("dwPositionX2", c_uint32),  # （X坐标2）
        ("dwPositionY2", c_uint32),  # （Y坐标2）
        ("byRes2", c_byte * 4)
    ]


class NET_DVR_NOISEREMOVE(Structure):
    _fields_ = [
        ("byDigitalNoiseRemoveEnable", c_byte),  # 0-不启用，1-普通模式数字降噪，2-专家模式数字降噪
        ("byDigitalNoiseRemoveLevel", c_byte),  # 普通模式数字降噪级别：0x0-0xF
        ("bySpectralLevel", c_byte),  # 专家模式下空域强度：0-100
        ("byTemporalLevel", c_byte),  # 专家模式下时域强度：0-100
        ("byDigitalNoiseRemove2DEnable", c_byte),  # 抓拍帧2D降噪，0-不启用，1-启用
        ("byDigitalNoiseRemove2DLevel", c_byte),  # 抓拍帧2D降噪级别，0-100
        ("byRes", c_byte * 2)  # 保留字节
    ]


class NET_DVR_CMOSMODECFG(Structure):
    _fields_ = [
        ("byCaptureMod", c_byte),  # 抓拍模式：0-抓拍模式1；1-抓拍模式2
        ("byBrightnessGate", c_byte),  # 亮度阈值
        ("byCaptureGain1", c_byte),  # 抓拍增益1, 0-100
        ("byCaptureGain2", c_byte),  # 抓拍增益2, 0-100
        ("dwCaptureShutterSpeed1", c_uint32),  # 抓拍快门速度1
        ("dwCaptureShutterSpeed2", c_uint32),  # 抓拍快门速度2
        ("byRes", c_byte * 4)  # 保留字节
    ]


class NET_DVR_DEFOGCFG(Structure):
    _fields_ = [
        ("byMode", c_byte),  # 模式，0-不启用，1-自动模式，2-常开模式
        ("byLevel", c_byte),  # 等级，0-100
        ("byRes", c_byte * 6)  # 保留字节
    ]


class NET_DVR_ELECTRONICSTABILIZATION(Structure):
    _fields_ = [
        ("byEnable", c_byte),  # 使能 0- 不启用，1- 启用
        ("byLevel", c_byte),  # 等级，0-100
        ("byRes", c_byte * 6)  # 保留字节
    ]


class NET_DVR_CORRIDOR_MODE_CCD(Structure):
    _fields_ = [
        ("byEnableCorridorMode", c_byte),  # 是否启用走廊模式 0～不启用， 1～启用
        ("byRes", c_byte * 11)  # 保留字节
    ]


class NET_DVR_SMARTIR_PARAM(Structure):
    _fields_ = [
        ("byMode", c_byte),  # 0～手动，1～自动
        ("byIRDistance", c_byte),  # 红外距离等级(等级，距离正比例)level:1~100 默认:50（手动模式下增加）
        ("byShortIRDistance", c_byte),  # 近光灯距离等级(1~100)
        ("byLongIRDistance", c_byte)  # 远光灯距离等级(1~100)
    ]


class NET_DVR_PIRIS_PARAM(Structure):
    _fields_ = [
        ("byMode", c_byte),  # 0-自动，1-手动
        ("byPIrisAperture", c_byte),  # 红外光圈大小等级(等级,光圈大小正比例)level:1~100 默认:50（手动模式下增加）
        ("byRes", c_byte * 6)  # 保留字段
    ]


class NET_DVR_LASER_PARAM_CFG(Structure):
    _fields_ = [
        ("byControlMode", c_byte),  # 控制模式 0-无效，1-自动，2-手动 默认自动
        ("bySensitivity", c_byte),  # 激光灯灵敏度 0-100 默认50
        ("byTriggerMode", c_byte),  # 激光灯触发模式 0-无效，1-机芯触发，2-光敏触发 默认机芯触发
        ("byBrightness", c_byte),  # 控制模式为手动模式下有效；激光灯亮度 0-255 默认100
        ("byAngle", c_byte),  # 激光灯角度 0-无效，范围1-36 默认12，激光灯照射范围为一个圆圈，调节激光角度是调节这个圆的半径的大小
        ("byLimitBrightness", c_byte),  # 控制模式为自动模式下有效；激光灯亮度限制 0~100 （新增）2014-01-26
        ("byEnabled", c_byte),  # 手动控制激光灯使能 0-关闭，1-启动
        ("byIllumination", c_byte),  # 激光灯强度配置0~100
        ("byLightAngle", c_byte),  # 补光角度 0~100
        ("byRes", c_byte * 7)  # 保留字段
    ]


class NET_DVR_FFC_PARAM(Structure):
    _fields_ = [
        ("byMode", c_byte),  # 1-Schedule Mode, 2-Temperature Mode, 3-Off
        ("byRes1", c_byte),  # 时间:按能力显示，单位分钟，选项有10,20,30,40,50,60,120,180,240
        ("wCompensateTime", c_uint16),  # 定时模式下生效
        ("byRes2", c_byte * 4)  # 保留字段
    ]


class NET_DVR_DDE_PARAM(Structure):
    _fields_ = [
        ("byMode", c_byte),  # 1-Off, 2-Normal Mode, 3-Expert Mode
        ("byNormalLevel", c_byte),  # 普通模式等级范围[1,100]，普通模式下生效
        ("byExpertLevel", c_byte),  # 专家模式等级范围[1,100]，专家模式下生效
        ("byRes", c_byte * 5)  # 保留字段
    ]


class NET_DVR_AGC_PARAM(Structure):
    _fields_ = [
        ("bySceneType", c_byte),  # 1-Normal Sence, 2-Highlight Sence, 3-Manual Sence
        ("byLightLevel", c_byte),  # 亮度等级[1,100]；手动模式下生效
        ("byGainLevel", c_byte),  # 增益等级[1,100]；手动模式下生效
        ("byRes", c_byte * 5)  # 保留字段
    ]


class NET_DVR_TIME_EX(Structure):
    _fields_ = [
        ("wYear", c_uint16),
        ("byMonth", c_byte),
        ("byDay", c_byte),
        ("byHour", c_byte),
        ("byMinute", c_byte),
        ("bySecond", c_byte),
        ("byRes", c_byte)
    ]


class NET_DVR_SNAP_CAMERAPARAMCFG(Structure):
    _fields_ = [
        ("byWDRMode", c_byte),  # 宽动态模式;0~关闭，1~数字宽动态 2~宽动态
        ("byWDRType", c_byte),  # 宽动态切换模式; 0~强制启用，1~按时间启用，2~按亮度启用
        ("byWDRLevel", c_byte),  # 宽动态等级，0~6索引对应1-7，默认索引2（即3级）；
        ("byRes1", c_byte),
        ("struStartTime", NET_DVR_TIME_EX),  # 开始宽动态时间
        ("struEndTime", NET_DVR_TIME_EX),  # 结束宽动态时间
        ("byDayNightBrightness", c_byte),  # 日夜转换亮度阈值，0-100，默认50；
        # 记忆色增强
        ("byMCEEnabled", c_byte),  # 记忆色增强使能，true：开启，false：关闭
        ("byMCELevel", c_byte),  # 记忆色增强强度，0~100，默认值50
        # 自动对比度
        ("byAutoContrastEnabled", c_byte),  # 自动对比度使能，true：开启，false：关闭
        ("byAutoContrastLevel", c_byte),  # 自动对比等级（0-100）,默认50
        # 细节增强
        ("byLSEDetailEnabled", c_byte),  # 细节增强使能，true：开启，false：关闭
        ("byLSEDetailLevel", c_byte),  # 细节增强等级（0-100）,默认50
        # 车牌增强
        ("byLPDEEnabled", c_byte),  # 车牌增强使能，true：开启，false：关闭
        ("byLPDELevel", c_byte),  # 车牌增强等级（0-100）,默认50
        # 对比度增强
        ("byLseEnabled", c_byte),  # 对比度增强使能，true：开启，false：关闭
        ("byLseLevel", c_byte),  # 对比度增强等级（0-100）,默认0
        ("byLSEHaloLevel", c_byte),  # 光晕抑制等级。范围 0-100,默认0
        ("byLseType", c_byte),  # 对比度增强切换模式; 0~强制启用，1~按时间启用，2~按亮度启用
        ("byRes2", c_byte * 3),
        ("struLSEStartTime", NET_DVR_TIME_EX),  # 开始对比度增强时间（当byLseType为1时生效）
        ("struLSEEndTime", NET_DVR_TIME_EX),  # 结束对比度增强时间（当byLseType为1时生效）
        ("byLightLevel", c_byte),  # 为亮度等级参数（0-100）,默认0，（当byLseType为2时生效）
        # 车牌对比度
        ("byPlateContrastLevel", c_byte),  # 车牌对比度等级，0~100，默认0
        # 车牌饱和度
        ("byPlateSaturationLevel", c_byte),  # 车牌饱和度等级，0~100，默认0
        ("byRes", c_byte * 9)  # 保留字段
    ]


class NET_DVR_OPTICAL_DEHAZE(Structure):
    _fields_ = [
        ("byEnable", c_byte),  # 0~不启用光学透雾，1~启用光学透雾
        ("byRes", c_byte * 7)
    ]


class NET_DVR_THERMOMETRY_AGC(Structure):
    _fields_ = [
        ("byMode", c_byte),  # AGC模式，0~无效，1~自动，2~手动
        ("byRes1", c_byte * 3),
        ("iHighTemperature", c_uint32),  # 最高温度，范围为：-273~9999摄氏度（1~手动模式下生效）
        ("iLowTemperature", c_uint32),  # 最低温度，范围为：-273~9999摄氏度（1~手动模式下生效）
        ("byRes", c_byte * 8)
    ]


class NET_DVR_CAMERAPARAMCFG_EX(Structure):
    """
    前端参数配置结构体
    """
    _fields_ = [
        ("dwSize", c_uint32),  # 结构体大小
        ("struVideoEffect", NET_DVR_VIDEOEFFECT),  # 亮度、对比度、饱和度、锐度、色调配置
        ("struGain", NET_DVR_GAIN),  # 自动增益
        ("struWhiteBalance", NET_DVR_WHITEBALANCE),  # 白平衡
        ("struExposure", NET_DVR_EXPOSURE),  # 曝光控制
        ("struGammaCorrect", NET_DVR_GAMMACORRECT),  # Gamma校正
        ("struWdr", NET_DVR_WDR),  # 宽动态
        ("struDayNight", NET_DVR_DAYNIGHT),  # 日夜转换
        ("struBackLight", NET_DVR_BACKLIGHT),  # 背光补偿
        ("struNoiseRemove", NET_DVR_NOISEREMOVE),  # 数字降噪
        ("byPowerLineFrequencyMode", c_byte),  # 0-50HZ; 1-60HZ
        ("byIrisMode", c_byte),  # 光圈模式
        ("byMirror", c_byte),  # 镜像：0 off，1- leftright，2- updown，3-center 4-Auto
        ("byDigitalZoom", c_byte),  # 数字缩放
        ("byDeadPixelDetect", c_byte),  # 坏点检测
        ("byBlackPwl", c_byte),  # 黑电平补偿
        ("byEptzGate", c_byte),  # EPTZ开关变量:0-不启用电子云台，1-启用电子云台
        ("byLocalOutputGate", c_byte),  # 本地输出开关变量
        ("byCoderOutputMode", c_byte),  # 编码器fpga输出模式
        ("byLineCoding", c_byte),  # 是否开启行编码
        ("byDimmerMode", c_byte),  # 调光模式
        ("byPaletteMode", c_byte),  # 调色板
        ("byEnhancedMode", c_byte),  # 增强方式（探测物体周边）
        ("byDynamicContrastEN", c_byte),  # 动态对比度增强
        ("byDynamicContrast", c_byte),  # 动态对比度
        ("byJPEGQuality", c_byte),  # JPEG图像质量
        ("struCmosModeCfg", NET_DVR_CMOSMODECFG),  # CMOS模式下前端参数配置，镜头模式从能力集获取
        ("byFilterSwitch", c_byte),  # 滤波开关
        ("byFocusSpeed", c_byte),  # 镜头调焦速度
        ("byAutoCompensationInterval", c_byte),  # 定时自动快门补偿
        ("bySceneMode", c_byte),  # 场景模式
        ("struDefogCfg", NET_DVR_DEFOGCFG),  # 透雾参数
        ("struElectronicStabilization", NET_DVR_ELECTRONICSTABILIZATION),  # 电子防抖
        ("struCorridorMode", NET_DVR_CORRIDOR_MODE_CCD),  # 走廊模式
        ("byExposureSegmentEnable", c_byte),  # 曝光时间和增益呈阶梯状调整
        ("byBrightCompensate", c_byte),  # 亮度增强
        ("byCaptureModeN", c_byte),  # 视频输入模式（N制）
        ("byCaptureModeP", c_byte),  # 视频输入模式（P制）
        ("struSmartIRParam", NET_DVR_SMARTIR_PARAM),  # 红外放过爆配置信息
        ("struPIrisParam", NET_DVR_PIRIS_PARAM),  # PIris配置信息
        ("struLaserParam", NET_DVR_LASER_PARAM_CFG),  # 激光参数
        ("struFFCParam", NET_DVR_FFC_PARAM),
        ("struDDEParam", NET_DVR_DDE_PARAM),
        ("struAGCParam", NET_DVR_AGC_PARAM),
        ("byLensDistortionCorrection", c_byte),  # 镜头畸变校正
        ("byDistortionCorrectionLevel", c_byte),  # 畸变校正等级
        ("byCalibrationAccurateLevel", c_byte),  # 畸变校正强度
        ("byZoomedInDistantViewLevel", c_byte),  # 远端放大等级
        ("struSnapCCD", NET_DVR_SNAP_CAMERAPARAMCFG),  # 抓拍机CCD参数
        ("struOpticalDehaze", NET_DVR_OPTICAL_DEHAZE),  # 光学透雾参数
        ("struThermAGC", NET_DVR_THERMOMETRY_AGC),  # 测温AGC配置
        ("byFusionMode", c_byte),  # 双光谱视频融合模式
        ("byHorizontalFOV", c_byte),  # 水平视场角
        ("byVerticalFOV", c_byte),  # 垂直视场角
        ("byBrightnessSuddenChangeSuppression", c_byte),  # 亮度突变抑制
        ("byGPSEnabled", c_byte),  # GPS开关使能
        ("byRes2", c_byte * 155)  # 保留字段
    ]


class NET_DVR_FOCUSMODE_CFG(Structure):
    _fields_ = [
        ("dwSize", c_uint32),
        ("byFocusMode", c_byte),  # 聚焦模式，0-自动，1-手动，2-半自动
        ("byAutoFocusMode", c_byte),  # 自动聚焦模式，0-关，1-模式A，2-模式B，3-模式AB，4-模式C 自动聚焦模式，需要在聚焦模式为自动时才显示
        ("wMinFocusDistance", c_uint16),  # 最小聚焦距离，单位CM, 0-自动，0xffff-无穷远
        ("byZoomSpeedLevel", c_byte),  # 变倍速度，为实际取值，1-3
        ("byFocusSpeedLevel", c_byte),  # 聚焦速度，为实际取值，1-3
        ("byOpticalZoom", c_byte),  # 光学变倍，0-255
        ("byDigtitalZoom", c_byte),  # 数字变倍，0-255
        ("fOpticalZoomLevel", c_float),  # 光学变倍(倍率值) [1,32], 最小间隔0.5 ，内部设备交互的时候*1000
        ("dwFocusPos", c_uint32),
        # dwFocusPos 是focus值（聚焦值），范围为[0x1000,0xC000]，这个值是sony坐标值，使用这个值是为了对外统一，保证不同的镜头对外focus值都转换在这个范围内 (手动聚焦模式下应用)
        ("byFocusDefinitionDisplay", c_byte),
        # 聚焦清晰度显示，0~不显示，1~显示, 开启会在码流上显示当前镜头目标的清晰度值，用于帮助客户调焦使相机抓拍能够达到最清晰的效果，该清晰度越大代表着越清晰，清晰度范围为：0~100.0000
        ("byFocusSensitivity", c_byte),  # 聚焦灵敏度，范围[0,2]，聚焦模式为自动、半自动时生效
        ("byRes1", c_byte * 2),
        ("dwRelativeFocusPos", c_uint32),  # 相对focus值，其低16位表示聚焦值，0~4000；高16位代表当前聚焦值获取时的温度值
        ("byRes", c_byte * 48)
    ]


class NET_DVR_IPDEVINFO_V31(Structure):
    _fields_ = [
        ("byEnable", c_byte),  # 该通道是否启用
        ("byProType", c_byte),  # 协议类型(默认为私有协议)，0- 私有协议，1- 松下协议，2- 索尼，更多协议通过NET_DVR_GetIPCProtoList获取
        ("byEnableQuickAdd", c_byte),  # 0-不支持快速添加；1-使用快速添加
        ("byRes1", c_byte),  # 保留，置为0
        ("sUserName", c_byte * NAME_LEN),  # 用户名
        ("sPassword", c_byte * PASSWD_LEN),  # 密码
        ("byDomain", c_byte * MAX_DOMAIN_NAME),  # 设备域名
        ("struIP", NET_DVR_IPADDR),  # IP地址
        ("wDVRPort", c_uint16),  # 端口号
        ("szDeviceID", c_byte * 32),  # 设备ID
        ("byEnableTiming", c_byte),  # 0-保留，1-不启用NVR对IPC自动校时，2-启用NVR对IPC自动校时
        ("byCertificateValidation", c_byte)  # 0-不启用证书验证 1-启用证书验证
    ]


class NET_DVR_IPCHANINFO(Structure):
    _fields_ = [
        ('byEnable', c_byte),  # 该通道是否在线
        ('byIPID', c_byte),  # IP设备ID低8位，当设备ID为0时表示通道不可用
        ('byChannel', c_byte),  # 通道号
        ('byIPIDHigh', c_byte),  # IP设备ID的高8位
        ('byTransProtocol', c_byte),  # 传输协议类型0-TCP/auto(具体有设备决定)，1-UDP 2-多播 3-仅TCP 4-auto
        ('byGetStream', c_byte),  # 是否对该通道取流，0-是，1-否
        ('byres', c_byte * 30)  # 保留
    ]


class NET_DVR_IPCHANINFO_V40(Structure):
    _fields_ = [
        ('byEnable', c_byte),  # IP通道在线状态，是一个只读的属性；0表示HDVR或者NVR设备的数字通道连接对应的IP设备失败，该通道不在线；1表示连接成功，该通道在线
        ('byRes1', c_byte),  # 保留，置为0
        ('wIPID', c_uint16),  # IP设备ID
        ('dwChannel', c_uint32),
        # IP设备的通道号，例如设备A（HDVR或者NVR设备）的IP通道01，对应的是设备B（DVS）里的通道04，则byChannel=4，如果前端接的是IPC则byChannel=1
        ('byTransProtocol', c_byte),  # 传输协议类型：0- TCP，1- UDP，2- 多播，0xff- auto(自动)
        ('byTransMode', c_byte),  # 传输码流模式：0- 主码流，1- 子码流
        ('byFactoryType', c_byte),  # 前端设备厂家类型
        ('byRes', c_byte * 241)  # 保留，置为0
    ]


class NET_DVR_GET_STREAM_UNION(Union):
    _fields_ = [
        ('struChanInfo', NET_DVR_IPCHANINFO),  # IP通道信息
        ('struIPChan', NET_DVR_IPCHANINFO_V40),  # 直接从设备取流（扩展）
        ('byUnionLen', c_byte * 492)  # 直接从设备取流（扩展）
    ]


class NET_DVR_STREAM_MODE(Structure):
    _fields_ = [
        ("byGetStreamType", c_byte),  # 取流方式
        ("byRes", c_byte * 3),  # 保留，置为0
        ("uGetStream", NET_DVR_GET_STREAM_UNION)  # 不同取流方式联合体
    ]


class NET_DVR_IPPARACFG_V40(Structure):
    _fields_ = [
        ("dwSize", c_uint32),  # 结构大小
        ("dwGroupNum", c_uint32),  # 设备支持的总组数（只读）
        ("dwAChanNum", c_uint32),  # 最大模拟通道个数（只读）
        ("dwDChanNum", c_uint32),  # 数字通道个数（只读）
        ("dwStartDChan", c_uint32),  # 起始数字通道（只读）
        ("byAnalogChanEnable", c_byte * MAX_CHANNUM_V30),  # 模拟通道资源是否启用，从低到高表示1-64通道：0-禁用，1-启用
        ("struIPDevInfo", NET_DVR_IPDEVINFO_V31 * MAX_IP_DEVICE_V40),  # IP设备信息，下标0对应设备IP ID为1
        ("struStreamMode", NET_DVR_STREAM_MODE * MAX_CHANNUM_V30),  # 取流模式
        ("byRes2", c_byte * 20)  # 保留，置为0
    ]


class NET_DVR_DISKSTATE(Structure):
    _fields_ = [
        ("dwVolume", c_uint32),  # 硬盘的容量
        ("dwFreeSpace", c_uint32),  # 硬盘的剩余空间
        ("dwHardDiskStatic", c_uint32)  # 硬盘的状态，按位: 1-休眠, 2-不正常, 3-休眠硬盘出错
    ]


class NET_DVR_CHANNELSTATE_V30(Structure):
    _fields_ = [
        ("byRecordStatic", c_byte),  # 通道是否在录像，0-不录像，1-录像
        ("bySignalStatic", c_byte),  # 连接的信号状态，0-正常，1-信号丢失
        ("byHardwareStatic", c_byte),  # 通道硬件状态，0-正常，1-异常，例如DSP死掉
        ("byRes1", c_byte),  # 保留
        ("dwBitRate", c_uint32),  # 实际码率
        ("dwLinkNum", c_uint32),  # 客户端连接的个数
        ("struClientIP", NET_DVR_IPADDR * MAX_LINK),  # 客户端的IP地址
        ("dwIPLinkNum", c_uint32),  # 如果该通道为IP接入，那么表示IP接入当前的连接数
        ("byExceedMaxLink", c_byte),  # 是否超出了单路6路连接数，0-未超出，1-超出
        ("byRes", c_byte * 3),  # 保留字节
        ("dwAllBitRate", c_uint32),  # 所有实际码率之和
        ("dwChannelNo", c_uint32)  # 当前的通道号，0xffffffff表示无效
    ]


class NET_DVR_WORKSTATE_V40(Structure):
    _fields_ = [
        ("dwSize", c_uint32),  # 结构体大小
        ("dwDeviceStatic", c_uint32),  # 设备的状态，0-正常，1-CPU占用率太高，超过85%，2-硬件错误，例如串口死掉
        ("struHardDiskStatic", NET_DVR_DISKSTATE * MAX_DISKNUM_V30),  # 硬盘状态，一次最多只能获取33个硬盘信息
        ("struChanStatic", NET_DVR_CHANNELSTATE_V30 * MAX_CHANNUM_V40),  # 通道的状态，从前往后顺序排列
        ("dwHasAlarmInStatic", c_uint32 * MAX_ALARMIN_V40),  # 有报警的报警输入口，按值表示，按下标值顺序排列，值为0xffffffff时当前及后续值无效
        ("dwHasAlarmOutStatic", c_uint32 * MAX_ALARMOUT_V40),  # 有报警输出的报警输出口，按值表示，按下标值顺序排列，值为0xffffffff时当前及后续值无效
        ("dwLocalDisplay", c_uint32),  # 本地显示状态，0-正常，1-不正常
        ("byAudioInChanStatus", c_byte * MAX_AUDIO_V30),  # 按位表示语音通道的状态，0-未使用，1-使用中，第0位表示第1个语音通道
        ("byRes1", c_byte * 2),
        ("fHumidity", c_uint16),  # 传感器获知的湿度，范围: 0.0 ~ 100.0
        ("fTemperature", c_uint16),  # 传感器获知的温度，范围：-20.0 ~ 90.0
        ("byRes", c_byte * 116)  # 保留
    ]


DEV_WORK_STATE_CB = fun_ctype(c_void_p, c_uint32, POINTER(NET_DVR_WORKSTATE_V40))


class NET_DVR_CHECK_DEV_STATE(Structure):
    _fields_ = [
        ("dwTimeout", c_uint32),  # 定时检测设备工作状态，单位ms，为0时，表示使用默认值(30000)。最小值为1000
        ("fnStateCB", DEV_WORK_STATE_CB),
        ("pUserData", c_void_p),
        ("byRes", c_ubyte * 60)
    ]


class NET_DVR_PTZABSOLUTEEX_CFG(ctypes.Structure):
    _fields_ = [
        ("dwSize", c_uint32),  # 结构体大小
        ("struPTZCtrl", NET_PTZ_INFO),  # 设备PTZF信息
        ("dwFocalLen", c_uint32),  # 焦距范围：0-100000MM
        ("fHorizontalSpeed", c_uint16),  # 水平转动速度：0.01-1000.00度/S
        ("fVerticalSpeed", c_uint16),  # 垂直转动速度：0.01-1000.00度/S
        ("byZoomType", c_byte),  # 镜头变倍配置类型0~ absoluteZoom，1~ focalLen
        ("byRes", c_byte * 123)  # 保留字段
    ]


class NET_DVR_GBT28181_CHANINFO_CFG(Structure):
    _fields_ = [
        ("dwSize", c_uint32),  # 结构体大小
        ("szVideoChannelNumID", c_byte * 64),  # 设备视频通道编码ID：64字节字符串，仅限数字
        ("byRes", c_byte * 256)  # 保留字段
    ]


class NET_DVR_AES_KEY_INFO(Structure):
    _fields_ = [
        ("sAESKey", c_byte * 16),  # 码流加密密钥
        ("byRes", c_byte * 64)  # 保留字节
    ]


# 巡航路径配置条件结构体
class NET_DVR_CRUISEPOINT_COND(Structure):
    _fields_ = [
        ("dwSize", c_uint32),
        ("dwChan", c_uint32),  # 通道号
        ("wRouteNo", c_uint16),  # 巡航路径号
        ("byRes", c_byte * 30)
    ]


# 巡航点参数结构体
class NET_DVR_CRUISEPOINT_PARAM(Structure):
    _fields_ = [
        ("wPresetNo", c_uint16),
        ("wDwell", c_uint16),
        ("bySpeed", c_byte),
        ("bySupport256PresetNo", c_byte),
        ("byRes", c_byte * 6)
    ]


# 巡航路径配置结构体V40
class NET_DVR_CRUISEPOINT_V40(Structure):
    _fields_ = [
        ("dwSize", c_uint32),
        ("struCruisePoint", NET_DVR_CRUISEPOINT_PARAM * 128),
        ("byRes", c_byte * 64)
    ]


# 巡航路径配置结构体V50
class NET_DVR_CRUISEPOINT_V50(Structure):
    _fields_ = [
        ("dwSize", c_uint32),
        ("struCruisePoint", NET_DVR_CRUISEPOINT_PARAM * 256),
        ("byRes", c_byte * 64)
    ]


# RS485报警配置结构体
class NET_DVR_ALARM_RS485CFG(Structure):
    _fields_ = [
        ("dwSize", c_uint32),  # 结构体大小
        ("sDeviceName", c_byte * NAME_LEN),  # 前端设备名称
        ("wDeviceType", c_uint16),  # 前端设备类型
        ("wDeviceProtocol", c_uint16),  # 前端设备协议
        ("dwBaudRate", c_uint32),  # 波特率
        ("byDataBit", c_byte),  # 数据位
        ("byStopBit", c_byte),  # 停止位
        ("byParity", c_byte),  # 是否校验
        ("byFlowcontrol", c_byte),  # 是否流控
        ("byDuplex", c_byte),  # 半双工/全双工
        ("byWorkMode", c_byte),  # 工作模式 (0-连接读卡器, 1-连接客户端, 2-连接扩展模块, 3-连接门禁主机, 4-连接梯控主机, 0xff-禁用)
        ("byChannel", c_byte),  # 485通道号
        ("bySerialType", c_byte),  # 串口类型
        ("byMode", c_byte),  # 模式 (0-连接读卡器, 1-连接客户端, 2-连接扩展模块, 3-连接门禁主机, 4-连接梯控主机, 0xff-禁用)
        ("byOutputDataType", c_byte),  # 输出数据类型
        ("byAddress", c_byte),  # 串口地址
        ("byStairsOutputDataType", c_byte),  # 0-无效，1-输出楼层号，2-输出卡号，当byMode为梯控主机时有效
        ("byRes", c_byte * 32)  # 保留字节
    ]


class NET_DVR_ALARMHOST_RS485_SLOT_CFG(Structure):
    """
    报警主机RS485槽位参数配置结构体
    """
    _fields_ = [
        ("dwSize", c_uint32),  # 结构体大小
        ("sDeviceName", c_byte * NAME_LEN),  # 前端设备名称
        ("wDeviceType", c_uint16),  # 前端设备类型
        ("wDeviceProtocol", c_uint16),  # 前端设备协议
        ("wAddress", c_uint16),  # 设备地址
        ("byChannel", c_byte),  # 485通道号
        ("bySlotChan", c_byte),  # 槽位号
        ("byRes", c_byte * 60)  # 保留字节
    ]


# 报警信息回调函数
MSGCallBack_V31 = fun_ctype(c_bool, c_uint32, LPNET_DVR_ALARMER, c_void_p, c_ulong, c_void_p)
MSGCallBack = fun_ctype(None, c_uint32, LPNET_DVR_ALARMER, c_void_p, c_ulong, c_void_p)
# 码流回调函数
REALDATACALLBACK = fun_ctype(None, c_long, c_ulong, POINTER(c_ubyte), c_ulong, c_void_p)
