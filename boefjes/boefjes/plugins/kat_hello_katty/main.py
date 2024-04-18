from os import getenv


def run(boefje_meta: dict) -> list[tuple[set, bytes | str]]:
    """run function that returns results for normalizers."""
    address = boefje_meta["arguments"]["input"]["address"]
    SERVER_INPUT = getenv("SERVER_INPUT", "Nothing :(")
    return [
        (set(), f"{address}|{SERVER_INPUT}")
    ]

