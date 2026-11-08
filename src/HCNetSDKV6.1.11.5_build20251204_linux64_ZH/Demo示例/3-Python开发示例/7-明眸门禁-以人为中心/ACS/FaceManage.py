import json
import os
import time
import HCNetACSTest
import HCNetSDK
from ctypes import *
from ACS.TransIsapi import TransIsapi
import datetime


class FaceManage:

    @staticmethod
    def search_face_info(user_id, employee, sdk):
        ptr_byte_array = create_string_buffer(1024)
        search_card_info_url = "POST /ISAPI/Intelligent/FDLib/FDSearch?format=json"
        ptr_byte_array.value = search_card_info_url.encode('utf-8')

        l_handler = sdk.NET_DVR_StartRemoteConfig(user_id, HCNetSDK.NET_DVR_FACE_DATA_SEARCH,
                                                  byref(ptr_byte_array), len(search_card_info_url),
                                                  None, None)
        if l_handler < 0:
            print("SearchFaceInfo NET_DVR_StartRemoteConfig 失败,错误码为:", sdk.NET_DVR_GetLastError())
            return
        else:
            print("SearchFaceInfo NET_DVR_StartRemoteConfig成功!")

            str_json_data = """{"searchResultPosition": 0,"FPID": "%s","maxResults": 1,"faceLibType": "blackFD","FDID": "1"}""" % employee
            print("输入参数：" + str_json_data)
            str_in_buff = json.dumps(str_json_data)
            ptr_in_buff = create_string_buffer(str_in_buff.encode('utf-8'))
            ptr_in_buff.value = str_json_data.encode('utf-8')
            m_struJsonData = HCNetSDK.NET_DVR_JSON_DATA_CFG()
            p_int = HCNetACSTest.ctypes.c_ulong()
            while True:
                dw_state = sdk.NET_DVR_SendWithRecvRemoteConfig(l_handler, byref(ptr_in_buff), len(str_in_buff),
                                                                byref(m_struJsonData), 1024, byref(p_int))

                if dw_state == -1:
                    print("NET_DVR_SendWithRecvRemoteConfig接口调用失败，错误码：",
                          sdk.NET_DVR_GetLastError())
                    break
                elif dw_state == HCNetSDK.NET_SDK_CONFIG_STATUS_NEED_WAIT:
                    print("Configuration waiting")
                    time.sleep(10)
                    continue
                elif dw_state == HCNetSDK.NET_SDK_CONFIG_STATUS_FAILED:
                    print("查询人脸失败")
                    break
                elif dw_state == HCNetSDK.NET_SDK_CONFIG_STATUS_EXCEPTION:
                    print("查询人脸异常")
                    break
                elif dw_state == HCNetSDK.NET_SDK_CONFIG_STATUS_SUCCESS:
                    lpJsonData = cast(m_struJsonData.lpJsonData, POINTER(c_char * 1024)).contents.value
                    json_end_index = lpJsonData.find(b'--MIME_boundary')  # 查找 JSON 数据的结束位置
                    json_data = lpJsonData[:json_end_index].decode('utf-8')  # 提取 JSON 字符串部分
                    json_object = json.loads(json_data)  # 解析 JSON 数据
                    print("dw_state:", dw_state, ", m_struJsonData:", json_data)
                    if json_object['numOfMatches'] != 0:
                        MatchList = list(json_object['MatchList'])
                        MatchList_1 = MatchList[0]
                        FPID = MatchList_1['FPID']
                        try:
                            with open(f"..//..//AddFacePicture//[" + FPID + "]_FacePic.jpg", "wb") as fout:
                                buffers = create_string_buffer(m_struJsonData.dwPicDataSize)
                                memmove(buffers, m_struJsonData.lpPicData, m_struJsonData.dwPicDataSize)
                                fout.write(buffers.raw)
                                fout.close()
                                print("获取人脸成功")
                        except FileNotFoundError as e:
                            print("文件未找到:", e)
                        except IOError as e:
                            print("IO 错误:", e)
                    break
                elif dw_state == HCNetSDK.NET_SDK_CONFIG_STATUS_FINISH:
                    print("获取人脸完成")
                    break

            if not sdk.NET_DVR_StopRemoteConfig(l_handler):
                print("NET_DVR_StopRemoteConfig failed, error code:", sdk.NET_DVR_GetLastError())
            else:
                print("NET_DVR_StopRemoteConfig successful")

    @staticmethod
    def add_face_by_binary(user_id, employee, sdk):
        ptr_byte_array = create_string_buffer(1024)
        search_card_info_url = "PUT /ISAPI/Intelligent/FDLib/FDSetUp?format=json"
        ptr_byte_array.value = search_card_info_url.encode('utf-8')
        l_handler = sdk.NET_DVR_StartRemoteConfig(user_id, HCNetSDK.NET_DVR_FACE_DATA_RECORD,
                                                  byref(ptr_byte_array), len(search_card_info_url),
                                                  None, None)
        if l_handler < 0:
            print("SearchFaceInfo NET_DVR_StartRemoteConfig 失败,错误码为:", sdk.NET_DVR_GetLastError())
            return
        else:
            print("Addface NET_DVR_StartRemoteConfig成功!")

            str_json_data = """{"faceLibType": "blackFD","FDID": "1","FPID": "%s"}""" % employee
            ptr_byte_array.value = str_json_data.encode('utf-8')
            struAddFaceDataCfg = HCNetSDK.NET_DVR_JSON_DATA_CFG()
            struAddFaceDataCfg.dwSize = sizeof(struAddFaceDataCfg)
            struAddFaceDataCfg.lpJsonData = cast(ptr_byte_array, c_void_p)
            struAddFaceDataCfg.dwJsonDataSize = len(str_json_data)
            # 从本地文件里面读取JPEG图片二进制数据
            picfile = None
            picdataLength = 0

            try:
                picfile = open("..//..//pic//FDLib.jpg", "rb")
            except FileNotFoundError as e:
                print("File not found:", e)

            try:
                picdataLength = os.path.getsize("..//..//pic//FDLib.jpg")
            except OSError as e:
                print("Error while getting file size:", e)

            if picdataLength < 0:
                print("Input file dataSize < 0")
            if picfile:
                picfile.close()
            ptrpicByte = create_string_buffer(picdataLength)
            try:
                with open("..//..//pic//FDLib.jpg", "rb") as picfile:
                    data = picfile.read()
                    ptrpicByte.value = data
            except IOError as e2:
                print("Error reading file:", e2)
            struAddFaceDataCfg.dwPicDataSize = picdataLength
            struAddFaceDataCfg.lpPicData = cast(ptrpicByte, c_void_p)
            ptr_out_buff = create_string_buffer(1024)
            p_int = HCNetACSTest.ctypes.c_ulong()
            while True:
                dw_state = sdk.NET_DVR_SendWithRecvRemoteConfig(l_handler, byref(struAddFaceDataCfg),
                                                                struAddFaceDataCfg.dwSize, byref(ptr_out_buff), 1024,
                                                                byref(p_int))
                if dw_state == -1:
                    print("NET_DVR_SendWithRecvRemoteConfig接口调用失败，错误码：",
                          sdk.NET_DVR_GetLastError())
                    break
                elif dw_state == HCNetSDK.NET_SDK_CONFIG_STATUS_NEED_WAIT:
                    print("Configuration waiting")
                    time.sleep(10)
                    continue
                elif dw_state == HCNetSDK.NET_SDK_CONFIG_STATUS_FAILED:
                    print("下发人脸失败")
                    break
                elif dw_state == HCNetSDK.NET_SDK_CONFIG_STATUS_EXCEPTION:
                    print("下发人脸异常")
                    break
                elif dw_state == HCNetSDK.NET_SDK_CONFIG_STATUS_SUCCESS:
                    ptr_out_buff = ptr_out_buff.raw
                    str_result = ptr_out_buff.decode('utf-8').rstrip('\x00').strip()
                    json_result = json.loads(str_result)
                    status_code = json_result.get("statusCode")
                    if status_code != 1:
                        print("下发人脸成功，但有异常情况")
                    else:
                        print("下发人脸成功")
                    print("dw_state:", dw_state, ", str_result:", str_result)
                    break
                elif dw_state == HCNetSDK.NET_SDK_CONFIG_STATUS_FINISH:
                    print("获取人脸完成")
                    break

            if not sdk.NET_DVR_StopRemoteConfig(l_handler):
                print("NET_DVR_StopRemoteConfig failed, error code:", sdk.NET_DVR_GetLastError())
            else:
                print("NET_DVR_StopRemoteConfig successful")

    @staticmethod
    def add_face_by_url(user_id, employee, sdk):
        ptr_byte_array = create_string_buffer(1024)
        strInBuffer = "PUT /ISAPI/Intelligent/FDLib/FDSetUp?format=json"
        ptr_byte_array.value = strInBuffer.encode('utf-8')
        l_handler = sdk.NET_DVR_StartRemoteConfig(user_id, HCNetSDK.NET_DVR_FACE_DATA_RECORD,
                                                  byref(ptr_byte_array), len(strInBuffer),
                                                  None, None)
        if l_handler < 0:
            print("SearchFaceInfo NET_DVR_StartRemoteConfig 失败,错误码为:", sdk.NET_DVR_GetLastError())
            return
        else:
            print("SearchFaceInfo NET_DVR_StartRemoteConfig成功!")
            struAddFaceDataCfg = HCNetSDK.NET_DVR_JSON_DATA_CFG()
            str_json_data = """{"faceURL": "http://10.19.37.105:6011/pic?1F34CD32B2003807EF5451E7D6E9823B[hik003]_FacePic.jpg","faceLibType": "blackFD","FDID": "1","FPID": "%s"}""" % employee
            print("输入参数：" + str_json_data)
            str_in_buff = json.dumps(str_json_data)
            ptr_in_buff = create_string_buffer(str_in_buff.encode('utf-8'))
            ptr_in_buff.value = str_json_data.encode('utf-8')
            struAddFaceDataCfg.dwSize = sizeof(struAddFaceDataCfg)
            struAddFaceDataCfg.lpJsonData = cast(ptr_in_buff, c_void_p)
            struAddFaceDataCfg.dwJsonDataSize = len(str_json_data)
            struAddFaceDataCfg.lpPicData = None
            struAddFaceDataCfg.dwPicDataSize = 0
            ptr_out_buff = create_string_buffer(1024)
            p_int = HCNetACSTest.ctypes.c_ulong()
            while True:
                dw_state = sdk.NET_DVR_SendWithRecvRemoteConfig(l_handler, byref(struAddFaceDataCfg),
                                                                struAddFaceDataCfg.dwSize,
                                                                byref(ptr_out_buff), 1024, byref(p_int))
                print(dw_state)
                if dw_state == -1:
                    print("NET_DVR_SendWithRecvRemoteConfig接口调用失败，错误码：",
                          sdk.NET_DVR_GetLastError())
                    break
                elif dw_state == HCNetSDK.NET_SDK_CONFIG_STATUS_NEED_WAIT:
                    print("Configuration waiting")
                    time.sleep(10)
                    continue
                elif dw_state == HCNetSDK.NET_SDK_CONFIG_STATUS_FAILED:
                    print("查询人脸失败")
                    break
                elif dw_state == HCNetSDK.NET_SDK_CONFIG_STATUS_EXCEPTION:
                    print("查询人脸异常")
                    break
                elif dw_state == HCNetSDK.NET_SDK_CONFIG_STATUS_SUCCESS:
                    ptr_out_buff = ptr_out_buff.raw
                    str_result = ptr_out_buff.decode('utf-8').rstrip('\x00').strip()
                    json_result = json.loads(str_result)
                    status_code = json_result.get("statusCode")
                    if status_code != 1:
                        print("下发人脸成功，但有异常情况")
                    else:
                        print("下发人脸成功")
                    print("dw_state:", dw_state, ", str_result:", str_result)
                    break
                elif dw_state == HCNetSDK.NET_SDK_CONFIG_STATUS_FINISH:
                    print("获取人脸完成")
                    break

            if not sdk.NET_DVR_StopRemoteConfig(l_handler):
                print("NET_DVR_StopRemoteConfig failed, error code:", sdk.NET_DVR_GetLastError())
            else:
                print("NET_DVR_StopRemoteConfig successful")

    @staticmethod
    def delete_face_info(user_id, employee_no, sdk):
        delete_face_url = "PUT /ISAPI/Intelligent/FDLib/FDSearch/Delete?format=json&FDID=1&faceLibType=blackFD"
        delete_face_json = f"""{{
            "FPID": [{{
                "value": "{employee_no}"
            }}]
        }}"""
        result = TransIsapi.put_isapi(user_id, delete_face_url, delete_face_json, sdk)
        print(result)

    @staticmethod
    def capture_face_info(user_id, sdk):
        stru_cap_cond = HCNetSDK.NET_DVR_CAPTURE_FACE_COND()
        stru_cap_cond.dwSize = sizeof(stru_cap_cond)
        l_capture_face_handler = sdk.NET_DVR_StartRemoteConfig(user_id, HCNetSDK.NET_DVR_CAPTURE_FACE_INFO,
                                                               byref(stru_cap_cond), stru_cap_cond.dwSize,
                                                               None, None)
        if l_capture_face_handler == -1:
            print("建立采集人脸长连接失败,错误码为:", sdk.NET_DVR_GetLastError())
            return
        else:
            print("建立采集人脸长连接成功!")
            stru_face_info = HCNetSDK.NET_DVR_CAPTURE_FACE_CFG()
            while True:
                print(sizeof(stru_face_info))
                dw_state = sdk.NET_DVR_GetNextRemoteConfig(l_capture_face_handler, byref(stru_face_info),
                                                           sizeof(stru_face_info))
                if dw_state == -1:
                    print("NET_DVR_GetNextRemoteConfig采集人脸失败，错误码：",
                          sdk.NET_DVR_GetLastError())
                    break
                elif dw_state == HCNetSDK.NET_SDK_CONFIG_STATUS_NEED_WAIT:
                    print("正在采集中,请等待...")
                    time.sleep(10)
                    continue
                elif dw_state == HCNetSDK.NET_SDK_CONFIG_STATUS_FAILED:
                    print("采集人脸失败")
                    break
                elif dw_state == HCNetSDK.NET_SDK_CONFIG_STATUS_EXCEPTION:
                    print("采集人脸异常, 网络异常导致连接断开")
                    break
                elif dw_state == HCNetSDK.NET_SDK_CONFIG_STATUS_SUCCESS:
                    if stru_face_info.dwFacePicSize > 0 and stru_face_info.pFacePicBuffer is not None:
                        sf = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                        new_name = f"{sf}_capFaceInfo.jpg"
                        try:
                            # 生成新的文件名
                            filename = os.path.join("..//..//pic//", new_name)
                            # 将字节写入文件
                            with open(filename, "wb") as fout:
                                bytes_data = cast(stru_face_info.pFacePicBuffer,
                                                  POINTER(c_ubyte * stru_face_info.dwFacePicSize))
                                fout.write(bytes_data.contents)

                            print("采集人脸成功，图片保存路径:", filename)
                        except FileNotFoundError as e:
                            # 处理文件未找到异常
                            print("文件未找到:", e)
                        except IOError as e:
                            # 处理IO异常
                            print("IO异常:", e)
                    break
                elif dw_state == HCNetSDK.NET_SDK_CONFIG_STATUS_FINISH:
                    print("获取人脸完成")
                    break

            if not sdk.NET_DVR_StopRemoteConfig(l_capture_face_handler):
                print("NET_DVR_StopRemoteConfig failed, error code:", sdk.NET_DVR_GetLastError())
            else:
                print("NET_DVR_StopRemoteConfig successful")
