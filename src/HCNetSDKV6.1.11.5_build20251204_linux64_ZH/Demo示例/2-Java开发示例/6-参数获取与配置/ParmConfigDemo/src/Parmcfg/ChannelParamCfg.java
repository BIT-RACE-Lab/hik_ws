package Parmcfg;

import NetSDKDemo.HCNetSDK;
import com.sun.jna.NativeLong;
import com.sun.jna.Pointer;
import com.sun.jna.ptr.IntByReference;

import java.awt.*;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.text.SimpleDateFormat;
import java.util.Date;
import com.sun.jna.Native;
import com.sun.jna.Library;
import com.sun.jna.Memory;


import static Parmcfg.TestDemo.hCNetSDK;


/**
 * 通道参数配置
 * @Author: jiangxin14
 * @Date: 2024-08-26  09:46
 */
public class ChannelParamCfg {


    /**
     * 获取与设置设备图像参数
     * @param iUserID
     */
    //获取设备的图像参数-移动侦测高亮显示
    public static void GetandSetPicCfg(int iUserID) {
        HCNetSDK.NET_DVR_PICCFG_V40 strPicCfg = new HCNetSDK.NET_DVR_PICCFG_V40();
        strPicCfg.dwSize = strPicCfg.size();
        Pointer pStrPicCfg = strPicCfg.getPointer();
        NativeLong lChannel = new NativeLong(1);
        IntByReference pInt = new IntByReference(0);
        boolean b_GetPicCfg = hCNetSDK.NET_DVR_GetDVRConfig(iUserID, HCNetSDK.NET_DVR_GET_PICCFG_V40, lChannel.intValue(),
                pStrPicCfg, strPicCfg.size(), pInt);
        if (b_GetPicCfg == false) {
            System.out.println("获取图像参数失败，错误码：" + hCNetSDK.NET_DVR_GetLastError());
        }
        strPicCfg.read();
        System.out.println("通道号：" + lChannel );
        System.out.println("预览的图像是否显示OSD：" + strPicCfg.dwShowOsd);
        System.out.println("移动侦测高亮显示是否开启:"+strPicCfg.struMotion.byEnableDisplay);
        strPicCfg.read();

        //直接把获取到的参数设置回去，如果有需要可以自行修改其中需要修改的字段
        boolean b_SetPicCfg = hCNetSDK.NET_DVR_SetDVRConfig(iUserID, HCNetSDK.NET_DVR_SET_PICCFG_V40,lChannel.intValue(),
                pStrPicCfg, strPicCfg.size());
        if (b_SetPicCfg == false) {
            System.out.println("设置图像参数移动侦测高亮参数失败，错误码：" + hCNetSDK.NET_DVR_GetLastError());
        }
        else {
            System.out.println("设置移动侦测高亮参数成功");

        }
    }

    /**
     * 球机PTZ参数获取设置
     * @param iUserID
     */

