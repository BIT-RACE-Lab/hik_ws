package Parmcfg;

import Commom.osSelect;
import NetSDKDemo.HCNetSDK;
import com.sun.jna.Native;
import com.sun.jna.NativeLong;
import com.sun.jna.Pointer;
import com.sun.jna.ptr.IntByReference;
import sun.misc.IOUtils;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Scanner;

/**
 * @create 2020-07-27-10:42
 */
public class TestDemo {
    static HCNetSDK hCNetSDK = null;
    static int lUserID = -1; //用户句柄
    public static FExceptionCallBack_Imp fExceptionCallBack;

    static class FExceptionCallBack_Imp implements HCNetSDK.FExceptionCallBack {
        public void invoke(int dwType, int lUserID, int lHandle, Pointer pUser) {
            System.out.println("异常事件类型:" + dwType);
            return;
        }
    }

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
                        //win系统加载SDK库路径
                        strDllPath = System.getProperty("user.dir") + "\\lib\\HCNetSDK.dll";

                    else if (osSelect.isLinux())
                        //Linux系统加载SDK库路径
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

    public static void main(String[] args) throws IOException, InterruptedException {
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
        
        //SDK初始化，一个程序进程只需要调用一次
        hCNetSDK.NET_DVR_Init();
        
        if (fExceptionCallBack == null) {
            fExceptionCallBack = new FExceptionCallBack_Imp();
        }
        Pointer pUser = null;
        if (!hCNetSDK.NET_DVR_SetExceptionCallBack_V30(0, 0, fExceptionCallBack, pUser)) {
            return;
        }
        System.out.println("设置异常消息回调成功");

        //启用SDK写日志
        hCNetSDK.NET_DVR_SetLogToFile(3, "./sdkLog", false);


        //登录设备，每一台设备只需要登录一次
        lUserID = TestDemo.loginDevice("10.9.137.21", (short) 8000, "admin", "");

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
                    System.out.println("\n[Module]手动获取设备在线状态");
                    DevManager.getDeviceStatus(lUserID);
                    break;
                }
                case "2":
                {
                    System.out.println("\n[Module]获取设备工作状态代码");
                    DevManager.getWorkS(lUserID);
                    break;
                }
                case "3":
                {
                    System.out.println("\n[Module]获取设备基本信息");
                    DevManager.getDeviceInfo(lUserID);
                    break;
                }

                case "4":
                {

                    System.out.println("\n[Module]设备抓图代码");
                    ChannelParamCfg.CaptureJPEGPicture(lUserID);
                    break;
                }
                case "5":
                {
                    //适用NVR等硬盘录像机设备
                    System.out.println("\n[Module]查询设备通道状态代码");
                    ChannelParamCfg.GetIPChannelInfo(lUserID);
                    break;
                }
                case "6":
                {
                    //获取和设置前端扩展参数
                    System.out.println("\n[Module]获取和设置前端扩展参数");
                    ChannelParamCfg.GetCameraPara(lUserID);
                    break;
                }
                case "7":
                {
                    //获取和设置网络参数
                    System.out.println("\n[Module]获取和设置网络参数");
                    ChannelParamCfg.GetNetCfg(lUserID);
                    break;
                }
                case "8":
                {
                    //获取和设置录像参数
                    System.out.println("\n[Module]获取和设置录像参数");
                    ChannelParamCfg.GetRecordCfg(lUserID);
                    break;
                }
                case "9":
                {
                    //获取和设置图像参数
                    System.out.println("\n[Module]获取和设置图像参数");
                    ChannelParamCfg.GetandSetPicCfg(lUserID);
                    break;
                }
                case "10":
                {
                    //获取和设置时间参数
                    System.out.println("\n[Module]获取和设置时间参数");
                    SdkSysCfg.GetandSetDevTime(lUserID);
                    break;
                }
                case "11":
                {
                    //获取设备软硬件能力信息
                    System.out.println("\n[Module]获取设备软硬件能力");
                    DevManager.GetSofthardware_Ability(lUserID);
                    break;
                }
                case "12":
                {
                    //获取设备JPEG抓图能力
                    System.out.println("\n[Module]获取设备JPEG抓图能力");
                    DevManager.GetJPEG_Cap_Ability(lUserID);
                    break;
                }
                case "13":
                {
                    //日志查找
                    System.out.println("\n[Module]日志查找");
                    DevManager.FindLog(lUserID);
                    break;
                }
                default:
                {
                    System.out.println("\n未知的指令操作!请重新输入!\n");
                }
            }
        }


        Thread.sleep(2000);
        //程序退出的时候调用注销登录接口，每一台设备分别调用一次
        if (hCNetSDK.NET_DVR_Logout(lUserID)) {
            System.out.println("注销成功");
        }
        
        //释放SDK资源，程序退出时调用，只需要调用一次
        hCNetSDK.NET_DVR_Cleanup();
        return;       
    }

    /**
     * 设备登录V30
     *
     * @param ip   设备IP
     * @param port SDK端口，默认设备的8000端口
     * @param user 设备用户名
     * @param psw  设备密码
     */
    public static int login_V30(String ip, short port, String user, String psw) {
        HCNetSDK.NET_DVR_DEVICEINFO_V30 m_strDeviceInfo = new HCNetSDK.NET_DVR_DEVICEINFO_V30();
        int iUserID = hCNetSDK.NET_DVR_Login_V30(ip, port, user, psw, m_strDeviceInfo);
        System.out.println("UserID:" + lUserID);
        if ((iUserID == -1) || (iUserID == 0xFFFFFFFF)) {
            System.out.println("登录失败，错误码为" + hCNetSDK.NET_DVR_GetLastError());
            return iUserID;
        } else {
            System.out.println(ip + ":设备登录成功！");
            return iUserID;
        }
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




























}


