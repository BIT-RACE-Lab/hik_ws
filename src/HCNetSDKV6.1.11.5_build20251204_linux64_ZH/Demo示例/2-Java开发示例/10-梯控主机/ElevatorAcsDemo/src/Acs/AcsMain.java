package Acs;

import Commom.osSelect;
import NetSDKDemo.HCNetSDK;
import com.sun.jna.Native;
import org.json.JSONException;

import java.io.UnsupportedEncodingException;
import java.util.Scanner;

/**
 *梯控主机Demo示例
 */
public class AcsMain {
    static HCNetSDK hCNetSDK = null;
    static int lUserID = -1;//用户句柄
    static int iCharEncodeType = 0;  //设备字符集
    /**
     * 根据不同操作系统选择不同的库文件和库路径
     *
     * @return
     */
    private static boolean createSDKInstance() {
        if (hCNetSDK == null) {
            synchronized (HCNetSDK.class) {
                String strDllPath = "";
                try {
                    //System.setProperty("jna.debug_load", "true");
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

    /**
     * @param args
     * @throws UnsupportedEncodingException
     * @throws InterruptedException
     */
    public static void main(String[] args) throws UnsupportedEncodingException, InterruptedException, JSONException {
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
        //SDK初始化，和进程保持同步，仅需要调用一次
        hCNetSDK.NET_DVR_Init();
        //开启SDK日志打印
        hCNetSDK.NET_DVR_SetLogToFile(3, "./sdklog", false);
        //设备登录
        lUserID = loginDevice("10.10.138.203", (short) 8000, "admin", "hik12345");    //登陆设备

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
                case "1": {
                    System.out.println("\n[Module]获取梯控主机参数示例代码");
                    ACSManage.acsCfg(lUserID);
                    break;
                }
                case "2": {
                    System.out.println("\n[Module]获取梯控主机状态示例代码");
                    ACSManage.getAcsStatus(lUserID);
                    break;
                }
                case "3": {
                    System.out.println("\n[Module]远程梯控示例代码");
                    DoorManage.controlGateway(lUserID,1,0);
                    break;
                }
                case "4": {
                    System.out.println("\n[Module]下发卡号示例代码");
                    CardManage.setOneCard(lUserID, "123456", (short) 1);
                    break;
                }
                case "5": {
                    System.out.println("\n[Module]查询卡号示例代码");
                    CardManage.getOneCard(lUserID, "123456");
                    break;
                }
                case "6": {
                    System.out.println("\n[Module]查询所有卡号示例代码");
                    CardManage.getAllCard(lUserID);
                    break;
                }
                case "7": {
                    System.out.println("\n[Module]删除卡号代码");
                    CardManage.delOneCard(lUserID, "123456");
                    break;
                }
                case "8": {
                    //
                    System.out.println("\n[Module]删除所有卡号代码");
                    CardManage.cleanCardInfo(lUserID);
                    break;
                }
                case "9": {
                    System.out.println("\n[Module]设置卡计划模板代码");
                    CardManage.setCardTemplate(lUserID,2);
                    break;
                }
                case "10":{
                    System.out.println("\n[Module]获取与设置楼层参数\"");
                    DoorManage.GetAndSetFloorCfg(lUserID,1);
                    break;
                }

                case "11": {
                    System.out.println("\n[Module]门禁历史事件查询代码");
                    EventSearch.searchAllEvent(lUserID);
                    break;
                }
                case "12": {
                    System.out.println("\n[Module]设置梯控计划模板代码");
                    DoorManage.doorTemplate(lUserID,1,1);
                    break;
                }
                default: {
                    System.out.println("\n未知的指令操作!请重新输入!\n");
                }
            }
        }

            /**登出操作*/
            AcsMain.logout();
            //释放SDK，程序退出前调用
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
    public static int loginDevice (String ip,short port, String user, String psw){
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
            deviceInfo.read();
            //获取设备字符编码格式
            iCharEncodeType = deviceInfo.byCharEncodeType;
        }
        return userID; // 返回登录结果
    }

        /**
         * 登出操作
         *
         */
        public static void logout () {

            /**设备登出*/
            if (lUserID >= 0) {
                hCNetSDK.NET_DVR_Logout(lUserID);
            }

        }


    }