    public static void SetPTZcfg(int iUserID) {
        HCNetSDK.NET_DVR_PTZPOS struPtTZPos = new HCNetSDK.NET_DVR_PTZPOS();
        IntByReference pUsers = new IntByReference(1);
        boolean b_GetPTZ = hCNetSDK.NET_DVR_GetDVRConfig(iUserID, HCNetSDK.NET_DVR_GET_PTZPOS, 1, struPtTZPos.getPointer(), struPtTZPos.size(), pUsers);
        if (b_GetPTZ == false) {
            System.out.println("获取PTZ坐标信息失败，错误码：" + hCNetSDK.NET_DVR_GetLastError());
        } else {
            struPtTZPos.read();
            int wPanPos = Integer.parseInt(Integer.toHexString(struPtTZPos.wPanPos).trim());
            float WPanPos = wPanPos * 0.1f;
            int wTiltPos = Integer.parseInt(Integer.toHexString(struPtTZPos.wTiltPos).trim());
            float WTiltPos = wTiltPos * 0.1f;
            int wZoomPos = Integer.parseInt(Integer.toHexString(struPtTZPos.wZoomPos).trim());
            float WZoomPos = wZoomPos * 0.1f;
            System.out.println("P参数：" + WPanPos + "\n");
            System.out.println("T参数：" + wTiltPos + "\n");
            System.out.println("Z参数：" + wZoomPos + "\n");
        }
//        struPtTZPos.wAction = 2;
        //本结构体中的wAction参数是设置时的操作类型，因此获取时该参数无效。实际显示的PTZ值是获取到的十六进制值的十分之一，
        // 如获取的水平参数P的值是0x1750，实际显示的P值为175度；获取到的垂直参数T的值是0x0789，实际显示的T值为78.9度，如果T未负值，获取的值减去360
        // 获取到的变倍参数Z的值是0x1100，实际显示的Z值为110倍。
//        String pHex="13669";
//        int pInter=Integer.parseInt(pHex);
//        short pInter = 13669;
//        System.out.println(pInter);
//        struPtTZPos.wPanPos = (short) pInter;
//        struPtTZPos.write();
//        boolean b_SetPTZ = hCNetSDK.NET_DVR_SetDVRConfig(iUserID, HCNetSDK.NET_DVR_SET_PTZPOS, 1, struPtTZPos.getPointer(), struPtTZPos.size());
//        if (b_GetPTZ == false) {
//            System.out.println("设置PTZ坐标信息失败，错误码：" + hCNetSDK.NET_DVR_GetLastError());
//        } else {
//
//            System.out.println("设置PTZ成功");
//        }

    }

    /**
     * 设置云台锁定信息
     * @param iUserID
     */
    public static void SetPTZLOCKCFG(int iUserID) {
        HCNetSDK.NET_DVR_PTZ_LOCKCFG struPtzLockCfg =new HCNetSDK.NET_DVR_PTZ_LOCKCFG();
        struPtzLockCfg.dwSize =struPtzLockCfg.size();
        Pointer pStrPtzLockCfg = struPtzLockCfg.getPointer();
        NativeLong lChannel = new NativeLong(1);
        IntByReference pInt = new IntByReference(0);
        boolean b_GetPtzLockCfg = hCNetSDK.NET_DVR_GetDVRConfig(iUserID, HCNetSDK.NET_DVR_GET_PTZLOCKCFG, lChannel.intValue(),
                pStrPtzLockCfg, struPtzLockCfg.size(), pInt);
        if (b_GetPtzLockCfg == false) {
            System.out.println("获取云台锁定信息失败，错误码：" + hCNetSDK.NET_DVR_GetLastError());
        }
        struPtzLockCfg.read();
        System.out.println("通道号：" + lChannel );
        System.out.println("云台锁定控制状态为：" + struPtzLockCfg.byWorkMode);

        struPtzLockCfg.read();
        struPtzLockCfg.byWorkMode= 1;    //0- 解锁，1- 锁定
        struPtzLockCfg.write();
        boolean b_SetPtzLockCfg = hCNetSDK.NET_DVR_SetDVRConfig(iUserID, HCNetSDK.NET_DVR_SET_PTZLOCKCFG,lChannel.intValue(),
                pStrPtzLockCfg, struPtzLockCfg.size());
        if (b_SetPtzLockCfg== false) {
            System.out.println("设置云台锁定信息失败，错误码：" + hCNetSDK.NET_DVR_GetLastError());
        }
        else {
            System.out.println("设置云台锁定信息成功");
            System.out.println("云台锁定控制状态当前为：" + struPtzLockCfg.byWorkMode);
        }
    }

//        public static void PTZControlOther(int iUserID){
//          boolean b_ptzcontrol=hCNetSDK.NET_DVR_PTZControl_Other(iUserID,1,HCNetSDK.TILT_UP,0);
//
//          if( b_ptzcontrol==false){
//              System.out.println("云台向上转动失败，错误码：" + hCNetSDK.NET_DVR_GetLastError());
//          }else{
//              System.out.println("设置向上转动成功");
//            }

    //      }

