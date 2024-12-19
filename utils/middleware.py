import json
from django.http.response import re
from django.utils.deprecation import MiddlewareMixin
from apps.User.models import UserOperationLog


class UserOperationLogMiddleware(MiddlewareMixin):
    """
    用户操作日志中间件
    """

    EXCLUDE_PATHS = [
        "/api/user/operation-log",  # 排除操作日志相关接口，避免无限递归
        "/api/docs",  # 排除文档相关接口
        "/api/schema",
    ]

    def should_log_request(self, request):
        """
        判断是否需要记录该请求
        """
        path = request.path_info
        # 排除特定路径
        if any(path.startswith(exclude_path) for exclude_path in self.EXCLUDE_PATHS):
            return False
        # 排除OPTIONS请求
        if request.method == "OPTIONS":
            return False
        # 排查GET请求
        if request.method == "GET":
            return False
        return True

    def get_client_ip(self, request):
        """
        获取客户端IP地址
        """
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR", "")

    def get_request_body(self, request):
        """
        获取请求体内容
        """
        try:
            if request.body:
                body = json.loads(request.body)
                # 移除敏感信息
                if isinstance(body, dict):
                    body = body.copy()
                    for key in ["password", "token", "access", "refresh"]:
                        if key in body:
                            body[key] = "******"
                return body
            return {}
        except json.JSONDecodeError:
            return {}

    def process_response(self, request, response):
        """
        在返回响应时记录操作日志
        """
        if not self.should_log_request(request):
            return response

        # 获取用户信息
        user = request.user if hasattr(request, "user") else None
        if not user:
            return response

        try:
            # 获取视图函数名称
            view_func = (
                request.resolver_match.func
                if hasattr(request, "resolver_match")
                else None
            )
            operation_type = (
                f"{request.method}_{view_func.__name__}"
                if hasattr(view_func, "__name__")
                else request.method
            )

            # 构建操作描述
            description_parts = [
                f"Path: {request.path_info}",
                f"Method: {request.method}",
                f"Query Params: {dict(request.GET.items())}",
            ]

            # 对于POST/PUT请求，记录请求体
            if request.method in ["POST", "PUT", "PATCH"]:
                body = self.get_request_body(request)
                if body:
                    description_parts.append(f"Body: {body}")

            # 记录响应状态码
            description_parts.append(f"Status: {response.status_code}")

            # 如果响应不成功，尝试获取错误信息
            if response.status_code >= 400:
                try:
                    response_data = json.loads(response.content.decode())
                    if isinstance(response_data, dict) and "detail" in response_data:
                        description_parts.append(f"Error: {response_data['detail']}")
                except:
                    pass

            description = " | ".join(description_parts)
            print(description)

            # 创建操作日志
            UserOperationLog.objects.create(
                user=user,
                operation_type=operation_type,
                description=description,
                ip_address=self.get_client_ip(request),
                status=response.status_code < 400,  # 根据状态码判断是否成功
            )
        except Exception as e:
            print(f"Failed to create operation log: {str(e)}")

        return response
