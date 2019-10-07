#!/usr/bin/env python3
import argparse
from getpass import getpass
from pprint import pprint
import time
import sys

sys.path.insert(1, "../")
import teslajsonpy
import teslajsonpy.streamer


def getargs():
    parser = argparse.ArgumentParser(
        description="Show all available data for the given Tesla login."
    )
    parser.add_argument("-e", "--email", help="Tesla login email address")
    parser.add_argument("-p", "--password", help="Password for given email address")

    parser.add_argument(
        "--nostream",
        action="store_true",
        help="If set, will not activate a stream for each vehicle",
    )

    args = parser.parse_args()

    if not args.email:
        args.email = input("Enter Tesla email address: ")
    if not args.password:
        args.password = getpass("Enter Tesla password: ")

    return args


def header(name):
    print()
    print("*" * 80)
    print("*** {} ***".format(name.center(72)))
    print("*" * 80)


def streammsg(msg):
    print("{}: {}".format(time.asctime(), msg))


def main():
    args = getargs()

    controller = teslajsonpy.Controller(args.email, args.password, 60)
    for vehicle in controller.get_vehicles():
        print()
        print()
        header("Next Vehicle")
        pprint(vehicle)

        header("Climate")
        pprint(controller.get_climate_params(vehicle["id"]))
        header("Charging")
        pprint(controller.get_charging_params(vehicle["id"]))
        header("State")
        pprint(controller.get_state_params(vehicle["id"]))
        header("Drive")
        pprint(controller.get_drive_params(vehicle["id"]))
        header("GUI")
        pprint(controller.get_gui_params(vehicle["id"]))

        if not args.nostream:
            header("Streaming data...")
            s = teslajsonpy.streamer.Stream(args.email, vehicle)
            starttime = time.time()
            s.start(streammsg)
            runtime = time.time() - starttime
            print("*** Stream closed after {:0.1f}s ***".format(runtime))


if __name__ == "__main__":
    main()