    /**
     * 获取(设置)前端参数(扩展)
     * @param iUserID
     */
    public static void GetCameraPara(int iUserID) {
        HCNetSDK.NET_DVR_CAMERAPARAMCFG_EX struCameraParam = new HCNetSDK.NET_DVR_CAMERAPARAMCFG_EX();
        Pointer pstruCameraParam = struCameraParam.getPointer();
        IntByReference ibrBytesReturned = new IntByReference(0);
        boolean b_GetCameraParam = hCNetSDK.NET_DVR_GetDVRConfig(iUserID, HCNetSDK.NET_DVR_GET_CCDPARAMCFG_EX, 1, pstruCameraParam, struCameraParam.size(), ibrBytesReturned);
        if (!b_GetCameraParam) {
            System.out.println("获取前端参数失败，错误码：" + hCNetSDK.NET_DVR_GetLastError());
        }
        struCameraParam.read();
        System.out.println("是否开启旋转：" + struCameraParam.struCorridorMode.byEnableCorridorMode);

        //直接把获取到的参数设置回去，如果有需要可以自行修改其中需要修改的字段
        boolean b_SetCameraParam = hCNetSDK.NET_DVR_SetDVRConfig(iUserID, HCNetSDK.NET_DVR_SET_CCDPARAMCFG_EX, 1, pstruCameraParam, struCameraParam.size());
        if (!b_SetCameraParam) {
            System.out.println("设置前端参数失败，错误码：" + hCNetSDK.NET_DVR_GetLastError());
        }
        struCameraParam.read();
        System.out.println("设置成功");
    }



    //获取和设置网络参数
    public  static  void  GetNetCfg(int iUserID) {
        HCNetSDK.NET_DVR_NETCFG_V50 struNetCfg = new HCNetSDK.NET_DVR_NETCFG_V50();
        Pointer pstruNetCfg = struNetCfg.getPointer();
        IntByReference ibrBytesReturned = new IntByReference(0);
        boolean b_GetNetCfg = hCNetSDK.NET_DVR_GetDVRConfig(iUserID, HCNetSDK.NET_DVR_GET_NETCFG_V50, 1, pstruNetCfg, struNetCfg.size(), ibrBytesReturned);
        if (!b_GetNetCfg) {
            System.out.println("获取网络参数失败，错误码：" + hCNetSDK.NET_DVR_GetLastError());
        }
        struNetCfg.read();
        System.out.println("是否启用DHCP：" + struNetCfg.byUseDhcp);

        //直接把获取到的参数设置回去，如果有需要可以自行修改其中需要修改的字段
        boolean b_SetNetCfg = hCNetSDK.NET_DVR_SetDVRConfig(iUserID, HCNetSDK.NET_DVR_SET_NETCFG_V50, 1, pstruNetCfg, struNetCfg.size());
        if (!b_SetNetCfg) {
            System.out.println("设置网络参数失败，错误码：" + hCNetSDK.NET_DVR_GetLastError());
        }
        struNetCfg.read();
        System.out.println("设置成功");
    }



    //获取和设置录像计划
    public static void GetRecordCfg(int iUserID){
        HCNetSDK.NET_DVR_RECORD_V40 struRecordCfg = new HCNetSDK.NET_DVR_RECORD_V40();
        Pointer pstruRecordCfg = struRecordCfg.getPointer();

        //System.out.println("指针为："+pstruRecordCfg);
        IntByReference ibrBytesReturned = new IntByReference(1);
        boolean b_GetRecordCfg = hCNetSDK.NET_DVR_GetDVRConfig(iUserID, HCNetSDK.NET_DVR_GET_RECORDCFG_V40, 1, pstruRecordCfg, struRecordCfg.size(), ibrBytesReturned);
        if (!b_GetRecordCfg) {
            System.out.println("获取录像计划失败，错误码：" + hCNetSDK.NET_DVR_GetLastError());
        }
        struRecordCfg.read();
        System.out.println("码流类型：" + struRecordCfg.byStreamType);

        //直接把获取到的参数设置回去，如果有需要可以自行修改其中需要修改的字段
        boolean b_SetRecordCfg = hCNetSDK.NET_DVR_SetDVRConfig(iUserID, HCNetSDK.NET_DVR_SET_RECORDCFG_V40, 1, pstruRecordCfg, struRecordCfg.size());
        if (!b_SetRecordCfg) {
            System.out.println("设置录像计划失败，错误码：" + hCNetSDK.NET_DVR_GetLastError());
        }
        struRecordCfg.read();
        System.out.println("设置成功");

    }



