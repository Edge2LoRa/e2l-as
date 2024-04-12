# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import e2l_module.__private__.demo_pb2 as demo__pb2


class GRPCDemoStub(object):
    """`service` 是用来给gRPC服务定义方法的, 格式固定, 类似于Golang中定义一个接口
    `service` is used to define methods for gRPC services in a fixed format, similar to defining
    an interface in Golang
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SimpleMethod = channel.unary_unary(
                '/demo.GRPCDemo/SimpleMethod',
                request_serializer=demo__pb2.Request.SerializeToString,
                response_deserializer=demo__pb2.Response.FromString,
                )
        self.ClientStreamingMethod = channel.stream_unary(
                '/demo.GRPCDemo/ClientStreamingMethod',
                request_serializer=demo__pb2.Request.SerializeToString,
                response_deserializer=demo__pb2.Response.FromString,
                )
        self.ServerStreamingMethod = channel.unary_stream(
                '/demo.GRPCDemo/ServerStreamingMethod',
                request_serializer=demo__pb2.Request.SerializeToString,
                response_deserializer=demo__pb2.Response.FromString,
                )
        self.BidirectionalStreamingMethod = channel.stream_stream(
                '/demo.GRPCDemo/BidirectionalStreamingMethod',
                request_serializer=demo__pb2.Request.SerializeToString,
                response_deserializer=demo__pb2.Response.FromString,
                )
        self.SimpleMethodsStatistics = channel.unary_unary(
                '/demo.GRPCDemo/SimpleMethodsStatistics',
                request_serializer=demo__pb2.SendStatistics.SerializeToString,
                response_deserializer=demo__pb2.ReplyStatistics.FromString,
                )
        self.ClientStreamingMethodStatistics = channel.stream_unary(
                '/demo.GRPCDemo/ClientStreamingMethodStatistics',
                request_serializer=demo__pb2.SendStatistics.SerializeToString,
                response_deserializer=demo__pb2.ReplyStatistics.FromString,
                )
        self.ServerStreamingMethodStatistics = channel.unary_stream(
                '/demo.GRPCDemo/ServerStreamingMethodStatistics',
                request_serializer=demo__pb2.SendStatistics.SerializeToString,
                response_deserializer=demo__pb2.ReplyStatistics.FromString,
                )
        self.BidirectionalStreamingMethodStatistics = channel.stream_stream(
                '/demo.GRPCDemo/BidirectionalStreamingMethodStatistics',
                request_serializer=demo__pb2.SendStatistics.SerializeToString,
                response_deserializer=demo__pb2.ReplyStatistics.FromString,
                )
        self.SimpleMethodsJoinUpdateMessage = channel.unary_unary(
                '/demo.GRPCDemo/SimpleMethodsJoinUpdateMessage',
                request_serializer=demo__pb2.SendJoinUpdateMessage.SerializeToString,
                response_deserializer=demo__pb2.ReplyJoinUpdateMessage.FromString,
                )
        self.SimpleMethodsLogMessage = channel.unary_unary(
                '/demo.GRPCDemo/SimpleMethodsLogMessage',
                request_serializer=demo__pb2.SendLogMessage.SerializeToString,
                response_deserializer=demo__pb2.ReplyLogMessage.FromString,
                )
        self.SimpleMethodsLogED = channel.unary_unary(
                '/demo.GRPCDemo/SimpleMethodsLogED',
                request_serializer=demo__pb2.SendLogED.SerializeToString,
                response_deserializer=demo__pb2.ReplyLogED.FromString,
                )
        self.SimpleMethodsLogGW = channel.unary_unary(
                '/demo.GRPCDemo/SimpleMethodsLogGW',
                request_serializer=demo__pb2.SendLogGW.SerializeToString,
                response_deserializer=demo__pb2.ReplyLogGW.FromString,
                )
        self.SimpleMethodsLogDM = channel.unary_unary(
                '/demo.GRPCDemo/SimpleMethodsLogDM',
                request_serializer=demo__pb2.SendLogDM.SerializeToString,
                response_deserializer=demo__pb2.ReplyLogDM.FromString,
                )


class GRPCDemoServicer(object):
    """`service` 是用来给gRPC服务定义方法的, 格式固定, 类似于Golang中定义一个接口
    `service` is used to define methods for gRPC services in a fixed format, similar to defining
    an interface in Golang
    """

    def SimpleMethod(self, request, context):
        """unary-unary(In a single call, the client can only send request once, and the server can
        only respond once.)
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ClientStreamingMethod(self, request_iterator, context):
        """stream-unary (In a single call, the client can transfer data to the server several times,
        but the server can only return a response once.)
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ServerStreamingMethod(self, request, context):
        """unary-stream (In a single call, the client can only transmit data to the server at one time,
        but the server can return the response many times.)
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def BidirectionalStreamingMethod(self, request_iterator, context):
        """stream-stream (In a single call, both client and server can send and receive data
        to each other multiple times.)
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SimpleMethodsStatistics(self, request, context):
        """unary-unary(In a single call, the client can only send request once, and the server can
        only respond once.)
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ClientStreamingMethodStatistics(self, request_iterator, context):
        """stream-unary (In a single call, the client can transfer data to the server several times,
        but the server can only return a response once.)
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ServerStreamingMethodStatistics(self, request, context):
        """unary-stream (In a single call, the client can only transmit data to the server at one time,
        but the server can return the response many times.)
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def BidirectionalStreamingMethodStatistics(self, request_iterator, context):
        """stream-stream (In a single call, both client and server can send and receive data
        to each other multiple times.)
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SimpleMethodsJoinUpdateMessage(self, request, context):
        """unary-unary(In a single call, the client can only send request once, and the server can
        only respond once.)
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SimpleMethodsLogMessage(self, request, context):
        """unary-unary(In a single call, the client can only send request once, and the server can
        only respond once.)
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SimpleMethodsLogED(self, request, context):
        """unary-unary(In a single call, the client can only send request once, and the server can
        only respond once.)
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SimpleMethodsLogGW(self, request, context):
        """unary-unary(In a single call, the client can only send request once, and the server can
        only respond once.)
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SimpleMethodsLogDM(self, request, context):
        """unary-unary(In a single call, the client can only send request once, and the server can
        only respond once.)
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_GRPCDemoServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SimpleMethod': grpc.unary_unary_rpc_method_handler(
                    servicer.SimpleMethod,
                    request_deserializer=demo__pb2.Request.FromString,
                    response_serializer=demo__pb2.Response.SerializeToString,
            ),
            'ClientStreamingMethod': grpc.stream_unary_rpc_method_handler(
                    servicer.ClientStreamingMethod,
                    request_deserializer=demo__pb2.Request.FromString,
                    response_serializer=demo__pb2.Response.SerializeToString,
            ),
            'ServerStreamingMethod': grpc.unary_stream_rpc_method_handler(
                    servicer.ServerStreamingMethod,
                    request_deserializer=demo__pb2.Request.FromString,
                    response_serializer=demo__pb2.Response.SerializeToString,
            ),
            'BidirectionalStreamingMethod': grpc.stream_stream_rpc_method_handler(
                    servicer.BidirectionalStreamingMethod,
                    request_deserializer=demo__pb2.Request.FromString,
                    response_serializer=demo__pb2.Response.SerializeToString,
            ),
            'SimpleMethodsStatistics': grpc.unary_unary_rpc_method_handler(
                    servicer.SimpleMethodsStatistics,
                    request_deserializer=demo__pb2.SendStatistics.FromString,
                    response_serializer=demo__pb2.ReplyStatistics.SerializeToString,
            ),
            'ClientStreamingMethodStatistics': grpc.stream_unary_rpc_method_handler(
                    servicer.ClientStreamingMethodStatistics,
                    request_deserializer=demo__pb2.SendStatistics.FromString,
                    response_serializer=demo__pb2.ReplyStatistics.SerializeToString,
            ),
            'ServerStreamingMethodStatistics': grpc.unary_stream_rpc_method_handler(
                    servicer.ServerStreamingMethodStatistics,
                    request_deserializer=demo__pb2.SendStatistics.FromString,
                    response_serializer=demo__pb2.ReplyStatistics.SerializeToString,
            ),
            'BidirectionalStreamingMethodStatistics': grpc.stream_stream_rpc_method_handler(
                    servicer.BidirectionalStreamingMethodStatistics,
                    request_deserializer=demo__pb2.SendStatistics.FromString,
                    response_serializer=demo__pb2.ReplyStatistics.SerializeToString,
            ),
            'SimpleMethodsJoinUpdateMessage': grpc.unary_unary_rpc_method_handler(
                    servicer.SimpleMethodsJoinUpdateMessage,
                    request_deserializer=demo__pb2.SendJoinUpdateMessage.FromString,
                    response_serializer=demo__pb2.ReplyJoinUpdateMessage.SerializeToString,
            ),
            'SimpleMethodsLogMessage': grpc.unary_unary_rpc_method_handler(
                    servicer.SimpleMethodsLogMessage,
                    request_deserializer=demo__pb2.SendLogMessage.FromString,
                    response_serializer=demo__pb2.ReplyLogMessage.SerializeToString,
            ),
            'SimpleMethodsLogED': grpc.unary_unary_rpc_method_handler(
                    servicer.SimpleMethodsLogED,
                    request_deserializer=demo__pb2.SendLogED.FromString,
                    response_serializer=demo__pb2.ReplyLogED.SerializeToString,
            ),
            'SimpleMethodsLogGW': grpc.unary_unary_rpc_method_handler(
                    servicer.SimpleMethodsLogGW,
                    request_deserializer=demo__pb2.SendLogGW.FromString,
                    response_serializer=demo__pb2.ReplyLogGW.SerializeToString,
            ),
            'SimpleMethodsLogDM': grpc.unary_unary_rpc_method_handler(
                    servicer.SimpleMethodsLogDM,
                    request_deserializer=demo__pb2.SendLogDM.FromString,
                    response_serializer=demo__pb2.ReplyLogDM.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'demo.GRPCDemo', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class GRPCDemo(object):
    """`service` 是用来给gRPC服务定义方法的, 格式固定, 类似于Golang中定义一个接口
    `service` is used to define methods for gRPC services in a fixed format, similar to defining
    an interface in Golang
    """

    @staticmethod
    def SimpleMethod(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/demo.GRPCDemo/SimpleMethod',
            demo__pb2.Request.SerializeToString,
            demo__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ClientStreamingMethod(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_unary(request_iterator, target, '/demo.GRPCDemo/ClientStreamingMethod',
            demo__pb2.Request.SerializeToString,
            demo__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ServerStreamingMethod(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/demo.GRPCDemo/ServerStreamingMethod',
            demo__pb2.Request.SerializeToString,
            demo__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def BidirectionalStreamingMethod(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(request_iterator, target, '/demo.GRPCDemo/BidirectionalStreamingMethod',
            demo__pb2.Request.SerializeToString,
            demo__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SimpleMethodsStatistics(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/demo.GRPCDemo/SimpleMethodsStatistics',
            demo__pb2.SendStatistics.SerializeToString,
            demo__pb2.ReplyStatistics.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ClientStreamingMethodStatistics(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_unary(request_iterator, target, '/demo.GRPCDemo/ClientStreamingMethodStatistics',
            demo__pb2.SendStatistics.SerializeToString,
            demo__pb2.ReplyStatistics.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ServerStreamingMethodStatistics(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/demo.GRPCDemo/ServerStreamingMethodStatistics',
            demo__pb2.SendStatistics.SerializeToString,
            demo__pb2.ReplyStatistics.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def BidirectionalStreamingMethodStatistics(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(request_iterator, target, '/demo.GRPCDemo/BidirectionalStreamingMethodStatistics',
            demo__pb2.SendStatistics.SerializeToString,
            demo__pb2.ReplyStatistics.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SimpleMethodsJoinUpdateMessage(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/demo.GRPCDemo/SimpleMethodsJoinUpdateMessage',
            demo__pb2.SendJoinUpdateMessage.SerializeToString,
            demo__pb2.ReplyJoinUpdateMessage.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SimpleMethodsLogMessage(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/demo.GRPCDemo/SimpleMethodsLogMessage',
            demo__pb2.SendLogMessage.SerializeToString,
            demo__pb2.ReplyLogMessage.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SimpleMethodsLogED(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/demo.GRPCDemo/SimpleMethodsLogED',
            demo__pb2.SendLogED.SerializeToString,
            demo__pb2.ReplyLogED.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SimpleMethodsLogGW(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/demo.GRPCDemo/SimpleMethodsLogGW',
            demo__pb2.SendLogGW.SerializeToString,
            demo__pb2.ReplyLogGW.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SimpleMethodsLogDM(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/demo.GRPCDemo/SimpleMethodsLogDM',
            demo__pb2.SendLogDM.SerializeToString,
            demo__pb2.ReplyLogDM.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)