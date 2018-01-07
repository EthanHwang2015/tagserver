# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import suiyi_tag_pb2 as suiyi__tag__pb2


class TagServerStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.Tag = channel.unary_unary(
        '/tagserver.TagServer/Tag',
        request_serializer=suiyi__tag__pb2.TagRequest.SerializeToString,
        response_deserializer=suiyi__tag__pb2.TagResponse.FromString,
        )


class TagServerServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def Tag(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_TagServerServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'Tag': grpc.unary_unary_rpc_method_handler(
          servicer.Tag,
          request_deserializer=suiyi__tag__pb2.TagRequest.FromString,
          response_serializer=suiyi__tag__pb2.TagResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'tagserver.TagServer', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))