    /**
     * 获取快球聚焦模式信息。
     * @param iUserID
     */
    public static void GetFocusMode(int iUserID) {
        HCNetSDK.NET_DVR_FOCUSMODE_CFG struFocusMode = new HCNetSDK.NET_DVR_FOCUSMODE_CFG();
        struFocusMode.read();
        struFocusMode.dwSize = struFocusMode.size();
        struFocusMode.write();
        Pointer pFocusMode = struFocusMode.getPointer();
        IntByReference ibrBytesReturned = new IntByReference(0);
        boolean b_GetCameraParam = hCNetSDK.NET_DVR_GetDVRConfig(iUserID, HCNetSDK.NET_DVR_GET_FOCUSMODECFG, 1, pFocusMode, struFocusMode.size(), ibrBytesReturned);
        if (!b_GetCameraParam) {
            System.out.println("获取快球聚焦模式失败，错误码：" + hCNetSDK.NET_DVR_GetLastError());
        }
        struFocusMode.read();
        System.out.println("聚焦模式：" + struFocusMode.byFocusMode);
        struFocusMode.byFocusMode = 1;
        struFocusMode.byFocusDefinitionDisplay = 1;
        struFocusMode.byFocusSpeedLevel = 3;
        struFocusMode.write();
        boolean b_SetCameraParam = hCNetSDK.NET_DVR_SetDVRConfig(iUserID, HCNetSDK.NET_DVR_SET_FOCUSMODECFG, 1, pFocusMode, struFocusMode.size());
        if (!b_SetCameraParam) {
            System.out.println("设置快球聚焦模式失败，错误码：" + hCNetSDK.NET_DVR_GetLastError());
        }
        struFocusMode.read();
        System.out.println("设置成功");
    }

    /**
     * 获取IP通道
     * @param iUserID
     * @throws UnsupportedEncodingException
     */
    public static void GetIPChannelInfo(int iUserID) throws UnsupportedEncodingException {
        IntByReference ibrBytesReturned = new IntByReference(0);//获取IP接入配置参数
        HCNetSDK.NET_DVR_IPPARACFG_V40 m_strIpparaCfg = new HCNetSDK.NET_DVR_IPPARACFG_V40();
        m_strIpparaCfg.write();
        //lpIpParaConfig 接收数据的缓冲指针
        Pointer lpIpParaConfig = m_strIpparaCfg.getPointer();
        boolean bRet = hCNetSDK.NET_DVR_GetDVRConfig(iUserID, HCNetSDK.NET_DVR_GET_IPPARACFG_V40, 0, lpIpParaConfig, m_strIpparaCfg.size(), ibrBytesReturned);
        m_strIpparaCfg.read();
        System.out.println("起始数字通道号：" + m_strIpparaCfg.dwStartDChan);

        for (int iChannum = 0; iChannum < m_strIpparaCfg.dwDChanNum; iChannum++) {
            int channum = iChannum + m_strIpparaCfg.dwStartDChan;
            HCNetSDK.NET_DVR_PICCFG_V40 strPicCfg = new HCNetSDK.NET_DVR_PICCFG_V40();
            strPicCfg.dwSize = strPicCfg.size();
            strPicCfg.write();
            Pointer pStrPicCfg = strPicCfg.getPointer();
            NativeLong lChannel = new NativeLong(channum);
            IntByReference pInt = new IntByReference(0);
            boolean b_GetPicCfg = hCNetSDK.NET_DVR_GetDVRConfig(iUserID, HCNetSDK.NET_DVR_GET_PICCFG_V40, lChannel.intValue(),
                    pStrPicCfg, strPicCfg.size(), pInt);
//            if (b_GetPicCfg == false) {
//                System.out.println("获取图像参数失败，错误码：" + hCNetSDK.NET_DVR_GetLastError());
//            }
            strPicCfg.read();
            m_strIpparaCfg.struStreamMode[iChannum].read();
            if (m_strIpparaCfg.struStreamMode[iChannum].byGetStreamType == 0) {
                m_strIpparaCfg.struStreamMode[iChannum].uGetStream.setType(HCNetSDK.NET_DVR_IPCHANINFO.class);
                m_strIpparaCfg.struStreamMode[iChannum].uGetStream.struChanInfo.read();

                System.out.println("--------------第"+ (iChannum+1) + "个通道------------------");
                int channel = m_strIpparaCfg.struStreamMode[iChannum].uGetStream.struChanInfo.byIPID   + m_strIpparaCfg.struStreamMode[iChannum].uGetStream.struChanInfo.byIPIDHigh * 256;
                System.out.println("channel:" +  channel);
                if(channel > 0){
                    System.out.println("ip： " + new String(m_strIpparaCfg.struIPDevInfo[channel-1].struIP.sIpV4).trim());
                }
                System.out.println("name： " + new String(strPicCfg.sChanName,"GBK").trim());
                if (m_strIpparaCfg.struStreamMode[iChannum].uGetStream.struChanInfo.byEnable == 1) {
                    System.out.println("IP通道" + channum + "在线");

                } else {

                    System.out.println("IP通道" + channum + "不在线");

                }
            }
        }
    }

