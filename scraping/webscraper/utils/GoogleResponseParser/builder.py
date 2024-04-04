
# Abstract factory builder
from .v1 import GoogleSearchResponseParserV1
from .v2 import GoogleSearchResponseParserV2

class GoogleSearchResponseParserBuilder:
    @staticmethod
    def build(version):
        if version == 1 or version == 'v1' or version == 'V1' or version == '1':
            return GoogleSearchResponseParserV1()
        elif version == 2 or version == 'v2' or version == 'V2' or version == '2' or version == 'latest':
            return GoogleSearchResponseParserV2()
        else:
            raise ValueError("Invalid version number")