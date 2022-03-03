import csv, json

SoftwareDefinitionEnum = ['SoftwareDefinition']


class CPE():
    # from  https://nmap.org/book/output-formats-cpe.html
    #
    # cpe:/<part>:<vendor>:<product>:<version>:<update>:<edition>:<language>
    #
    #   part is a (application), o (Operating system), h (Hardware)
    #
    def __init__(self, cpe_str:str):
        if not cpe_str.lower().startswith("cpe:/"):
            raise KeyError("CPE string shoud start with cpe:/")
        fields = cpe_str[5:].rstrip().split(":")
        self.part = fields.pop(0)
        self.checkPart()
        self.vendor = fields.pop(0)
        self.product = fields.pop(0)
        self.version = fields.pop(0)
        try:
            self.update = fields.pop(0)
            self.edition = fields.pop(0)
            self.language = fields.pop(0)
        except IndexError:
            pass


    def checkPart(self):
        assert(self.part in ["a","h","o"])



class SoftwareDefinition():
    def __init__(self, data):
        self.id = self.get_id(data)
        self.type = 'SoftwareDefinition'

        d_cpe = data['cpe']
        self.cpe = CPE(d_cpe) if d_cpe != "" else None

        # Server IP Addresss where the Software is listening
        self.address = data['host']

        self.product = data['product']

        self.version = data['version']

        self.openTCPPorts = [int(data['port'])]
        self.openUDPPorts = []
        self.vendor = self.cpe.vendor if self.cpe is not None else "unknown"
        self.hasSoftwareConnections = []


    @classmethod
    def get_id(cls, datum):
        if datum['cpe'] != "":
            id = datum['cpe']
        else:
            id = f"unknown:{datum['protocol']}:{datum['data']['address']}:{datum['port']}:{datum['extrainfo']}"
        return id

    def main_dict(self):
        js = {
            "id": self.id,
            "type": self.type,
            "address": self.address,
            "vendor": self.vendor,
            "version": self.version,
            "product": self.product,
            "openTCPPorts": self.openTCPPorts,
            "openUDPPorts": self.openUDPPorts,
        }
        return js

    def json(self):
        return json.dumps(self.main_dict())


class SoftwareObjectsFromNmap:
    localSoftware = []
    software_objects = {}

    @classmethod
    def jsondump(cls, filename):
        print(json.dumps(SoftwareObjectsFromNmap.localSoftware))
        with open(filename, "w") as f:
            json.dump(SoftwareObjectsFromNmap.localSoftware, f)

    @classmethod
    def SoftwareDefinitionFromNmapData(cls, nmap_csv : str, data : dict):
        sw_data = nmap_csv.strip().split(';')
        d = {}
        host = sw_data.pop(0)
        host = data['address']
        hostname = sw_data.pop(0)
        hostname_type = sw_data.pop(0)
        protocol = sw_data.pop(0)
        port = sw_data.pop(0)
        name = sw_data.pop(0)
        state = sw_data.pop(0)
        product = sw_data.pop(0)
        extrainfo = sw_data.pop(0)
        reason = sw_data.pop(0)
        version = sw_data.pop(0)
        conf = sw_data.pop(0)
        cpe = sw_data.pop(0)

        d['host'] = host
        d['hosname'] = hostname
        d['hostname_type'] = hostname_type
        d['protocol'] = protocol
        d['port'] = port
        d['name'] = name
        d['state'] = state
        d['product'] = product
        d['extrainfo'] = extrainfo
        d['reason'] = reason
        d['version'] = version
        d['conf'] = conf
        d['cpe'] = cpe
        d['data'] = data
        print(json.dumps(d))

        SoftwareObjectsFromNmap.localSoftware.append(d)

    @classmethod
    def add_scanned_data(cls, data):
        for d in data:
            SoftwareObjectsFromNmap.localSoftware.append(d)

    @classmethod
    def build_objects(cls):
        for d in SoftwareObjectsFromNmap.localSoftware:
            swd = SoftwareDefinition(d)
            SoftwareObjectsFromNmap.software_objects[swd.id] = swd

    @classmethod
    def json(cls):
        r = []
        for k in SoftwareObjectsFromNmap.software_objects.keys():
            r.append(SoftwareObjectsFromNmap.software_objects[k].main_dict())

        return json.dumps(r)


if __name__ == "__main__":
    CPE("cpe:/a:apache:http_server:2.4.51")