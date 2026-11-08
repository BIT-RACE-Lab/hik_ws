package com.hik;

import CommonMethod.ConfigFileUtil;

import java.util.HashMap;
import java.util.Map;

/**
 * @author jiangxin
 * @create 2021-04-21-11:28
 * 功能模块：透传接口实现语音播放设置，功能：实现获取组合播报内容，设置组合语音播报设置，
 */
public class VoiceManage {


    /**
     * 平台下发语言播报，适用平台自定义下发文本信息，设备响应进行单独播报
     * @param lUserID
     */
    public static void voiceBroadcastInfo(int lUserID)
    {
        String voiceBroadcastInfoURL = "PUT /ISAPI/Parking/channels/1/voiceBroadcastInfo";
        Map<String, Object> parameter = new HashMap<>();
        parameter.put("TTSInfo","[v1]测试语音播报"); //[V]中数字表示音量等级，取值范围1-10)
        String strInbuff = ConfigFileUtil.getReqBodyFromTemplate("/conf/ITC/voiceBroadcastInfo.xml", parameter);
        System.out.println("语音播报输入报文:" + strInbuff);
        String responseString = ISAPI.stdXMLConfig(lUserID,voiceBroadcastInfoURL,strInbuff);
        System.out.println("语音播报返回报文："+responseString);
        return;
    }

    /**
     * 获取组合语音播报参数
     * @param lUserID
     */
    public static void getCombinateBroadcastInfo(int lUserID) {
        String getCombinateBroadcastInfoUrl =  "GET /ISAPI/Parking/channels/1/voiceBroadcastInfo/combinateBroadcast?format=json";
        String responseString =  ISAPI.stdXMLConfig(lUserID, getCombinateBroadcastInfoUrl, "");
        System.out.println("取组合语音播报参数返回报文："+responseString);
        return;
    }

    /**
     * 设置组合语音播报参数
     * @param lUserID
     */
    public static void setCombinateBroadcastInfo(int lUserID) {
        String setCombinateBroadcastInfoUrl = "PUT /ISAPI/Parking/channels/1/voiceBroadcastInfo/combinateBroadcast?format=json";
        String strInbuff = ConfigFileUtil.readFileContent("/conf/ITC/CombinateBroadcast.json");
        System.out.println("设置组合语音播报输入报文:" + strInbuff);
        String responseString = ISAPI.stdXMLConfig(lUserID,setCombinateBroadcastInfoUrl,strInbuff);
        System.out.println("设置组合语音播报返回报文："+responseString);
        return;

    }


}
