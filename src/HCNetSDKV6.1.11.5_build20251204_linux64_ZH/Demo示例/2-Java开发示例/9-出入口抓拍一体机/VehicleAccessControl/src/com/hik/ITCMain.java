package com.hik;

import CommonMethod.osSelect;
import NetSDKDemo.HCNetSDK;
import com.sun.jna.Memory;
import com.sun.jna.Native;
import com.sun.jna.Platform;
import com.sun.jna.Pointer;
import com.sun.jna.ptr.IntByReference;

import javax.swing.JOptionPane;
import javax.xml.ws.Action;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.nio.ByteBuffer;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Scanner;

/**
 * @author jiangxin
 * @create 2021-01-13-11:07
 */
public class ITCMain {
    static HCNetSDK hCNetSDK = null;
    static int lUserID = -1; //用户句柄
    /**
     * 动态库加载
     *
     * @return
     */
    private static boolean createSDKInstance() {
        if (hCNetSDK == null) {
            synchronized (HCNetSDK.class) {
                String strDllPath = "";
                try {
                    if (osSelect.isWindows())
                        //win系统加载库路径
                        strDllPath = System.getProperty("user.dir") + "\\lib\\HCNetSDK.dll";
                    else if (osSelect.isLinux())
                        //Linux系统加载库路径
                        strDllPath = System.getProperty("user.dir") + "/lib/libhcnetsdk.so";
                    hCNetSDK = (HCNetSDK) Native.loadLibrary(strDllPath, HCNetSDK.class);
                } catch (Exception ex) {
                    System.out.println("loadLibrary: " + strDllPath + " Error: " + ex.getMessage());
                    return false;
                }
            }
        }
        return true;
    }

