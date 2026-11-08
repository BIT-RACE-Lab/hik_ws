package Acs;


import Commom.osSelect;
import NetSDKDemo.HCNetSDK;
import com.sun.jna.Native;
import org.json.JSONException;

import java.io.UnsupportedEncodingException;
import java.util.Scanner;


public class AcsMain {

	static HCNetSDK hCNetSDK = null;
	static int lUserID = -1;//用户句柄
	static int iCharEncodeType = 0;//设备字符集



	/**
	 * 根据不同操作系统选择不同的库文件和库路径
	 * @return
	 */
	private static boolean createSDKInstance()
	{
		if(hCNetSDK == null)
		{
			synchronized (HCNetSDK.class)
			{
				String strDllPath = "";
				try
				{
					//System.setProperty("jna.debug_load", "true");
					if(osSelect.isWindows())
						//win系统加载库路径
						strDllPath = System.getProperty("user.dir") + "\\lib\\HCNetSDK.dll";
					else if(osSelect.isLinux())
						//Linux系统加载库路径
						strDllPath =  System.getProperty("user.dir") + "/lib/libhcnetsdk.so";
					hCNetSDK = (HCNetSDK) Native.loadLibrary(strDllPath, HCNetSDK.class);
				}catch (Exception ex) {
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
	 * @throws JSONException 
	 */
	public static void main(String[] args) throws UnsupportedEncodingException, InterruptedException, JSONException  {


		if(hCNetSDK == null)
		{
			if(!createSDKInstance())
			{
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
		lUserID=loginDevice("10.9.137.105",(short) 8000,"admin","hik12345");	//登陆设备

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
					System.out.println("\n[Module]获取门禁参数示例代码");
					ACSManage.acsCfg(lUserID);
					break;
				}
				case "2":
				{
					System.out.println("\n[Module]获取门禁状态示例代码");
					ACSManage.getAcsStatus(lUserID);
					break;
				}
				case "3":
				{
					System.out.println("\n[Module]远程控门示例代码");
					ACSManage.remoteControlGate(lUserID);
					break;
				}
				case "4":
				{
					System.out.println("\n[Module]下发人员示例代码");
					UserManage.addUserInfo(lUserID,"12345");
					break;
				}
				case "5":
				{
					System.out.println("\n[Module]查询人员示例代码");
					UserManage.searchUserInfo(lUserID);
					break;
				}
				case "6":
				{
					System.out.println("\n[Module]删除人员代码");
					//支持按人员和全部删除
					UserManage.deleteUserInfo(lUserID);
					break;
				}
				case "7":
				{
					//先下发人员，人员工号上绑定卡号
					System.out.println("\n[Module]下发卡号代码");
					CardManage.addCardInfo(lUserID,"test001","12345");
					break;
				}
				case "8":
				{
					//按照人员工号查看绑定的卡号
					System.out.println("\n[Module]查询卡号代码");
					CardManage.searchCardInfo(lUserID,"test001");
					break;
				}
				case "9":
				{
					//按照人员工号删除绑定的卡号
					System.out.println("\n[Module]删除卡号代码");
					CardManage.deleteCardInfo(lUserID,"12345");
					break;
				}
				case "10":
				{
					//先下发人员，人员工号上绑定人脸图片
					System.out.println("\n[Module]二进制方式下发人脸代码");
					FaceManage.addFaceByBinary(lUserID,"test001");
					break;
				}
				case "12":
				{
					//先下发人员，人员工号上绑定人脸图片
					System.out.println("\n[Module]URL方式下发人脸代码");
					FaceManage.addFaceByUrl(lUserID,"test001");
					break;
				}
				case "13":
				{
					//根据人员工号查询人脸图片
					System.out.println("\n[Module]查询人脸代码");
					FaceManage.searchFaceInfo(lUserID,"test001");
					break;
				}
				case "14":
				{
					//根据人员工号删除人脸图片
					System.out.println("\n[Module]删除人脸代码");
					FaceManage.deleteFaceInfo(lUserID,"test001");

					break;
				}
				case "15":
				{
					System.out.println("\n[Module]采集人脸代码");
					FaceManage.captureFaceInfo(lUserID);
					break;
				}
				case "16":
				{
					System.out.println("\n[Module]门禁历史事件查询代码");
					EventSearch.searchAllEvent(lUserID);
					break;
				}
				case "17":{
					//人员下发默认1号计划模板：全天24小时有权限，自定义设置计划模板建议从2号模板开始
					System.out.println("\n[Module]设置计划模板代码");
					UserManage.setCardTemplate(lUserID,2);
					break;
				}
				default:
				{
					System.out.println("\n未知的指令操作!请重新输入!\n");
				}
			}
		}

		/**
		 * 增加sleep时间，保证程序一直运行，

		 */
		Thread.sleep(1000);
		/**
		 * 注销设备
		 */
		AcsMain.logout();

		//释放SDK，程序退出前调用
		hCNetSDK.NET_DVR_Cleanup();
		
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
//			int startDChan = deviceInfo.struDeviceV30.byStartDChan;
//			System.out.println("预览起始通道号: " + startDChan);
		}
		return userID; // 返回登录结果
	}

	/**
	 * 登出操作
	 *
	 */
	public static void logout(){
		/**登出和清理，释放SDK资源*/
		if (lUserID>=0)
		{
			if (!hCNetSDK.NET_DVR_Logout(lUserID))
			{
				System.err.println("设备注销失败，错误码：" + hCNetSDK.NET_DVR_GetLastError());
				return;
			}
			System.out.println("设备注销成功！！！");
		}

	}
}//AcsMain  Class结束
