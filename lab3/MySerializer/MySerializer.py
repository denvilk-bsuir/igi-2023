from MySerializer.json_utils import Json
from MySerializer.xml_utils import Xml

class MySerializer:
    @staticmethod
    def createSerializer(format):
        if format == ".json":
            return Json()

        elif format == ".xml":
            return Xml()

        else:
            raise Exception("Wrong format")    