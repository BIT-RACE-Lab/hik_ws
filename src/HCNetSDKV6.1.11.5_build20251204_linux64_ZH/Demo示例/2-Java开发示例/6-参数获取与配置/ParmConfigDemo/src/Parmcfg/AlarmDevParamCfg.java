package Parmcfg;

import NetSDKDemo.HCNetSDK;
import com.sun.jna.Pointer;
import com.sun.jna.ptr.IntByReference;

import static Parmcfg.TestDemo.hCNetSDK;

/**
 * 报警主机设备相关参数获取与配置
 * @Author: jiangxin14
 * @Date: 2024-08-26  10:02
 */
public class AlarmDevParamCfg {


    /**
     * 获取报警主机RS485参数
     *
     * @param lUserID
     */
    public static void getRs485Cfg(int lUserID) {
        HCNetSDK.NET_DVR_ALARM_RS485CFG rs485CFG = new HCNetSDK.NET_DVR_ALARM_RS485CFG();
        rs485CFG.dwSize = rs485CFG.size();
        Pointer pointer = rs485CFG.getPointer();
        IntByReference pInt1 = new IntByReference(0);
        rs485CFG.write();
        boolean bGetRs485 = hCNetSDK.NET_DVR_GetDVRConfig(lUserID, HCNetSDK.NET_DVR_GET_ALARM_RS485CFG, 3, pointer, rs485CFG.dwSize, pInt1);
        if (!bGetRs485) {
            System.out.println("获取报警主机RS485参数失败！错误号：" + hCNetSDK.NET_DVR_GetLastError());
            return;
        }
        rs485CFG.read();
        return;

    }

    public static void getRs485SlotInfo(int iUserID) {
        HCNetSDK.NET_DVR_ALARMHOST_RS485_SLOT_CFG strRs485SlotCFG = new HCNetSDK.NET_DVR_ALARMHOST_RS485_SLOT_CFG();
        strRs485SlotCFG.dwSize = strRs485SlotCFG.size();
        Pointer pRs485SlotCFG = strRs485SlotCFG.getPointer();
        IntByReference pInt1 = new IntByReference(0);
        strRs485SlotCFG.write();
        String Schannel = "0000000100000001";  //高2字节表示485通道号，低2字节表示槽位号，都从1开始
        int channel = Integer.parseInt(Schannel, 2);
        boolean bRs485Slot = hCNetSDK.NET_DVR_GetDVRConfig(iUserID, HCNetSDK.NET_DVR_GET_ALARMHOST_RS485_SLOT_CFG, channel, pRs485SlotCFG, strRs485SlotCFG.dwSize, pInt1);
        if (!bRs485Slot) {
            System.out.println("获取报警主机RS485槽位参数失败！错误号：" + hCNetSDK.NET_DVR_GetLastError());
            return;
        }
        strRs485SlotCFG.read();
        return;

    }
}
