import logging
import sys

from communicators.get_findings import get_findings
from communicators.get_random_ooi import get_random_ooi
from communicators.toggle_plugin import toggle_plugin

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("katty")


ORGANISATION_ID = ""
CHOSEN_PLUGIN = ""


if __name__ == "__main__":
    if not ORGANISATION_ID or not CHOSEN_PLUGIN:
        logging.fatal("Not all variables are set!")
        sys.exit(1)
    while True:
        choice = input(
            "What do you want to do?\n1).\tGet the findings.\n2).\tToggle a plugin.\n3).\tGet a random OOI.\n"
        )
        if choice == "1":
            get_findings(ORGANISATION_ID)

        elif choice == "2":
            toggle_plugin(ORGANISATION_ID, CHOSEN_PLUGIN)

        elif choice == "3":
            get_random_ooi(ORGANISATION_ID)

        else:
            break
    logger.info("END")