    /**
     * 获取高精度PTZ绝对位置配置,一般热成像设备支持
     * @param iUserID
     */
    //
    public static void GetPTZAbsoluteEx(int iUserID) {
        HCNetSDK.NET_DVR_STD_CONFIG struSTDcfg = new HCNetSDK.NET_DVR_STD_CONFIG();
        HCNetSDK.NET_DVR_PTZABSOLUTEEX_CFG struPTZ = new HCNetSDK.NET_DVR_PTZABSOLUTEEX_CFG();
        struSTDcfg.read();
        IntByReference channel = new IntByReference(1);
        struSTDcfg.lpCondBuffer = channel.getPointer();
        struSTDcfg.dwCondSize = 4;
        struSTDcfg.lpOutBuffer = struPTZ.getPointer();
        struSTDcfg.dwOutSize = struPTZ.size();
        struSTDcfg.lpInBuffer = Pointer.NULL;
        struSTDcfg.dwInSize = 0;
        struSTDcfg.write();
        boolean bGetPTZ = hCNetSDK.NET_DVR_GetSTDConfig(iUserID, HCNetSDK.NET_DVR_GET_PTZABSOLUTEEX, struSTDcfg);
        if (bGetPTZ == false) {
            System.out.println("获取PTZ参数错误,错误码：" + hCNetSDK.NET_DVR_GetLastError());
            return;
        }
        struPTZ.read();
        System.out.println("焦距范围：" + struPTZ.dwFocalLen);
        System.out.println("聚焦参数：" + struPTZ.struPTZCtrl.dwFocus);
        return;
    }

    /**
     * 设置球机预置点
     * @param iUserID
     */
    public static void GetCruisePoint(int iUserID) {
        HCNetSDK.NET_DVR_CRUISEPOINT_COND struCruisepointCond = new HCNetSDK.NET_DVR_CRUISEPOINT_COND();
        struCruisepointCond.read();
        struCruisepointCond.dwSize = struCruisepointCond.size();
        struCruisepointCond.dwChan = 1;
        struCruisepointCond.wRouteNo = 1;
        struCruisepointCond.write();

        HCNetSDK.NET_DVR_CRUISEPOINT_V50 struCruisepointV40 = new HCNetSDK.NET_DVR_CRUISEPOINT_V50();
        struCruisepointV40.read();
        struCruisepointV40.dwSize = struCruisepointV40.size();
        struCruisepointV40.write();

        // 错误信息列表
        IntByReference pInt = new IntByReference(0);
        Pointer lpStatusList = pInt.getPointer();

        boolean flag = hCNetSDK.NET_DVR_GetDeviceConfig(iUserID, 6714, 1,
                struCruisepointCond.getPointer(), struCruisepointCond.size(), lpStatusList, struCruisepointV40.getPointer(), struCruisepointV40.size());
        if (flag == false) {
            int iErr = hCNetSDK.NET_DVR_GetLastError();
            System.out.println("NET_DVR_STDXMLConfig失败，错误号：" + iErr);
            return;
        }
        struCruisepointV40.read();
    }

