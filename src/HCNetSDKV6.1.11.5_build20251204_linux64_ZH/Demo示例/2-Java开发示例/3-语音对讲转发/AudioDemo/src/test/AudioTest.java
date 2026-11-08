package test;

import Common.osSelect;
import com.sun.jna.Memory;
import com.sun.jna.Native;
import com.sun.jna.Pointer;
import com.sun.jna.ptr.ByteByReference;
import jdk.nashorn.internal.runtime.UnwarrantedOptimismException;
import test.HCNetSDK.FVoiceDataCallback_MR_V30;
import test.HCNetSDK.FVoiceDataCallBack_V30;

import java.io.*;
import java.nio.ByteBuffer;
import java.util.Scanner;

public class AudioTest {
    static int lUserID = -1;
    static HCNetSDK hCNetSDK = null;
    static int lVoiceComHandle = -1; //语音对讲句柄
    static int lVoiceHandle = -1; //语音转发句柄
    static int Count = 0;
    static File file = null;
    static File filePcm = null;
    static File Recvfile = null;
    static FileOutputStream outputStream = null;
    static FileOutputStream outputStreamPcm = null;
    static FileOutputStream outputStreamG722 = null;

    static File fileEncode = null;
    static FileOutputStream outputStreamG711 = null;
    static FileInputStream VoiceG722PCMfile = null;
    static Pointer pDecHandle = null;
    static Pointer pEncHandleG722 = null;
    static Pointer pEncHandleG711 = null;
    static cbVoiceDataCallBack_MR_V30 cbVoiceDataCallBack = null;
    static cbVoicePcmDataCallBack_MR_V30 cbVoicePcmDataCallBack_mr_v30=null;
    static VoiceDataCallBack voiceDatacallback = null;
    static g722CallBack g722_callback = null;
    static int PCM_SEND = 1920;


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

    public static void main(String args[]) throws InterruptedException, IOException {
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
        boolean initSuc = hCNetSDK.NET_DVR_Init();
        if (initSuc != true) {
            System.out.println("初始化失败");
        }
        hCNetSDK.NET_DVR_SetLogToFile(3, "./sdkLog", false);



        //设备登录
        lUserID = AudioTest.loginDevice("10.9.137.105", (short) 8000, "admin", "hik12345");

        //获取设备音频编码参数，确定转发音频参数
        AudioTest.getCurrentAudioCompress(lUserID);


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
                    //语音对讲适用于客户端应用，B/S架构的实现双向语音通话，使用语音转发实现
                    System.out.println("\n[Module]开启语音对讲示例代码");
                    lVoiceHandle=AudioTest.startVoiceCom(lUserID);
                    break;
                }
                case "2": {
                    //先开启语音对讲
                    System.out.println("\n[Module]停止语音对讲示例代码");
                    AudioTest.stopVoiceCom(lVoiceHandle);
                    break;
                }
                case "3": {
                    System.out.println("\n[Module]开启G711u格式语音转发示例代码");
                    lVoiceComHandle=AudioTest.startVoiceG711Trans(lUserID);
                    break;
                }
                case "4": {
                    System.out.println("\n[Module]停止G711u语音转发示例代码");
                    AudioTest.stopVoiceG711Trans(lVoiceComHandle);
                    break;
                }
                case "5":{
                    System.out.println("\n[Module]开启G722语音转发示例代码");
                    lVoiceComHandle=AudioTest.startVoiceG722Trans(lUserID);
                    break;

                }
                case "6":{
                    System.out.println("\n[Module]关闭G722语音转发示例代码");
                   AudioTest.startVoiceG722Trans(lVoiceComHandle);
                    break;

                }
                case "7":{
                    System.out.println("\n[Module]开启PCM语音转发示例代码");
                    AudioTest.startTransPCMData(lUserID);
                    break;

                }
                default: {
                    System.out.println("\n未知的指令操作!请重新输入!\n");
                }
            }
        }

        //PCM音频转发
//        AudioTest.startTransPCMData(lUserID);
//        if (lVoiceHandle > -1) {
//            AudioTest.stopVoiceG711Trans(lVoiceHandle);
//        }


        //开启G711u语音转发
//        AudioTest.startVoiceG711Trans(lUserID);
//        if (lVoiceHandle > -1) {
//            AudioTest.stopVoiceG711Trans(lVoiceHandle);
//        }

        //开启G722语音转发
