import bluetooth_rcserver as brc
import grpc_rcserver
import sys

if __name__ == "__main__":
    mode = "bluetooth"
    if len(sys.argv) >= 2:
        mode = sys.argv[1]

    if mode == "web":
        grpc_rcserver.GRPCServer()
    else:
        brc.BluetoothRCServer()