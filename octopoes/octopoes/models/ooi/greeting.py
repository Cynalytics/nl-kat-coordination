from __future__ import annotations

from typing import Literal
from octopoes.models.persistence import ReferenceField
from octopoes.models.ooi.network import IPAddress


from octopoes.models import OOI, Reference

class Greeting(OOI):
    object_type: Literal["Greeting"] = "Greeting"
    
    greeting: str
    time: int
    address: Reference = ReferenceField(IPAddress, max_issue_scan_level=0, max_inherit_scan_level=4)
    
    # attributes that make the object identifiable (These get used to make the primary key "Greeting/<greeting>/<time>/<address>")
    _natural_key_attrs = ["greeting", "time", "address"]
    
    

Greeting.model_rebuild()
    