    /**
     * 设备抓图保存到缓冲区
     * @param iUserID
     */
    public static void GetPictoPointer(int iUserID) {
        HCNetSDK.NET_DVR_JPEGPARA jpegpara = new HCNetSDK.NET_DVR_JPEGPARA();
        jpegpara.read();
        jpegpara.wPicSize = 255;
        jpegpara.wPicQuality = 0;
        jpegpara.write();
        HCNetSDK.BYTE_ARRAY byte_array = new HCNetSDK.BYTE_ARRAY(10 * 1024 * 1024);
        IntByReference ret = new IntByReference(0);
        boolean b = hCNetSDK.NET_DVR_CaptureJPEGPicture_NEW(iUserID, 1, jpegpara, byte_array.getPointer(), byte_array.size(), ret);
        if (b == false) {
            System.out.println("抓图失败：" + hCNetSDK.NET_DVR_GetLastError());
            return;
        }
        byte_array.read();
        System.out.println("ret:"+ret.getValue());
        String filePath = ".\\pic\\test.jpg"; // 指定保存文件的路径和名称
        try {
            WriteBytesToFile(byte_array.byValue,ret.getValue(), filePath);
            System.out.println("图片已成功保存为：" + filePath);
        } catch (IOException e) {
            System.err.println("写入文件时发生错误：" + e.getMessage());
            e.printStackTrace();
        }
        System.out.println("抓图成功");
        return;
    }


    /**
     * 将字节数组写入到指定的文件路径。
     *
     * @param bytes 字节数组
     * @param filePath 文件保存路径
     * @throws IOException 如果文件写入过程中发生错误
     */
    private static void WriteBytesToFile(byte[] bytes,int len, String filePath) throws IOException {
        File file = new File(filePath);
        FileOutputStream fos = new FileOutputStream(file);

        fos.write(bytes,0,len);
        fos.close(); // 关闭输出流
    }

    /**
     * 这里应该替换为你实际获取字节数组的方法。
     * 示例中省略具体实现，直接返回null。
     *
     * @return 图片的字节数组
     */
    private static byte[] getYourImageBytes() {
        // 这里应该是从数据库、网络或其他来源获取字节数组的逻辑
        // 返回示例：null，实际使用时需要替换为有效数据
        return null;
    }

    /**
     * 录像起止时间查询
     * @param iUserID
     */
    public static void SearchRecordTime(int iUserID) {
        HCNetSDK.NET_DVR_RECORD_TIME_SPAN_INQUIRY struRecInq = new HCNetSDK.NET_DVR_RECORD_TIME_SPAN_INQUIRY();
        struRecInq.read();
        struRecInq.dwSize = struRecInq.size();
        struRecInq.byType = 0;
        struRecInq.write();
        HCNetSDK.NET_DVR_RECORD_TIME_SPAN struRecSpan = new HCNetSDK.NET_DVR_RECORD_TIME_SPAN();
        //通道号说明：一般IPC/IPD通道号为1，32路以及以下路数的NVR的IP通道通道号从33开始，64路及以上路数的NVR的IP通道通道号从1开始。
        if (hCNetSDK.NET_DVR_InquiryRecordTimeSpan(iUserID, 35, struRecInq, struRecSpan) == false) {
            System.out.println("录像起止时间查询失败，错误码：" + hCNetSDK.NET_DVR_GetLastError());
        } else {
            System.out.println("录像起止时间查询成功");
            struRecSpan.read();
            System.out.println("开启时间：" + "年：" + struRecSpan.strBeginTime.dwYear + "\n");
            System.out.println("开启时间：" + "月：" + struRecSpan.strBeginTime.dwMonth + "\n");
            System.out.println("开启时间：" + "日：" + struRecSpan.strBeginTime.dwDay + "\n");
            System.out.println("开启时间：" + "时：" + struRecSpan.strBeginTime.dwHour + "\n");
            System.out.println("停止时间：" + "年：" + struRecSpan.strEndTime.dwYear + "\n");
            System.out.println("停止时间：" + "月：" + struRecSpan.strEndTime.dwMonth + "\n");
            System.out.println("停止时间：" + "日：" + struRecSpan.strEndTime.dwDay + "\n");
            System.out.println("停止时间：" + "时：" + struRecSpan.strEndTime.dwHour + "\n");
        }
    }

