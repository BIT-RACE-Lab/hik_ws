package com.hik;

import CommonMethod.ConfigFileUtil;
import com.sun.scenario.effect.impl.sw.sse.SSEBlend_SRC_OUTPeer;

import java.util.HashMap;
import java.util.Map;

/**
 * LCD屏显示控制
 * @Author: jiangxin14
 * @Date: 2024-08-23  16:09
 */
public class LCDdisplayManage {

    /**
     * 设置相机控制模式LCD字符显示,包含过车和空闲两种场景
     * 相机控制： 相机控制（设备自动控制）：设备自行识别黑、授权名单以及临时车牌，并根据displayPassingVehicleInfoEnabled、allowListDisplayEnabled、blockListDisplayEnabled、temporaryListDisplayEnabled中所配置的策略，自动显示过车信息。
     */
     public static void setCameractrlModeLCDdisplayInfo(int lUserID)
     {
         String CameractrlModeLCDdisplayInfoUrl = "PUT /ISAPI/Parking/channels/1/LCD?format=json&powerOffSaveEnabled=true";
         /**
          * 相机控制模式下LCD显示效果，通过调整CameractrlModeLCDdisplayInfo.json 中参数进行修改，Demo示例中仅作为演示效果示例
          */
         Map<String, Object> parameter = new HashMap<>();
         parameter.put("ctrlMode","camera"); //设置为相机控制模式
         parameter.put("content","测试显示内容1"); //设置空闲模式下显示文本内容
         String strInbuff = ConfigFileUtil.getReqBodyFromTemplate("/conf/ITC/CameractrlModeLCDdisplayInfo.json", parameter);
        System.out.println("设置相机控制模式输入报文:" + strInbuff);
         String responseString = ISAPI.stdXMLConfig(lUserID,CameractrlModeLCDdisplayInfoUrl,strInbuff);
        System.out.println("设置相机控制模式下LCD显示报返回报文："+responseString);
        return;
     }

    /**
     * 获取当前LCD参数
     * @param lUserID
     */
    public static void getctrlModeLCDdisplayInfo(int lUserID)
     {
         String getLCDdisplayInfoUrl = "GET /ISAPI/Parking/channels/1/LCD?format=json";
         String responseString = ISAPI.stdXMLConfig(lUserID,getLCDdisplayInfoUrl,"");
         System.out.println("获取LCD参数返回报文:"+ responseString);
     }


    /**
     * 设置平台控制模式LCD参数显示
     * 平台控制模式： 平台控制（手动控制）：完全由用户下发CustomContentList内容来显示，该模式displayPassingVehicleInfoEnabled、
     * allowListDisplayEnabled、blockListDisplayEnabled、temporaryListDisplayEnabled中所配置的自动控制策略将不生效。
     * 此接口可以设置平台控制模式下字体大小，颜色等参数，/ISAPI/System/LCDScreen/displayInfo?format=json接口仅负责下发内容参数
     * @param lUserID
     */
     public static void setplatformctrlModeLCDdisplayInfo(int lUserID)
     {
         String platformctrlModeLCDdisplayInfoUrl = "PUT /ISAPI/Parking/channels/1/LCD?format=json&powerOffSaveEnabled=true";
         /**
          * 平台控制模式下LCD显示效果，可以调用POST /ISAPI/System/LCDScreen/displayInfo?format=json接口根据场景自定义下发内容
          */
         Map<String, Object> parameter = new HashMap<>();
         parameter.put("ctrlMode","platform"); //设置为平台控制模式
         parameter.put("content","测试显示内容1"); //设置空闲模式下显示文本内容
         String strInbuff = ConfigFileUtil.getReqBodyFromTemplate("/conf/ITC/CameractrlModeLCDdisplayInfo.json", parameter);
         System.out.println("设置平台控制模式输入报文:" + strInbuff);
         String responseString = ISAPI.stdXMLConfig(lUserID,platformctrlModeLCDdisplayInfoUrl,strInbuff);
         System.out.println("设置平台控制模式下LCD显示报返回报文："+responseString);
         return;
     }

