#!/usr/bin/env python3
""" basename - return filename portion of pathname
License: 3-clause BSD (see https://opensource.org/licenses/BSD-3-Clause)
Author: Hubert Tournier
"""

import getopt
import logging
import re
import os
import sys

# Version string used by the what(1) and ident(1) commands:
ID = "@(#) $Id: basename - return filename portion of pathname v1.0.0 (May 24, 2021) by Hubert Tournier $"

# Default parameters. Can be overcome by command line options
parameters = {"Multiple arguments": False, "Suffix": "", "Zero": False}

################################################################################
def display_help():
    """Displays usage and help"""
    print("usage: basename string [suffix]", file=sys.stderr)
    print("       basename [-a] [-s suffix] string [...]", file=sys.stderr)


################################################################################
def display_full_help():
    """Displays usage and help"""
    print()
    print("usage: basename string [suffix]")
    print("       basename [-a|--multiple] [-s|--suffix suffix] [-z|--zero] string [...]")
    print("       basename [-d|--debug] [-h|--help|-?] [-v|--version] [--]")
    print("  ----------------   ---------------------------------------------------")
    print("  -a|--multiple        Support multiple arguments and treat each as a name")
    print("  -d|--debug           Enable debug mode")
    print("  -h|--help|-?         Print usage and this help message and exit")
    print("  -s|--suffix SUFFIX   Remove trailing SUFFIX. Implies -a")
    print("  -v|--version         Print version and exit")
    print("  -z|--zero            End each output line with NUL, not newline")
    print("  --                   Options processing terminator")
    print()


################################################################################
def process_command_line():
    """Process command line"""
    # pylint: disable=C0103
    global parameters
    # pylint: enable=C0103

    try:
        # option letters followed by : expect an argument
        # same for option strings followed by =
        options, remaining_arguments = getopt.getopt(
            sys.argv[1:],
            "adhs:vz?",
            ["debug", "help", "multiple=", "suffix=", "version", "zero"],
        )
    except getopt.GetoptError as error:
        logging.critical(error)
        display_help()
        sys.exit(1)

    for option, argument in options:

        if option in ("-a", "--multiple"):
            parameters["Multiple arguments"] = True

        elif option in ("-d", "--debug"):
            logging.disable(logging.NOTSET)

        elif option in ("-h", "--help", "-?"):
            display_full_help()
            sys.exit(0)

        elif option in ("-s", "--suffix"):
            parameters["Suffix"] = argument

        elif option in ("-v", "--version"):
            print(ID.replace("@(" + "#)" + " $" + "Id" + ": ", "").replace(" $", ""))
            sys.exit(0)

        elif option in ("-z", "--zero"):
            parameters["Zero"] = True

    logging.debug("process_commandline(): parameters:")
    logging.debug(parameters)
    logging.debug("process_commandline(): remaining_arguments:")
    logging.debug(remaining_arguments)

    return remaining_arguments


################################################################################
def process_pathname(pathname):
    """Do basename processing on a pathname"""

    # First stripping trailing slashes:
    # Regular Expression means slash character, 0 to N times (*), at the end of the string ($)
    pathname = re.sub(re.escape(os.sep) + "*$", "", pathname)

    # If string consists entirely of slash characters, string shall be set to a single slash
    # character:
    if not pathname:
        return os.sep

    # Delete any prefix ending with the last slash character present in string:
    # Regular Expression means any character (.), 0 to N times (*), till a slash character
    pathname = re.sub(".*" + re.escape(os.sep), "", pathname)

    # Delete the suffix unless if it is identical to the remaining characters in string:
    if pathname != parameters["Suffix"]:
        # A non-existent suffix is ignored.
        # Regular Expression means the suffix string, at the end of the string ($)
        pathname = re.sub(re.escape(parameters["Suffix"]) + "$", "", pathname)

    return pathname


################################################################################
def print_pathname(pathname):
    """print() wrapper to handle the zero option"""
    if parameters["Zero"]:
        sys.stdout.buffer.write(bytes(pathname, encoding="utf8"))
        sys.stdout.buffer.write(bytes([0x00]))
    else:
        print(pathname)


################################################################################
def main():
    """The program's main entry point"""
    program_name = os.path.basename(sys.argv[0])
    console_log_format = program_name + ": %(levelname)s: %(message)s"
    logging.basicConfig(format=console_log_format, level=logging.DEBUG)
    logging.disable(logging.INFO)

    arguments = process_command_line()

    if len(arguments) == 0:
        display_help()
        sys.exit(1)

    # If -a is specified, then every argument is treated as a string as if basename were invoked
    # with just one argument. If -s is specified, then the suffix is taken as its argument, and all
    # other arguments are treated as a string
    if (
        len(arguments) == 2
        and not parameters["Multiple arguments"]
        and parameters["Suffix"] == ""
    ):
        parameters["Suffix"] = arguments[1]
        print_pathname(process_pathname(arguments[0]))
    else:
        for argument in arguments:
            print_pathname(process_pathname(argument))

    sys.exit(0)


if __name__ == "__main__":
    main()