    /**
     * 月历录像查询
     * @param iUserID
     */
    public static void GetRecMonth(int iUserID) {
        HCNetSDK.NET_DVR_MRD_SEARCH_PARAM struMrdSeaParam = new HCNetSDK.NET_DVR_MRD_SEARCH_PARAM();
        struMrdSeaParam.read();
        struMrdSeaParam.dwSize = struMrdSeaParam.size();
        struMrdSeaParam.wYear = 2021;
        struMrdSeaParam.byMonth = 1;
        //通道号说明：一般IPC/IPD通道号为1，32路以及以下路数的NVR的IP通道通道号从33开始，64路及以上路数的NVR的IP通道通道号从1开始。
        struMrdSeaParam.struStreamInfo.dwChannel = 33;
        struMrdSeaParam.write();
        HCNetSDK.NET_DVR_MRD_SEARCH_RESULT struMrdSeaResu = new HCNetSDK.NET_DVR_MRD_SEARCH_RESULT();
        struMrdSeaResu.read();
        struMrdSeaResu.dwSize = struMrdSeaResu.size();
        struMrdSeaResu.write();
        IntByReference list = new IntByReference(0);
        boolean b_GetResult = hCNetSDK.NET_DVR_GetDeviceConfig(iUserID, HCNetSDK.NET_DVR_GET_MONTHLY_RECORD_DISTRIBUTION, 0, struMrdSeaParam.getPointer(),
                struMrdSeaParam.size(), list.getPointer(), struMrdSeaResu.getPointer(), struMrdSeaResu.size());
        if (b_GetResult == false) {
            System.out.println("月历录像查询失败，错误码：" + hCNetSDK.NET_DVR_GetLastError());
        } else {
            struMrdSeaResu.read();
            for (int i = 0; i <= 32; i++) {
                int day = i + 1;
                System.out.println("" + day + "号是否录像文件" + struMrdSeaResu.byRecordDistribution[i]);
            }
        }
    }

    /**
     * 设备抓图
     * @param iUserID
     */
    public static void CaptureJPEGPicture(int iUserID) {
        SimpleDateFormat sdf = new SimpleDateFormat("yyyyMMddHHmmss");
//        String curTime0 = sdf.format(new Date());
        Boolean result = false;
        int count = 0;
        while (!result) {
            try {
                Thread.sleep(1 * 1000); //设置暂停的时间 5 秒
                String curTime0 = sdf.format(new Date());
                count++;
                String filename = ".\\pic\\" + curTime0 + count + ".jpg" + "\0";
                byte[] fileByte = filename.getBytes("UTF-8");

                HCNetSDK.NET_DVR_JPEGPARA strJpegParm = new HCNetSDK.NET_DVR_JPEGPARA();
                strJpegParm.read();
                strJpegParm.wPicSize = 2;
                strJpegParm.wPicQuality = 0;
                strJpegParm.write();
                boolean b_Cap = hCNetSDK.NET_DVR_CaptureJPEGPicture(iUserID, 1, strJpegParm, fileByte);
                if (b_Cap == false) {
                    System.out.println("抓图失败,错误码为:" + hCNetSDK.NET_DVR_GetLastError());
                    return;
                }
                System.out.println(sdf.format(new Date()) + "--循环执行第" + count + "次");
                if (count == 3) {
                    result = true;
                    break;
                }
            } catch (InterruptedException e) {
                e.printStackTrace();
            } catch (UnsupportedEncodingException e) {
                e.printStackTrace();
            }
        }
    }


}

