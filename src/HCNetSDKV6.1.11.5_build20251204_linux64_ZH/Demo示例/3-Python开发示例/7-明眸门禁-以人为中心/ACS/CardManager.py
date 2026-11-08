import json
import time
import HCNetACSTest
import HCNetSDK
from ACS.TransIsapi import TransIsapi
from ctypes import *


class CardManage:
    @staticmethod
    def add_card_info(user_id, card_no, sdk):
        ptr_byte_array = create_string_buffer(1024)
        str_in_buffer = "POST /ISAPI/AccessControl/CardInfo/Record?format=json"
        ptr_byte_array.value = str_in_buffer.encode('utf-8')

        l_handler = sdk.NET_DVR_StartRemoteConfig(user_id, HCNetSDK.NET_DVR_JSON_CONFIG,
                                                  byref(ptr_byte_array), len(str_in_buffer),
                                                  None, None)
        if l_handler < 0:
            print("AddCardInfo NET_DVR_StartRemoteConfig failed, error code:", sdk.NET_DVR_GetLastError())
            return
        else:
            print("AddCardInfo NET_DVR_StartRemoteConfig successful!")

            str_json_data = """{"CardInfo": {"employeeNo": "employeeNo1","cardNo": "%s","cardType": "normalCard"}}""" % card_no
            print(str_json_data)
            str_in_buff = json.dumps(str_json_data)
            ptr_in_buff = create_string_buffer(str_in_buff.encode('utf-8'))
            ptr_in_buff.value = str_json_data.encode('utf-8')
            ptr_output = create_string_buffer(1024)
            p_int = c_ulong()
            while True:
                dw_state = sdk.NET_DVR_SendWithRecvRemoteConfig(l_handler, byref(ptr_in_buff),
                                                                len(str_in_buff), byref(ptr_output),
                                                                1024, byref(p_int))
                ptr_output = ptr_output.raw
                str_result = ptr_output.decode('utf-8').rstrip('\x00').strip()
                print(str_result)
                print("dw_state:", dw_state, ", str_result:", str_result)

                json_result = json.loads(str_result)
                status_code = json_result.get("statusCode")
                status_string = json_result.get("statusString")

                if dw_state == -1:
                    print("NET_DVR_SendWithRecvRemoteConfig failed, error code:",
                          sdk.NET_DVR_GetLastError())
                    break
                elif dw_state == HCNetSDK.NET_SDK_CONFIG_STATUS_NEED_WAIT:
                    print("Configuration waiting")
                    time.sleep(10)
                    continue
                elif dw_state == HCNetSDK.NET_SDK_CONFIG_STATUS_FAILED:
                    print("Failed to add card, json return:", json_result)
                    break
                elif dw_state == HCNetSDK.NET_SDK_CONFIG_STATUS_EXCEPTION:
                    print("Exception while adding card, json return:", json_result)
                    break
                elif dw_state == HCNetSDK.NET_SDK_CONFIG_STATUS_SUCCESS:
                    if status_code != 1:
                        print("Successful card addition, but with exceptions:", json_result)
                    else:
                        print("Successful card addition, json return:", json_result)
                    break
                elif dw_state == HCNetSDK.NET_SDK_CONFIG_STATUS_FINISH:
                    print("Card addition complete")
                    break

            if not sdk.NET_DVR_StopRemoteConfig(l_handler):
                print("NET_DVR_StopRemoteConfig failed, error code:", sdk.NET_DVR_GetLastError())
            else:
                print("NET_DVR_StopRemoteConfig successful")

    @staticmethod
    def search_card_info(user_id, employee_no, sdk):
        search_card_info_url = "POST /ISAPI/AccessControl/CardInfo/Search?format=json"
        search_card_info_json = f"""{{
            "CardInfoSearchCond": {{
                "searchID": "20231229001",
                "searchResultPosition": 0,
                "maxResults": 30,
                "EmployeeNoList": [
                    {{
                        "employeeNo": "{employee_no}"
                    }}
                ]
            }}
        }}"""
        result = TransIsapi.put_isapi(user_id, search_card_info_url, search_card_info_json, sdk)
        print(result)

    @staticmethod
    def search_all_card_info(user_id, sdk):
        search_card_info_url = "POST /ISAPI/AccessControl/CardInfo/Search?format=json"
        search_card_info_json = """{
            "CardInfoSearchCond": {
                "searchID": "20231229001",
                "searchResultPosition": 0,
                "maxResults": 30
            }
        }"""
        result = TransIsapi.put_isapi(user_id, search_card_info_url, search_card_info_json, sdk)
        print(result)

    @staticmethod
    def delete_card_info(user_id, employee_no, sdk):
        delete_card_info_url = "PUT /ISAPI/AccessControl/CardInfo/Delete?format=json "
        delete_card_info_json = f"""{{
            "CardInfoDelCond": {{
                "EmployeeNoList": [
                    {{
                        "employeeNo": "{employee_no}"
                    }}
                ]
            }}
        }}"""
        result = TransIsapi.put_isapi(user_id, delete_card_info_url, delete_card_info_json, sdk)
        print(result)

    @staticmethod
    def delete_all_card_info(user_id, sdk):
        delete_all_card_info_url = "PUT /ISAPI/AccessControl/CardInfo/Delete?format=json"
        delete_all_card_info_json = """{"CardInfoDelCond": {}}"""
        result = TransIsapi.put_isapi(user_id, delete_all_card_info_url, delete_all_card_info_json, sdk)
        print(result)

    @staticmethod
    def get_all_card_number(user_id, sdk):
        get_all_card_number_url = "GET /ISAPI/AccessControl/CardInfo/Count?format=json"
        result = TransIsapi.get_isapi(user_id, get_all_card_number_url, sdk)
        num = result['CardInfoCount']['cardNumber']
        return str(num)
