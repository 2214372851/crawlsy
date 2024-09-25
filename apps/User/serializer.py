from rest_framework import serializers
from apps.User.models import UserModel, RoleModel, PermissionModel, MenuModel
from utils.verify import is_username, is_email, is_phone, is_password


class UserSerializer(serializers.ModelSerializer):
    """
    用户管理序列化器
    """
    createTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updateTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    role = serializers.PrimaryKeyRelatedField(many=True, queryset=RoleModel.objects, required=True)
    password = serializers.CharField(write_only=True)

    def validate_username(self, value):
        if not 30 > len(value) > 1:
            raise serializers.ValidationError('用户名长度必须在2到30个字符之间')

        if not is_username(value):
            raise serializers.ValidationError('用户名应由中文字符、英文字母或下划线组成')
        return value

    def validate_email(self, value):
        if len(value) > 40:
            raise serializers.ValidationError('邮箱号不能超过40个字符')
        if not is_email(value):
            raise serializers.ValidationError('邮箱号不合法')
        return value

    def validate_password(self, data):
        if not 6 < len(data) < 16:
            raise serializers.ValidationError('密码长度必须在6到16个字符之间')
        if not is_password(data):
            raise serializers.ValidationError('密码必须包含大小写字母与数字,不能包含特殊字符')
        return data

    def create(self, validated_data):
        validated_data['password'] = UserModel.make_password(validated_data['password'])
        user = super().create(validated_data=validated_data)
        user.save()
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = UserModel.make_password(validated_data['password'])
        instance = super().update(instance, validated_data)
        return instance

    class Meta:
        model = UserModel
        exclude = ['id', ]
        read_only_fields = ('uid',)


class RoleSerializer(serializers.ModelSerializer):
    """
    角色管理序列化器
    """
    createTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updateTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    permissions = serializers.PrimaryKeyRelatedField(many=True, queryset=PermissionModel.objects, required=True)

    class Meta:
        model = RoleModel
        fields = '__all__'
        read_only_fields = ('id',)


class PermissionSerializer(serializers.ModelSerializer):
    """
    权限管理序列化器
    """
    createTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updateTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    menu = serializers.PrimaryKeyRelatedField(queryset=MenuModel.objects, required=True)

    class Meta:
        model = PermissionModel
        fields = '__all__'
        read_only_fields = ('id',)


class MenuSerializer(serializers.ModelSerializer):
    """
    菜单管理序列化器
    """
    createTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updateTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    parent = serializers.PrimaryKeyRelatedField(queryset=MenuModel.objects, required=False, allow_null=True)

    class Meta:
        model = MenuModel
        fields = '__all__'
        read_only_fields = ('id',)
