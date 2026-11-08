package Parmcfg;

import Commom.*;
import NetSDKDemo.*;
import com.sun.jna.Native;
import com.sun.jna.Pointer;

import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.nio.ByteBuffer;
import java.text.SimpleDateFormat;
import java.util.*;

/**
 * @create 2025-05-19-10:42
 */
public class TrafficDemo {
    static HCNetSDK hCNetSDK = null;
    static int lUserID = -1; //用户句柄
    private int lHandle = -1;
    static int iNum = 0;
    FRemoteCfgCallBackAlarmInfo radarAlarmInfoGet = null;

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
            hCNetSDK.NET_DVR_SetSDKInitCfg(3, ptrByteArray1.getPointer());

            System.arraycopy(strPath2.getBytes(), 0, ptrByteArray2.byValue, 0, strPath2.length());
            ptrByteArray2.write();
            hCNetSDK.NET_DVR_SetSDKInitCfg(4, ptrByteArray2.getPointer());

            String strPathCom = System.getProperty("user.dir") + "/lib/";
            HCNetSDK.NET_DVR_LOCAL_SDK_PATH struComPath = new HCNetSDK.NET_DVR_LOCAL_SDK_PATH();
            System.arraycopy(strPathCom.getBytes(), 0, struComPath.sPath, 0, strPathCom.length());
            struComPath.write();
            hCNetSDK.NET_DVR_SetSDKInitCfg(2, struComPath.getPointer());
        }

        //SDK初始化，一个程序进程只需要调用一次
        hCNetSDK.NET_DVR_Init();
        //启用SDK写日志
        hCNetSDK.NET_DVR_SetLogToFile(3, "./sdkLog", false);


        //登录设备，每一台设备只需要登录一次
        lUserID = TrafficDemo.login_V40("10.99.107.19", (short) 8000, "admin", "wjGcIl4I");


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
                    System.out.println("\n[Module]网络触发抓拍");
                    TrafficDemo.continuousShoot(lUserID, 1, 1);
                    break;
                }
                case "2":
                {
                    System.out.println("\n[Module]调用手动触发抓拍");
                    TrafficDemo.manualSnap(lUserID);
                    break;
                }
                case "3":
                {
                    System.out.println("\n[Module]雷视目标获取");
                    TrafficDemo trafficDemo = new TrafficDemo();
                    int iHanle = trafficDemo.StartRemoteConfig(lUserID);
                    try {
                        Thread.sleep(10000);
                    } catch (InterruptedException e) {
                        // TODO Auto-generated catch block
                        e.printStackTrace();
                    } //这里只是测试，实际开发如果需要一直接收数据，需要保持程序一直运行
                    //断开长连接
                    trafficDemo.StopRemoteConfig(iHanle);
                    break;
                }
                case "4":
                {
                    System.out.println("\n[Module]交通数据获取");
                    TrafficDemo.searchTrafficData(lUserID);
                    break;
                }
                default:
                {
                    System.out.println("\n未知的指令操作!请重新输入!\n");
                }
            }
        }

        //程序退出的时候调用注销登录接口，每一台设备分别调用一次
        if (hCNetSDK.NET_DVR_Logout(lUserID)) {
            System.out.println("注销成功");
        }

        //释放SDK资源，程序退出时调用，只需要调用一次
        hCNetSDK.NET_DVR_Cleanup();
        return;
    }

    /**
     * 设备登录V40 与V30功能一致
     *
     * @param ip   设备IP
     * @param port SDK端口，默认设备的8000端口
     * @param user 设备用户名
     * @param psw  设备密码
     */
    public static int login_V40(String ip, short port, String user, String psw) {
        //注册
        HCNetSDK.NET_DVR_USER_LOGIN_INFO m_strLoginInfo = new HCNetSDK.NET_DVR_USER_LOGIN_INFO();//设备登录信息
        HCNetSDK.NET_DVR_DEVICEINFO_V40 m_strDeviceInfo = new HCNetSDK.NET_DVR_DEVICEINFO_V40();//设备信息

        String m_sDeviceIP = ip;//设备ip地址
        m_strLoginInfo.sDeviceAddress = new byte[HCNetSDK.NET_DVR_DEV_ADDRESS_MAX_LEN];
        System.arraycopy(m_sDeviceIP.getBytes(), 0, m_strLoginInfo.sDeviceAddress, 0, m_sDeviceIP.length());

        String m_sUsername = user;//设备用户名
        m_strLoginInfo.sUserName = new byte[HCNetSDK.NET_DVR_LOGIN_USERNAME_MAX_LEN];
        System.arraycopy(m_sUsername.getBytes(), 0, m_strLoginInfo.sUserName, 0, m_sUsername.length());

        String m_sPassword = psw;//设备密码
        m_strLoginInfo.sPassword = new byte[HCNetSDK.NET_DVR_LOGIN_PASSWD_MAX_LEN];
        System.arraycopy(m_sPassword.getBytes(), 0, m_strLoginInfo.sPassword, 0, m_sPassword.length());

        m_strLoginInfo.wPort = port;
        m_strLoginInfo.bUseAsynLogin = false; //是否异步登录：0- 否，1- 是
        m_strLoginInfo.write();

        int iUserID = hCNetSDK.NET_DVR_Login_V40(m_strLoginInfo, m_strDeviceInfo);
        if (iUserID == -1) {
            System.out.println("登录失败，错误码为" + hCNetSDK.NET_DVR_GetLastError());
            return iUserID;
        } else {
            System.out.println(ip + ":设备登录成功！");
            return iUserID;
        }

    }

    public static void continuousShoot(int lUserId, int licenseId, int tailDelay) {
        HCNetSDK.NET_DVR_JPEGPARA netDvrJpegpara = new HCNetSDK.NET_DVR_JPEGPARA();
        netDvrJpegpara.read();
        netDvrJpegpara.wPicQuality = 0;
        netDvrJpegpara.wPicSize = 0xff; // 自动
        netDvrJpegpara.write();
        HCNetSDK.NET_DVR_SNAPCFG snapCfg = new HCNetSDK.NET_DVR_SNAPCFG();
        snapCfg.read();
        snapCfg.dwSize = snapCfg.size();
        snapCfg.byRelatedDriveWay = 0; // 关联车道号0
        snapCfg.bySnapTimes = 1; // 连拍次数
        snapCfg.wSnapWaitTime = (short) tailDelay; // 等待1秒
        snapCfg.wIntervalTime[0] = 200; // 间隔200ms
        snapCfg.dwSnapVehicleNum = licenseId;
        snapCfg.struJpegPara = netDvrJpegpara;
        Arrays.fill(snapCfg.byRes2, (byte) 0); // 保留字段置0
        snapCfg.write();
        // 调用连续抓拍
        boolean result = hCNetSDK.NET_DVR_ContinuousShoot(lUserId, snapCfg);
        if (!result) {
            System.out.println("车尾抓拍失败，错误码：" + hCNetSDK.NET_DVR_GetLastError());
        } else {
            System.out.println("车尾抓拍成功，车牌id: " + licenseId);
        }
    }

    public static void manualSnap(int lUserId) {
        HCNetSDK.NET_DVR_MANUALSNAP netDvrManualsnap = new HCNetSDK.NET_DVR_MANUALSNAP();
        netDvrManualsnap.read();
        netDvrManualsnap.byOSDEnable = 0;  // 抓拍图片上是否关闭OSD信息叠加：0- 不关闭(默认)，1- 关闭
        netDvrManualsnap.byLaneNo = 1; // 车道号，取值范围：1~6，默认为1
        netDvrManualsnap.write();
        HCNetSDK.NET_DVR_PLATE_RESULT netDvrPlateResult = new HCNetSDK.NET_DVR_PLATE_RESULT();

        // 调用手动触发抓拍
        boolean result = hCNetSDK.NET_DVR_ManualSnap(lUserId, netDvrManualsnap, netDvrPlateResult);
        if (!result) {
            System.out.println("手动触发抓拍失败，错误码：" + hCNetSDK.NET_DVR_GetLastError());
        } else {
            netDvrPlateResult.read();
            try {
                System.out.println("手动触发抓拍成功，识别结果车牌号:" + "" + new String(netDvrPlateResult.struPlateInfo.sLicense, "GBK").trim() + ", 类型: " + netDvrPlateResult.byResultType);
            } catch (UnsupportedEncodingException e) {
                e.printStackTrace();
            }
        }
    }


    public class FRemoteCfgCallBackAlarmInfo implements HCNetSDK.FRemoteConfigCallBack {
        public void invoke(int dwType, Pointer lpBuffer, int dwBufLen, Pointer pUserData) {
            System.out.println("长连接回调获取数据,NET_SDK_CALLBACK_TYPE_STATUS:" + dwType);
            switch (dwType) {
                case 0:// NET_SDK_CALLBACK_TYPE_STATUS
                    HCNetSDK.BYTE_ARRAY struCallbackStatus = new HCNetSDK.BYTE_ARRAY(4);
                    struCallbackStatus.write();
                    Pointer pStatus = struCallbackStatus.getPointer();
                    pStatus.write(0, lpBuffer.getByteArray(0, struCallbackStatus.size()), 0, 4);
                    struCallbackStatus.read();

                    int iStatus = 0;

                    for (int i = 0; i < 4; i++) {
                        int ioffset = i * 8;
                        int iByte = struCallbackStatus.byValue[i] & 0xff;
                        iStatus = iStatus + (iByte << ioffset);
                    }

                    switch (iStatus) {
                        case 1000:// NET_SDK_CALLBACK_STATUS_SUCCESS
                            System.out.println("获取成功并且结束, dwStatus:" + iStatus);
                            break;
                        case 1001:
                            System.out.println("正在获取中..., dwStatus:" + iStatus);
                            break;
                        case 1002:
                            System.out.println("获取失败, dwStatus:" + iStatus);
                            break;
                    }
                    break;
                case 2:// 获取状态数据
                    HCNetSDK.NET_DVR_ALARM_SEARCH_RESULT m_struRadarResult = new HCNetSDK.NET_DVR_ALARM_SEARCH_RESULT();
                    m_struRadarResult.write();
                    Pointer pStatusInfo = m_struRadarResult.getPointer();
                    pStatusInfo.write(0, lpBuffer.getByteArray(0, m_struRadarResult.size()), 0, m_struRadarResult.size());
                    m_struRadarResult.read();

                    System.out.println("查询到雷视目标信息, dwAlarmComm:0x" + Integer.toHexString(m_struRadarResult.dwAlarmComm)
                            + ",报警设备序列号:" + new String(m_struRadarResult.struAlarmer.sSerialNumber).trim()
                            + ",报警设备IP地址:" + new String(m_struRadarResult.struAlarmer.sDeviceIP).trim());

                    //雷视目标信息是JSON数据，需要解析JSON里面具体字段，这里直接将JSON保存到本地
                    if(m_struRadarResult.dwAlarmComm == 0x4993){
                        if ((m_struRadarResult.dwAlarmLen > 0) && (m_struRadarResult.pAlarmInfo != null)) {
                            SimpleDateFormat sf = new SimpleDateFormat("yyyyMMddHHmmss");
                            String newName = sf.format(new Date());
                            FileOutputStream fout;
                            try {
                                fout = new FileOutputStream(".\\out\\SaveFile\\" + newName + "_" + iNum + "_radarInfo.json");
                                //将字节写入文件
                                long offset = 0;
                                ByteBuffer buffers = m_struRadarResult.pAlarmInfo.getByteBuffer(offset, m_struRadarResult.dwAlarmLen);
                                byte[] bytes = new byte[m_struRadarResult.dwAlarmLen];
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
                            iNum++;
                        }
                    }
                    else if(m_struRadarResult.dwAlarmComm == 0x6009)
                    {
                        HCNetSDK.NET_DVR_ALARM_ISAPI_INFO m_struISAPIInfo = new HCNetSDK.NET_DVR_ALARM_ISAPI_INFO();
                        m_struISAPIInfo.write();
                        Pointer pISAPIInfo= m_struISAPIInfo.getPointer();
                        pISAPIInfo.write(0, m_struRadarResult.pAlarmInfo.getByteArray(0, m_struISAPIInfo.size()), 0, m_struISAPIInfo.size());
                        m_struISAPIInfo.read();

                        HCNetSDK.BYTE_ARRAY m_strISAPIData = new HCNetSDK.BYTE_ARRAY(m_struISAPIInfo.dwAlarmDataLen);
                        m_strISAPIData.write();
                        Pointer pPlateInfo = m_strISAPIData.getPointer();
                        pPlateInfo.write(0, m_struISAPIInfo.pAlarmData.getByteArray(0, m_strISAPIData.size()), 0, m_strISAPIData.size());
                        m_strISAPIData.read();
                        System.out.println(new String(m_strISAPIData.byValue).trim() +"\n");
                    }
                default:
                    break;
            }
        }
    }


    public int StartRemoteConfig(int lUserId) {
        HCNetSDK.NET_DVR_ALARM_SEARCH_COND struSearchCond = new HCNetSDK.NET_DVR_ALARM_SEARCH_COND();
        struSearchCond.dwSize = struSearchCond.size();
        struSearchCond.dwAlarmComm = 0x4993;//0x4993-智能检测报警(雷视目标检测报警)，0x1112-人脸识别结果，0x2902-人脸比对结果
        struSearchCond.wEventType = 2;//0-表示所有事件,1-混合目标检测（mixedTargetDetection）,2-雷视目标检测（radarVideoDetection）
        struSearchCond.wSubEventType = 0;//子事件类型，0-表示所有子事件
        struSearchCond.byNoBoundary = 1;//是否不带boundary，0-否，1-是，仅dwAlarmComm为智能检测报警时有效
        struSearchCond.write();

        //注意回调函数定义必须是全局的
        if (radarAlarmInfoGet == null) {
            radarAlarmInfoGet = new FRemoteCfgCallBackAlarmInfo();
        }

        lHandle = hCNetSDK.NET_DVR_StartRemoteConfig(lUserId, HCNetSDK.NET_DVR_GET_ALARM_INFO,
                struSearchCond.getPointer(), struSearchCond.size(), radarAlarmInfoGet, null);
        if (lHandle == -1) {
            System.out.println("建立获取雷视目标信息长连接失败，错误号:" + hCNetSDK.NET_DVR_GetLastError());
            return -1;
        }
        System.out.println("建立获取雷视目标信息长连接成功!");
        return lHandle;

    }

    public void StopRemoteConfig(int lVoiceHandle) {

        if (lHandle > -1) {
            hCNetSDK.NET_DVR_StopRemoteConfig(lHandle);
            System.out.println("断开获取雷视目标信息长连接");
        }
    }


    /**
     * 采用透传ISAPI协议方式查询交通数据
     */
    public static void searchTrafficData(int userID) {
        // 查询交通数据 URL
        String searchDataUrl = "POST /ISAPI/Traffic/ContentMgmt/dataOperation";

        // 构造起始查询参数
        Map<String, Object> parameter = new HashMap<>();

        // 一级字段
        parameter.put("operationType", "search");       //<!--req, enum, 操作类型, subType:string, [search#查询,deleteByID#根据ID删除,deleteByTime#根据时间删除], attr:opt{req, string, 取值范围}-->
        parameter.put("searchID", "CB3CA997-3A30-0001-64F9-5374CEBE1AA3");      //<!--req, string, 本次查询标识-->
        parameter.put("startTime", "2025-06-12T00:00:00Z");     //<!--req, datetime, 开始时间-->
        parameter.put("endTime", "2025-06-12T23:59:59Z");       //<!--req, datetime, 结束时间-->
        parameter.put("dataType", "0");     //<!--req, enum, 数据类型, subType:int, [0#卡口,1#电警,2#事件,3#取证,4#激光特征,5#非授权名单报警数据,6#人体属性,7#人脸属性（人脸抓拍）,8#渣土车,9#路面状态数据,10#能见度数据,11#气象状态数据,12#船舶航道或者航向角偏移检测,13#船舶卡口检测(Ship),14#道路异物检测(foreignObjectInRoadDetection),15#安全帽检测,16#升降梯超员检测,17#道闸开关闸数据,18#CID事件,19#雷达周界,20#火车,21#桥梁挠度异常事件(BridgeDeflectionAbnormalEvent),22#人脸比对(alarmResult),23#车辆OBU标签信息上报(vehicleOBUInfo),24#智慧城管(cityManagement),25#驾照考试监考员行为检测事件(InvigilatorBehaviorEvent),26#车位检测(PackingSpaceRecognition),27#道路养护(roadMaint),28#水质检测数据(waterQualityDetection),29#水尺水位检测事件(GaugeReadingEvent)], desc:dataType为1对应violationType违法类型(字典)dataType为2对应violationType事件类型(字典);dataType为3对应violationType取证类型(字典),12#船舶航道或者航向角偏移检测对应搜索数据为ShipChannelAbnormal-->
        /**
         * <!--req, string, 违法类型, dep:and,{$.DataOperation.searchCond.criteria.dataType,be,0},{$.DataOperation.searchCond.criteria.dataType,lt,8},
         * desc:对应索引(字典),支持多选（无该字段或-1：全部）
         * 若dataType为0，该字段值为0;（代表着dataType为卡口数据时，是不存在违法类型的。  因此violationType值强制性赋值为0）。
         * 若dataType为1可通过获取违法字典动态获取取值/ISAPI/ITC/illegalDictionary,若有多个,数字索引中间用逗号间隔;;
         * 若dataType为2时对应交通事件类型字典,输入为事件对应的字符串（如：abandonedObject，pedestrian等）,不是数字索引,若有多个,字符串中间用逗号间隔;
         * 若dataType为3时可通过获取违法字典动态获取取值/ISAPI/ITC/EvidenceDictionary,若有多个,数字索引中间用逗号间隔;
         * 若dataType为6,7时该字段不赋值;-->
         */
        parameter.put("violationType", "0");
        parameter.put("channel", "");       //<!--req, int, 通道, range:[1,12], desc:无该字段:全部-->
        parameter.put("plateType", "");     //<!--req, enum, 车牌类型, subType:int, [0#标准民用车与军车,1#02式民用车牌,2#武警车,3#警车,4#民用车双行尾牌,5#使馆车牌,6#农用车牌,7#摩托车牌,8#新能源车牌,255#其他]-->
        parameter.put("plateColor", "");    //<!--req, enum, 车牌颜色, subType:int, [0#蓝色,1#黄色,2#白色,3#黑色,4#绿色,5#民航黑色,6#民航绿色,7#红色,8#新能源绿色,9#新能源黄绿色,16#黄绿色,17#渐变绿色,255#其他]-->
        parameter.put("direction", "");     //<!--opt, enum, 监测点方向, subType:int, [1#上行,2#下行,3#双向,4#由东向西,5#由南向北,6#由西向东,7#由北向南,8#其他]-->
        parameter.put("trafficSurveyVehicleType", "");      //<!--ro, opt, enum, 交调车辆类型, subType:int, [0#未知,1#中小客车,2#大客车,3#小型货车,4#中型货车,5#大型货车,6#特大型货车,7#集装箱货车,8#摩托车,9#拖拉机]-->
        parameter.put("plate", "");     //<!--req, string, 车牌, range:[1,32]-->
        parameter.put("speedMin", "");      //<!--opt, int, 最小速度-->
        parameter.put("speedMax", "");      //<!--opt, int, 最大速度-->
        parameter.put("vehicleType", "");   //<!--opt, enum, 车辆大类, subType:string, [0#其它车型,1#小型车,2#大型车,3#行人触发,4#二轮车触发,5#三轮车触发]-->
        parameter.put("vehicleColor", "");  //<!--opt, enum, 车辆颜色, subType:int, [0#黑,1#白,2#银,3#灰,4#黑,5#红,6#深蓝,7#蓝,8#黄,9#绿,10#棕,11#粉,12#紫,13#深灰,14#青,15#橙,255#其他]-->
        parameter.put("laneNo", "");        //<!--opt, int, 车道号-->
        parameter.put("surveilType", "0");  //<!--req, enum, 监控类型, subType:int, [0#全部,1#授权名单数据,2#非授权名单数据]-->
        parameter.put("romoteHost", "");    //<!--req, int, 远程主机, range:[1,4], desc:无该字段：全部-->
        parameter.put("analysised", "true");    //<!--opt, bool, 分析状态, desc:false-未分析,true-已分析-->
        parameter.put("matchedResult", "");     //<!--opt, enum, 匹配结果, subType:string, [videoData#视频数据(没有匹配电子车牌或者OBU的卡口数据),RFData#单独的电子车牌数据,fuseData#卡口电子车牌融合数据(匹配到电子车牌的卡口数据),OBUFuseData#OBU融合数据(匹配到OBU信息的卡口数据)], dep:and,{$.DataOperation.searchCond.criteria.dataType,eq,0}, desc:当dataType=0卡口时，本参数有效，注意：当查询单独的电子车牌数据(ePlateResult)时，需要特殊处理，即dataType=0，matchedResult=RFData，其他的单独数据都通过当dataType区分，如dataType=23查询单独的OBU数据-->
        parameter.put("tollRoadVehicleSeries", "");     //<!--ro, opt, enum, 收费公路车辆系列, subType:int, [1#客车,2#货车,3#专项作业车], desc:按《JT-T 489-2019 收费公路车辆通行费车型分类》,需与tollRoadVehicleType组合使用-->
        parameter.put("tollRoadVehicleType", "");       //<!--ro, opt, enum, 收费公路车辆类型, subType:int, [1#1类,2#2类,3#3类,4#4类,5#5类,6#6类], desc:按《JT-T 489-2019 收费公路车辆通行费车型分类》,需与tollRoadVehicleSeries组合使用-->
        parameter.put("axleType", "");      //<!--req, enum, 国内车辆收费标准轴型, subType:int, [0#未知,11#2轴货车/2轴客车,12#2轴载货汽车/2轴客车,122#3轴中置轴挂车列车/3轴铰接列车/3轴客车,15#3轴载货汽车15型号,112#3轴载货汽车112型号/3轴客车,125#4轴中置轴挂车列车125型号/4轴铰接列车/4轴客车,152#4轴中置轴挂车列车152型号/4轴客车,1222#4轴全挂汽车列车/4轴客车,115#4轴载货汽车/4轴客车,155#5轴中置轴挂车列车155型号/5轴铰链列车155型号/5轴客车,1125#5轴中置轴挂车列车1125型号/5轴铰链列车1125型号/5轴客车,129#5轴铰链列车129型号/5轴客车,1152#5轴全挂汽车列车1522型号/5轴客车,11222#5轴全挂汽车列车11222型号/5轴客车,159#6轴中置轴挂车列车159型号/6轴中置轴挂车列车159-2型号/6轴铰链列车159-3型号/6轴铰链列车159-4型号/6轴客车,1155#6轴中置轴挂车列车1155-1型号/6轴中置轴挂车列车1155-2型号/6轴客车,1129#6轴铰链列车1129型号/6轴客车,11522#6轴全挂车11522-1型号/6轴全挂车11522-2型号/6轴客车]-->
        parameter.put("dangmark", "all");   //<!--opt, enum, 危险品车, subType:string, [unknown#未知,yes#是,no#否,all#全部]-->
        parameter.put("sendFlag", "");      //<!--req, enum, 发送标识, subType:string, [0#尚未发送,1#发送成功,2#无需发送], desc:无该字段：全部-->
        parameter.put("searchResultPosition", "0");     //<!--req, int, 查询起始位置-->
        parameter.put("maxResults", "20");      //<!--req, int, 本次查询条数-->
        parameter.put("vehicleSubTypeList", "");    //<!--opt, array, 车辆类型查询条件列表, subType:object-->

        // 获取查询交通数据的请求报文
        String XmlInput = ConfigFileUtil.getReqBodyFromTemplate("/conf/trafficTerminal/TrafficDataParam.xml", parameter);
        System.out.println("查询交通数据报文：" + XmlInput);

        // 发起交通数据查询
        String result = TransIsapi.put_isapi(userID, searchDataUrl, XmlInput);
        System.out.println("查询交通数据结果:" + result);

        // 定义要提取的字段
        List<String> fields = Arrays.asList(
                "ctrl", "drive", "part", "fileNo", "startOffset", "picLen", "captureTime"
        );

        // 提取字段
        xmlParse.TrafficDataResult data = xmlParse.extractFields(result, 0, fields);

        System.out.println("searchID = " + data.searchID);
        for (String field : fields) {
            System.out.println(field + " = " + data.fields.get(field));
        }

        // ==== 图片信息查询部分 ====

        // 构造参数用于填充图片查询 XML 模板
        Map<String, Object> picRecParam = new HashMap<>();
        picRecParam.put("searchID", data.searchID.replaceAll("^\\{|\\}$", ""));
        picRecParam.put("vehicleID", UUID.randomUUID().toString().toUpperCase());
        for (String field : fields) {
            picRecParam.put(field, data.fields.get(field));
        }

        // 读取图片查询 XML 模板并替换参数
        String picRecXml = ConfigFileUtil.getReqBodyFromTemplate("/conf/trafficTerminal/picRecParam.xml", picRecParam);
        System.out.println("查询交通数据图片报文：" + picRecXml);

        // 发起图片请求
        String picRecUrl = "POST /ISAPI/Traffic/ContentMgmt/picRecInfo";
        String picRecResult = TransIsapi.put_isapi(userID, picRecUrl, picRecXml);
        System.out.println("查询交通数据图片结果:" + picRecResult);
    }
}


