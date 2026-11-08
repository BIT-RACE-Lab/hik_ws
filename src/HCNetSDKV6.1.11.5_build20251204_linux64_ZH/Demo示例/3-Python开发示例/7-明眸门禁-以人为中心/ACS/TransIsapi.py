import ctypes
import json
import time
import HCNetSDK
from ctypes import *


class TransIsapi:

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
            strres = string_at(struXMLOutput.lpOutBuffer, struXMLOutput.dwOutBufferSize) \
                .decode('utf-8').rstrip('\x00').strip()
            result = json.loads(strres)
            print(result)
            return result

    def put_isapi(lUserID, url, inputXml, sdk):
        struXMLInput = HCNetSDK.NET_DVR_XML_CONFIG_INPUT()
        struXMLInput.dwSize = sizeof(struXMLInput)
        url_r = create_string_buffer(bytes(url, encoding="utf-8"))
        struXMLInput.lpRequestUrl = addressof(url_r)
        struXMLInput.dwRequestUrlLen = len(url_r)

        inputXml_r = bytes(inputXml, encoding="utf-8")
        struXMLInput.lpInBuffer = cast(inputXml_r, c_void_p)
        struXMLInput.dwInBufferSize = len(inputXml_r)
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
            strres = string_at(struXMLOutput.lpOutBuffer, struXMLOutput.dwOutBufferSize) \
                .decode('utf-8').rstrip('\x00').strip()
            result = json.loads(strres)
            return result
