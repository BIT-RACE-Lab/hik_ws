package Parmcfg;

import NetSDKDemo.HCNetSDK;
import com.sun.jna.Memory;
import com.sun.jna.Pointer;
import com.sun.jna.ptr.IntByReference;

import static Parmcfg.TestDemo.*;

/**
 * 设备维护管理
 * @Author: jiangxin14
 * @Date: 2024-08-12  16:56
 */
public class DevManager {

    public static fRemoteConfigCallBack fDevStatusCallBack = null;




    /**
     * 手动获取设备在线状态
     * @param iUserID
     */
    public static void getDeviceStatus(int iUserID) {
        boolean devStatus = TestDemo.hCNetSDK.NET_DVR_RemoteControl(iUserID, HCNetSDK.NET_DVR_CHECK_USER_STATUS, null, 0);
        if (devStatus == false) {
            System.out.println("设备不在线");

        } else {
            System.out.println("设备在线");
        }
    }

    /**
     * 获取设备工作状态，CPU，硬盘状态,通道状态，一般适用于硬盘录像机设备
     * @param iUserID
     */
    public static void getWorkS(int iUserID) {

        HCNetSDK.NET_DVR_GETWORKSTATE_COND strWorkStatusCond = new HCNetSDK.NET_DVR_GETWORKSTATE_COND();
        strWorkStatusCond.read();
        strWorkStatusCond.dwSize = strWorkStatusCond.size(); //设置结构体大小
        strWorkStatusCond.byFindChanByCond = 0; //0- 查找全部通道，1- 根据dwFindChanNo数组中各元素所指定的有效通道号进行查找
        strWorkStatusCond.byFindHardByCond = 0; //0- 查找全部磁盘，1- 根据dwFindHardStatus数组中各元素所指定的有效硬盘号进行查找
        strWorkStatusCond.write();
        Pointer lpInBuffer = strWorkStatusCond.getPointer();
        Pointer pUser = null;
        if (fDevStatusCallBack == null)
        {
            fDevStatusCallBack =new fRemoteConfigCallBack();
        }
        int devStatus = TestDemo.hCNetSDK.NET_DVR_StartRemoteConfig(iUserID,HCNetSDK.NET_DVR_GET_WORK_STATUS_V50,lpInBuffer,strWorkStatusCond.size(),
                fDevStatusCallBack,pUser);

        if (devStatus <= -1) {
            System.err.println("获取设备状态NET_DVR_StartRemoteConfig建立失败,错误码：" + TestDemo.hCNetSDK.NET_DVR_GetLastError());
            return;
        }

        System.out.println("获取设备工作状态成功");

        // 添加延时，这里假设延时 5 秒，可根据实际情况调整
        try {
            Thread.sleep(5000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        //调用 NET_DVR_StopRemoteConfig 停止远程配置
        boolean stopResult = hCNetSDK.NET_DVR_StopRemoteConfig(devStatus);
        if (stopResult) {
            System.out.println("成功停止远程配置");
        } else {
            System.err.println("停止远程配置失败，错误码：" + hCNetSDK.NET_DVR_GetLastError());
        }
    }

    /**
     * 获取设备状态回调函数
     */
    static class fRemoteConfigCallBack  implements   HCNetSDK.FRemoteConfigCallBack
    {
        public void invoke(int dwType, Pointer lpBuffer, int dwBufLen, Pointer pUserData){

            switch (dwType)
            {
                case HCNetSDK.NET_SDK_CALLBACK_TYPE_STATUS:
                {
                    HCNetSDK.BYTE_ARRAY struCallbackStatus = new HCNetSDK.BYTE_ARRAY(dwBufLen);
                    struCallbackStatus.write();
                    Pointer pStatus = struCallbackStatus.getPointer();
                    pStatus.write(0, lpBuffer.getByteArray(0, struCallbackStatus.size()), 0, dwBufLen);
                    struCallbackStatus.read();
//                    System.out.println(new String(struCallbackStatus.byValue));
                    break;
                }
                case HCNetSDK.NET_SDK_CALLBACK_TYPE_PROGRESS:
                {
                    HCNetSDK.BYTE_ARRAY struPrscess = new HCNetSDK.BYTE_ARRAY(dwBufLen);
                    struPrscess.write();
                    Pointer pStatus = struPrscess.getPointer();
                    pStatus.write(0, lpBuffer.getByteArray(0, struPrscess.size()), 0, dwBufLen);
                    struPrscess.read();
                    System.out.println("进度值："+ new String(struPrscess.byValue));
                    break;
                }
                case HCNetSDK.NET_SDK_CALLBACK_TYPE_DATA:{
                    HCNetSDK.NET_DVR_WORKSTATE_V40 strWorKStatus = new HCNetSDK.NET_DVR_WORKSTATE_V40();
                    strWorKStatus.read();
                    strWorKStatus.dwSize = strWorKStatus.size();
                    strWorKStatus.write();
                    Pointer lpOutBuffer = strWorKStatus.getPointer();
                    lpOutBuffer.write(0, lpBuffer.getByteArray(0, strWorKStatus.size()), 0, dwBufLen);
                    strWorKStatus.read();
                    System.out.println("设备状态："+strWorKStatus.dwDeviceStatic);//0－正常；1－CPU占用率太高，超过85%；2－硬件错误，例如串口异常
                    System.out.println("第一个硬盘状态：硬盘容量："+strWorKStatus.struHardDiskStatic[0].dwVolume+" 硬盘剩余容量："+strWorKStatus.struHardDiskStatic[0].dwFreeSpace+
                            " 硬盘状态："+strWorKStatus.struHardDiskStatic[0].dwHardDiskStatic);
                    System.out.println("第一路通道状态：是否录像："+strWorKStatus.struChanStatic[0].byRecordStatic+" 信号连接状态："+strWorKStatus.struChanStatic[0].bySignalStatic+
                            " 连接该通道的客户端个数："+strWorKStatus.struChanStatic[0].dwLinkNum);
                    break;

                }
                default:{
                    break;
                }


            }

        }

    }


    //获取设备的基本参数
    public static void  getDeviceInfo(int iUserID) {
        HCNetSDK.NET_DVR_DEVICECFG_V40 m_strDeviceCfg = new HCNetSDK.NET_DVR_DEVICECFG_V40();
        m_strDeviceCfg.dwSize = m_strDeviceCfg.size();
        m_strDeviceCfg.write();
        Pointer pStrDeviceCfg = m_strDeviceCfg.getPointer();
        IntByReference pInt = new IntByReference(0);
        boolean b_GetCfg = TestDemo.hCNetSDK.NET_DVR_GetDVRConfig(iUserID, HCNetSDK.NET_DVR_GET_DEVICECFG_V40,
                0Xffffffff, pStrDeviceCfg, m_strDeviceCfg.dwSize, pInt);
        if (b_GetCfg == false) {
            System.out.println("获取参数失败  错误码：" + TestDemo.hCNetSDK.NET_DVR_GetLastError());
        }
        System.out.println("获取参数成功");
        m_strDeviceCfg.read();
        System.out.println("设备名称:" + new String(m_strDeviceCfg.sDVRName).trim() + "设备序列号：" + new String(m_strDeviceCfg.sSerialNumber));
        System.out.println("模拟通道个数" + m_strDeviceCfg.byChanNum);
        parseVersion(m_strDeviceCfg.dwSoftwareVersion);
        parseBuildTime(m_strDeviceCfg.dwSoftwareBuildDate);
        parseDSPBuildDate(m_strDeviceCfg.dwDSPSoftwareBuildDate);

    }


    public  static void parseBuildTime(int buildTime)
    {
        int year =( (buildTime & 0XFF << 16) >> 16)+2000;
        int month = (buildTime & 0XFF << 8) >> 8 ;
        int data = buildTime & 0xFF;
        System.out.println("Build:"+year+"."+month+"."+data);



    }

    public  static void parseDSPBuildDate(int DSPBuildDate )
    {
        int year =( (DSPBuildDate & 0XFF << 16) >> 16)+2000;
        int month = (DSPBuildDate & 0XFF << 8) >> 8 ;
        int data = DSPBuildDate & 0xFF;
        System.out.println("DSPBuildDate:"+year+"."+month+"."+data);
    }
    //设备版本解析
    public static void parseVersion(int version) {
        int firstVersion = (version & 0XFF << 24) >> 24;
        int secondVersion = (version & 0XFF << 16) >> 16 ;
        int lowVersion = version & 0XFF;

        System.out.println("firstVersion:"+ firstVersion);
        System.out.println("secondVersion:"+ secondVersion);
        System.out.println("lowVersion:"+ lowVersion);
    }


    //获取设备软硬件能力
    public  static  void  GetSofthardware_Ability(int iUserID){
        Pointer pInBuf = null;
        int dwInLength = 0;
        int dwOutLength = 1024*10;
        Memory pOutBuf = new Memory(dwOutLength);
        boolean result = hCNetSDK.NET_DVR_GetDeviceAbility(iUserID, hCNetSDK.DEVICE_SOFTHARDWARE_ABILITY, pInBuf, dwInLength, pOutBuf, dwOutLength);
        if (result) {
            // 从输出缓冲区获取 XML 数据
            String xmlData = pOutBuf.getString(0);
            System.out.println("设备软硬件能力信息（XML 格式）：");
            System.out.println(xmlData);
        }else {
            System.out.println("获取设备软硬件能力失败！错误码："+hCNetSDK.NET_DVR_GetLastError());
        }
    }

    //设备JPEG抓图能力
    public  static  void  GetJPEG_Cap_Ability(int iUserID){
        // 构建输入的 XML 数据
        String inputXml = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n" +
                "<!--req, 获取JPEG抓图能力时pInBuf参数描述-->\n" +
                "<JpegCaptureAbility version=\"2.0\">\n" +
                "        <channelNO>1</channelNO><!--req,通道号-->\n" +
                "</JpegCaptureAbility>";
        // 输入缓冲区
        byte[] inputBytes = inputXml.getBytes();
        int dwInLength = inputBytes.length;
        Memory pInBuf = new Memory(dwInLength);
        pInBuf.write(0, inputBytes, 0, dwInLength);
        int dwOutLength = 1024*10;// 输出缓冲区
        Memory pOutBuf = new Memory(dwOutLength);
        boolean result = hCNetSDK.NET_DVR_GetDeviceAbility(iUserID, hCNetSDK.DEVICE_JPEG_CAP_ABILITY, pInBuf, dwInLength, pOutBuf, dwOutLength);
        if (result) {
            // 从输出缓冲区获取 XML 数据
            String xmlData = pOutBuf.getString(0);
            System.out.println("设备JPEG抓图能力（XML 格式）：");
            System.out.println(xmlData);
        }else {
            System.out.println("设备JPEG抓图能力！错误码："+hCNetSDK.NET_DVR_GetLastError());
        }
    }

    //日志查找
    public  static  void  FindLog(int iUserID){
        // 初始化查找条件
        HCNetSDK.NET_DVR_FIND_LOG_COND findCond = new HCNetSDK.NET_DVR_FIND_LOG_COND();
        findCond.dwSelectMode = 2;//按2-时间查找
        findCond.dwMainType = 0; //日志主类型,全部
        findCond.dwSubType = 0; //日志次类型,全部
        // 初始化开始时间
        HCNetSDK.NET_DVR_TIME_V50 startTime = new HCNetSDK.NET_DVR_TIME_V50();
        startTime.wYear = 2023;
        startTime.byMonth = 2;
        startTime.byDay = 1;
        startTime.byHour = 0;
        startTime.byMinute = 0;
        startTime.bySecond = 0;
        startTime.byISO8601 = 0;
        startTime.wMillisecond = 0;
        startTime.cTimeDifferenceH = 0;
        startTime.cTimeDifferenceM = 0;
        // 初始化结束时间
        HCNetSDK.NET_DVR_TIME_V50 endTime = new HCNetSDK.NET_DVR_TIME_V50();
        endTime.wYear = 2023;
        endTime.byMonth = 2;
        endTime.byDay = 7;
        endTime.byHour = 11;
        endTime.byMinute = 22;
        endTime.bySecond = 0;
        endTime.byISO8601 = 0;
        endTime.wMillisecond = 0;
        endTime.cTimeDifferenceH = 0;
        endTime.cTimeDifferenceM = 0;
        // 将开始时间和结束时间赋值给查找条件结构体
        findCond.struStartTime = startTime;
        findCond.struEndTime = endTime;
        // 开始查找日志
        int lLogHandle = hCNetSDK.NET_DVR_FindDVRLog_V50(iUserID, findCond);
        if (lLogHandle < 0) {
            System.out.println("日志查找失败,错误码："+hCNetSDK.NET_DVR_GetLastError());
            return;
        }
        // 用于存储是否找到日志的标志
        boolean foundLog = false;
        // 日志信息结构体实例
        HCNetSDK.NET_DVR_LOG_V50 logData = new HCNetSDK.NET_DVR_LOG_V50();
        // 循环获取日志
        int result = hCNetSDK.NET_DVR_FindNextLog_V50(lLogHandle, logData);
        HCNetSDK.NET_DVR_TIME_V50 logTime = logData.struLogTime;
        HCNetSDK.NET_DVR_IPADDR remoteHostAddr = logData.struRemoteHostAddr;
        while (result>0) {
            foundLog = true;
            if(result==1000){
                System.out.println("获取日志信息成功:");
                System.out.println("日志时间: " + logTime.wYear + "-" + logTime.byMonth + "-" + logTime.byDay + " " +
                        logTime.byHour + ":" + logTime.byMinute + ":" + logTime.bySecond+ ", 主类型: " + logData.dwMajorType + ", 次类型: " + logData.dwMinorType
                        + ", 远程主机地址: " + remoteHostAddr.getIpV4String());
                result = hCNetSDK.NET_DVR_FindNextLog_V50(lLogHandle, logData);
            } else if (result==HCNetSDK.NET_DVR_FILE_NOFIND) {
                System.out.println("未查找到日志");
                break;
            } else if (result==HCNetSDK.NET_DVR_ISFINDING) {
                System.out.println("正在查找请等待");
                result = hCNetSDK.NET_DVR_FindNextLog_V50(lLogHandle, logData);
            } else if (result==HCNetSDK.NET_DVR_NOMOREFILE) {
                System.out.println("没有更多的日志，查找结束");
                break;
            } else if (result==HCNetSDK.NET_DVR_FILE_EXCEPTION) {
                System.out.println("查找日志时异常");
                break;
            }
        }
        // 根据是否找到日志输出相应信息
        if (!foundLog){
            System.out.println("查找失败");
        }
        // 释放查找日志的资源
        boolean closeResult = hCNetSDK.NET_DVR_FindLogClose_V30(lLogHandle);
        if (closeResult) {
            System.out.println("日志查找资源释放成功");
        } else {
            System.out.println("日志查找资源释放失败,错误码: "+hCNetSDK.NET_DVR_GetLastError());
        }
    }

}
