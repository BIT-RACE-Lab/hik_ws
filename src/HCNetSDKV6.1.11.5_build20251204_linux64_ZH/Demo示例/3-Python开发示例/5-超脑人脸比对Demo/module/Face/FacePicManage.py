import os

from module.common.TransIsapi import TransIsapi
from xml.etree.ElementTree import Element, SubElement, ElementTree, tostring
from ctypes import *
from xml.dom import minidom
import HCNetSDK
import json


class FacePicManage:

    @staticmethod
    def get_all_face_lib(lUserID, sdk):
        request_url = "GET /ISAPI/Intelligent/FDLib"
        result = TransIsapi.put_isapi(lUserID, request_url, "", sdk)
        print(result)

    @staticmethod
    def get_face_lib(lUserID, FDID, sdk):
        request_url = "GET /ISAPI/Intelligent/FDLib/" + FDID
        result = TransIsapi.put_isapi(lUserID, request_url, "", sdk)
        print(result)

    @staticmethod
    def create_face_lib(lUserID, ID, Name, sdk):
        root = Element('CreateFDLibList')
        CreateFDLib = Element('CreateFDLib')
        id = Element('id')
        id.text = ID
        name = Element('name')
        name.text = Name
        thresholdValue = Element('thresholdValue')
        thresholdValue.text = '70'

        CreateFDLib.append(id)
        CreateFDLib.append(name)
        CreateFDLib.append(thresholdValue)
        root.append(CreateFDLib)

        document1 = ElementTree(root)

        requestXml = tostring(document1.getroot()).decode()
        print(requestXml)
        request_url = "POST /ISAPI/Intelligent/FDLib"
        result = TransIsapi.put_isapi(lUserID, request_url, requestXml, sdk)
        print(result)

    @staticmethod
    def delete_face_lib(lUserID, FDID, sdk):
        request_url = "DELETE /ISAPI/Intelligent/FDLib/" + FDID
        result = TransIsapi.put_isapi(lUserID, request_url, "", sdk)
        print(result)

    @staticmethod
    def upload_pic(lUserID, FDID, sdk):
        stru_face_lib_cond = HCNetSDK.NET_DVR_FACELIB_COND()
        stru_face_lib_cond.dwSize = sizeof(stru_face_lib_cond)
        field_array = create_string_buffer(1024)
        field_array.value = FDID.encode('utf-8')
        # 人脸库ID
        for i in range(0, HCNetSDK.NET_SDK_MAX_FDID_LEN):
            stru_face_lib_cond.szFDID[i] = 0
        stru_face_lib_cond.szFDID = cast(field_array, POINTER(c_ubyte * HCNetSDK.NET_SDK_MAX_FDID_LEN)).contents
        stru_face_lib_cond.byConcurrent = 0  # 设备并发处理：0 - 不开启(设备自动会建模)，1 - 开始(设备不会自动进行建模)
        stru_face_lib_cond.byCover = 1  # 是否覆盖式导入(人脸库存储满的情况下强制覆盖导入时间最久的图片数据)：0 - 否，1 - 是
        stru_face_lib_cond.byCustomFaceLibID = 0
        load_handler = sdk.NET_DVR_UploadFile_V40(lUserID, HCNetSDK.IMPORT_DATA_TO_FACELIB,
                                                  byref(stru_face_lib_cond), stru_face_lib_cond.dwSize,
                                                  None, None, 0)
        if load_handler < 0:
            print("NET_DVR_UploadFile_V40失败，错误号", sdk.NET_DVR_GetLastError())
            return
        else:
            print("NET_DVR_UploadFile_V40成功")
        stru_send_param = HCNetSDK.NET_DVR_SEND_PARAM_IN()
        # 从本地文件里面读取JPEG图片二进制数据
        picfile = None
        picdataLength = 0

        try:
            picfile = open("..//..//resource//pic//FDLib.jpg", "rb")
        except FileNotFoundError as e:
            print("File not found:", e)

        try:
            picdataLength = os.path.getsize("..//..//resource//pic//FDLib.jpg")
        except OSError as e:
            print("Error while getting file size:", e)

        if picdataLength < 0:
            print("Input file dataSize < 0")
        if picfile:
            picfile.close()
        ptrpicByte = create_string_buffer(picdataLength)
        stru_send_param.dwSendDataLen = picdataLength
        stru_send_param.pSendData = cast(ptrpicByte, c_void_p)
        stru_send_param.byPicType = 1
        try:
            with open("..//..//resource//pic//FDLib.jpg", "rb") as picfile:
                data = picfile.read()
                ptrpicByte.value = data
        except IOError as e2:
            print("Error reading file:", e2)
        # 将字符串转换为字节数组
        byFDLibName = "testName".encode("UTF-8")
        strInBuffer1 = "<FaceAppendData version=\"2.0\" xmlns=\"http://www.hikvision.com/ver20/XMLSchema\"><bornTime>2024-01-10T09:54:00Z</bornTime><name>"
        strInBuffer2 = "</name><sex>male</sex><province>11</province><city>01</city><certificateType>officerID</certificateType><certificateNumber>1123123123</certificateNumber><PersonInfoExtendList><PersonInfoExtend><id>1</id><enable>true</enable><name>test1</name><value>test2</value></PersonInfoExtend></PersonInfoExtendList></FaceAppendData>"

        # 计算总的字节大小
        iStringSize = len(byFDLibName) + len(strInBuffer1) + len(strInBuffer2)

        # 创建 BYTE_ARRAY 对象
        ptrByte = create_string_buffer(1024)
        ptrByte.value = strInBuffer1.encode("UTF-8") + byFDLibName + strInBuffer2.encode("UTF-8")

        # 打印结果
        print(ptrByte.value)
        stru_send_param.pSendAppendData = cast(ptrByte, c_void_p)
        stru_send_param.dwSendAppendDataLen = len(ptrByte)
        i_send_data = sdk.NET_DVR_UploadSend(load_handler, stru_send_param, None)
        if i_send_data <= -1:
            print("NET_DVR_UploadSend失败，错误号:", sdk.NET_DVR_GetLastError())
            return
        while True:
            p_int = c_ulong()
            state = sdk.NET_DVR_GetUploadState(load_handler, byref(p_int))
            print(state)
            if state == 1:
                print("上传成功")
                stru_upload_ret = HCNetSDK.NET_DVR_UPLOAD_FILE_RET()
                upload_result = sdk.NET_DVR_GetUploadResult(load_handler, byref(stru_upload_ret),
                                                            sizeof(stru_upload_ret))
                print(upload_result, '--------------')
                if upload_result:
                    picId = string_at(stru_upload_ret.sUrl, sizeof(stru_upload_ret.sUrl)) \
                        .decode('utf-8').rstrip('\x00').strip()
                    print("图片ID:", picId)
                else:
                    print("NET_DVR_GetUploadResult失败，错误号:", sdk.NET_DVR_GetLastError())
                break
            elif state == 2:
                print("进度：", p_int.value)
                continue
            print("返回值：", state)
            break
        b_close = sdk.NET_DVR_UploadClose(load_handler)
        if not b_close:
            print("NET_DVR_UploadSend失败，错误号:", sdk.NET_DVR_GetLastError())
            return
        else:
            print("关闭图片上传连接成功！！！")

    @staticmethod
    def get_facelib_faceinfo(lUserID, ID, Name, sdk):
        # 创建根元素
        root = Element("FDSearchDescription")

        # 添加子元素
        searchID = SubElement(root, "searchID")
        searchID.text = "C929433A-AD10-0001-CA62-1A701E0015F1"  # 条件不同每次传的searchID也要不一样

        maxResults = SubElement(root, "maxResults")
        maxResults.text = "50"

        searchResultPosition = SubElement(root, "searchResultPosition")
        searchResultPosition.text = "0"

        FDID = SubElement(root, "FDID")
        FDID.text = ID  # Assuming ID is defined somewhere

        name = SubElement(root, "name")
        name.text = Name  # Assuming Name is defined somewhere

        sex = SubElement(root, "sex")
        sex.text = "male"

        province = SubElement(root, "province")
        province.text = "11"

        city = SubElement(root, "city")
        city.text = "01"
        # 转换为格式化的XML字符串
        requestXml = minidom.parseString(tostring(root)).toprettyxml(indent="    ")
        print(requestXml)
        request_url = "POST /ISAPI/Intelligent/FDLib/FDSearch"
        result = TransIsapi.put_isapi(lUserID, request_url, requestXml, sdk)
        print(result)

    @staticmethod
    def FCSearch(lUserID, inFDID, sdk):
        root = Element('FCSearchDescription')
        searchID = Element('searchID')
        searchID.text = "C929433A-AD10-0001-CA62-1A701E0015F9"
        searchResultPosition = Element('searchResultPosition')
        searchResultPosition.text = "0"
        maxResults = Element('maxResults')
        maxResults.text = "50"
        FDID = Element('FDID')
        FDID.text = inFDID
        snapStartTime = Element('snapStartTime')
        snapStartTime.text = "2021-04-14T17:00:00Z"
        snapEndTime = Element('snapEndTime')
        snapEndTime.text = "2021-04-15T11:53:00Z"
        faceMatchInfoEnable = Element('faceMatchInfoEnable')
        faceMatchInfoEnable.text = "true"
        eventType = Element('eventType')
        eventType.text = "whiteFaceContrast"
        sortord = Element('sortord')
        sortord.text = "time"
        root.append(searchID)
        root.append(searchResultPosition)
        root.append(maxResults)
        root.append(FDID)
        root.append(snapStartTime)
        root.append(snapEndTime)
        root.append(faceMatchInfoEnable)
        root.append(eventType)
        root.append(sortord)

        document1 = ElementTree(root)

        requestXml = tostring(document1.getroot()).decode()
        print(requestXml)
        request_url = "POST /ISAPI/Intelligent/FDLib/FCSearch"
        result = TransIsapi.put_isapi(lUserID, request_url, requestXml, sdk)
        print(result)


    @staticmethod
    def FDSearch(lUserID, inFDID, inModeData, sdk):
        root = Element('FDSearchDescription')
        searchID = Element('searchID')
        searchID.text = "C929433A-AD10-0001-CA62-1A701E0015F9"
        searchResultPosition = Element('searchResultPosition')
        searchResultPosition.text = "0"
        maxResults = Element('maxResults')
        maxResults.text = "50"
        FDID = Element('FDID')
        FDID.text = inFDID
        FaceModeList = Element('FaceModeList')
        ModeInfo = Element('ModeInfo')
        similarity = Element('similarity')
        similarity.text = "80"
        modeData = Element('modeData')
        modeData.text = inModeData
        root.append(searchID)
        root.append(searchResultPosition)
        root.append(maxResults)
        root.append(FDID)
        root.append(FaceModeList)
        FaceModeList.append(ModeInfo)
        ModeInfo.append(similarity)
        ModeInfo.append(modeData)
        document1 = ElementTree(root)

        requestXml = tostring(document1.getroot()).decode()
        print(requestXml)
        request_url = "POST /ISAPI/Intelligent/FDLib/FDSearch"
        result = TransIsapi.put_isapi(lUserID, request_url, requestXml, sdk)
        print(result)
