from kikyo import Kikyo

from kikyo_bundle.datahub import PulsarBasedDataHub
from kikyo_bundle.oss import MinioBasedOSS, AliyunOSS
from kikyo_bundle.search import EsBasedSearch


def configure_kikyo(client: Kikyo):
    PulsarBasedDataHub(client)
    MinioBasedOSS(client)
    AliyunOSS(client)
    EsBasedSearch(client)
