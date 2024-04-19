from __future__ import annotations

from ipaddress import IPv4Address, IPv6Address
from typing import Literal


from octopoes.models import OOI, Reference

class Greeting(OOI):
    object_type: Literal["Greeting"] = "Greeting"

    
    greeting: str
    time: int
    address: IPv4Address | IPv6Address
    
    # attributes that make the object identifiable (These get used to make the primary key "Greeting/greeting/time")
    _natural_key_attrs = ["greeting", "time"]
    
    @classmethod
    def format_reference_human_readable(cls, reference: Reference) -> str:
        return "testGreeting"
    

Greeting.model_rebuild()
    