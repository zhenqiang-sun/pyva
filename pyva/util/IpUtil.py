import ipaddress
import socket


class IpUtil:
    """
    IP工具类

    作者：孙振强
    版本：2.0.1
    创建时间：2022-10-07
    修改时间：2023-11-21
    """

    @staticmethod
    def validateIp(ip):
        """
        验证IP地址是否合法

        参数:
            ip (str): 待验证的IP地址

        返回:
            bool: IP地址是否合法，是则返回True，否则返回False
        """
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False

    @staticmethod
    def parseIp(ip):
        """
        解析IP地址

        参数:
            ip (str): 待解析的IP地址

        返回:
            ipaddress.IPv4Address / ipaddress.IPv6Address: 解析后的IP地址对象
        """
        return ipaddress.ip_address(ip)

    @staticmethod
    def convertIpv4ToIpv6(ipv4):
        """
        将IPv4地址转换为IPv6地址

        参数:
            ipv4 (int): IPv4地址

        返回:
            ipaddress.IPv6Address: 转换后的IPv6地址对象
        """
        return ipaddress.IPv6Address("::ffff:" + str(ipv4))

    @staticmethod
    def isIpInRange(ip, start_ip, end_ip):
        """
        判断IP地址是否在指定范围内

        参数:
            ip (str): 待判断的IP地址
            start_ip (str): 范围的起始IP地址
            end_ip (str): 范围的结束IP地址

        返回:
            bool: IP地址是否在范围内，是则返回True，否则返回False
        """
        return start_ip <= ip <= end_ip

    @staticmethod
    def getHostIp():
        """
        获取主机的IP地址

        返回:
            str: 主机的IP地址
        """
        return socket.gethostbyname(socket.gethostname())