//        try {
//            AudioTest.startVoiceG722Trans(lUserID);
//        } catch (IOException e) {
//            e.printStackTrace();
//        }
//        //延迟一段时间，保证最后一次数据发送完成
//        Thread.sleep(1000);
//        if (lVoiceHandle> -1)
//        {
//            AudioTest.stopVoiceG722Trans(lVoiceHandle);
//        }


        AudioTest.logout();
        //释放SDK
        hCNetSDK.NET_DVR_Cleanup();
    }


    /**
     * 语音对讲回调函数，接收设备和平台双方发送的语音数据
     */
    static class VoiceDataCallBack implements HCNetSDK.FVoiceDataCallBack_V30 {
        public void invoke(int lVoiceComHandle, Pointer pRecvDataBuffer, int dwBufSize, byte byAudioFlag, int pUser) {
            //回调函数里保存语音对讲中双方通话语音数据
            if (Count == 250) {//降低打印频率
                System.out.println("语音对讲数据回调....");
                Count = 0;
            }
            Count++;
        }
    }

    static class cbVoicePcmDataCallBack_MR_V30 implements HCNetSDK.FVoiceDataCallback_MR_V30 {
        public void invoke(int lVoiceComHandle, Pointer pRecvDataBuffer, int dwBufSize, byte byAudioFlag, Pointer pUser) {
            System.out.println("-----=cbVoiceDataCallBack_MR_V30 enter---------");
        }
    }

    //G711语音转发设备回调音频数据
    static class cbVoiceDataCallBack_MR_V30 implements HCNetSDK.FVoiceDataCallback_MR_V30 {
        public void invoke(int lVoiceComHandle, Pointer pRecvDataBuffer, int dwBufSize, byte byAudioFlag, Pointer pUser) {
            //语音回调函数，实现的是接收设备那边传过来的音频数据（g711编码），如果只需要平台发送音频到设备，不需要接收设备发送的音频，
            // 回调函数里什么都不实现
            //不影响业务功能
            if (Count == 250) {//降低打印频率
                System.out.println("-----=cbVoiceDataCallBack_MR_V30 enter---------");
                Count = 0;
            }
            Count++;

            if (byAudioFlag == 1) {
//                System.out.println("设备发过来的语音");
                //设备发送过来的语音数据
                try {
                    //将设备发送过来的语音数据写入文件
                    long offset = 0;
                    ByteBuffer buffers = pRecvDataBuffer.getByteBuffer(offset, dwBufSize);
                    byte[] bytes = new byte[dwBufSize];
                    buffers.rewind();
                    buffers.get(bytes);
                    outputStream.write(bytes);  //这里实现的是将设备发送的g711音频数据写入文件
                    //解码
                    if (pDecHandle == null) {
                        pDecHandle = hCNetSDK.NET_DVR_InitG711Decoder();
                    }
                    HCNetSDK.NET_DVR_AUDIODEC_PROCESS_PARAM struAudioParam = new HCNetSDK.NET_DVR_AUDIODEC_PROCESS_PARAM();
                    struAudioParam.in_buf = pRecvDataBuffer;
                    struAudioParam.in_data_size = dwBufSize;
                    HCNetSDK.BYTE_ARRAY ptrVoiceData = new HCNetSDK.BYTE_ARRAY(320);
                    ptrVoiceData.write();
                    struAudioParam.out_buf = ptrVoiceData.getPointer();
                    struAudioParam.out_frame_size = 320;
                    struAudioParam.g711_type = 0; //G711编码类型：0- U law，1- A law
                    struAudioParam.write();
                    if (!hCNetSDK.NET_DVR_DecodeG711Frame(pDecHandle, struAudioParam)) {
                        System.out.println("NET_DVR_DecodeG711Frame failed, error code:" + hCNetSDK.NET_DVR_GetLastError());
                    }
                    struAudioParam.read();
                    //将解码之后PCM音频数据写入文件
                    long offsetPcm = 0;
                    ByteBuffer buffersPcm = struAudioParam.out_buf.getByteBuffer(offsetPcm, struAudioParam.out_frame_size);
                    byte[] bytesPcm = new byte[struAudioParam.out_frame_size];
                    buffersPcm.rewind();
                    buffersPcm.get(bytesPcm);
                    outputStreamPcm.write(bytesPcm);  //这里实现的是将设备发送的pcm音频数据写入文件，（前面的代码实现的就是将g711解码成pcm音频）

                } catch (Exception e) {
                    e.printStackTrace();
                }

            } else if (byAudioFlag == 0) {
                System.out.println("客户端发送音频数据");
            }
        }
    }

    static class g722CallBack implements HCNetSDK.FVoiceDataCallback_MR_V30 {
        public void invoke(int lVoiceComHandle, Pointer pRecvDataBuffer, int dwBufSize, byte byAudioFlag, Pointer pUser) {
            System.out.println("-----g722CallBack enter---------");
            if (byAudioFlag == 1) {
                System.out.println("设备发过来的语音");
                //设备发送过来的语音数据（建议另建线程或者消息事件方式将数据拷贝到回调函数外面处理，避免阻塞回调）
                try {
                    //将设备发送过来的语音数据写入文件
                    //第一次先创建文件和句柄
                    if (outputStream == null) {
                        Recvfile = new File(System.getProperty("user.dir") + "\\AudioFile\\DeviceSaveData.g722");
                        if (!Recvfile.exists()) {
                            try {
                                Recvfile.createNewFile();
                            } catch (Exception e) {
                                e.printStackTrace();
                            }
                        }
                        try {
                            outputStream = new FileOutputStream(Recvfile);
                        } catch (FileNotFoundException e) {
                            // TODO Auto-generated catch block
                            e.printStackTrace();
                        }
                    }

                    //音频数据二进制写入文件
                    if (outputStream != null) {
                        long offset = 0;
                        ByteBuffer buffers = pRecvDataBuffer.getByteBuffer(offset, dwBufSize);
                        byte[] bytes = new byte[dwBufSize];
                        buffers.rewind();
                        buffers.get(bytes);
                        outputStream.write(bytes);
                    }
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
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

    /**
     * 获取音频编码参数
     * @param userID 设备注册句柄
     */
    public static void getCurrentAudioCompress(int userID)
    {
        HCNetSDK.NET_DVR_COMPRESSION_AUDIO net_dvr_compression_audio=new HCNetSDK.NET_DVR_COMPRESSION_AUDIO();
        boolean b_AudioCompress=hCNetSDK.NET_DVR_GetCurrentAudioCompress(userID,net_dvr_compression_audio);
        if (b_AudioCompress == false)
        {
            System.out.println("获取音频编码格式参数失败，错误码为" + hCNetSDK.NET_DVR_GetLastError());
            return;
        }
        net_dvr_compression_audio.read();
        System.out.println("音频编码类型:"+net_dvr_compression_audio.byAudioEncType);
        System.out.println("音频采样率："+net_dvr_compression_audio.byAudioSamplingRate);
        return;
    }



    /**
         * 设备注销
         */
        public static boolean logout() {

            if (hCNetSDK.NET_DVR_Logout(lUserID)) {
                System.out.println("注销成功");
            }

            return true;
        }




        /**
         * 开启语音对讲
         *
         * @param userID
         */
        public static int startVoiceCom(int userID) {
            if (lVoiceHandle >=0)
            {
                System.out.println("语音对讲已经开启，请先关闭");
                return -1;
            }
            if (voiceDatacallback == null) {
                voiceDatacallback = new VoiceDataCallBack();
            }
            int voiceChannel = 1; //语音通道号。对于设备本身的语音对讲通道，从1开始；对于设备的IP通道，为登录返回的
            // 起始对讲通道号(byStartDTalkChan) + IP通道索引 - 1，例如客户端通过NVR跟其IP Channel02所接前端IPC进行对讲，则dwVoiceChan=byStartDTalkChan + 1
            boolean bret = true;  //需要回调的语音数据类型：0- 编码后的语音数据，1- 编码前的PCM原始数据
            int Handle = hCNetSDK.NET_DVR_StartVoiceCom_V30(userID, voiceChannel, bret, voiceDatacallback, null);
            if (Handle <= -1) {
                System.err.println("语音对讲开启失败，错误码为" + hCNetSDK.NET_DVR_GetLastError());
                return -1;
            }
            System.out.println("语音对讲开始成功！");
            return Handle;

        }

    /**
     * 停止语音对讲
     * @param handle
     * @return
     */
    public static boolean stopVoiceCom(int handle) {
        if (handle<0)
        {
            System.out.println("语音对讲未开启，请先开启对讲");
            return false;
        }
        if (!hCNetSDK.NET_DVR_StopVoiceCom(handle)) {
            System.err.println("停止对讲失败，错误码为" + hCNetSDK.NET_DVR_GetLastError());
            return false;
        }
        System.out.println("语音对讲停止成功！");
        return true;
        }


        /**
         * 开启语音转发
         * 设备音频编码格式G711u
         *
         * @return
         */
        public static int startVoiceG711Trans(int userID) {

            //设置语音G711回调函数
            if (cbVoiceDataCallBack == null) {
                cbVoiceDataCallBack = new cbVoiceDataCallBack_MR_V30();
            }
            file = new File(System.getProperty("user.dir") + "\\AudioFile\\DeviceSaveData.g711");  //保存回调函数的音频数据

            if (!file.exists()) {
                try {
                    file.createNewFile();
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
            try {
                outputStream = new FileOutputStream(file);
            } catch (FileNotFoundException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }

            //保存解码后音频数据
            filePcm = new File(System.getProperty("user.dir") + "\\AudioFile\\DecodeSaveData.pcm");  //保存回调函数的音频数据

            if (!filePcm.exists()) {
                try {
                    filePcm.createNewFile();
                } catch (IOException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }
            }
            try {
                outputStreamPcm = new FileOutputStream(filePcm);
            } catch (FileNotFoundException e3) {
                // TODO Auto-generated catch block
                e3.printStackTrace();
            }
            int voiceChannel = 1; //语音通道号。对于设备本身的语音对讲通道，从1开始；对于设备的IP通道，为登录返回的
            // 起始对讲通道号(byStartDTalkChan) + IP通道索引 - 1，例如客户端通过NVR跟其IP Channel02所接前端IPC进行对讲，则dwVoiceChan=byStartDTalkChan + 1
            lVoiceComHandle = hCNetSDK.NET_DVR_StartVoiceCom_MR_V30(userID, voiceChannel, cbVoiceDataCallBack, null);
            if (lVoiceComHandle == -1) {
                System.out.println("语音转发启动失败,err=" + hCNetSDK.NET_DVR_GetLastError());
                return -1;
            }

            //创建线程编码音频数据发生给设备
            AudioG711EncoderThread audioG711EncoderThread = new AudioG711EncoderThread(lVoiceHandle);
            Thread thread = new Thread(audioG711EncoderThread);
            thread.start();

            return lVoiceComHandle;
        }

    /**
     * 停止G711语音转发
     * @param lVoiceHandle
     */
    public static void stopVoiceG711Trans(int lVoiceHandle) {
            if (pEncHandleG711 != null)
            {
                hCNetSDK.NET_DVR_ReleaseG711Encoder(pEncHandleG711);
            }
            if (pDecHandle != null) {
                hCNetSDK.NET_DVR_ReleaseG711Decoder(pDecHandle);
            }
            if (lVoiceHandle > -1) {
                hCNetSDK.NET_DVR_StopVoiceCom(lVoiceHandle);
            }
            if (outputStream != null) {
                try {
                    outputStream.close();
                } catch (IOException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }
            }
            if (outputStreamPcm != null) {
                try {
                    outputStreamPcm.close();
                } catch (IOException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }
            }

        }


    /**
     * G722音频格式语音转发.通常设备支持的g722音频编码格式：采样率16k 位数16，单通道 测试音频需要保持一致
     * @param userID
     * @throws IOException
     */
    public static int startVoiceG722Trans(int userID) throws IOException {
        int voiceChannel = 1; //语音通道号。对于设备本身的语音对讲通道，从1开始；对于设备的IP通道，为登录返回的
        // 起始对讲通道号(byStartDTalkChan) + IP通道索引 - 1，例如客户端通过NVR跟其IP Channel02所接前端IPC进行对讲，则dwVoiceChan=byStartDTalkChan + 1

        //设置语音回调函数
        if (g722_callback == null) {
            g722_callback = new g722CallBack();
        }
        //开始语音转发
        lVoiceComHandle = hCNetSDK.NET_DVR_StartVoiceCom_MR_V30(userID, voiceChannel, g722_callback, null);
        if (lVoiceComHandle == -1) {
            System.out.println("语音转发启动失败");
            return -1;
        }
        //创建线程编码音频数据发生给设备
        AudioG722EncodeThread audioG722EncoderThread = new AudioG722EncodeThread(lVoiceComHandle);
        Thread thread = new Thread(audioG722EncoderThread);
        thread.start();
        //以下代码是读取本地音频文件发送给设备
        //可以创建线程，在子线程里实现，这样可以不影响主线程其他功能操作
        //读取本地PCM文件中语音数据
/*        int dataLength = 0;
        try {
            //创建从文件读取数据的FileInputStream流
            VoiceG722PCMfile= new FileInputStream(new File(System.getProperty("user.dir") + "\\AudioFile\\g722.pcm"));
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
        if (dataLength <   0) {
            System.out.println("input file dataSize < 0");
            return;
        }

        //保存PCM编码成G722后的音频编码数据
        fileEncode = new File(System.getProperty("user.dir") + "\\AudioFile\\EncodeData.g7");
        if (!fileEncode.exists()) {
            try {
                fileEncode.createNewFile();
            } catch (IOException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }
        }
        try {
            //创建保存G722数据的文件
            outputStreamG722 = new FileOutputStream(fileEncode);
        } catch (FileNotFoundException e3) {
            // TODO Auto-generated catch block
            e3.printStackTrace();
        }

        //PCM编码成G722
        int iEncodeSize = 0;
        HCNetSDK.NET_DVR_AUDIOENC_INFO enc_info = new HCNetSDK.NET_DVR_AUDIOENC_INFO();
        enc_info.write();
        pEncHandleG722 = hCNetSDK.NET_DVR_InitG722Encoder(enc_info); //创建G722编码库句柄

        byte[] buffer = new byte[1280];
        int readLength;
        while ((readLength = VoiceG722PCMfile.read(buffer)) != -1) {
            System.out.println("读取长度readLength="+readLength);
            if (readLength < 1280) { // 如果读取的字节数不足固定长度，则在 byte 数组后面补 0
                byte[] newBuffer = new byte[1280];
                System.arraycopy(buffer, 0, newBuffer, 0, readLength);
                buffer = newBuffer;
            }
            HCNetSDK.BYTE_ARRAY ptrPcmData = new HCNetSDK.BYTE_ARRAY(1280);
            System.arraycopy(buffer, 0, ptrPcmData.byValue, 0, 1280);
            ptrPcmData.write();
            HCNetSDK.BYTE_ARRAY ptrG722Data = new HCNetSDK.BYTE_ARRAY(80);
            ptrG722Data.write();
            HCNetSDK.NET_DVR_AUDIOENC_PROCESS_PARAM struEncParam = new HCNetSDK.NET_DVR_AUDIOENC_PROCESS_PARAM();
            struEncParam.in_buf = ptrPcmData.getPointer();
            struEncParam.out_buf = ptrG722Data.getPointer();
            struEncParam.out_frame_size = 80;
            struEncParam.write();
            //每次读取1280字节PCM数据，编程输出80字节G722数据
            if (!hCNetSDK.NET_DVR_EncodeG722Frame(pEncHandleG722, struEncParam)) {
                System.out.println("NET_DVR_EncodeG711Frame failed, error code:" + hCNetSDK.NET_DVR_GetLastError());
                break;
            }
            struEncParam.read();
            ptrG722Data.read();
            //测试代码，将编码后发送给设备的语音数据保存到本地
            long offsetG722 = 0;
            ByteBuffer buffersG722 = struEncParam.out_buf.getByteBuffer(offsetG722, struEncParam.out_frame_size);
            byte[] bytesG722 = new byte[struEncParam.out_frame_size];
            buffersG722.rewind();
            buffersG722.get(bytesG722);
            try {
                outputStreamG722.write(bytesG722);
            } catch (IOException e1) {
                // TODO Auto-generated catch block
                e1.printStackTrace();
            }
            System.err.println("struEncParam.out_frame_size:" + struEncParam.out_frame_size);
            for (int i = 0; i < struEncParam.out_frame_size / 80; i++) {
                HCNetSDK.BYTE_ARRAY ptrG722Send = new HCNetSDK.BYTE_ARRAY(80);
                System.arraycopy(ptrG722Data.byValue, i * 80, ptrG722Send.byValue, 0, 80);
                ptrG722Send.write();
                //G722数据发送给设备，每次发送80字节，发送时间间隔20毫秒
                if (!hCNetSDK.NET_DVR_VoiceComSendData(lVoiceHandle, ptrG722Send.byValue, 80)) {
                    System.out.println("NET_DVR_VoiceComSendData failed, error code:" + hCNetSDK.NET_DVR_GetLastError());
                }
                //需要实时速率发送数据
                try {
                    Thread.sleep(20);
                } catch (InterruptedException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }
            }

        }*/
        return lVoiceComHandle;
    }

    /**
     * 关闭G722语音转发通道和释放资源
     * @param Handle
     */
    public static void stopVoiceG722Trans(int Handle )
    {
        //数据发送结束，关闭编码库资源
        if (pEncHandleG722 != null)
        {
            hCNetSDK.NET_DVR_ReleaseG722Encoder(pEncHandleG722);
        }
        //关闭发送设备文件资源
        if (VoiceG722PCMfile != null) {
            try {
                VoiceG722PCMfile.close();
            } catch (IOException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }
            System.out.println("VoiceG722PCMfile.close");
        }

        if (outputStreamG722 != null) {
            try {
                outputStreamG722.close();
            } catch (IOException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }
            System.out.println("outputStreamG722.close");
        }
        //停止语音对讲或者转发，释放资源
        if (Handle > -1) {
            hCNetSDK.NET_DVR_StopVoiceCom(Handle);
        }
        //释放解码库资源
        if (pDecHandle != null) {
            hCNetSDK.NET_DVR_ReleaseG722Decoder(pDecHandle);
            System.out.println("NET_DVR_ReleaseG711Decoder");
        }
        //释放回调函数中读写文件的资源
        if (outputStream != null) {
            try {
                outputStream.close();
            } catch (IOException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }
            System.out.println("outputStream.close");
        }
    }


        
    /**
     * pcm音频转发
     * @param luserID
     */
    public static void startTransPCMData(int luserID) {
        // 语音转发
        File decPCMVoiceTransFile = new File("..\\ReceiveVoiceTransData.pcm");
        try {
            // 获取文件的输出流
            FileOutputStream outputStream = new FileOutputStream(decPCMVoiceTransFile);
        } catch (IOException e) {
            e.printStackTrace();
            return;
        }
        //设置语音PCM回调函数
        if (cbVoicePcmDataCallBack_mr_v30==null)
        {
            cbVoicePcmDataCallBack_mr_v30= new cbVoicePcmDataCallBack_MR_V30();
        }
        lVoiceComHandle = hCNetSDK.NET_DVR_StartVoiceCom_MR_V30(lUserID, 1, cbVoicePcmDataCallBack_mr_v30, null);
        if (lVoiceComHandle < 0) {
            System.out.println("NET_DVR_StartVoiceCom_MR_V30 error," + hCNetSDK.NET_DVR_GetLastError());
            hCNetSDK.NET_DVR_Logout(lUserID);
            hCNetSDK.NET_DVR_Cleanup();
            return;
        }
        System.out.println("NET_DVR_StartVoiceCom_MR_V30 suss\n");
        //读取发送到设备的PCM音频文件，视频采样率和位数需要和设备编码参数保持一致
        File m_hStreamFile = new File(System.getProperty("user.dir") + "\\AudioFile\\16kAudio.pcm");
        try {
            // 获取文件的输入流
            FileInputStream inputStream = new FileInputStream(m_hStreamFile);
            int PCMdataLength = 0;
            try {
                //返回文件的总字节数
                PCMdataLength = inputStream.available();
            } catch (IOException e1) {
                e1.printStackTrace();
            }
            if (PCMdataLength < 0) {
                System.out.println("MP3 file dataSize < 0");
                return;
            }
            HCNetSDK.BYTE_ARRAY ptrVoicePcmByte = new HCNetSDK.BYTE_ARRAY(PCMdataLength);
            try {
                inputStream.read(ptrVoicePcmByte.byValue);
            } catch (IOException e2) {
                e2.printStackTrace();
            }
            ptrVoicePcmByte.write();
            for (int i = 0; i < PCMdataLength / PCM_SEND; i++) {
                HCNetSDK.BYTE_ARRAY ptrPcmSend = new HCNetSDK.BYTE_ARRAY(PCM_SEND);
                System.arraycopy(ptrVoicePcmByte.byValue, i * PCM_SEND, ptrPcmSend.byValue, 0, PCM_SEND);
                ptrPcmSend.write();
                if ( hCNetSDK.NET_DVR_VoiceComSendData(lVoiceComHandle, ptrPcmSend.byValue, PCM_SEND) ==false) {
                    System.out.println("NET_DVR_VoiceComSendData failed, error code:" + hCNetSDK.NET_DVR_GetLastError());
                }
                else
                {
                    System.out.println("NET_DVR_VoiceComSendData"+PCM_SEND+"succeed ,data is " + i * PCM_SEND);
                }
                //需要实时速率发送数据
                try {
                    Thread.sleep(40);
                } catch (InterruptedException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
            return;
        }
        return;
    }
}





