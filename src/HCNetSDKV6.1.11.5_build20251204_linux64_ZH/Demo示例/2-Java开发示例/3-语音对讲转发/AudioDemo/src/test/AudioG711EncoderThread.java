package test;

import com.sun.jna.Pointer;

import java.io.*;
import java.nio.ByteBuffer;

import static test.AudioTest.hCNetSDK;
import static test.AudioTest.lVoiceComHandle;

/**
 * @Author: jiangxin14
 * @Date: 2024-08-07  15:12
 */
public class AudioG711EncoderThread implements Runnable{

    private int lVoiceComHandle; // 假设这是您的声音通信句柄

    public AudioG711EncoderThread(int lVoiceHandle) {
        this.lVoiceComHandle = lVoiceComHandle;
    }


    @Override
    public void run() {
                    // 执行线程任务
                    FileInputStream Voicefile = null;
//            FileOutputStream Encodefile = null;
                    int dataLength = 0;
                    try {
                        //创建从文件读取数据的FileInputStream流
                        Voicefile = new FileInputStream(new File(System.getProperty("user.dir") + "\\AudioFile\\send2device.pcm"));
                    } catch (FileNotFoundException e) {
                        e.printStackTrace();
                    }
                    try {
                        //返回文件的总字节数
                        dataLength = Voicefile.available();
                    } catch (IOException e1) {
                        e1.printStackTrace();
                    }
                    if (dataLength < 0) {
                        System.out.println("input file dataSize < 0");
                        return;
                    }
                    HCNetSDK.BYTE_ARRAY ptrVoiceByte = new HCNetSDK.BYTE_ARRAY(dataLength);
                    try {
                        Voicefile.read(ptrVoiceByte.byValue);
                    } catch (IOException e2) {
                        e2.printStackTrace();
                    }
                    ptrVoiceByte.write();
                    int iEncodeSize = 0;
                    HCNetSDK.NET_DVR_AUDIOENC_INFO enc_info = new HCNetSDK.NET_DVR_AUDIOENC_INFO();
                    enc_info.write();
                    Pointer pEncHandleG711 = hCNetSDK.NET_DVR_InitG711Encoder(enc_info);
                    while ((dataLength - iEncodeSize) > 640) {
                        HCNetSDK.BYTE_ARRAY ptrPcmData = new HCNetSDK.BYTE_ARRAY(640);
                        System.arraycopy(ptrVoiceByte.byValue, iEncodeSize, ptrPcmData.byValue, 0, 640);
                        ptrPcmData.write();

                        HCNetSDK.BYTE_ARRAY ptrG711Data = new HCNetSDK.BYTE_ARRAY(320);
                        ptrG711Data.write();

                        HCNetSDK.NET_DVR_AUDIOENC_PROCESS_PARAM struEncParam = new HCNetSDK.NET_DVR_AUDIOENC_PROCESS_PARAM();
                        struEncParam.in_buf = ptrPcmData.getPointer();
                        struEncParam.out_buf = ptrG711Data.getPointer();
                        struEncParam.out_frame_size = 320;
                        struEncParam.g711_type = 0;//G711编码类型：0- U law，1- A law
                        struEncParam.write();

                        if (!hCNetSDK.NET_DVR_EncodeG711Frame(pEncHandleG711, struEncParam)) {
                            System.out.println("NET_DVR_EncodeG711Frame failed, error code:" + hCNetSDK.NET_DVR_GetLastError());
                            hCNetSDK.NET_DVR_ReleaseG711Encoder(pEncHandleG711);
                            //	hCNetSDK.NET_DVR_StopVoiceCom(lVoiceHandle);
                            return;
                        }
                        struEncParam.read();
                        ptrG711Data.read();

                        long offsetG711 = 0;
                        ByteBuffer buffersG711 = struEncParam.out_buf.getByteBuffer(offsetG711, struEncParam.out_frame_size);
                        byte[] bytesG711 = new byte[struEncParam.out_frame_size];
                        buffersG711.rewind();
                        buffersG711.get(bytesG711);

                        iEncodeSize += 640;
//            System.out.println("编码字节数：" + iEncodeSize);
                        for (int i = 0; i < struEncParam.out_frame_size / 160; i++) {
                            HCNetSDK.BYTE_ARRAY ptrG711Send = new HCNetSDK.BYTE_ARRAY(160);
                            System.arraycopy(ptrG711Data.byValue, i * 160, ptrG711Send.byValue, 0, 160);
                            ptrG711Send.write();
                            if (!hCNetSDK.NET_DVR_VoiceComSendData(lVoiceComHandle, ptrG711Send.byValue, 160)) {
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

