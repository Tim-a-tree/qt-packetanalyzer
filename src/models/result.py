class Result:
    def __init__(self, status : str, packet_number : int, req_type : bool, packet_data : str):
        self.status = status
        self.packet_number = packet_number
        self.req_type = req_type
        self.packet_data = packet_data