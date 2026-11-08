#!/usr/bin/env python3
# coding=utf-8

import ctypes
import os
import signal
import sys
import threading

import cv2
import numpy as np
import rospy
from cv_bridge import CvBridge
from sensor_msgs.msg import Image

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PACKAGE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))
WORKSPACE_SRC_DIR = os.path.abspath(os.path.join(PACKAGE_DIR, '..'))
DEFAULT_SDK_ROOT = os.path.join(WORKSPACE_SRC_DIR, 'HCNetSDKV6.1.11.5_build20251204_linux64_ZH')
DEFAULT_DEMO_DIR = os.path.join(
    DEFAULT_SDK_ROOT,
    'Demo示例',
    '3-Python开发示例',
    '1-预览取流解码Demo',
)

sys.path.insert(0, DEFAULT_DEMO_DIR)

from HCNetSDK import *  # noqa: E402,F401,F403
from PlayCtrl import *  # noqa: E402,F401,F403


class HikvisionCameraNode:
    def __init__(self):
        self.sdk_root = rospy.get_param('~sdk_root', DEFAULT_SDK_ROOT)
        self.sdk_lib_dir = rospy.get_param('~sdk_lib_dir', os.path.join(self.sdk_root, '库文件'))
        self.sdk_com_dir = rospy.get_param('~sdk_com_dir', os.path.join(self.sdk_lib_dir, 'HCNetSDKCom'))
        self.camera_ip = rospy.get_param('~camera_ip', '10.10.138.111')
        self.camera_port = int(rospy.get_param('~camera_port', 8000))
        self.camera_user = rospy.get_param('~camera_user', 'admin')
        self.camera_password = rospy.get_param('~camera_password', '')
        self.channel = int(rospy.get_param('~channel', 1))
        self.stream_type = int(rospy.get_param('~stream_type', 0))
        self.display = rospy.get_param('~display', True)
        self.topic = rospy.get_param('~topic', 'image_raw')
        self.frame_id = rospy.get_param('~frame_id', 'camera')

        self.publisher = rospy.Publisher(self.topic, Image, queue_size=1)
        self.bridge = CvBridge()
        self.lock = threading.Lock()
        self.real_play_handle = -1
        self.user_id = -1
        self.sdk_loaded = False
        self.play_port = ctypes.c_long(-1)
        self.decode_callback_ref = None
        self.realdata_callback_ref = None
        self.frame_count = 0

        self.objdll = None
        self.playctrldll = None

        self._validate_paths()
        self._load_libraries()
        self._configure_sdk_paths()
        self._initialize_sdk()
        self._login()
        self._start_preview()

        rospy.on_shutdown(self.shutdown)
        signal.signal(signal.SIGINT, self._signal_handler)
        rospy.loginfo('hikvision camera node started, publishing to %s', self.publisher.resolved_name)

    def _validate_paths(self):
        required = [
            self.sdk_root,
            self.sdk_lib_dir,
            self.sdk_com_dir,
            DEFAULT_DEMO_DIR,
        ]
        for path in required:
            if not os.path.exists(path):
                raise RuntimeError('required path not found: %s' % path)

    def _load_libraries(self):
        self.objdll = ctypes.cdll.LoadLibrary(os.path.join(self.sdk_lib_dir, 'libhcnetsdk.so'))
        self.playctrldll = ctypes.cdll.LoadLibrary(os.path.join(self.sdk_lib_dir, 'libPlayCtrl.so'))
        self.sdk_loaded = True

    def _configure_sdk_paths(self):
        sdk_path = NET_DVR_LOCAL_SDK_PATH()
        sdk_path.sPath = self.sdk_lib_dir.encode('utf-8')
        self.objdll.NET_DVR_SetSDKInitCfg(2, ctypes.byref(sdk_path))
        self.objdll.NET_DVR_SetSDKInitCfg(3, ctypes.create_string_buffer(os.path.join(self.sdk_lib_dir, 'libcrypto.so.3').encode('utf-8')))
        self.objdll.NET_DVR_SetSDKInitCfg(4, ctypes.create_string_buffer(os.path.join(self.sdk_lib_dir, 'libssl.so.3').encode('utf-8')))

    def _initialize_sdk(self):
        self.objdll.NET_DVR_Init()
        self.objdll.NET_DVR_SetConnectTime(2000, 1)
        self.objdll.NET_DVR_SetReconnect(10000, 1)
        log_dir = os.path.join(os.path.expanduser('~'), '.ros', 'hikvision_hcnetsdk_ros_logs')
        os.makedirs(log_dir, exist_ok=True)
        self.objdll.NET_DVR_SetLogToFile(3, log_dir.encode('utf-8'), False)
        if not self.playctrldll.PlayM4_GetPort(ctypes.byref(self.play_port)):
            raise RuntimeError('failed to allocate PlayM4 port')

    def _login(self):
        login_info = NET_DVR_USER_LOGIN_INFO()
        device_info = NET_DVR_DEVICEINFO_V40()
        login_info.sDeviceAddress = self.camera_ip.encode('utf-8')
        login_info.wPort = self.camera_port
        login_info.sUserName = self.camera_user.encode('utf-8')
        login_info.sPassword = self.camera_password.encode('utf-8')
        login_info.byUseTransport = 0
        login_info.bUseAsynLogin = 0
        login_info.byLoginMode = 0
        login_info.byHttps = 0
        login_info.byVerifyMode = 0
        self.objdll.NET_DVR_Login_V40.restype = ctypes.c_long
        self.user_id = self.objdll.NET_DVR_Login_V40(ctypes.byref(login_info), ctypes.byref(device_info))
        if self.user_id < 0:
            raise RuntimeError('login failed, error code: %s' % self.objdll.NET_DVR_GetLastError())
        rospy.loginfo('logged into camera %s:%s on user id %s', self.camera_ip, self.camera_port, self.user_id)

    def _start_preview(self):
        preview_info = NET_DVR_PREVIEWINFO()
        preview_info.hPlayWnd = 0
        preview_info.lChannel = self.channel
        preview_info.dwStreamType = self.stream_type
        preview_info.dwLinkMode = 0
        preview_info.bBlocked = 1
        self.realdata_callback_ref = REALDATACALLBACK(self._on_real_data)
        self.real_play_handle = self.objdll.NET_DVR_RealPlay_V40(self.user_id, ctypes.byref(preview_info), self.realdata_callback_ref, None)
        if self.real_play_handle < 0:
            raise RuntimeError('preview failed, error code: %s' % self.objdll.NET_DVR_GetLastError())
        rospy.loginfo('preview started on channel %s with handle %s', self.channel, self.real_play_handle)

    def _on_real_data(self, lPlayHandle, dwDataType, pBuffer, dwBufSize, pUser):
        if dwDataType == NET_DVR_SYSHEAD:
            with self.lock:
                self.playctrldll.PlayM4_SetStreamOpenMode(self.play_port, 0)
                if not self.playctrldll.PlayM4_OpenStream(self.play_port, pBuffer, dwBufSize, 1024 * 1024):
                    rospy.logerr_throttle(5.0, 'PlayM4_OpenStream failed: %s', self.playctrldll.PlayM4_GetLastError(self.play_port))
                    return
                self.playctrldll.PlayM4_SetDecodeEngine(self.play_port, 0)
                self.decode_callback_ref = DECCBFUNWIN(self._on_decoded_frame)
                self.playctrldll.PlayM4_SetDecCallBackExMend(self.play_port, self.decode_callback_ref, None, 0, None)
                if not self.playctrldll.PlayM4_Play(self.play_port, None):
                    rospy.logerr_throttle(5.0, 'PlayM4_Play failed: %s', self.playctrldll.PlayM4_GetLastError(self.play_port))
                    return
                rospy.loginfo('decode pipeline ready')
            return

        if dwDataType == NET_DVR_STREAMDATA:
            if not self.playctrldll.PlayM4_InputData(self.play_port, pBuffer, dwBufSize):
                rospy.logwarn_throttle(5.0, 'PlayM4_InputData failed: %s', self.playctrldll.PlayM4_GetLastError(self.play_port))
            return

    def _on_decoded_frame(self, nPort, pBuf, nSize, pFrameInfo, nUser, nReserved2):
        frame_info = pFrameInfo.contents
        width = int(frame_info.nWidth)
        height = int(frame_info.nHeight)
        frame_type = int(frame_info.nType)
        raw = ctypes.string_at(pBuf, nSize)

        image = None
        if frame_type == 3:
            yuv = np.frombuffer(raw, dtype=np.uint8)
            expected = width * height * 3 // 2
            if yuv.size < expected:
                rospy.logwarn_throttle(5.0, 'YV12 frame too small: %s < %s', yuv.size, expected)
                return
            yuv = yuv[:expected].reshape((height * 3 // 2, width))
            image = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR_YV12)
        elif frame_type == 7:
            bgra = np.frombuffer(raw, dtype=np.uint8)
            expected = width * height * 4
            if bgra.size < expected:
                rospy.logwarn_throttle(5.0, 'BGRA frame too small: %s < %s', bgra.size, expected)
                return
            bgra = bgra[:expected].reshape((height, width, 4))
            image = cv2.cvtColor(bgra, cv2.COLOR_BGRA2BGR)
        else:
            rospy.logwarn_throttle(10.0, 'unsupported decoded frame type: %s', frame_type)
            return

        if image is None:
            return

        message = self.bridge.cv2_to_imgmsg(image, encoding='bgr8')
        message.header.stamp = rospy.Time.now()
        message.header.frame_id = self.frame_id
        self.publisher.publish(message)

        if self.display:
            cv2.imshow('hikvision_camera', image)
            cv2.waitKey(1)

        self.frame_count += 1
        if self.frame_count % 100 == 0:
            rospy.loginfo('published %s frames', self.frame_count)

    def shutdown(self):
        with self.lock:
            if self.real_play_handle >= 0:
                self.objdll.NET_DVR_StopRealPlay(self.real_play_handle)
                self.real_play_handle = -1
            if self.play_port.value > -1:
                self.playctrldll.PlayM4_Stop(self.play_port)
                self.playctrldll.PlayM4_CloseStream(self.play_port)
                self.playctrldll.PlayM4_FreePort(self.play_port)
                self.play_port = ctypes.c_long(-1)
            if self.user_id >= 0:
                self.objdll.NET_DVR_Logout(self.user_id)
                self.user_id = -1
            if self.sdk_loaded:
                self.objdll.NET_DVR_Cleanup()
                self.sdk_loaded = False
        if self.display:
            cv2.destroyAllWindows()
        rospy.loginfo('hikvision camera node stopped')

    def _signal_handler(self, signum, frame):
        self.shutdown()
        raise SystemExit(0)


def main():
    rospy.init_node('hikvision_camera_node', anonymous=False)
    HikvisionCameraNode()
    rospy.spin()


if __name__ == '__main__':
    main()
