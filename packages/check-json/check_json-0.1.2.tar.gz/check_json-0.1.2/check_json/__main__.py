#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Christopher Peterson"

import argparse
import logging
import re
import sys
from collections import namedtuple
from pprint import pformat
from typing import List

import jq  # type:ignore
import nagiosplugin  # type:ignore


def file_to_string(filepath: str):
    """
    Given a file path, put its contents into a string
    """
    try:
        with open(filepath, "r") as fileobj:
            return fileobj.read()
    except FileNotFoundError as err:
        logging.debug(pformat(err))
        print(f"File not found: `{filepath}`", file=sys.stderr)
        sys.exit(3)
    except OSError as err:
        logging.debug(pformat(err))
        print(f"OS error opening file: `{filepath}`", file=sys.stderr)
        sys.exit(3)


def gen_filter_name(filter_string: str, default: str = None):
    """
    xx
    """
    regex = re.compile("(?<=#) ?[0-9a-zA-Z_-]*$")
    match = regex.search(filter_string)
    logging.debug(
        "Filter name regex match: `%s` from filter `%s`", pformat(match), filter_string
    )
    return match.group(0).strip() if match else default


def parse_args(argv=None):
    """Parse args"""

    usage_examples: str = """examples of use:

        # A minimal example: report OK if a single filter evaluates to other
        # than false/null.

        %(prog)s --filter '.select(somekey)' /path/to/jsonfile

        # As above, but label that filter "myfilter" in the reporting

        %(prog)s --filter '.select(somekey) # myfilter' /path/to/jsonfile

        # Multiple, separate filters
        %(prog)s --filter '.somekey != "somevalue"' \\
            --filter '.otherkey != "othervalue"' /path/to/jsonfile

        # Source a filter from a jsonfile
        %(prog)s --filter-file /path/to/filterfile /path/to/jsonfile
    """
    descr: str = """
        Icinga2/Nagios plugin to run some number of JQ filters on a JSON file,
        failing if any of the results are false/null.

        Outputs Nagios standard perfdata for each filter reported with `1`
        for success and `0` for failure.

        If a given filter is concluded by a
        comment string of the format `# some-descriptive-string`, it will be
        used as the perfdata label for that filter.

        Refer to the JQ Manual for for your version of libjq, for all of the
        things you can do in a filter:
        https://stedolan.github.io/jq/manual/
        """
    parser = argparse.ArgumentParser(
        description=descr,
        epilog=usage_examples,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--filter",
        "-f",
        action="extend",
        dest="filters",
        help="A JQ filter to run on the given JSON file.",
        nargs="+",
        type=str,
    )

    parser.add_argument(
        "--filter-file",
        "-F",
        action="extend",
        dest="filters",
        help="A file containing a JQ filter to run on the given JSON file.",
        nargs="+",
        type=file_to_string,
    )

    parser.add_argument(
        "--fail-status",
        "-s",
        choices=["critical", "warning"],
        default="warning",
        dest="fail_status",
        help=(
            "Specify the status to report when a filter comes back false/null. "
            "Defaults to warning."
        ),
        type=str.lower,
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="count",
        default=0,
        dest="verbosity",
        help="Set output verbosity (-v=warning, -vv=debug)",
    )

    parser.add_argument(
        "jsonfile",
        action="store",
        help="The path(s) to the file(s) to inspect",
        metavar="jsonfile",
        type=str,
    )

    args = parser.parse_args(argv) if argv else parser.parse_args()

    if not args.filters:
        parser.error(
            "At least one of either `--filter` or `--filter-file` is required."
        )

    if args.verbosity >= 2:
        log_level = logging.DEBUG
    elif args.verbosity >= 1:
        log_level = logging.INFO
    else:
        log_level = logging.WARNING

    logging.basicConfig(level=log_level)

    return args


Filter = namedtuple("Filter", "name filtobj")


class JsonFile(nagiosplugin.Resource):
    """
    Determines if filters succeed or fail on the given JSON file
    """

    def __init__(self, *, filters: List[str], filepath: str):
        """
        Compile filter strings into filter objects, and ingest JSON file
        """
        self.json = file_to_string(filepath)
        logging.debug("JSON file contents: %s", self.json)
        self.filters = [
            Filter(gen_filter_name(f, default=f"filter{i}"), jq.compile(f))
            for i, f in enumerate(filters)
        ]
        logging.debug("Readied filters: %s", pformat(self.filters))

    def probe(self):
        for filt in self.filters:
            filt_result = filt.filtobj.input(text=self.json).all()
            value = 1 if filt_result else 0
            logging.info(
                "Ran filter `%s` on JSON. Result: `%s`", filt.name, filt_result
            )
            yield nagiosplugin.Metric(filt.name, value, context="filters")


@nagiosplugin.guarded
def main():
    """Main"""

    args = parse_args(sys.argv[1:])
    logging.debug("Argparse results: %s", pformat(args))

    if args.fail_status == "warning":
        warning = nagiosplugin.Range("@0:0")
        critical = None
    else:
        warning = None
        critical = nagiosplugin.Range("@0:0")
    check = nagiosplugin.Check(
        JsonFile(filters=args.filters, filepath=args.jsonfile),
        nagiosplugin.ScalarContext("filters", warning=warning, critical=critical),
    )
    check.main(args.verbosity)


if __name__ == "__main__":
    main()
