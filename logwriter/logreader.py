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
        logging.info("opened log file: %s", fo.name)
        error_in_fo = False
        prev_line = None
        for line in fo:
            try:
                timestamp, data = line.split()
            except ValueError:
                logging.error("failed to read line: %s", line.encode('unicode-escape'))
                retcode = 1
                error_in_fo = True
                continue
            if len(timestamp) != 26:
                logging.error("incorrect timestamp format: %s", timestamp.encode('unicode-escape'))
                retcode = 1
                error_in_fo = True
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
                    error_in_fo = True
            prev_line = line

        if error_in_fo:
            logging.error("log file is corrupted: %s", fo.name)
        else:
            logging.info("log file is ok: %s", fo.name)
        error_in_fo = False

    return retcode

if __name__ == '__main__':
    sys.exit(main())
