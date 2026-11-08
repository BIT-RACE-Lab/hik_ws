package com.hik;


import CommonMethod.ConfigFileUtil;
import NetSDKDemo.HCNetSDK;
import com.sun.jna.Pointer;
import org.dom4j.Document;
import org.dom4j.DocumentHelper;
import org.dom4j.Element;
import sun.nio.cs.ext.MacHebrew;

import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

/**
 * @author jiangxin
 * @create 2021-04-20-15:44
 * 车辆黑白名单管理，功能:黑白名单的上传、删除
 *
 */
public class VechileListManage {

    static FVehicleCrtlCB fVehicleCrtlCB = null;
    static int iStatus = 0;
        //车辆授权名单下发
        public static void addVechileList(int lUserID) throws Exception {
            if (fVehicleCrtlCB == null)
            {
                fVehicleCrtlCB = new FVehicleCrtlCB();
            }
            int lHandle = ITCMain.hCNetSDK.NET_DVR_StartRemoteConfig(lUserID, HCNetSDK.NET_DVR_VEHICLELIST_CTRL_START, null, 0, fVehicleCrtlCB, Pointer.NULL);
            if (lHandle <= -1) {

                System.out.println("NET_DVR_StartRemoteConfig failed errorCode:" + ITCMain.hCNetSDK.NET_DVR_GetLastError());
                return;
            }
                HCNetSDK.NET_DVR_VEHICLE_CONTROL_LIST_INFO struVehicleControl = new HCNetSDK.NET_DVR_VEHICLE_CONTROL_LIST_INFO();
                struVehicleControl.read();
                struVehicleControl.dwSize = struVehicleControl.size();
                struVehicleControl.dwChannel = 1; //通道号，出入口抓拍机，一体机默认1
                String sLicense = "浙A12345";    //车牌号码
                struVehicleControl.sLicense = sLicense.getBytes("GBK"); //车牌号码
                struVehicleControl.byListType = 0; //名单属性：0- 授权名单，1- 非授权名单
                struVehicleControl.byPlateType = 0; //0- 标准民用车与军车车牌  //参考SDK使用手册中车牌类型枚举类型
                /**
                 * VCA_BLUE_PLATE
                 * 0- 蓝色车牌
                 * VCA_YELLOW_PLATE
                 * 1- 黄色车牌
                 * VCA_WHITE_PLATE
                 * 2- 白色车牌
                 * VCA_BLACK_PLATE
                 * 3- 黑色车牌
                 * VCA_GREEN_PLATE
                 * 4- 绿色车牌
                 * VCA_BKAIR_PLATE
                 * 5- 民航黑色车牌
                 * VCA_OTHER = 0xff
                 * 0xff- 其他
                 */
                struVehicleControl.byPlateColor = 0; //车牌颜色
                //有效开始时间
                struVehicleControl.struStartTime.wYear = (short) 2024;
                struVehicleControl.struStartTime.byMonth = (byte) 01;
                struVehicleControl.struStartTime.byDay = (byte) 01;
                struVehicleControl.struStartTime.byHour = (byte) 00;
                struVehicleControl.struStartTime.byMinute = (byte) 00;
                struVehicleControl.struStartTime.bySecond = (byte) 00;
                //有效结束时间
                struVehicleControl.struStopTime.wYear = (short) 2028;
                struVehicleControl.struStopTime.byMonth = (byte) 12;
                struVehicleControl.struStopTime.byDay = (byte) 30;
                struVehicleControl.struStopTime.byHour = (byte) 23;
                struVehicleControl.struStopTime.byMinute = (byte) 59;
                struVehicleControl.struStopTime.bySecond = (byte) 59;
                struVehicleControl.write();
                boolean bSend = ITCMain.hCNetSDK.NET_DVR_SendRemoteConfig(lHandle, HCNetSDK.ENUM_SENDDATA, struVehicleControl.getPointer(), struVehicleControl.size());
                if (!bSend) {
                    System.err.println("NET_DVR_SendRemoteConfig失败，错误码：" + ITCMain.hCNetSDK.NET_DVR_GetLastError());
                    //关闭下发长连接
                    ITCMain.hCNetSDK.NET_DVR_StopRemoteConfig(lHandle);
                }
                /**
                 * 循环下发车牌名单，继续调用NET_DVR_SendRemoteConfig下发下一张车牌名单
                 */
            // 循环判断下发状态
            while (true) {
                if (iStatus == 1000 || iStatus == 1002) {
                    // 调用方法关闭长连接
                    boolean b_StopHandle = ITCMain.hCNetSDK.NET_DVR_StopRemoteConfig(lHandle);
                    if (b_StopHandle) {
                        System.out.println("长连接已关闭");
                    } else {
                        System.out.println("关闭长连接失败 errorCode:"+ + ITCMain.hCNetSDK.NET_DVR_GetLastError());
                    }
                    break; // 退出循环
                }
            }
        }

