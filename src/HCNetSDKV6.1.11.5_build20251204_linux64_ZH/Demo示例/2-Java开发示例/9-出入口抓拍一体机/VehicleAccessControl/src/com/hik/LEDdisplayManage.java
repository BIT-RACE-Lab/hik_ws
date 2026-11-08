package com.hik;

import CommonMethod.ConfigFileUtil;

/**
 * LED屏幕显示设置
 * @author jiangxin
 * @create 2021-04-21-11:28
 */

    public class LEDdisplayManage {

    /** 获取LED屏幕单场景显示参数(需要看设备是否支持此功能，例如守尉设备支持)
    * 命令：GET /ISAPI/Parking/channels/<channelID>/LEDConfigurations/multiScene/<SID>?format=json
    * channelID =通道号，一般默认1
    * SID场景号：1：passingVehicle（过车场景），2：noVehicle（无过车场景）
    * */
    public void getLEDdisplayMultiScene(int lUserID) throws Exception {

        //  获取LED屏幕过车场景显示参数命令：GET /ISAPI/Parking/channels/1/LEDConfigurations/multiScene/1?format=json    channelID：通道号  SID:场景编号
        String StringpassingVehicle = ISAPI.stdXMLConfig(lUserID, "GET /ISAPI/Parking/channels/1/LEDConfigurations/multiScene/1?format=json", "");
        System.out.println("LED过车场景显示配置参数报文："+StringpassingVehicle);
        //获取LED屏幕空闲场景显示参数命令：GET /ISAPI/Parking/channels/1/LEDConfigurations/multiScene/2?format=json
        String StringnoVehicle = ISAPI.stdXMLConfig(lUserID, "GET /ISAPI/Parking/channels/1/LEDConfigurations/multiScene/2?format=json", "");
        System.out.println("LED空闲场景显示配置参数报文："+StringnoVehicle);
        return;
    }

    /**
     * 设置LED屏幕单场景显示参数(需要看设备是否支持此功能，例如守尉设备支持)
     * @param lUserID
     */
    public void setLEDdisplayMultiScene(int lUserID) {
        String   setLEDdisplayMultiSceneUrl = "PUT /ISAPI/Parking/channels/1/LEDConfigurations/multiScene/2?format=json";
        //空闲场景输入报文
        String strInbuff = ConfigFileUtil.readFileContent("/conf/ITC/SingleSceneLEDConfigurations.json");
        System.out.println("设置LED空闲场景输入报文:" + strInbuff);
        String responseString = ISAPI.stdXMLConfig(lUserID,setLEDdisplayMultiSceneUrl,strInbuff);
        System.out.println("设置LED空闲场景返回报文："+responseString);
        return;



    }


}
