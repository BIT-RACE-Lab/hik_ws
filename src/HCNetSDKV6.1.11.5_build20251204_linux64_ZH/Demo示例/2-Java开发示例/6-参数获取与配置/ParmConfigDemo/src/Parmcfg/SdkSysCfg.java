package Parmcfg;

import NetSDKDemo.HCNetSDK;
import com.sun.jna.NativeLong;
import com.sun.jna.Pointer;
import com.sun.jna.ptr.IntByReference;

import java.io.UnsupportedEncodingException;

import static Parmcfg.TestDemo.hCNetSDK;

/**
 * @Author: jiangxin14
 * @Date: 2024-08-24  15:59
 */
public class SdkSysCfg {

    public static flowTestcallback flowcallback; //网络流量监测回调函数
    public static dev_work_state_cb workStateCb; //设备状态回调

    /**
     * PC电脑有多网卡，绑定网卡，指定使用的实际网卡
     */
    public static void getandBindIP() {
        HCNetSDK.BYTE_TWODIM[] struByteArray = new HCNetSDK.BYTE_TWODIM[16];
        IntByReference pInt = new IntByReference(0);
        boolean pEnableBind = false;
        if (!hCNetSDK.NET_DVR_GetLocalIP(struByteArray, pInt, pEnableBind)) {
            System.out.println("NET_DVR_GetLocalIP失败，错误号:" + hCNetSDK.NET_DVR_GetLastError());
        } else {
            int inum = pInt.getValue();
            for (int i = 0; i < inum; i++) {
                System.out.println("网卡序号:" + i + ", 网卡IP: " + new String(struByteArray[i].strIP).trim());
                //选择需要绑定的网卡
                if ("10.9.137.101".equals(new String(struByteArray[i].strIP))) {
                    hCNetSDK.NET_DVR_SetValidIP(i, true);
                }
            }
        }
    }

    /**
     * 绑定PC端访问设备的端口访问
     */
    //端口绑定
    public void bindPort() {
        HCNetSDK.NET_DVR_LOCAL_TCP_PORT_BIND_CFG strLocalTcpBind = new HCNetSDK.NET_DVR_LOCAL_TCP_PORT_BIND_CFG();
        strLocalTcpBind.read();
        strLocalTcpBind.wLocalBindTcpMinPort = 30000;
        strLocalTcpBind.wLocalBindTcpMaxPort = 30200;
        strLocalTcpBind.write();
        Pointer pStrLocalTcoBind = strLocalTcpBind.getPointer();
        if (hCNetSDK.NET_DVR_SetSDKLocalCfg(0, pStrLocalTcoBind) == false) {
            System.out.println("绑定失败，错误码为" + hCNetSDK.NET_DVR_GetLastError());
        }
        System.out.println("绑定成功");
    }

    /**
     * 获取与设置设备时间参数
     * @param iUserID
     */
    public static void GetandSetDevTime(int iUserID) {
        HCNetSDK.NET_DVR_TIME m_Time = new HCNetSDK.NET_DVR_TIME();
        Pointer pTime = m_Time.getPointer();
        IntByReference pInt = new IntByReference(0);
        boolean b_GetTime = hCNetSDK.NET_DVR_GetDVRConfig(iUserID, HCNetSDK.NET_DVR_GET_TIMECFG, 0xffffffff, pTime, m_Time.size(), pInt);
        if (b_GetTime == false) {
            System.out.println("获取时间参数失败，错误码：" + hCNetSDK.NET_DVR_GetLastError());
        }
        m_Time.read();
        System.out.println("年：" + m_Time.dwYear + "月:" + m_Time.dwMonth + "日:" + m_Time.dwDay + "时：" + m_Time.dwHour +
                "分：" + m_Time.dwMinute + "秒：" + m_Time.dwSecond);

        //直接把获取到的参数设置回去，如果有需要可以自行修改其中需要修改的字段
        boolean b_SetPicCfg = hCNetSDK.NET_DVR_SetDVRConfig(iUserID, HCNetSDK.NET_DVR_SET_TIMECFG,0xffffffff,
                m_Time.getPointer(), m_Time.size());
        if (b_SetPicCfg == false) {
            System.out.println("设置时间失败，错误码：" +  hCNetSDK.NET_DVR_GetLastError());
        }
        else {
            System.out.println("设置时间参数成功");

        }
    }