    //下发车牌授权名单状态回调函数
    static class FVehicleCrtlCB implements HCNetSDK.FRemoteConfigCallBack {
        public void invoke(int dwType, Pointer lpBuffer, int dwBufLen, Pointer pUserData) {
            switch (dwType) {
                case HCNetSDK.NET_SDK_CALLBACK_TYPE_STATUS:
                    HCNetSDK.BYTE_ARRAY struCallbackStatus = new HCNetSDK.BYTE_ARRAY(40);
                    struCallbackStatus.write();
                    Pointer pStatus = struCallbackStatus.getPointer();
                    pStatus.write(0, lpBuffer.getByteArray(0, struCallbackStatus.size()), 0, dwBufLen);
                    struCallbackStatus.read();

                    for (int i = 0; i < 4; i++) {
                        int ioffset = i * 8;
                        int iByte = struCallbackStatus.byValue[i] & 0xff;
                        iStatus = iStatus + (iByte << ioffset);
                    }
                    switch (iStatus) {
                        case HCNetSDK.NET_SDK_CALLBACK_STATUS_SUCCESS:// NET_SDK_CALLBACK_STATUS_SUCCESS
                        {
                            System.out.println("下发成功");
                            //增加消息事件，查询成功之后调用NET_DVR_StopRemoteConfig释放资源
                            break;
                        }

                        case HCNetSDK.NET_SDK_CALLBACK_STATUS_PROCESSING:
                        {
                            System.out.println("下发中...");
                            break;
                        }

                        case HCNetSDK.NET_SDK_CALLBACK_STATUS_FAILED:
                        {
                            System.out.println("下发失败,错误码： dwStatus:" + iStatus);
                            //增加消息事件，查询失败之后调用NET_DVR_StopRemoteConfig释放资源
                            break;
                        }
                    }
                    break;
                default:
                    break;
            }
        }
    }

    /**
     * 查询车牌授权/非授权名单
     * @param lUserID
     */
    public static void searchVechileList(int lUserID)
    {
        String searchVechileListUrl = "POST /ISAPI/Traffic/channels/1/searchLPListAudit";
        //输入参数，XML或者JSON数据,查询多条人员信息json报文
        Map<String, Object> parameter = new HashMap<>();
        parameter.put("searchID", UUID.randomUUID()); // 查询id
        parameter.put("maxResults", 30); // 最大查询数量
        String strInbuff = ConfigFileUtil.getReqBodyFromTemplate("/conf/ITC/searchVechileList.xml", parameter);
        System.out.println("查询的json报文:" + strInbuff);
        String responseString = ISAPI.stdXMLConfig(lUserID,searchVechileListUrl,strInbuff);
        System.out.println("查询返回报文："+responseString);
        return;
    }

    /**
     * 删除车辆授权/非授权名单
     * @param lUserID
     */
    public static void deleteVechileList(int lUserID)
    {
        String deleteVechileListUrl = "PUT /ISAPI/Traffic/channels/1/DelLicensePlateAuditData?format=json";
        //输入参数，XML或者JSON数据
        Map<String, Object> parameter = new HashMap<>();
        parameter.put("plateColor","yellow"); // 查询id
        parameter.put("licensePlate", "京AA12345"); // 最大查询数量
        String strInbuff = ConfigFileUtil.getReqBodyFromTemplate("/conf/ITC/DeleteVechileList.json", parameter);
        System.out.println("删除车牌输入报文:" + strInbuff);
        String responseString = ISAPI.stdXMLConfig(lUserID,deleteVechileListUrl,strInbuff);
        System.out.println("删除车牌返回报文："+responseString);
        return;
    }






    /**
     * 删除车牌授权名单接口，目前设备版本已经已经不使用此接口
     * @param lUserID
     * @param xmlInput
     */
    public void deleteVechileList_old(int lUserID,String xmlInput)
    {

        ISAPI.stdXMLConfig(lUserID,"DELETE /ISAPI/ITC/Entrance/VCL",xmlInput);

    }

    /**
     * 查询车牌授权名单接口，目前设备版本已经已经不使用此接口
     * @param lUserID
     * @param xmlInput
     */
    public void getVechileList(int lUserID,String xmlInput)
    {

        //获取查询车牌授权名单URL: POST /ISAPI/ITC/Entrance/VCL
        ISAPI.stdXMLConfig(lUserID,"POST /ISAPI/ITC/Entrance/VCL",xmlInput);

    }

    //  删除车牌授权名单输入报文
    public  String deleteXml()
    {
        Document document1;
        Element root = DocumentHelper.createElement("VCLDelCond");
        document1 = DocumentHelper.createDocument(root);
        Element delVCLCond = root.addElement("delVCLCond");
        delVCLCond.setText("1");
        Element plateNum = root.addElement("plateNum"); //车牌号
        plateNum.setText("皖A88888");
        Element plateColor = root.addElement("plateColor"); //车牌颜色
        plateColor.setText("0");
        Element plateType = root.addElement("plateType");  //车牌类型
        plateType.setText("0");
        Element cardNo = root.addElement("cardNo");  //卡号
        cardNo.setText("0");
        String requestXml = document1.asXML();
        return requestXml;
    }

    //查询车牌授权名单输入报文
    public String getXml()
    {
        Document document1;
        Element root = DocumentHelper.createElement("VCLDelCond");
        document1 = DocumentHelper.createDocument(root);
        Element getVCLNum = root.addElement("getVCLNum"); // 指定获取名单最大数量：由控件指定获取多少条数据
        getVCLNum.setText("10");
        Element startOffSet = root.addElement("startOffSet");  //指定名单搜索起始点
        startOffSet.setText("0");
        Element getVCLCond = root.addElement("getVCLCond");  //获取名单条件：0-全部，1-车牌号码，2-卡号，3-名单类型
        getVCLCond.setText("1");
        Element plateNum = root.addElement("plateNum"); //车牌号
        plateNum.setText("皖A88888");
        Element plateType = root.addElement("plateType");  //车牌类型  名单类型：0-授权名单，1-非授权
        plateType.setText("0");
        Element cardNo = root.addElement("cardNo");  //卡号
        cardNo.setText("0");
        String requestXml = document1.asXML();
        return requestXml;


    }
}
