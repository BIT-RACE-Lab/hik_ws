package test;

import com.sun.jna.Pointer;

import java.io.*;
import java.nio.ByteBuffer;

import static test.AudioTest.hCNetSDK;

/**
 * @Author: jiangxin14
 * @Date: 2024-08-07  16:06
 */
public class AudioG722EncodeThread implements Runnable{

    private int lVoiceComHandle; // 假设这是您的声音通信句柄

    public AudioG722EncodeThread(int lVoiceComHandle) {
        this.lVoiceComHandle = lVoiceComHandle;
    }

    @Override
    public void run() {
        FileInputStream VoiceG722PCMfile = null;
        int dataLength = 0;
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

        //PCM编码成G722
        int iEncodeSize = 0;
        HCNetSDK.NET_DVR_AUDIOENC_INFO enc_info = new HCNetSDK.NET_DVR_AUDIOENC_INFO();
        enc_info.write();
        Pointer pEncHandleG722 = hCNetSDK.NET_DVR_InitG722Encoder(enc_info); //创建G722编码库句柄

        byte[] buffer = new byte[1280];
        int readLength;
        while (true) {
            try {
                if (!((readLength = VoiceG722PCMfile.read(buffer)) != -1))
                    break;
            System.out.println("读取长度readLength="+readLength);
            if (readLength < 1280) { // 如果读取的字节数不足固定长度，则在 byte 数组后面补 0
                byte[] newBuffer = new byte[1280];
                System.arraycopy(buffer, 0, newBuffer, 0, readLength);
                buffer = newBuffer;
            }}catch (IOException e) {
                e.printStackTrace();
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
            System.out.println("struEncParam.out_frame_size:" + struEncParam.out_frame_size);
            for (int i = 0; i < struEncParam.out_frame_size / 80; i++) {
                HCNetSDK.BYTE_ARRAY ptrG722Send = new HCNetSDK.BYTE_ARRAY(80);
                System.arraycopy(ptrG722Data.byValue, i * 80, ptrG722Send.byValue, 0, 80);
                ptrG722Send.write();
                //G722数据发送给设备，每次发送80字节，发送时间间隔20毫秒
                if (!hCNetSDK.NET_DVR_VoiceComSendData(lVoiceComHandle, ptrG722Send.byValue, 80)) {
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

        }
    }
}