    /**
     * 获取用户参数
     * @param iUserID
     * @throws UnsupportedEncodingException
     */
    public static void getUsrCfg(int iUserID) throws UnsupportedEncodingException {
        HCNetSDK.NET_DVR_USER_V30  usercfg= new HCNetSDK.NET_DVR_USER_V30();
        usercfg.dwSize = usercfg.size();
        Pointer pUserCfg = usercfg.getPointer();
        NativeLong lChannel = new NativeLong(1);
        IntByReference pInt = new IntByReference(0);
        boolean b_GetUserCfg = hCNetSDK.NET_DVR_GetDVRConfig(iUserID, HCNetSDK.NET_DVR_GET_USERCFG_V30, lChannel.intValue(),
                pUserCfg, usercfg.size(), pInt);
        if (b_GetUserCfg == false) {
            System.out.println("获取用户参数失败，错误码：" + hCNetSDK.NET_DVR_GetLastError());
        }
        usercfg.read();
        //System.out.println("用户名称：" + usercfg.struUser[1].sUserName);
        System.out.println("name： " + new String(usercfg.struUser[0].sUserName,"GBK").trim());
        System.out.println("password： " + new String(usercfg.struUser[0].sPassword,"GBK").trim());

    }

    static class flowTestcallback implements HCNetSDK.FLOWTESTCALLBACK {
        public void invoke(int lFlowHandle, HCNetSDK.NET_DVR_FLOW_INFO pFlowInfo,
                           Pointer pUser) {
            pFlowInfo.read();
            System.out.println("发送的流量数据：" + pFlowInfo.dwSendFlowSize);
            System.out.println("接收的流量数据：" + pFlowInfo.dwRecvFlowSize);
        }
    }

    /**
     * 设备网络流量监测
     * @param iUserID
     * @throws InterruptedException
     */
    public void netFlowDec(int iUserID) throws InterruptedException {
        HCNetSDK.NET_DVR_FLOW_TEST_PARAM struFlowPam = new HCNetSDK.NET_DVR_FLOW_TEST_PARAM();
        struFlowPam.read();
        struFlowPam.dwSize = struFlowPam.size();
        struFlowPam.lCardIndex = 0;
        struFlowPam.dwInterval = 1;
        struFlowPam.write();
        Pointer pUser = null;
        if (flowcallback == null) {
            flowcallback = new flowTestcallback();
        }
        int FlowHandle = hCNetSDK.NET_DVR_StartNetworkFlowTest(iUserID, struFlowPam, flowcallback, pUser);
        if (FlowHandle <= -1) {
            System.out.println("开启流量检测失败，错误码：" + hCNetSDK.NET_DVR_GetLastError());
        } else {
            System.out.println("开启流量检测成功");
        }
        Thread.sleep(20000);
        hCNetSDK.NET_DVR_StopNetworkFlowTest(FlowHandle);
    }

    /**
     * 球机GIS信息获取，需要特定设置支持
     * @param iUserID
     */

    public static void GetGisInfo(int iUserID) {
        HCNetSDK.NET_DVR_STD_CONFIG struStdCfg = new HCNetSDK.NET_DVR_STD_CONFIG();
        HCNetSDK.NET_DVR_GIS_INFO struGisInfo = new HCNetSDK.NET_DVR_GIS_INFO();
        struStdCfg.read();
        IntByReference lchannel = new IntByReference(1);
        struStdCfg.lpCondBuffer = lchannel.getPointer();
        struStdCfg.dwCondSize = 4;
        struStdCfg.lpOutBuffer = struGisInfo.getPointer();
        struStdCfg.dwOutSize = struGisInfo.size();
        struStdCfg.write();//设置前之前要write()
        boolean getSTDConfig = hCNetSDK.NET_DVR_GetSTDConfig(iUserID, HCNetSDK.NET_DVR_GET_GISINFO, struStdCfg);
        if (getSTDConfig == false) {
            System.out.println("查询GIS信息失败，错误码：" + hCNetSDK.NET_DVR_GetLastError());
        } else {
            struGisInfo.read();
            System.out.println("查询成功\n");
            System.out.println(struGisInfo.struPtzPos.fPanPos + "\n");
            System.out.println(struGisInfo.struPtzPos.fTiltPos + "\n");
            System.out.println(struGisInfo.struPtzPos.fZoomPos + "\n");
            System.out.println(struGisInfo.fHorizontalValue);
            System.out.println(struGisInfo.fVerticalValue);
        }

    }

