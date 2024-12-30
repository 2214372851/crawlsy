from rest_framework import serializers
from apps.User.models import (
    UserModel,
    RoleModel,
    PermissionModel,
    MenuModel,
    UserOperationLog,
)
from utils.verify import is_username, is_email, is_phone, is_password


class UserSerializer(serializers.ModelSerializer):
    """
    用户管理序列化器
    """

    createTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updateTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    lastLoginTime = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", read_only=True
    )
    role = serializers.PrimaryKeyRelatedField(
        many=True, queryset=RoleModel.objects, required=True
    )
    password = serializers.CharField(write_only=True)
    feishu_id = serializers.CharField(write_only=True, required=False, allow_blank=True)
    feishu = serializers.SerializerMethodField(read_only=True)

    def get_feishu(self, obj):
        return bool(obj.feishu_id)

    def validate_username(self, value):
        if not 30 > len(value) > 1:
            raise serializers.ValidationError("用户名长度必须在2到30个字符之间")

        if not is_username(value):
            raise serializers.ValidationError(
                "用户名应由中文字符、英文字母或下划线组成"
            )
        return value

    def validate_email(self, value):
        if len(value) > 40:
            raise serializers.ValidationError("邮箱号不能超过40个字符")
        if not is_email(value):
            raise serializers.ValidationError("邮箱号不合法")
        return value

    def validate_password(self, data):
        if not 6 < len(data) < 16:
            raise serializers.ValidationError("密码长度必须在6到16个字符之间")
        if not is_password(data):
            raise serializers.ValidationError(
                "密码必须包含大小写字母与数字,不能包含特殊字符"
            )
        return data

    def create(self, validated_data):
        validated_data["password"] = UserModel.make_password(validated_data["password"])
        user = super().create(validated_data=validated_data)
        user.save()
        return user

    def update(self, instance, validated_data):
        if "password" in validated_data:
            validated_data["password"] = UserModel.make_password(
                validated_data["password"]
            )
        instance = super().update(instance, validated_data)
        return instance

    class Meta:
        model = UserModel
        exclude = [
            "id",
        ]
        read_only_fields = ("uid",)


class UserOptionSerializer(serializers.ModelSerializer):
    """
    用户选项序列化器
    """

    class Meta:
        model = UserModel
        fields = ("id", "username")


class RoleSerializer(serializers.ModelSerializer):
    """
    角色管理序列化器
    """

    createTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updateTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    permissions = serializers.PrimaryKeyRelatedField(
        many=True, queryset=PermissionModel.objects, required=True
    )

    class Meta:
        model = RoleModel
        fields = "__all__"
        read_only_fields = ("id",)


class PermissionSerializer(serializers.ModelSerializer):
    """
    权限管理序列化器
    """

    createTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updateTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    menu = serializers.PrimaryKeyRelatedField(queryset=MenuModel.objects, required=True)

    class Meta:
        model = PermissionModel
        fields = "__all__"
        read_only_fields = ("id",)


class MenuSerializer(serializers.ModelSerializer):
    """
    菜单管理序列化器
    """

    createTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updateTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    parent = serializers.PrimaryKeyRelatedField(
        queryset=MenuModel.objects, required=False, allow_null=True
    )

    class Meta:
        model = MenuModel
        fields = "__all__"
        read_only_fields = ("id",)


class MenuOptionSerializer(serializers.ModelSerializer):
    """
    菜单选项序列化器
    """

    class Meta:
        model = MenuModel
        fields = ("id", "name")


class RoleOptionSerializer(serializers.ModelSerializer):
    """
    角色选项序列化器
    """

    class Meta:
        model = RoleModel
        fields = ("id", "name")


class PermissionOptionSerializer(serializers.ModelSerializer):
    """
    角色选项序列化器
    """

    class Meta:
        model = PermissionModel
        fields = ("id", "name")


class UserOperationLogSerializer(serializers.ModelSerializer):
    """
    用户操作日志序列化器
    """

    operation_time = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", read_only=True
    )
    user = serializers.SerializerMethodField(read_only=True)

    def get_user(self, obj):
        if not obj.user:
            return {"uid": None, "username": "无该用户"}
        return {"uid": obj.user.uid, "username": obj.user.username}
        # return obj.user.username if obj.user else "已删除用户"

    class Meta:
        model = UserOperationLog
        fields = [
            "id",
            "user",
            "operation_type",
            "description",
            "ip_address",
            "operation_time",
            "status",
        ]
        read_only_fields = ("id", "operation_time")
