package com.hik;

import CommonMethod.ConfigFileUtil;
import NetSDKDemo.HCNetSDK;
import com.sun.jna.Pointer;
import com.sun.jna.ptr.IntByReference;

import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

/**
 * @author jiangxin
 * @create 2021-04-20-17:17
 * <p>
 * 远程控制道闸模块，功能：远程控制道闸开启、关闭、获取道闸状态
 */
public class BarrierGateManage {


    /**
     * 道闸控制
     * @param lUserID
     */
    public static void BarrierGateCtrl(int lUserID) {

        HCNetSDK.NET_DVR_BARRIERGATE_CFG struBarrierCfg = new HCNetSDK.NET_DVR_BARRIERGATE_CFG();
        struBarrierCfg.read();
        struBarrierCfg.dwSize = struBarrierCfg.size();
        struBarrierCfg.byEntranceNo = 1;   //出入口编号，取值范围：[1,8]
        struBarrierCfg.byBarrierGateCtrl = 1; //控制参数：0- 关闭道闸，1- 开启道闸，2- 停止道闸，3- 锁定道闸，4- 解锁道闸
        struBarrierCfg.byLaneNo = 1; //道闸号：0- 表示无效值(设备需要做有效值判断)，1- 道闸1
        struBarrierCfg.dwChannel = 1; //通道号
        struBarrierCfg.byUnlock = 0; //启用解锁使能：0- 不启用，1- 启用
        struBarrierCfg.write();
        boolean b_Gate = ITCMain.hCNetSDK.NET_DVR_RemoteControl(lUserID, HCNetSDK.NET_DVR_BARRIERGATE_CTRL, struBarrierCfg.getPointer(), struBarrierCfg.size());
        if (!b_Gate) {
            System.err.println("远程控制道闸失败，错误码：" + ITCMain.hCNetSDK.NET_DVR_GetLastError());
        }
        System.out.println("远程道闸控制成功");

    }


    /**
     * 获取道闸状态
     *   <barrierGateStatus>
     *     <!--ro, opt, enum, 出入口道闸状态, subType:int, [0#无信号,1#关到位,2#开到位]-->1
     *   </barrierGateStatus>
     * @param lUserID
     */
    public static void getBarrierGateState(int lUserID)
    {
        String getBarrierGateStateUrl = "GET /ISAPI/Parking/channels/1/barrierGate/barrierGateStatus";
        String responseString = ISAPI.stdXMLConfig(lUserID,getBarrierGateStateUrl,"");
        System.out.println("获取道闸状态返回报文："+responseString);
        return;
    }

    //出入口控制参数获取
    public static void getEntranceParmCfg(int lUserID) {
        HCNetSDK.NET_DVR_BARRIERGATE_COND struBarrierCond = new HCNetSDK.NET_DVR_BARRIERGATE_COND();
        struBarrierCond.read();
        struBarrierCond.byLaneNo = 1; //车道号：0- 表示无效值(设备需要做有效值判断)，1- 车道1
        struBarrierCond.write();
        Pointer pStruBarrierCond = struBarrierCond.getPointer();
        HCNetSDK.NET_DVR_ENTRANCE_CFG struEnterCfg = new HCNetSDK.NET_DVR_ENTRANCE_CFG();
        struEnterCfg.read();
        struEnterCfg.dwSize = struEnterCfg.size();
        struEnterCfg.write();
        Pointer pStruEnterCfg = struEnterCfg.getPointer();
        IntByReference list = new IntByReference(0);
        boolean b_getEnterState = ITCMain.hCNetSDK.NET_DVR_GetDeviceConfig(lUserID, HCNetSDK.NET_DVR_GET_ENTRANCE_PARAMCFG, 1, pStruBarrierCond,
                struBarrierCond.size(), list.getPointer(), pStruEnterCfg, struEnterCfg.size());
        if (!b_getEnterState) {
            System.err.println("获取出入口控制参数失败，错误码：" + ITCMain.hCNetSDK.NET_DVR_GetLastError());
        }

        struEnterCfg.read();
        System.out.println("触发模式：" + "0x" + Integer.toHexString(struEnterCfg.dwRelateTriggerMode));
        System.out.println("道闸状态：" + struEnterCfg.byGateSingleIO[0]);  //单个IO触发参数，数组0表示IO1，数组1表示IO2，依次类推，具体数组值的含义：0- 无，1- 道闸开到位，2- 道闸关到位，3- 消防报警
    }


}
