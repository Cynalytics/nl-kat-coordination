from bits.definitions import BitDefinition
from octopoes.models.ooi.greeting import Greeting

BIT = BitDefinition(
    id="check-greeting",
    consumes=Greeting,
    parameters=[],
    module="bits.check_greeting.check_greeting",
    default_enabled=True, # TODO: maybe change this
)