    /**
     * 设置LCD图片显示，一般用于二维码图片显示，通常适用2#入场无车牌,4#出场有车牌未付费两种场景、5-出场无车牌三种场景
     * @param lUserID
     */
    public static void setPicDisplayEnterNolicense(int lUserID)
     {
         String setPicDisplayUrl = "POST /ISAPI/System/LCDScreen/displayInfo?format=json";
         /**
          *
          */
         Map<String, Object> parameter = new HashMap<>();
         parameter.put("QRCodeBase64","iVBORw0KGgoAAAANSUhEUgAAAPoAAAD6CAIAAAAHjs1qAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAEKElEQVR4nO3dwW7bMBQAwb" +
                 "rw//9yeumZCsKyJL0z1yC2oix4eXjS69fH+fr6WvTJr9fruu9d97s3+r37AuD/kTshcidE7oTInRC5EyJ3QuROiNwJeY9/vG5SOGPdtG/d3HTXhHLdf/DGN" +
                 "pzuhMidELkTIndC5E6I3AmROyFyJ0TuhDxMVcfWTQpv3Pscu3EiO+PMNpzuhMidELkTIndC5E6I3AmROyFyJ0TuhExNVT/PupnrzCefOeu9kdOdELkTIndC5" +
                 "E6I3AmROyFyJ0TuhMidEFPVf2bd7PPGXdUzOd0JkTshcidE7oTInRC5EyJ3QuROiNwJmZqq1jYdz9w3PdOZbTjdCZE7IXInRO6EyJ0QuRMid0LkTojcCXmYqn" +
                 "7etG9s177pzPfumtfe2IbTnRC5EyJ3QuROiNwJkTshcidE7oTInZD3mTuFu6ybFN54n2+85jGnOyFyJ0TuhMidELkTIndC5E6I3AmROyEPQ8Qbn1s7Mws8c6N" +
                 "03e+Ofd7/1+lOiNwJkTshcidE7oTInRC5EyJ3QuROyMKx2Zmbjru2UW+cfa6bqa9rY3xVTndC5E6I3AmROyFyJ0TuhMidELkTIndCpnZVHz76wjnijF17vbvu5" +
                 "I3bt053QuROiNwJkTshcidE7oTInRC5EyJ3Ql5nbljeOHPddSfHztwo3cXpTojcCZE7IXInRO6EyJ0QuRMid0LkTsi2XdV1Pu+5tbu2QndZd81Od0LkTojcCZE" +
                 "7IXInRO6EyJ0QuRMid0Kmpqo3Pj92rDY3vfGpxTOc7oTInRC5EyJ3QuROiNwJkTshcidE7oS8d1/AT+x6mu6MM+eXu+biY+vuhtOdELkTIndC5E6I3AmROyFyJ" +
                 "0TuhMidkIW7qrWN0plPHjtzTryLJwDDt8idELkTIndC5E6I3AmROyFyJ0TuhCx8r+rDF8feunrmG0zPtG567XQnRO6EyJ0QuRMid0LkTojcCZE7IXIn5FXbg7zx6" +
                 "cE3vt901302VYW/5E6I3AmROyFyJ0TuhMidELkTIndC3p+3Qzme2O16iu+NzpyMznC6EyJ3QuROiNwJkTshcidE7oTInRC5E/Ie//jzdjd3TQp33ckz3+e667/gd" +
                 "CdE7oTInRC5EyJ3QuROiNwJkTshcifkYao6duOTacfW/UUzc8R1M8ja9q3TnRC5EyJ3QuROiNwJkTshcidE7oTInZCpqWrNrvnlzMx1xrq/d9eddLoTIndC5E6I3A" +
                 "mROyFyJ0TuhMidELkTYqp6hF3P6T1zV3XdXq/TnRC5EyJ3QuROiNwJkTshcidE7oTInZCHodqN71V1zd//3jOtex6y050QuRMid0LkTojcCZE7IXInRO6EyJ2Q+0Z" +
                 "uj3a9o3SdM9/Jus66SbDTnRC5EyJ3QuROiNwJkTshcidE7oTInZA/2q1JFatAjGUAAAAASUVORK5CYII="); //图片BASE64编码
         parameter.put("sence",2); //设置场景模式，2-入场无车牌
         parameter.put("license","无车牌"); //
         parameter.put("amounts",0); //金额随意下发，此场景不显示
         parameter.put("notice","无牌车请扫码"); //通知信息
         String strInbuff = ConfigFileUtil.getReqBodyFromTemplate("/conf/ITC/PicDisPlayInfo.json", parameter);
         System.out.println("设置图片显示输入报文:" + strInbuff);
         String responseString = ISAPI.stdXMLConfig(lUserID,setPicDisplayUrl,strInbuff);
         System.out.println("设置图片显示返回报文："+responseString);
         return;



     }


