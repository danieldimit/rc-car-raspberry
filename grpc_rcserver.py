import grpc
import time
from concurrent import futures
import grpc_connector.client_pb2_grpc as client_pb2_grpc
import grpc_connector.client_pb2 as client_pb2

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class GRPCServer:

    def __init__(self):
        self.port = "50051"

        self.serve()

    def serve(self):
        print("Starting server...")
        print("Listening on port: " + self.port)

        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        client_pb2_grpc.add_CommandHandlerServicer_to_server(self.CommandHandlerService(), server)
        server.add_insecure_port('[::]:' + self.port)
        server.start()
        try:
            while True:
                time.sleep(_ONE_DAY_IN_SECONDS)
        except KeyboardInterrupt:
            server.stop(0)

    class CommandHandlerService(client_pb2_grpc.CommandHandlerServicer):

        def Command(self, request, context):
            print(request.commandType)
            return client_pb2.Empty()