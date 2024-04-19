import time
from collections.abc import Iterable
from ipaddress import ip_address
import logging

from boefjes.job_models import NormalizerMeta
from octopoes.models import OOI
from octopoes.models.ooi.network import Network
from octopoes.models.ooi.greeting import Greeting



def run(normalizer_meta: NormalizerMeta, raw: bytes | str) -> Iterable[OOI]:
    """"""
    logging.info("Normalizer checkpoint 1")
    raw = str(raw, "utf-8")
    [address, server_input] = raw.split("|")
    try:
        yield Network(name=normalizer_meta.raw_data.boefje_meta.arguments["input"]["network"]["name"])
    except:
        logging.error("NETWORK ERRORED")
    
    logging.info("Normalizer checkpoint 2")

    yield Greeting(address=ip_address(address), greeting=server_input, time=int(time.time()))
    logging.info("Normalizer checkpoint 3")