    /**
     * 设置LCD图片显示，一般用于二维码图片显示，通常适用2#入场无车牌,4#出场有车牌未付费两种场景、5-出场无车牌三种场景
     * @param lUserID
     */
    public static void setPicDisplayExitNoPay(int lUserID)
    {
        String setPicDisplayUrl = "POST /ISAPI/System/LCDScreen/displayInfo?format=json";
        /**
         *
         */
        Map<String, Object> parameter = new HashMap<>();
        parameter.put("QRCodeBase64","iVBORw0KGgoAAAANSUhEUgAAAPoAAAD6CAIAAAAHjs1qAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAEKElEQVR4nO3dwW7bMBQAwb" +
                "rw//9yeumZCsKyJL0z1yC2oix4eXjS69fH+fr6WvTJr9fruu9d97s3+r37AuD/kTshcidE7oTInRC5EyJ3QuROiNwJeY9/vG5SOGPdtG/d3HTXhHLdf/DGN" +
                "pzuhMidELkTIndC5E6I3AmROyFyJ0TuhDxMVcfWTQpv3Pscu3EiO+PMNpzuhMidELkTIndC5E6I3AmROyFyJ0TuhExNVT/PupnrzCefOeu9kdOdELkTIndC5" +
                "E6I3AmROyFyJ0TuhMidEFPVf2bd7PPGXdUzOd0JkTshcidE7oTInRC5EyJ3QuROiNwJmZqq1jYdz9w3PdOZbTjdCZE7IXInRO6EyJ0QuRMid0LkTojcCXmYqn" +
                "7etG9s177pzPfumtfe2IbTnRC5EyJ3QuROiNwJkTshcidE7oTInZD3mTuFu6ybFN54n2+85jGnOyFyJ0TuhMidELkTIndC5E6I3AmROyEPQ8Qbn1s7Mws8c6N" +
                "03e+Ofd7/1+lOiNwJkTshcidE7oTInRC5EyJ3QuROyMKx2Zmbjru2UW+cfa6bqa9rY3xVTndC5E6I3AmROyFyJ0TuhMidELkTIndCpnZVHz76wjnijF17vbvu5" +
                "I3bt053QuROiNwJkTshcidE7oTInRC5EyJ3Ql5nbljeOHPddSfHztwo3cXpTojcCZE7IXInRO6EyJ0QuRMid0LkTsi2XdV1Pu+5tbu2QndZd81Od0LkTojcCZE" +
                "7IXInRO6EyJ0QuRMid0Kmpqo3Pj92rDY3vfGpxTOc7oTInRC5EyJ3QuROiNwJkTshcidE7oS8d1/AT+x6mu6MM+eXu+biY+vuhtOdELkTIndC5E6I3AmROyFyJ" +
                "0TuhMidkIW7qrWN0plPHjtzTryLJwDDt8idELkTIndC5E6I3AmROyFyJ0TuhCx8r+rDF8feunrmG0zPtG567XQnRO6EyJ0QuRMid0LkTojcCZE7IXIn5FXbg7zx6" +
                "cE3vt901302VYW/5E6I3AmROyFyJ0TuhMidELkTIndC3p+3Qzme2O16iu+NzpyMznC6EyJ3QuROiNwJkTshcidE7oTInRC5E/Ie//jzdjd3TQp33ckz3+e667/gd" +
                "CdE7oTInRC5EyJ3QuROiNwJkTshcifkYao6duOTacfW/UUzc8R1M8ja9q3TnRC5EyJ3QuROiNwJkTshcidE7oTInZCpqWrNrvnlzMx1xrq/d9eddLoTIndC5E6I3A" +
                "mROyFyJ0TuhMidELkTYqp6hF3P6T1zV3XdXq/TnRC5EyJ3QuROiNwJkTshcidE7oTInZCHodqN71V1zd//3jOtex6y050QuRMid0LkTojcCZE7IXInRO6EyJ2Q+0Z" +
                "uj3a9o3SdM9/Jus66SbDTnRC5EyJ3QuROiNwJkTshcidE7oTInZA/2q1JFatAjGUAAAAASUVORK5CYII="); //图片BASE64编码
        parameter.put("sence",4); //设置场景模式，2-入场无车牌
        parameter.put("amounts",30); //缴费金额
        parameter.put("license","浙A12345"); //
        parameter.put("notice","请缴费"); //通知信息
        String strInbuff = ConfigFileUtil.getReqBodyFromTemplate("/conf/ITC/PicDisPlayInfo.json", parameter);
        System.out.println("设置图片显示输入报文:" + strInbuff);
        String responseString = ISAPI.stdXMLConfig(lUserID,setPicDisplayUrl,strInbuff);
        System.out.println("设置图片显示返回报文："+responseString);
        return;



    }