    //报警回调函数
    public static void main(String[] args) throws Exception {


        if (hCNetSDK == null) {
            if (!createSDKInstance()) {
                System.out.println("Load SDK fail");
                return;
            }
        }
        //linux系统建议调用以下接口加载组件库
        if (osSelect.isLinux()) {
            HCNetSDK.BYTE_ARRAY ptrByteArray1 = new HCNetSDK.BYTE_ARRAY(256);
            HCNetSDK.BYTE_ARRAY ptrByteArray2 = new HCNetSDK.BYTE_ARRAY(256);
            //这里是库的绝对路径，请根据实际情况修改，注意改路径必须有访问权限
            String strPath1 = System.getProperty("user.dir") + "/lib/libcrypto.so.1.1";
            String strPath2 = System.getProperty("user.dir") + "/lib/libssl.so.1.1";
            System.arraycopy(strPath1.getBytes(), 0, ptrByteArray1.byValue, 0, strPath1.length());
            ptrByteArray1.write();
            hCNetSDK.NET_DVR_SetSDKInitCfg(HCNetSDK.NET_SDK_INIT_CFG_LIBEAY_PATH, ptrByteArray1.getPointer());
            System.arraycopy(strPath2.getBytes(), 0, ptrByteArray2.byValue, 0, strPath2.length());
            ptrByteArray2.write();
            hCNetSDK.NET_DVR_SetSDKInitCfg(HCNetSDK.NET_SDK_INIT_CFG_SSLEAY_PATH, ptrByteArray2.getPointer());
            String strPathCom = System.getProperty("user.dir") + "/lib/";
            HCNetSDK.NET_DVR_LOCAL_SDK_PATH struComPath = new HCNetSDK.NET_DVR_LOCAL_SDK_PATH();
            System.arraycopy(strPathCom.getBytes(), 0, struComPath.sPath, 0, strPathCom.length());
            struComPath.write();
            hCNetSDK.NET_DVR_SetSDKInitCfg(HCNetSDK.NET_SDK_INIT_CFG_SDK_PATH, struComPath.getPointer());
        }

        /**初始化*/
        hCNetSDK.NET_DVR_Init();
        /**加载日志*/
        hCNetSDK.NET_DVR_SetLogToFile(3, "./sdklog", false);
        //设备登录
        lUserID=ITCMain.loginDevice( "10.9.137.222", (short) 8000, "admin", "hik12345");  //登录设备


        for (boolean exit = false; !exit; ) {
            System.out.println("请输入您想要执行的demo实例! （退出请输入yes）");
            Scanner input = new Scanner(System.in);
            String str = input.next();
            // 转换为标准输入
            str = str.toLowerCase();
            if (str.equals("yes")) {
                // 退出程序
                exit = true;
                break;
            }
            switch (str) {
                case "1":
                {
                    System.out.println("\n[Module]下发车辆授权名单示例代码");
                    VechileListManage.addVechileList(lUserID);
                    break;
                }
                case "2":
                {
                    System.out.println("\n[Module]查询车辆授权名单示例代码");
                    VechileListManage.searchVechileList(lUserID);
                    break;
                }
                case "3":
                {
                    System.out.println("\n[Module]删除车辆授权名单示例代码");
                    VechileListManage.deleteVechileList(lUserID);
                    break;
                }
                case "4":
                {
                    System.out.println("\n[Module]远程道闸控制示例代码");
                    BarrierGateManage.BarrierGateCtrl(lUserID);
                    break;
                }
                case "5":
                {
                    System.out.println("\n[Module]获取道闸状态示例代码");
                    BarrierGateManage.getBarrierGateState(lUserID);
                    break;
                }
                case "6":
                {
                    System.out.println("\n[Module]语音播报示例代码");
                    VoiceManage.voiceBroadcastInfo(lUserID);
                    break;
                }
                case "7":
                {
                    System.out.println("\n[Module]获取组合语音播报参数示例代码");
                    VoiceManage.getCombinateBroadcastInfo(lUserID);
                    break;
                }
                case "8":
                {
                    System.out.println("\n[Module]语音播报示例代码");
                    VoiceManage.setCombinateBroadcastInfo(lUserID);
                    break;
                }
                case "9":
                {
                    System.out.println("\n[Module]相机控制LCD显示参数示例代码");
                    LCDdisplayManage.setCameractrlModeLCDdisplayInfo(lUserID);
                    break;
                }
                case "10":
                {
                    System.out.println("\n[Module]获取当前LCD参数示例代码");
                    LCDdisplayManage.getctrlModeLCDdisplayInfo(lUserID);
                    break;
                }
                case "11":
                {
                    System.out.println("\n[Module]设置平台模式LCD参数示例代码");
                    LCDdisplayManage.setplatformctrlModeLCDdisplayInfo(lUserID);
                    break;
                }
                //此后所有case都属于平台控制模式下发LCD显示，需要先调用setplatformctrlModeLCDdisplayInfo接口设置设备未平台模式
                case "12":
                {
                    System.out.println("\n[Module]下发入场无车牌图片显示示例代码");
                    LCDdisplayManage.setPicDisplayEnterNolicense(lUserID);
                    break;
                }
                case "13":
                {
                    System.out.println("\n[Module]车辆出场未缴费场景图片显示示例代码");
                    LCDdisplayManage.setPicDisplayExitNoPay(lUserID);
                    break;
                }
                case "14":
                {
                    System.out.println("\n[Module]设置车辆入场有车牌自定义显示示例代码");
                    LCDdisplayManage.setEnterLicenseDisplay(lUserID);
                    break;
                }
                case "15":
                {
                    System.out.println("\n[Module]设置余位显示示例代码");
                    LCDdisplayManage.setParkingLotDisPlay(lUserID);
                    break;
                }

                default:
                {
                    System.out.println("\n未知的指令操作!请重新输入!\n");
                }
            }
        }






//        vechileListManage.addVechileList(lUserID);
//        vechileListManage.deleteVechileList.json(lUserID, vechileListManage.deleteXml());
//        vechileListManage.getVechileList(lUserID,vechileListManage.getXml());
//        barrierGateManage.BarrierGateCtrl(lUserID);
//        barrierGateManage.getBarrierGateState(lUserID);
//        leDdisplayManage.LEDdisplayCfg(lUserID,leDdisplayManage.LEDdisplayXml());
//         leDdisplayManage.getLEDdisplayMultiScene(lUserID);

//        String str=leDdisplayManage.MultiScenejson();
//        System.out.println(str);
//
//            leDdisplayManage.setLEDdisplayMultiScene(lUserID);
//        voiceManage.getVoiceBroadcastInfo(lUserID)；
//        voiceManage.setVoiceBroadcastInfo(lUserID);




        hCNetSDK.NET_DVR_Logout(lUserID);
        hCNetSDK.NET_DVR_Cleanup();
        return;
    }


