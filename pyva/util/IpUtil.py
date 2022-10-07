import socket


class IpUtil:
    @staticmethod
    def getHostIp():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("10.0.0.1", 8080))
            ip = s.getsockname()[0]
        finally:
            s.close()
        return ip
