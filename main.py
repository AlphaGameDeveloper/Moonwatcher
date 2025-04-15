# Copyright (c) 2025 Damien Boisvert (AlphaGameDeveloper)
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from argparse import ArgumentParser
from datetime import datetime
import logging

if __name__ == "__main__":
    parser = ArgumentParser(
        prog="Moonwatcher",
        description="Taking photos of the night sky",
        epilog="(c) Damien Boisvert (AlphaGameDeveloper) %s" % datetime.now().year,
    )
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Enable debug mode",
    )

    parser.add_argument(
        "-l",
        "--latitude",
        type=float,
        required=True,
        help="Latitude of the location"
    )
    parser.add_argument(
        "-L",
        "--longitude",
        type=float,
        required=True,
        help="Longitude of the location"
    )
    
    args = parser.parse_args()

    # config logging
    logging.basicConfig(
        level=logging.DEBUG if args.debug else logging.INFO,
        format="[%(asctime)-20s]  %(levelname)-8s  %(message)s",
    )
    
    