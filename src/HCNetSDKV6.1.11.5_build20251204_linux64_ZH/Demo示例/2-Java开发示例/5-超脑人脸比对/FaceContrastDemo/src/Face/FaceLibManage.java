package Face;

/**
 * @Author: jiangxin14
 * @Date: 2024-08-09  15:05
 */
public class FaceLibManage {

    /**
     * 获取所有人脸库信息
     * @param userID
     */
    public static void getAllFaceLibInfo(int userID)
    {
        String requestUrl = "GET /ISAPI/Intelligent/FDLib";
        String strOutXML = ISAPI.sdk_isapi(userID, requestUrl, "");
        System.out.println(strOutXML);
        return;

    }

    /**
     * 创建人脸库
     * @param userID
     */
    public static void setOneFaceLib(int userID)
    {
        /*创建一个人脸库，创建成功的返回结果里面包含FDID*/
        String requestUrl = "POST /ISAPI/Intelligent/FDLib";
        String strOutXML = ISAPI.sdk_isapi(userID, requestUrl, FacePicManage.fDCreate_XmlCreat("9", "sdkceshi"));
        System.out.println(strOutXML);
        return;
    }

    /**删除一个人脸库
    /* DELETE /ISAPI/Intelligent/FDLib/<FDID>，FDID为人脸库ID
     * 通过getAllFaceLib里面代码可以查询设备当前所有人脸库信息可以获取人脸库ID
     */
    public static void deleteOneFaceLib(int userID,String FDID)
    {
        String requestUrl = "DELETE /ISAPI/Intelligent/FDLib/" + FDID;
        String strOutXML = ISAPI.sdk_isapi(userID, requestUrl, "");
        System.out.println(strOutXML);
    }




}
