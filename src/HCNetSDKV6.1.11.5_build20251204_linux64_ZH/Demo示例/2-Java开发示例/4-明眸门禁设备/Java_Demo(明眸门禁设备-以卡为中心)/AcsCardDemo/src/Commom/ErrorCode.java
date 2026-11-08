package Commom;

/**
 * @Author: jiangxin14
 * @Date: 2024-08-09  14:13
 */

public enum ErrorCode {
        NET_ERR_TIME_OVERLAP(1900, "时间段重叠"),
        NET_ERR_HOLIDAY_PLAN_OVERLAP(1901, "假日计划重叠"),
        NET_ERR_CARDNO_NOT_SORT(1902, "卡号未排序"),
        NET_ERR_CARDNO_NOT_EXIST(1903, "卡号不存在"),
        NET_ERR_ILLEGAL_CARDNO(1904, "卡号错误"),
        NET_ERR_ZONE_ALARM(1905, "防区处于布防状态(参数修改不允许)"),
        NET_ERR_NOT_SUPPORT_ONE_MORE_CARD ( 1920,"不支持一人多卡"),
        NET_ERR_DELETE_NO_EXISTENCE_FACE(1921,"删除的人脸不存在"),
        NET_ERR_OFFLINE_CAPTURING(1929, "离线采集中，无法响应"),
        NET_DVR_ERR_OUTDOOR_COMMUNICATION(1950, "与门口机通信异常"),
        NET_DVR_ERR_ROOMNO_UNDEFINED(1951, "未设置房间号"),
        NET_DVR_ERR_NO_CALLING(1952, "无呼叫"),
        NET_DVR_ERR_RINGING(1953, "响铃"),
        NET_DVR_ERR_IS_CALLING_NOW(1954, "正在通话"),
        NET_DVR_ERR_LOCK_PASSWORD_WRONG(1955, "智能锁密码错误"),
        NET_DVR_ERR_CONTROL_LOCK_FAILURE(1956, "开关锁失败"),
        NET_DVR_ERR_CONTROL_LOCK_OVERTIME(1957, "开关锁超时"),
        NET_DVR_ERR_LOCK_DEVICE_BUSY(1958, "智能锁设备繁忙"),
        NET_DVR_ERR_UNOPEN_REMOTE_LOCK_FUNCTION(1959, "远程开锁功能未打开");




        private final int code;
        private final String description;

        ErrorCode(int code, String description) {
            this.code = code;
            this.description = description;
        }

        public int getCode() {
            return code;
        }

        public String getDescription() {
            return description;
        }

        // 根据错误码获取描述的方法
        public static String getDescription(int code) {
            for (ErrorCode errorCode : ErrorCode.values()) {
                if (errorCode.getCode() == code) {
                    return errorCode.getDescription();
                }
            }
            return "未知错误码";
        }
    }


