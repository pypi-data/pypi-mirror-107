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
ID = "@(#) $Id: basename - return filename portion of pathname v1.1.0 (May 26, 2021) by Hubert Tournier $"

# Default parameters. Can be superseded by environment variables, then command line options
parameters = {"Multiple": False, "Posix": False, "Suffix": "", "Zero": False}


################################################################################
def display_help(extended=False):
    """Displays usage and help"""
    print("usage: basename string [suffix]", file=sys.stderr)
    if not parameters["Posix"]:
        if extended:
            print(
                "       basename [-a|--multiple] [-s|--suffix suffix] [-z|--zero] string [...]",
                file=sys.stderr,
            )
            print(
                "       basename [--debug] [--help|-?] [--version] [--]",
                file=sys.stderr,
            )
            print(
                "  ------------------   ---------------------------------------------------",
                file=sys.stderr,
            )
            print(
                "  -a|--multiple        Support multiple arguments and treat each as a name",
                file=sys.stderr,
            )
            print(
                "  -s|--suffix SUFFIX   Remove trailing SUFFIX. Implies -a",
                file=sys.stderr,
            )
            print(
                "  -z|--zero            End each output line with NUL, not newline",
                file=sys.stderr,
            )
            print("  --debug              Enable debug mode", file=sys.stderr)
            print(
                "  --help|-?            Print usage and this help message and exit",
                file=sys.stderr,
            )
            print("  --version            Print version and exit", file=sys.stderr)
            print(
                "  --                   Options processing terminator", file=sys.stderr
            )
            print()
        else:
            print("       basename [-a] [-s suffix] string [...]", file=sys.stderr)


################################################################################
def process_environment_variables():
    """Process environment variables"""
    # pylint: disable=C0103
    global parameters
    # pylint: enable=C0103

    # From "man environ":
    # POSIXLY_CORRECT
    # When set to any value, this environment variable
    # modifies the behaviour of certain commands to (mostly)
    # execute in a strictly POSIX-compliant manner.
    if "POSIXLY_CORRECT" in os.environ.keys():
        parameters["Posix"] = True

    logging.debug("process_environment_variables(): parameters:")
    logging.debug(parameters)


################################################################################
def process_command_line():
    """Process command line"""
    # pylint: disable=C0103
    global parameters
    # pylint: enable=C0103

    # option letters followed by : expect an argument
    # same for option strings followed by =
    character_options = ""
    string_options = []
    if parameters["Posix"]:
        character_options = "?"
        string_options = ["debug", "help", "version"]
    else:
        character_options = "as:z?"
        string_options = ["debug", "help", "multiple=", "suffix=", "version", "zero"]

    try:
        options, remaining_arguments = getopt.getopt(
            sys.argv[1:], character_options, string_options
        )
    except getopt.GetoptError as error:
        logging.critical(error)
        display_help()
        sys.exit(1)

    for option, argument in options:

        if option in ("-a", "--multiple"):
            parameters["Multiple"] = True

        elif option in ("-s", "--suffix"):
            parameters["Suffix"] = argument

        elif option in ("-z", "--zero"):
            parameters["Zero"] = True

        elif option == "--debug":
            logging.disable(logging.NOTSET)

        elif option in ("--help", "-?"):
            display_help(True)
            sys.exit(0)

        elif option == "--version":
            print(ID.replace("@(" + "#)" + " $" + "Id" + ": ", "").replace(" $", ""))
            sys.exit(0)

    logging.debug("process_command_line(): parameters:")
    logging.debug(parameters)
    logging.debug("process_command_line(): remaining_arguments:")
    logging.debug(remaining_arguments)

    return remaining_arguments


################################################################################
def basename(pathname):
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

    process_environment_variables()
    arguments = process_command_line()

    if len(arguments) == 0:
        display_help()
        sys.exit(1)

    # If -a is specified, then every argument is treated as a string as if basename were invoked
    # with just one argument. If -s is specified, then the suffix is taken as its argument, and all
    # other arguments are treated as a string
    if (
        len(arguments) == 2
        and not parameters["Multiple"]
        and parameters["Suffix"] == ""
    ):
        parameters["Suffix"] = arguments[1]
        print_pathname(basename(arguments[0]))
    else:
        for argument in arguments:
            print_pathname(basename(argument))

    sys.exit(0)


if __name__ == "__main__":
    main()
