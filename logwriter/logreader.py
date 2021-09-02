#!/usr/bin/env python3
# -*- coding: utf8 -*-

import argparse
import hashlib
import logging
import sys


def main():
    ap = argparse.ArgumentParser(description="logreader")
    ap.add_argument(
        "logfile",
        nargs='+',
        type=argparse.FileType('r'),
        help="filepath of a log file to read and verify")
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

    retcode = 0

    for fo in args.logfile:
        logging.info("log file %s opened", fo.name)
        prev_line = None
        for line in fo:
            try:
                timestamp, data = line.split()
            except ValueError:
                logging.error("failed to read line: %s", line)
                retcode = 1
                continue
            if prev_line is not None:
                checksum = hashlib.sha256(prev_line.encode('utf8')).hexdigest()
                if checksum == data:
                    logging.debug("line at %s verified", timestamp)
                else:
                    logging.error(
                        "line at %s doesn't provide good digest",
                        timestamp)
                    retcode = 1
            prev_line = line

    return retcode

if __name__ == '__main__':
    sys.exit(main())