    /**
     * 平台模式下，车辆入场有车牌场景自定义下发显示
     * @param lUserID
     */
    public static void setEnterLicenseDisplay(int lUserID){

        String setEnterLicenseDisplayUrl = "POST /ISAPI/System/LCDScreen/displayInfo?format=json";
        /**
         *
         */
        Map<String, Object> parameter = new HashMap<>();
        parameter.put("sence",1); //设置场景模式，2-入场有车牌
        parameter.put("license","浙A12345"); //车牌信息
        parameter.put("customInfo","入场有车牌自定义显示"); //通知信息
        parameter.put("enterTime","2020-08-03T17:30:08+08:00"); //入场时间
        String strInbuff = ConfigFileUtil.getReqBodyFromTemplate("/conf/ITC/EnterLiceseDisplay.json", parameter);
        System.out.println("设置入场有车牌显示输入报文:" + strInbuff);
        String responseString = ISAPI.stdXMLConfig(lUserID,setEnterLicenseDisplayUrl,strInbuff);
        System.out.println("设置入场有车牌返回报文："+responseString);
        return;


    }

    /**
     * 空闲场景下余位显示，余位显示需要先设备端开启余位显示，可以在设备web页面入口设置中开启，也可以通过PUT /ISAPI/Parking/channels/1/LCD?format=json&powerOffSaveEnabled=true接口开启余位显示
     * @param lUserID
     */
    public static void setParkingLotDisPlay(int lUserID)
    {
        String setEnterLicenseDisplayUrl = "POST /ISAPI/System/LCDScreen/displayInfo?format=json";
        /**
         *
         */
        Map<String, Object> parameter = new HashMap<>();
        parameter.put("sence",10); //设置场景模式，10-空闲场景
        parameter.put("parkingLot","100"); //车牌信息
        String strInbuff = ConfigFileUtil.getReqBodyFromTemplate("/conf/ITC/ParkingLotDisPlay.json", parameter);
        System.out.println("设置余位显示输入报文:" + strInbuff);
        String responseString = ISAPI.stdXMLConfig(lUserID,setEnterLicenseDisplayUrl,strInbuff);
        System.out.println("设置余位返回报文："+responseString);
        return;

    }




}
