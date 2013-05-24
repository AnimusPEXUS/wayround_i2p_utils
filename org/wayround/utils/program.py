#!/usr/bin/python3

import sys
import logging

import org.wayround.utils.getopt
import org.wayround.utils.program_help

def program(command_name, config, commands, loglevel='INFO'):

    # Logging settings
    for i in [
        (logging.CRITICAL, '-c-'),
        (logging.ERROR   , '-e-'),
        (logging.WARN    , '-w-'),
        (logging.WARNING , '-w-'),
        (logging.INFO    , '-i-'),
        (logging.DEBUG   , '-d-')
        ]:
        logging.addLevelName(i[0], i[1])
    del i

    opts, args = org.wayround.utils.getopt.getopt_keyed(sys.argv[1:])

    args_l = len(args)

    # Setup logging level and format
    log_level = 'INFO'

    if '--loglevel' in opts:
        log_level_u = opts['--loglevel'].upper()

        if not log_level_u in list(logging._levelNames):
            print("-e- Wrong --loglevel parameter")
        else:
            log_level = log_level_u

        del(opts['--loglevel'])
        del(log_level_u)

    logging.basicConfig(
        format="%(levelname)s %(message)s",
        level=log_level
        )

    command = None
    subcommand = None

    if args_l > 0:
        command = args[0]

    if args_l > 1:
        subcommand = args[1]

    show_help = '--help' in opts

    ret = 0

    if not show_help:

        if not command in commands:
            logging.error("No such command: {}".format(command))
            ret = 1
        else:
            if not subcommand in commands[command]:
                logging.error("No such subcommand: {}::{}".format(command, subcommand))
                ret = 1

            else:
                ret = 0
                try:
                    ret = commands[command][subcommand](config, opts, args[2:])
                except:
                    print()
                    logging.exception(
                        "Error while executing command: {}::{}".format(
                            command,
                            subcommand
                            )
                        )
                    ret = 1

                if not isinstance(ret, int):
                    logging.warning(
                        "Command returned not integer (resetting to 1). It returned(type:{}):\n{}".format(
                            type(ret),
                            ret
                            )
                        )
                    ret = 1


    else:
        ret = 0
        txt = org.wayround.utils.program_help.program_help(
            command_name, commands, command, subcommand
            )
        if not isinstance(txt, str):
            logging.error(
                "Error getting help for: {}::{}".format(
                    command,
                    subcommand
                    )
                )
            ret = 1
        else:
            print(txt)

    logging.info("Exit Code: {}".format(ret))

    return ret