    /**
     * 登录设备，支持 V40 和 V30 版本，功能一致。
     *
     * @param ip      设备IP地址
     * @param port    SDK端口，默认为设备的8000端口
     * @param user    设备用户名
     * @param psw     设备密码
     * @return 登录成功返回用户ID，失败返回-1
     */
    public static int loginDevice(String ip, short port, String user, String psw) {
        // 创建设备登录信息和设备信息对象
        HCNetSDK.NET_DVR_USER_LOGIN_INFO loginInfo = new HCNetSDK.NET_DVR_USER_LOGIN_INFO();
        HCNetSDK.NET_DVR_DEVICEINFO_V40 deviceInfo = new HCNetSDK.NET_DVR_DEVICEINFO_V40();

        // 设置设备IP地址
        byte[] deviceAddress = new byte[HCNetSDK.NET_DVR_DEV_ADDRESS_MAX_LEN];
        byte[] ipBytes = ip.getBytes();
        System.arraycopy(ipBytes, 0, deviceAddress, 0, Math.min(ipBytes.length, deviceAddress.length));
        loginInfo.sDeviceAddress = deviceAddress;

        // 设置用户名和密码
        byte[] userName = new byte[HCNetSDK.NET_DVR_LOGIN_USERNAME_MAX_LEN];
        byte[] password = psw.getBytes();
        System.arraycopy(user.getBytes(), 0, userName, 0, Math.min(user.length(), userName.length));
        System.arraycopy(password, 0, loginInfo.sPassword, 0, Math.min(password.length, loginInfo.sPassword.length));
        loginInfo.sUserName = userName;

        // 设置端口和登录模式
        loginInfo.wPort = port;
        loginInfo.bUseAsynLogin = false; // 同步登录
        loginInfo.byLoginMode = 0; // 使用SDK私有协议

        // 执行登录操作
        int userID = hCNetSDK.NET_DVR_Login_V40(loginInfo, deviceInfo);
        if (userID == -1) {
            System.err.println("登录失败，错误码为: " + hCNetSDK.NET_DVR_GetLastError());
        } else {
            System.out.println(ip + " 设备登录成功！");
            // 处理通道号逻辑
            int startDChan = deviceInfo.struDeviceV30.byStartDChan;
            System.out.println("预览起始通道号: " + startDChan);
        }
        return userID; // 返回登录结果
    }



    //手动抓拍
    public void setManualSnap() {
        HCNetSDK.NET_DVR_MANUALSNAP struManualParam = new HCNetSDK.NET_DVR_MANUALSNAP();
        struManualParam.read();
        struManualParam.byOSDEnable = 0;
        struManualParam.byChannel = 1;
        struManualParam.byLaneNo = 1;
        struManualParam.write();
        HCNetSDK.NET_DVR_PLATE_RESULT struPlateResult = new HCNetSDK.NET_DVR_PLATE_RESULT();
        struPlateResult.read();
        struPlateResult.pBuffer1 = new Memory(2 * 1024 * 1024);
        struPlateResult.pBuffer2 = new Memory(2 * 1024 * 1024);
        struPlateResult.write();
        boolean bSet = hCNetSDK.NET_DVR_ManualSnap(lUserID, struManualParam, struPlateResult);
        if (bSet == false) {
            int iErr = hCNetSDK.NET_DVR_GetLastError();
            JOptionPane.showMessageDialog(null, "NET_DVR_ManualSnap：手动抓拍失败，错误码：" + iErr);
        } else {
            struPlateResult.read();
            JOptionPane.showMessageDialog(null, "手动抓拍成功!");
            if (struPlateResult.dwPicLen > 0) {
                SimpleDateFormat sf = new SimpleDateFormat("yyyyMMddHHmmss");
                String newName = sf.format(new Date());
                FileOutputStream fout;
                try {
                    fout = new FileOutputStream("\\pic\\" + newName + "01.jpg");
                    //将字节写入文件
                    long offset = 0;
                    ByteBuffer buffers = struPlateResult.pBuffer1.getByteBuffer(offset, struPlateResult.dwPicLen);
                    byte[] bytes = new byte[struPlateResult.dwPicLen];
                    buffers.rewind();
                    buffers.get(bytes);
                    fout.write(bytes);
                    fout.close();
                } catch (FileNotFoundException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                } catch (IOException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }
            }
        }
    }