    static class dev_work_state_cb implements HCNetSDK.DEV_WORK_STATE_CB {
        public boolean invoke(Pointer pUserdata, int iUserID, HCNetSDK.NET_DVR_WORKSTATE_V40 lpWorkState) {

            lpWorkState.read();
            System.out.println("设备状态:" + lpWorkState.dwDeviceStatic);
            for (int i = 0; i < HCNetSDK.MAX_CHANNUM_V40; i++) {
                int channel = i + 1;
                System.out.println("第" + channel + "通道是否在录像：" + lpWorkState.struChanStatic[i].byRecordStatic);
            }
            return true;
        }

    }

    //定时巡检设备
    public static void regularInspection() {
        HCNetSDK.NET_DVR_CHECK_DEV_STATE struCheckStatus = new HCNetSDK.NET_DVR_CHECK_DEV_STATE();
        struCheckStatus.read();
        struCheckStatus.dwTimeout = 1000; //定时检测设备工作状态，单位：ms，0表示使用默认值(30000)，最小值为1000
        if (workStateCb == null) {
            workStateCb = new dev_work_state_cb();
        }
        struCheckStatus.fnStateCB = workStateCb;
        struCheckStatus.write();
        boolean b_state = hCNetSDK.NET_DVR_StartGetDevState(struCheckStatus);
        if (!b_state) {
            System.out.println("定时巡检设备状态失败：" + hCNetSDK.NET_DVR_GetLastError());
        }
    }

    //获取GB28181参数
    public static void getGB28181Info(int iUserID) {

        HCNetSDK.NET_DVR_STREAM_INFO streamInfo = new HCNetSDK.NET_DVR_STREAM_INFO();
        streamInfo.read();
        streamInfo.dwSize = streamInfo.size(); //设置结构体大小
        streamInfo.dwChannel = 1; //设置通道
        streamInfo.write();
        Pointer lpInBuffer = streamInfo.getPointer();
        HCNetSDK.NET_DVR_GBT28181_CHANINFO_CFG gbt28181ChaninfoCfg = new HCNetSDK.NET_DVR_GBT28181_CHANINFO_CFG();
        gbt28181ChaninfoCfg.read();
        gbt28181ChaninfoCfg.dwSize = gbt28181ChaninfoCfg.size();
        gbt28181ChaninfoCfg.write();
        Pointer lpOutBuffer = gbt28181ChaninfoCfg.getPointer();
        IntByReference lpBytesReturned = new IntByReference(0);
        //3251对应它的宏定义
        boolean bRet = hCNetSDK.NET_DVR_GetDeviceConfig(iUserID, 3251, 1, lpInBuffer,
                streamInfo.size(), lpBytesReturned.getPointer(), lpOutBuffer, gbt28181ChaninfoCfg.size());
        gbt28181ChaninfoCfg.read();

        if (bRet == false) {
            System.out.println("获取失败,错误码：" + hCNetSDK.NET_DVR_GetLastError());
            return;
        }
    }

    /**
     * 获取码流加密信息
     * @param iUserID
     */
    public static void GetAesKeyInfo(int iUserID) {
        HCNetSDK.NET_DVR_AES_KEY_INFO net_dvr_aes_key_info = new HCNetSDK.NET_DVR_AES_KEY_INFO();
        net_dvr_aes_key_info.read();
        Pointer pnet_dvr_aes_key_info = net_dvr_aes_key_info.getPointer();
        IntByReference pInt = new IntByReference(0);
        boolean b_GetCfg = hCNetSDK.NET_DVR_GetDVRConfig(iUserID, HCNetSDK.NET_DVR_GET_AES_KEY,
                0Xffffffff, pnet_dvr_aes_key_info, net_dvr_aes_key_info.size(), pInt);
        if (b_GetCfg == false) {
            System.out.println("获取码流加密失败  错误码：" + hCNetSDK.NET_DVR_GetLastError());
        }
        System.out.println("获取码流加密信息成功");


    }








}
