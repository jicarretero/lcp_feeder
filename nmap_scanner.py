import nmap
import ipaddress
from enum import Enum
from models.SoftwareModel import SoftwareDefinition, SoftwareObjectsFromNmap
import json

STR_TCP_STATES = [ "", "ESTABLISHED", "SYN_SENT", "SYN_RECV", "FIN_WAIT_1", "FIN_WAIT_2", "CLOSED", "TIME_WAIT",
                   "CLOSE_WAIT", "LAST_ACK", "LISTEN",  "CLOSING"]


class TCP_STATES(Enum):
    TCP_ESTABLISHED = 1
    TCP_SYN_SENT = 2
    TCP_SYN_RECV = 3
    TCP_FIN_WAIT1 = 4
    TCP_FIN_WAIT2 = 5
    TCP_TIME_WAIT = 6
    TCP_CLOSE = 7
    TCP_CLOSE_WAIT = 8
    TCP_LAST_ACK = 9
    TCP_LISTEN = 10
    TCP_CLOSING = 11


TCP_FILE = '/proc/net/tcp'
UDP_FILE = '/proc/net/udp'


class PortScanner:
    def __init__(self, config):
        self.nm = nmap.PortScanner()
        self.software = []
        self.open_ports = []
        self.rmt_connections = {}
        self.config = config

    @staticmethod
    def addr_to_host_port(d):
        str_host_inv, str_port = d.strip().split(':')
        str_host = str_host_inv[6:8] + str_host_inv[4:6] + str_host_inv[2:4] + str_host_inv[0:2]
        ip = ipaddress.IPv4Address(int(str_host, 16))
        port = int(str_port, 16)
        return str(ip), port

    def read_tcp(self):
        with open(TCP_FILE) as f:
            tcp_data = f.read().split("\n")

        for d in tcp_data[1:]:
            try:
                connection = d.split()
                sl = connection[0].strip()
                local_address, local_port = PortScanner.addr_to_host_port(connection[1])
                rmt_address, rmt_port = PortScanner.addr_to_host_port(connection[2])
                st = int(connection[3].strip(), 16)
                print(sl, " ", local_address, ":", local_port, " ", rmt_address, ":", rmt_port, " ", STR_TCP_STATES[st], " ", st)
                if TCP_STATES(st) == TCP_STATES.TCP_LISTEN:
                    self.open_ports.append({'address': local_address, 'port': local_port})
            except Exception:
                print("---------------------------")
                print(d)
                print("---------------------------")

    def scan_open_ports(self):
        for a in self.open_ports:
            print("-------------- Scanning: ", a['address'], ":", a['port'])
            ip = a['address'] if a['address'] != '0.0.0.0' else '127.0.0.1'
            self.nm.scan(ip, str(a['port']))
            print("Scan Info: ", self.nm.scaninfo())
            csv_data = self.nm.csv().split('\n')[1]
            print("CSV Info:  ", self.nm.csv())
            SoftwareObjectsFromNmap.SoftwareDefinitionFromNmapData(csv_data, a)

        SoftwareObjectsFromNmap.jsondump(self.config.test_config_file)

    def load_from_file_or_scan(self):
        try:
            with open(self.config.test_config_file, "r") as f:
                data = json.load(f)
                SoftwareObjectsFromNmap.add_scanned_data(data)
        except (json.JSONDecodeError, FileNotFoundError):
            self.scan_open_ports()

        SoftwareObjectsFromNmap.build_objects()

