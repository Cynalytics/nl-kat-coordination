import time
from collections.abc import Iterable
from ipaddress import AddressValueError, IPv4Network, NetmaskValueError
import logging

from boefjes.job_models import NormalizerMeta
from octopoes.models import OOI, Reference
from octopoes.models.ooi.network import IPAddressV4, IPAddressV6, Network
from octopoes.models.ooi.greeting import Greeting


def is_ipv4(string: str) -> bool:
    try:
        IPv4Network(string)
        return True
    except (AddressValueError, NetmaskValueError, ValueError) as e:
        return False

def run(normalizer_meta: NormalizerMeta, raw: bytes | str) -> Iterable[OOI]:
    """"""
    
    logging.info("Normalizer checkpoint 1")
    raw = str(raw, "utf-8")
    [address, server_input] = raw.split("|")
    network = Network(name=normalizer_meta.raw_data.boefje_meta.arguments["input"]["network"]["name"])
    yield network
    
    netblock_ref = None
    if "NetBlock" in normalizer_meta.raw_data.boefje_meta.arguments["input"]["object_type"]:
        netblock_ref = Reference.from_str(normalizer_meta.raw_data.boefje_meta.input_ooi)

    ip = (
            IPAddressV4(network=network.reference, address=address, netblock=netblock_ref)
            if is_ipv4(address)
            else IPAddressV6(network=network.reference, address=address, netblock=netblock_ref)
        )

    yield Greeting(address=ip.reference, greeting=server_input, time=int(time.time()))
