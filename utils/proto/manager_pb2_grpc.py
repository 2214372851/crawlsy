# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
import utils.proto.manager_pb2 as manager__pb2

GRPC_GENERATED_VERSION = '1.67.1'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in manager_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class SpiderNodeServiceStub(object):
    """定义服务
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.TasksStatus = channel.unary_unary(
                '/spider_node.SpiderNodeService/TasksStatus',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=manager__pb2.TaskResponse.FromString,
                _registered_method=True)
        self.TaskStatus = channel.unary_unary(
                '/spider_node.SpiderNodeService/TaskStatus',
                request_serializer=manager__pb2.TaskStatusRequest.SerializeToString,
                response_deserializer=manager__pb2.TaskResponse.FromString,
                _registered_method=True)
        self.TaskStart = channel.unary_unary(
                '/spider_node.SpiderNodeService/TaskStart',
                request_serializer=manager__pb2.TaskStartRequest.SerializeToString,
                response_deserializer=manager__pb2.TaskResponse.FromString,
                _registered_method=True)
        self.TaskDelete = channel.unary_unary(
                '/spider_node.SpiderNodeService/TaskDelete',
                request_serializer=manager__pb2.TaskDeleteRequest.SerializeToString,
                response_deserializer=manager__pb2.TaskResponse.FromString,
                _registered_method=True)
        self.TaskReload = channel.unary_unary(
                '/spider_node.SpiderNodeService/TaskReload',
                request_serializer=manager__pb2.TaskReloadRequest.SerializeToString,
                response_deserializer=manager__pb2.TaskResponse.FromString,
                _registered_method=True)
        self.TaskLogsOpen = channel.unary_unary(
                '/spider_node.SpiderNodeService/TaskLogsOpen',
                request_serializer=manager__pb2.TaskLogsOpenRequest.SerializeToString,
                response_deserializer=manager__pb2.TaskResponse.FromString,
                _registered_method=True)
        self.TaskLogsClose = channel.unary_unary(
                '/spider_node.SpiderNodeService/TaskLogsClose',
                request_serializer=manager__pb2.TaskLogsCloseRequest.SerializeToString,
                response_deserializer=manager__pb2.TaskResponse.FromString,
                _registered_method=True)
        self.PipList = channel.unary_unary(
                '/spider_node.SpiderNodeService/PipList',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=manager__pb2.TaskResponse.FromString,
                _registered_method=True)
        self.PipInstall = channel.unary_unary(
                '/spider_node.SpiderNodeService/PipInstall',
                request_serializer=manager__pb2.PipRequest.SerializeToString,
                response_deserializer=manager__pb2.TaskResponse.FromString,
                _registered_method=True)
        self.PipUninstall = channel.unary_unary(
                '/spider_node.SpiderNodeService/PipUninstall',
                request_serializer=manager__pb2.PipRequest.SerializeToString,
                response_deserializer=manager__pb2.TaskResponse.FromString,
                _registered_method=True)
        self.PipUpdate = channel.unary_unary(
                '/spider_node.SpiderNodeService/PipUpdate',
                request_serializer=manager__pb2.PipRequest.SerializeToString,
                response_deserializer=manager__pb2.TaskResponse.FromString,
                _registered_method=True)
        self.ExtendUpdate = channel.unary_unary(
                '/spider_node.SpiderNodeService/ExtendUpdate',
                request_serializer=manager__pb2.ExtendUpdateRequest.SerializeToString,
                response_deserializer=manager__pb2.TaskResponse.FromString,
                _registered_method=True)
        self.ResultWrite = channel.unary_unary(
                '/spider_node.SpiderNodeService/ResultWrite',
                request_serializer=manager__pb2.ResultWriteRequest.SerializeToString,
                response_deserializer=manager__pb2.TaskResponse.FromString,
                _registered_method=True)


class SpiderNodeServiceServicer(object):
    """定义服务
    """

    def TasksStatus(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def TaskStatus(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def TaskStart(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def TaskDelete(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def TaskReload(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def TaskLogsOpen(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def TaskLogsClose(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def PipList(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def PipInstall(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def PipUninstall(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def PipUpdate(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ExtendUpdate(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ResultWrite(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_SpiderNodeServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'TasksStatus': grpc.unary_unary_rpc_method_handler(
                    servicer.TasksStatus,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=manager__pb2.TaskResponse.SerializeToString,
            ),
            'TaskStatus': grpc.unary_unary_rpc_method_handler(
                    servicer.TaskStatus,
                    request_deserializer=manager__pb2.TaskStatusRequest.FromString,
                    response_serializer=manager__pb2.TaskResponse.SerializeToString,
            ),
            'TaskStart': grpc.unary_unary_rpc_method_handler(
                    servicer.TaskStart,
                    request_deserializer=manager__pb2.TaskStartRequest.FromString,
                    response_serializer=manager__pb2.TaskResponse.SerializeToString,
            ),
            'TaskDelete': grpc.unary_unary_rpc_method_handler(
                    servicer.TaskDelete,
                    request_deserializer=manager__pb2.TaskDeleteRequest.FromString,
                    response_serializer=manager__pb2.TaskResponse.SerializeToString,
            ),
            'TaskReload': grpc.unary_unary_rpc_method_handler(
                    servicer.TaskReload,
                    request_deserializer=manager__pb2.TaskReloadRequest.FromString,
                    response_serializer=manager__pb2.TaskResponse.SerializeToString,
            ),
            'TaskLogsOpen': grpc.unary_unary_rpc_method_handler(
                    servicer.TaskLogsOpen,
                    request_deserializer=manager__pb2.TaskLogsOpenRequest.FromString,
                    response_serializer=manager__pb2.TaskResponse.SerializeToString,
            ),
            'TaskLogsClose': grpc.unary_unary_rpc_method_handler(
                    servicer.TaskLogsClose,
                    request_deserializer=manager__pb2.TaskLogsCloseRequest.FromString,
                    response_serializer=manager__pb2.TaskResponse.SerializeToString,
            ),
            'PipList': grpc.unary_unary_rpc_method_handler(
                    servicer.PipList,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=manager__pb2.TaskResponse.SerializeToString,
            ),
            'PipInstall': grpc.unary_unary_rpc_method_handler(
                    servicer.PipInstall,
                    request_deserializer=manager__pb2.PipRequest.FromString,
                    response_serializer=manager__pb2.TaskResponse.SerializeToString,
            ),
            'PipUninstall': grpc.unary_unary_rpc_method_handler(
                    servicer.PipUninstall,
                    request_deserializer=manager__pb2.PipRequest.FromString,
                    response_serializer=manager__pb2.TaskResponse.SerializeToString,
            ),
            'PipUpdate': grpc.unary_unary_rpc_method_handler(
                    servicer.PipUpdate,
                    request_deserializer=manager__pb2.PipRequest.FromString,
                    response_serializer=manager__pb2.TaskResponse.SerializeToString,
            ),
            'ExtendUpdate': grpc.unary_unary_rpc_method_handler(
                    servicer.ExtendUpdate,
                    request_deserializer=manager__pb2.ExtendUpdateRequest.FromString,
                    response_serializer=manager__pb2.TaskResponse.SerializeToString,
            ),
            'ResultWrite': grpc.unary_unary_rpc_method_handler(
                    servicer.ResultWrite,
                    request_deserializer=manager__pb2.ResultWriteRequest.FromString,
                    response_serializer=manager__pb2.TaskResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'spider_node.SpiderNodeService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('spider_node.SpiderNodeService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class SpiderNodeService(object):
    """定义服务
    """

    @staticmethod
    def TasksStatus(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/spider_node.SpiderNodeService/TasksStatus',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            manager__pb2.TaskResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def TaskStatus(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/spider_node.SpiderNodeService/TaskStatus',
            manager__pb2.TaskStatusRequest.SerializeToString,
            manager__pb2.TaskResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def TaskStart(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/spider_node.SpiderNodeService/TaskStart',
            manager__pb2.TaskStartRequest.SerializeToString,
            manager__pb2.TaskResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def TaskDelete(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/spider_node.SpiderNodeService/TaskDelete',
            manager__pb2.TaskDeleteRequest.SerializeToString,
            manager__pb2.TaskResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def TaskReload(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/spider_node.SpiderNodeService/TaskReload',
            manager__pb2.TaskReloadRequest.SerializeToString,
            manager__pb2.TaskResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def TaskLogsOpen(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/spider_node.SpiderNodeService/TaskLogsOpen',
            manager__pb2.TaskLogsOpenRequest.SerializeToString,
            manager__pb2.TaskResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def TaskLogsClose(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/spider_node.SpiderNodeService/TaskLogsClose',
            manager__pb2.TaskLogsCloseRequest.SerializeToString,
            manager__pb2.TaskResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def PipList(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/spider_node.SpiderNodeService/PipList',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            manager__pb2.TaskResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def PipInstall(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/spider_node.SpiderNodeService/PipInstall',
            manager__pb2.PipRequest.SerializeToString,
            manager__pb2.TaskResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def PipUninstall(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/spider_node.SpiderNodeService/PipUninstall',
            manager__pb2.PipRequest.SerializeToString,
            manager__pb2.TaskResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def PipUpdate(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/spider_node.SpiderNodeService/PipUpdate',
            manager__pb2.PipRequest.SerializeToString,
            manager__pb2.TaskResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def ExtendUpdate(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/spider_node.SpiderNodeService/ExtendUpdate',
            manager__pb2.ExtendUpdateRequest.SerializeToString,
            manager__pb2.TaskResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def ResultWrite(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/spider_node.SpiderNodeService/ResultWrite',
            manager__pb2.ResultWriteRequest.SerializeToString,
            manager__pb2.TaskResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)