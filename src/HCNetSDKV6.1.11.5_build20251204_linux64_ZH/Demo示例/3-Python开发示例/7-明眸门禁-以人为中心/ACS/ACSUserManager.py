import json
import time
from ctypes import byref, create_string_buffer, c_ulong
import HCNetACSTest
import HCNetSDK
from ACS.TransIsapi import TransIsapi


class UserManage:
    def add_user_info(self, l_user_id, employee_no, sdk):
        ptr_byte_array = create_string_buffer(1024)
        str_in_buffer = "PUT /ISAPI/AccessControl/UserInfo/SetUp?format=json"
        ptr_byte_array.value = str_in_buffer.encode('utf-8')

        l_handler = sdk.NET_DVR_StartRemoteConfig(l_user_id, HCNetSDK.NET_DVR_JSON_CONFIG,
                                                  byref(ptr_byte_array), len(str_in_buffer), None, None)

        if l_handler < 0:
            print("AddUserInfo NET_DVR_StartRemoteConfig 失败,错误码为", sdk.NET_DVR_GetLastError())
            return
        else:
            print("AddUserInfo NET_DVR_StartRemoteConfig 成功!")

            name = "test".encode('utf-8')
            str_in_buffer1 = f'{{\n"UserInfo":{{\n"employeeNo":"{employee_no}",\n"name":"'
            str_in_buffer2 = f'",\n"userType":"normal",\n"Valid":{{\n"enable":true,\n"beginTime":"2023-12-27T14:49:08",\n"endTime":"2030-08-01T17:30:08",\n"timeType":"local"\n}},"belongGroup":"1","doorRight":"1","RightPlan":[{{"doorNo":1,"planTemplateNo":"1"}}]}}}}'

            i_string_size = len(name) + len(str_in_buffer1) + len(str_in_buffer2)
            ptr_byte = create_string_buffer(i_string_size)

            ptr_byte.value = (str_in_buffer1 + name.decode('utf-8') + str_in_buffer2).encode('utf-8')

            print(ptr_byte.value.decode('utf-8'))

            ptr_out_buff = create_string_buffer(1024)
            print(ptr_out_buff.value.decode('utf-8'))
            # 创建一个整数引用对象，初始值为0
            p_int = HCNetACSTest.ctypes.c_ulong()
            print(p_int)
            while True:
                print(
                    sdk.NET_DVR_SendWithRecvRemoteConfig(l_handler, byref(ptr_byte), i_string_size, byref(ptr_out_buff),
                                                         1024, HCNetACSTest.ctypes.byref(p_int)))
                dw_state = sdk.NET_DVR_SendWithRecvRemoteConfig(l_handler, byref(ptr_byte), i_string_size,
                                                                byref(ptr_out_buff), 1024, byref(p_int))

                if dw_state == -1:
                    print("NET_DVR_SendWithRecvRemoteConfig接口调用失败，错误码：", sdk.NET_DVR_GetLastError())
                    break

                ptr_out_buff = ptr_out_buff.raw
                str_result = ptr_out_buff.decode('utf-8').rstrip('\x00').strip()
                json_result = json.loads(str_result)
                status_code = json_result.get("statusCode", 0)

                if dw_state == HCNetSDK.NET_SDK_CONFIG_STATUS_NEED_WAIT:
                    print("配置等待")
                    time.sleep(10)
                    continue
                elif dw_state == HCNetSDK.NET_SDK_CONFIG_STATUS_FAILED:
                    print("下发人员失败, json retun:", json_result)
                    break
                elif dw_state == HCNetSDK.NET_SDK_CONFIG_STATUS_EXCEPTION:
                    print("下发人员异常, json retun:", json_result)
                    break
                elif dw_state == HCNetSDK.NET_SDK_CONFIG_STATUS_SUCCESS:
                    if status_code != 1:
                        print("下发人员成功,但是有异常情况:", json_result)
                    else:
                        print("下发人员成功: json retun:", json_result)
                    break
                elif dw_state == HCNetSDK.NET_SDK_CONFIG_STATUS_FINISH:
                    print("下发人员完成")
                    break

            if not sdk.NET_DVR_StopRemoteConfig(l_handler):
                print("NET_DVR_StopRemoteConfig接口调用失败，错误码：", sdk.NET_DVR_GetLastError())
            else:
                print("NET_DVR_StopRemoteConfig接口成功")

    @staticmethod
    def search_user_info(user_id, sdk):
        ptr_byte_array = create_string_buffer(1024)
        str_in_buffer = "POST /ISAPI/AccessControl/UserInfo/Search?format=json"
        ptr_byte_array.value = str_in_buffer.encode('utf-8')

        l_handler = sdk.NET_DVR_StartRemoteConfig(user_id, HCNetSDK.NET_DVR_JSON_CONFIG,
                                                  byref(ptr_byte_array), len(str_in_buffer), None, None)

        if l_handler < 0:
            print("SearchUserInfo NET_DVR_StartRemoteConfig 失败,错误码为", sdk.NET_DVR_GetLastError())
            return
        else:
            json_object = {
                "UserInfoSearchCond": {
                    "searchID": "666",
                    "searchResultPosition": 0,
                    "maxResults": 30
                }
            }

            str_in_buff = json.dumps(json_object)
            print("查询的json报文:", str_in_buff)

            ptr_in_buff = create_string_buffer(str_in_buff.encode('utf-8'))
            ptr_out_buff = create_string_buffer(20 * 1024)
            p_int = c_ulong()

            while True:
                dw_state = sdk.NET_DVR_SendWithRecvRemoteConfig(l_handler, byref(ptr_in_buff), len(str_in_buff),
                                                                byref(ptr_out_buff), 20 * 1024, byref(p_int))

                if dw_state == -1:
                    print("NET_DVR_SendWithRecvRemoteConfig接口调用失败，错误码：", sdk.NET_DVR_GetLastError())
                    break
                elif dw_state == HCNetSDK.NET_SDK_CONFIG_STATUS_NEED_WAIT:
                    print("配置等待")
                    time.sleep(10)
                    continue
                elif dw_state == HCNetSDK.NET_SDK_CONFIG_STATUS_FAILED:
                    print("查询人员失败")
                    break
                elif dw_state == HCNetSDK.NET_SDK_CONFIG_STATUS_EXCEPTION:
                    print("查询人员异常")
                    break
                elif dw_state == HCNetSDK.NET_SDK_CONFIG_STATUS_SUCCESS:
                    ptr_out_buff = ptr_out_buff.raw
                    print(ptr_out_buff.decode('utf-8').rstrip('\x00'))
                    print("查询人员成功, json:", ptr_out_buff.decode('utf-8').rstrip('\x00').strip())
                    break
                elif dw_state == HCNetSDK.NET_SDK_CONFIG_STATUS_FINISH:
                    print("获取人员完成")
                    break

            if not sdk.NET_DVR_StopRemoteConfig(l_handler):
                print("NET_DVR_StopRemoteConfig接口调用失败，错误码：", sdk.NET_DVR_GetLastError())
            else:
                print("NET_DVR_StopRemoteConfig接口成功")
                l_handler = -1

    @staticmethod
    def delete_user_info(user_id, sdk):
        delete_user_json = """{"UserInfoDetail":{"mode":"byEmployeeNo","EmployeeNoList":[{"employeeNo":"employeeNo1"}]}}"""
        # delete_user_json = "{\n" \
        #                    "\t\"UserInfoDetail\": {\t\n" \
        #                    "\t\t\"mode\":  \"all\",\t\n" \
        #                    "\t\t\"EmployeeNoList\": [\t\n" \
        #                    "\t\t]\n" \
        #                    "\n" \
        #                    "\t}\n" \
        #                    "}"

        delete_user_url = "PUT /ISAPI/AccessControl/UserInfoDetail/Delete?format=json"
        TransIsapi.put_isapi(user_id, delete_user_url, delete_user_json, sdk)

        while True:
            get_delete_process_url = "GET /ISAPI/AccessControl/UserInfoDetail/DeleteProcess?format=json"
            delete_result = TransIsapi.get_isapi(user_id, get_delete_process_url, sdk)
            # json_object = json.loads(delete_result)
            json_object1 = delete_result.get("UserInfoDetailDeleteProcess", {})
            process = json_object1.get("status", "")
            print("process =", process)

            if process == "processing":
                print("正在删除")
                continue
            elif process == "success":
                print("删除成功")
                break
            elif process == "failed":
                print("删除失败")
                break
