import ctypes
import json
import os
import time
import HCNetSDK
import xml.etree.ElementTree as ET
from ctypes import *


class TransIsapi:

    @staticmethod
    def get_isapi(lUserID, url, sdk):
        struXMLInput = HCNetSDK.NET_DVR_XML_CONFIG_INPUT()
        struXMLInput.dwSize = sizeof(struXMLInput)
        url_r = create_string_buffer(bytes(url, encoding="utf-8"))
        struXMLInput.lpRequestUrl = addressof(url_r)
        struXMLInput.dwRequestUrlLen = len(url)
        struXMLInput.lpInBuffer = None
        struXMLInput.dwInBufferSize = 0
        struXMLInput.dwRecvTimeOut = 5000  # 超时时间
        struXMLInput.byForceEncrpt = 0

        # 输出参数
        M1 = 8 * 1024
        buff1 = (c_ubyte * M1)()
        M2 = 1024
        buff2 = (c_ubyte * M2)()
        struXMLOutput = HCNetSDK.NET_DVR_XML_CONFIG_OUTPUT()
        struXMLOutput.dwSize = sizeof(struXMLOutput)
        struXMLOutput.lpOutBuffer = addressof(buff1)
        struXMLOutput.dwOutBufferSize = sizeof(struXMLOutput)
        struXMLOutput.lpStatusBuffer = addressof(buff2)
        struXMLOutput.dwStatusSize = sizeof(struXMLOutput)

        if not sdk.NET_DVR_STDXMLConfig(lUserID, byref(struXMLInput), byref(struXMLOutput)):
            iErr = sdk.NET_DVR_GetLastError()
            print(f"NET_DVR_STDXMLConfig失败，错误号 {iErr} ----URL: {url}")
            return None
        else:
            print("输出文本大小：", struXMLOutput.dwReturnedXMLSize)
            return TransIsapi.res_handle(struXMLOutput)

    @staticmethod
    def put_isapi(lUserID, url, inputXml, sdk, flag=None):
        struXMLInput = HCNetSDK.NET_DVR_XML_CONFIG_INPUT()
        struXMLInput.dwSize = sizeof(struXMLInput)
        url_r = create_string_buffer(bytes(url, encoding="utf-8"))
        struXMLInput.lpRequestUrl = addressof(url_r)
        struXMLInput.dwRequestUrlLen = len(url_r)
        inputXml_r = bytes(inputXml, encoding="utf-8")
        struXMLInput.lpInBuffer = cast(inputXml_r, c_void_p)
        struXMLInput.dwInBufferSize = len(inputXml_r)
        if flag:
            # 从本地文件里面读取JPEG图片二进制数据
            picfile = None
            picdataLength = 0

            try:
                picfile = open(flag, "rb")
            except FileNotFoundError as e:
                print("File not found:", e)

            try:
                picdataLength = os.path.getsize(flag)
            except OSError as e:
                print("Error while getting file size:", e)

            if picdataLength < 0:
                print("Input file dataSize < 0")
            if picfile:
                picfile.close()
            ptrpicByte = create_string_buffer(picdataLength)
            struXMLInput.lpInBuffer = cast(ptrpicByte, c_void_p)
            struXMLInput.dwInBufferSize = picdataLength
            try:
                with open("..//..//resource//pic//FDLib.jpg", "rb") as picfile:
                    data = picfile.read()
                    ptrpicByte.value = data
            except IOError as e2:
                print("Error reading file:", e2)
        struXMLInput.dwRecvTimeOut = 5000
        struXMLInput.byForceEncrpt = 0

        struXMLOutput = HCNetSDK.NET_DVR_XML_CONFIG_OUTPUT()
        M1 = 8 * 1024
        buff1 = (c_ubyte * M1)()
        M2 = 1024
        buff2 = (c_ubyte * M2)()
        struXMLOutput.dwSize = sizeof(struXMLOutput)
        struXMLOutput.lpOutBuffer = addressof(buff1)
        struXMLOutput.dwOutBufferSize = 8 * 1024
        struXMLOutput.lpStatusBuffer = addressof(buff2)
        struXMLOutput.dwStatusSize = 1024

        if not sdk.NET_DVR_STDXMLConfig(lUserID, byref(struXMLInput), byref(struXMLOutput)):
            iErr = sdk.NET_DVR_GetLastError()
            print(f"NET_DVR_STDXMLConfig失败，错误号 {iErr} ----URL: {url}")
            return None
        else:
            print("输出文本大小：", struXMLOutput.dwReturnedXMLSize)
            return TransIsapi.res_handle(struXMLOutput)

    @staticmethod
    def res_handle(struXMLOutput):
        strres = string_at(struXMLOutput.lpOutBuffer, struXMLOutput.dwOutBufferSize) \
            .decode('utf-8').rstrip('\x00').strip()
        stares = string_at(struXMLOutput.lpStatusBuffer, struXMLOutput.dwStatusSize) \
            .decode('utf-8').rstrip('\x00').strip()
        res = strres if len(strres) != 0 else stares
        try:
            result = json.loads(res)
        except:
            result = res
        return result

    @staticmethod
    def convert_str_to_xml(xml_string):
        root = ET.fromstring(xml_string)
        # 查找<modeData>元素
        mode_data = root.find('.//{http://www.isapi.org/ver20/XMLSchema}modeData').text
        return mode_data