    //设置LED屏显示
    public void btnLEDDisplayCfg() throws UnsupportedEncodingException {
        HCNetSDK.NET_DVR_LEDDISPLAY_CFG struLEDDisplayCfg = new HCNetSDK.NET_DVR_LEDDISPLAY_CFG();
        struLEDDisplayCfg.read();
        struLEDDisplayCfg.dwSize = struLEDDisplayCfg.size();
        struLEDDisplayCfg.write();

        HCNetSDK.NET_DVR_STD_CONFIG struConfigParam = new HCNetSDK.NET_DVR_STD_CONFIG();
        struConfigParam.read();
        IntByReference dwChannel = new IntByReference(1);
        struConfigParam.lpCondBuffer = dwChannel.getPointer();
        struConfigParam.dwCondSize = 4;
        struConfigParam.lpInBuffer = null;
        struConfigParam.dwInSize = 0;
        struConfigParam.lpOutBuffer = struLEDDisplayCfg.getPointer();
        struConfigParam.dwOutSize = struLEDDisplayCfg.size();
        struConfigParam.byDataType = 0;
        struConfigParam.write();

        boolean bGet = hCNetSDK.NET_DVR_GetSTDConfig(lUserID, HCNetSDK.NET_DVR_GET_LEDDISPLAY_CFG, struConfigParam);
        if (bGet == false) {
            int iErr = hCNetSDK.NET_DVR_GetLastError();
            System.out.println("NET_DVR_GET_LEDDISPLAY_CFG：获取LED屏幕显示配置失败，错误码：" + iErr);
            return;
        } else {
            System.out.println("获取LED屏幕显示配置成功!");
        }

        struConfigParam.read();
        struLEDDisplayCfg.read();

        byte[] strLEDContent = "测试test".getBytes("GBK");
        for (int i = 0; i < 512; i++) {
            struLEDDisplayCfg.sDisplayInfo[i] = 0;
        }
        for (int i = 0; i < strLEDContent.length; i++) {
            struLEDDisplayCfg.sDisplayInfo[i] = strLEDContent[i];
        }
        struLEDDisplayCfg.byDisplayMode = 1; //显示方式：0- 左移，1- 右移，2- 立即显示
        struLEDDisplayCfg.bySpeedType = 1; //速度类型：0- 快，1- 中，2- 慢
        struLEDDisplayCfg.dwShowTime = 10; //显示时长，取值范围：1~60，单位：秒
        struLEDDisplayCfg.write();

        struConfigParam.lpInBuffer = struLEDDisplayCfg.getPointer();
        struConfigParam.dwInSize = struLEDDisplayCfg.size();
        struConfigParam.lpOutBuffer = null;
        struConfigParam.dwOutSize = 0;
        struConfigParam.byDataType = 0;
        struConfigParam.write();

        boolean bSet = hCNetSDK.NET_DVR_SetSTDConfig(lUserID, HCNetSDK.NET_DVR_SET_LEDDISPLAY_CFG, struConfigParam);
        if (bSet == false) {
            int iErr = hCNetSDK.NET_DVR_GetLastError();
            System.out.println("NET_DVR_SET_VOICEBROADCAST_CFG：LED屏幕显示配置失败，错误码：" + iErr);
            return;
        } else {
            System.out.println("LED屏幕显示配置成功!");
            return;
        }
    }




  /*  public void setGateCfg()
    {
        int count=3;
//        HCNetSDK.NET_DVR_BARRIERGATE_COND.ByReference[] struGateCond=(HCNetSDK.NET_DVR_BARRIERGATE_COND[])new HCNetSDK.NET_DVR_BARRIERGATE_COND.ByReference().toArray(count);
        Pointer pdr=null;
        HCNetSDK.NET_DVR_ENTRANCE_CFG[]  struEntraCfg=(HCNetSDK.NET_DVR_ENTRANCE_CFG[])new HCNetSDK.NET_DVR_ENTRANCE_CFG(pdr).toArray(count);
//        HCNetSDK.NET_DVR_BARRIERGATE_COND.ByReference  struGateCond=new HCNetSDK.NET_DVR_BARRIERGATE_COND.ByReference();
//        HCNetSDK.NET_DVR_BARRIERGATE_COND[]  pstru=(HCNetSDK.NET_DVR_BARRIERGATE_COND[])struGateCond.toArray(count);
//        HCNetSDK.NET_DVR_BARRIERGATE_COND pstru=(HCNetSDK.NET_DVR_BARRIERGATE_COND)struGateCond;



//        Pointer pdr=new Memory(3*struGateCond[0].size());
        IntByReference pint=new IntByReference(0);


        boolean bSet3 = hCNetSDK.NET_DVR_GetDeviceConfig(lUserID,HCNetSDK.NET_DVR_GET_ENTRANCE_PARAMCFG,1,pdr,struGateCond.size(),pint.getPointer(),struEntraCfg.getPointer(),struEntraCfg.size());

        if (bSet3 == false) {
            int iErr = hCNetSDK.NET_DVR_GetLastError();
            System.out.println("NET_DVR_SET_CHARGE_ACCOUNTINFO：停车费用下发播报失败，错误码：" + iErr);
        } else {
            System.out.println("停车费用下发播报成功!");
        }*/


//        struGateCond[].read();
//        struGateCond.byLaneNo=1; //车道号
//        struGateCond.write();









}
