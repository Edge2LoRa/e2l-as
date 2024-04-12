import os
import logging
import time
import math
from rpc_module.__private__ import edge2applicationserver_pb2_grpc
from rpc_module.__private__.edge2applicationserver_pb2 import ResponseMessage

log = logging.getLogger(__name__)


class Edge2LoRaApplicationServer(
    edge2applicationserver_pb2_grpc.Edge2ApplicationServerServicer
):
    def __init__(self, e2l_module) -> None:
        super().__init__()
        self.e2l_module = e2l_module

    def register_function(self, callback):
        self.data_received_callback = callback

    def store_e2gw_pub_info(self, request, context):
        gw_rpc_endpoint_address = request.gw_ip_addr
        gw_rpc_endpoint_port = request.gw_port

        gw_pub_key_compressed = request.e2gw_pub_key
        ret = self.e2l_module.handle_gw_pub_info(
            gw_rpc_endpoint_address, gw_rpc_endpoint_port, gw_pub_key_compressed
        )
        if ret != 0:
            return ResponseMessage(status_code=500, message=b"Error")
        return ResponseMessage(status_code=200, message=b"Success")

    def new_data(self, request, context):
        # now = math.floor(time.time() * 1000)
        gw_id = request.gw_id
        dev_eui = request.dev_eui
        dev_addr = request.dev_addr
        aggregated_data = request.aggregated_data
        fcnts = list(request.fcnts)
        timetag = request.timetag
        # delta_time = now - timetag

        self.e2l_module.handle_edge_data(
            gw_id=gw_id,
            dev_eui=dev_eui,
            dev_addr=dev_addr,
            aggregated_data=aggregated_data,
            timetag=timetag,
            fcnts=fcnts,
        )

        return ResponseMessage(status_code=0, message="OK")

    def gw_log(self, request, context):
        gw_id = request.gw_id
        dev_addr = request.dev_addr
        log = request.log
        frame_type = request.frame_type
        fcnt = request.fcnt
        timetag = request.timetag

        self.e2l_module.handle_gw_log(
            gw_id=gw_id,
            dev_addr=dev_addr,
            log_message=log,
            frame_type=frame_type,
            fcnt=fcnt,
            timetag=timetag,
        )
        return ResponseMessage(status_code=0, message="OK")

    def sys_log(self, request, context):
        gw_id = request.gw_id
        memory_usage = request.memory_usage
        memory_available = request.memory_available
        cpu_usage = request.cpu_usage
        data_received = request.data_received
        data_transmitted = request.data_transmitted
        self.e2l_module.handle_sys_log(
            gw_id=gw_id,
            memory_usage=memory_usage,
            memory_available=memory_available,
            cpu_usage=cpu_usage,
            data_received=data_received,
            data_transmitted=data_transmitted,
        )
        return ResponseMessage(status_code=0, message="OK")

    def gw_frames_stats(self, request, context):
        gw_id = request.gw_id
        legacy_frames = request.legacy_frames
        legacy_fcnts_it = list(request.legacy_fcnts)
        legacy_fcnts = []
        for elem in legacy_fcnts_it:
            legacy_fcnts.append({"dev_addr": elem.dev_addr, "fcnt": elem.fcnt})
        edge_frames = request.edge_frames
        edge_fcnts_it = list(request.edge_fcnts)
        edge_fcnts = []
        for elem in legacy_fcnts_it:
            edge_fcnts.append({"dev_addr": elem.dev_addr, "fcnt": elem.fcnt})
        edge_not_processed_frames = request.edge_not_processed_frames
        edge_not_processed_fcnts_it = list(request.edge_not_processed_fcnts)
        edge_not_processed_fcnts = []
        for elem in legacy_fcnts_it:
            edge_not_processed_fcnts.append(
                {"dev_addr": elem.dev_addr, "fcnt": elem.fcnt}
            )

        self.e2l_module.handle_gw_frames_stats(
            gw_id=gw_id,
            legacy_frames=legacy_frames,
            legacy_fcnts=legacy_fcnts,
            edge_frames=edge_frames,
            edge_fcnts=edge_fcnts,
            edge_not_processed_frames=edge_not_processed_frames,
            edge_not_processed_fcnts=edge_not_processed_fcnts,
        )
        return ResponseMessage(status_code=0, message="OK")
