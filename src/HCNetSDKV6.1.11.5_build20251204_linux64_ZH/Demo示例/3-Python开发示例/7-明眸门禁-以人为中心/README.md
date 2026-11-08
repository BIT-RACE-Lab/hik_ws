# 目录分层结构说明



## 一、demo示例入口

HCNetACSTest.py示例代码入口

## 二、DevModule分产品类型的定义实现

##### 目前Demo实现
<ol>
<li>明眸门禁人员管理(工号)——增删改查 </li>
<li>明眸门禁人员管理(卡片)——增删改查</li>
<li>明眸门禁人员管理(人脸)——查询、二进制和URL方式下发、采集、删除</li>
<li>明眸门禁参数配置——获取（设置）门禁主机参数、获取门禁主机工作状态、远程控门</li>
</ol>

```
# 人员管理模块
    ACSUserManager.UserManage().search_user_info(UserID, sdk)     # 查询人员
    ACSUserManager.UserManage().add_user_info(UserID, '20231229', sdk)  # 添加修改人员
    ACSUserManager.UserManage().delete_user_info(UserID, sdk)   # 删除人员

# 卡号管理模块
    CardManage.search_card_info(UserID, "20231229", sdk)    # 查询指定工号人员的工卡信息
    CardManage.add_card_info(UserID, "20240103", sdk) # 添加工卡，参数为卡号
    CardManage.search_all_card_info(UserID, sdk)    # 查询所有工卡信息
    CardManage.delete_card_info(UserID, "20231229", sdk)  # 删除指定工号下人员的所有工卡
    CardManage.delete_all_card_info(UserID, sdk)  # 删除所有人员工卡
# 人脸管理模块
    FaceManage.search_face_info(UserID, "hik003", sdk)  # 查询人脸
    FaceManage.add_face_by_binary(UserID, "20240103", sdk)  # 按二进制方式下发人脸图片
    FaceManage.add_face_by_url(UserID, "20240103", sdk)     # 按URL方式下发人脸图片
    FaceManage.delete_face_info(UserID, "20240103", sdk)     # 删除人脸
    FaceManage.capture_face_info(UserID, sdk)       # 人脸采集
# 门禁管理模块
    ACSManage.acs_cfg(UserID, sdk)  # 获取(设置)门禁主机参数
    ACSManage.get_acs_status(UserID, sdk)  # 获取门禁主机工作状态
    ACSManage.remote_control_gate(UserID, sdk)  # 远程控门
```
