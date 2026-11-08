import HCNetSDK
from HCNetSDK import *


class ACSManage:

    # 获取(设置)门禁主机参数
    @staticmethod
    def acs_cfg(lUserID, sdk):
        # 获取门禁主机参数
        stru_acs_cfg = HCNetSDK.NET_DVR_ACS_CFG()
        stru_acs_cfg.dwSize = sizeof(stru_acs_cfg)
        int_by_reference = ctypes.c_ulong()
        b_get_acs_cfg = sdk.NET_DVR_GetDVRConfig(lUserID, HCNetSDK.NET_DVR_GET_ACS_CFG, 0xFFFFFFFF, byref(stru_acs_cfg),
                                                 stru_acs_cfg.dwSize, byref(int_by_reference))
        if b_get_acs_cfg:
            print("获取门禁主机参数成功")
            print("1.是否显示抓拍图片：", stru_acs_cfg.byShowCapPic)
            print("2.是否显示卡号：", stru_acs_cfg.byShowCardNo)
            print("3.是否开启语音提示：", stru_acs_cfg.byVoicePrompt)
            print("4.联动抓图是否上传：", stru_acs_cfg.byUploadCapPic)
        else:
            print("获取门禁主机参数失败，错误码为：", sdk.NET_DVR_GetLastError())
            return
        # 设置门禁主机参数
        stru_acs_cfg.byShowCardNo = 1  # 开启显示卡号
        stru_acs_cfg.byVoicePrompt = 0  # 关闭语音提示
        stru_acs_cfg.byUploadCapPic = 1  # 开启联动抓图后，设备上抓拍的图片才会通过报警布防上传，否则没有不上传
        stru_acs_cfg.byShowCapPic = 1
        b_set_acs_cfg = sdk.NET_DVR_SetDVRConfig(lUserID, HCNetSDK.NET_DVR_SET_ACS_CFG, 0xFFFFFFFF, byref(stru_acs_cfg),
                                                 stru_acs_cfg.dwSize)
        if b_set_acs_cfg:
            print("设置门禁主机参数成功！！！")
        else:
            print("设置门禁主机参数失败，错误码为：", sdk.NET_DVR_GetLastError())
        return

    # 获取门禁主机工作状态
    @staticmethod
    def get_acs_status(lUserID, sdk):
        net_dvr_acs_work_statusV50 = HCNetSDK.NET_DVR_ACS_WORK_STATUS_V50()
        net_dvr_acs_work_statusV50.dwSize = sizeof(net_dvr_acs_work_statusV50)
        int_by_reference = ctypes.c_ulong()
        b_get_acs_cfg = sdk.NET_DVR_GetDVRConfig(lUserID, HCNetSDK.NET_DVR_GET_ACS_WORK_STATUS_V50, 0xFFFFFFFF,
                                                 byref(net_dvr_acs_work_statusV50),
                                                 net_dvr_acs_work_statusV50.dwSize, byref(int_by_reference))
        if b_get_acs_cfg:
            print("获取门禁主机工作状态成功!!!")
            print("1.门锁状态(或者梯控的继电器开合状态):", net_dvr_acs_work_statusV50.byDoorLockStatus[0])
            print("2.门状态(或者梯控的楼层状态):", net_dvr_acs_work_statusV50.byDoorStatus[0])
            print("3.门磁状态：", net_dvr_acs_work_statusV50.byMagneticStatus[0])
            print("4.事件报警输入状态：", net_dvr_acs_work_statusV50.byCaseStatus[0])
        else:
            print("获取门禁主机工作状态，错误码为：", sdk.NET_DVR_GetLastError())
        return

    # 远程控门
    @staticmethod
    def remote_control_gate(userID, sdk):
        """
        [in] 门禁序号（楼层编号、锁ID），从1开始，-1表示对所有门（或者梯控的所有楼层）进行操作
            第三个参数dwStaic
         [in] 命令值：0- 关闭（对于梯控，表示受控），1- 打开（对于梯控，表示开门），2- 常开（对于梯控，表示自由、通道状态），3- 常关（对于梯控，表示禁用），4- 恢复（梯控，普通状态），5- 访客呼梯（梯控），6- 住户呼梯（梯控）
        """
        b_gate = sdk.NET_DVR_ControlGateway(userID, 1, 1)
        if b_gate:
            print("远程控门成功")
        else:
            print("远程控门失败,错误码为：", sdk.NET_DVR_GetLastError())
        return
