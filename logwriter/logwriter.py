#!/usr/bin/env python3
# -*- coding: utf8 -*-

from datetime import datetime
import argparse
import hashlib
import logging
import os
import sys
import time
import uuid


def main():
    ap = argparse.ArgumentParser(description="logwriter")
    ap.add_argument(
        "directory",
        help="directory where to create a log file")
    ap.add_argument(
        "-p",
        type=int,
        help="pause between 2 consequent writes in seconds")
    ap.add_argument(
        "--fsync",
        action="store_true",
        help="run fsync after each write")
    ap.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="set log level to DEBUG")
    args = ap.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    # name of a target log file is unique for each run
    log_name = str(uuid.uuid4()) + ".log"

    # TODO: limit size of the log file, rotate log file
    # TODO: check given log file

    with open(log_name, "w") as log_file:
        logging.info("log file %s created", log_name)
        timestamp = datetime.now()
        log_line = f"{timestamp.isoformat()} started\n"
        log_file.write(log_line)
        while True:
            try:
                data = hashlib.sha256(log_line.encode('utf8')).hexdigest()
                timestamp = datetime.now()
                log_line = f"{timestamp.isoformat()} {data}\n"
                log_file.write(log_line)
                log_file.flush()
                if args.fsync:
                    os.fsync(log_file.fileno())
                time.sleep(args.p)
            except KeyboardInterrupt:
                logging.info("stopped")
                break


if __name__ == '__main__':
    sys.exit(main())
