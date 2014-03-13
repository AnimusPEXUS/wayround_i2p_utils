#!/usr/bin/python3

import copy
import inspect
import logging
import sys

import org.wayround.utils.error
import org.wayround.utils.getopt


NO_DOCUMENTATION = '(No documentation)'


def logging_setup(loglevel='INFO'):

    loglevel = loglevel.upper()

    # Logging settings
    for i in [
        (logging.CRITICAL, '-c-'),
        (logging.ERROR, '-e-'),
        (logging.WARN, '-w-'),
        (logging.WARNING, '-w-'),
        (logging.INFO, '-i-'),
        (logging.DEBUG, '-d-')
        ]:
        logging.addLevelName(i[0], i[1])
    del i

    opts = org.wayround.utils.getopt.getopt_keyed(sys.argv[1:])[0]

    # Setup logging level and format
    log_level = loglevel

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

    return


def command_processor(
    command_name, commands, opts_and_args_list, additional_data
    ):

    """
    command_name used only for help rendering purposes, so if not given --
    program name will not be rendered in help

    returned value is a dict(code, message)

    accepted ``commands`` must be dict of dicts with following example
    structure:

    dict(
        _order = 'order in which commands appeared in generated help text',
        command_name1 = dict(
            _help = 'command help text',
            _order = \
                'order in which subcommands appeared in generated help text',
            subcommand_name0 = callback,
            subcommand_name1 = callback,
            subcommand_name2 = callback,
            subcommand_name3 = callback,
            ...
            subcommand_namen = callback
            ),
        command_name2 = dict(
            _help = 'command help text',
            _order = \
                'order in which subcommands appeared in generated help text',
            subcommand_name0 = callback,
            subcommand_name1 = callback,
            subcommand_name2 = callback,
            subcommand_name3 = callback,
            ...
            subcommand_namen = callback
            ),
        ...
        command_namen = dict(
            _help = 'command help text',
            _order = \
                'order in which subcommands appeared in generated help text',
            subcommand_name0 = callback,
            subcommand_name1 = callback,
            subcommand_name2 = callback,
            subcommand_name3 = callback,
            ...
            subcommand_namen = callback
            )
        )

    callbacks must accept 3 parameters:
        comm - command and subcommand name wrapped woth puple. this can be used
            if single callback is used for all commands in ``commands`` dict
        opts - options which this function derives from opts_and_args_list
        args - arguments which this function derives from opts_and_args_list
        adds - additional data, which is simply passed from additional_data
            parameter

    In place of dicts you can use OrderedDicts, if you prefer. In this case
    '_order' dict items not needed.

    callbacks must return `int' or `dict' with structure:
    dict(code=<int>, message=<str>)

    this function returns `dict' with structure:
    dict(code=<int>, message=<str>)
    """

    opts, args = org.wayround.utils.getopt.getopt_keyed(opts_and_args_list)

    args_l = len(args)

    command = None
    subcommand = None

    if args_l > 0:
        command = args[0]

    if args_l > 1:
        subcommand = args[1]

    show_help = '--help' in opts

    ret = dict(code=0, message='No errors')

    if not show_help:

        if not command in commands:
            ret = dict(
                code=1,
                message="No such command: {} (try '--help')".format(command)
                )
        else:
            if not subcommand in commands[command]:
                ret = dict(
                    code=1,
                    message="No such subcommand: {}::{}".format(
                        command,
                        subcommand
                        )
                    )

            else:

                try:
                    res = commands[command][subcommand](
                        (command, subcommand,),
                        opts,
                        args[2:],
                        additional_data
                        )
                except BrokenPipeError:
                    ret = dict(
                        code=1,
                        message="BrokenPipeError"
                        )
                except KeyboardInterrupt:
                    ret = dict(
                        code=1,
                        message="Interrupted With Keyboard"
                        )
                except:
                    e = sys.exc_info()

                    ex_txt = org.wayround.utils.error.return_exception_info(
                        e,
                        tb=True
                        )

                    ret = dict(
                        code=1,
                        message=(
                            "Error while executing command: {}::{}\n{}".format(
                                command,
                                subcommand,
                                ex_txt
                                )
                            )
                        )

                else:

                    if isinstance(res, int):
                        txt = None

                        if res == 0:
                            txt = 'No errors'
                        else:
                            txt = 'Some error (Read documentation).'

                        ret = dict(
                            code=res,
                            message=txt
                            )
                    elif isinstance(res, dict):

                        ret = dict(
                            code=res['code'],
                            message=res['message']
                            )

                    else:
                        ret = dict(
                            code=1,
                            message=(
                                "Command returned not integer and not "
                                "dict (resetting to 1)."
                                " It has returned(type:{}):\n{}".format(
                                    type(res),
                                    res
                                    )
                                )
                            )

    else:
        ret['code'] = 0
        txt = program_help(
            command_name, commands, command, subcommand
            )
        if not isinstance(txt, str):
            ret = dict(
                code=1,
                message="Error getting help for: {}::{}".format(
                    command,
                    subcommand
                    )
                )
        else:
            ret['message'] = txt

    return ret


def program(command_name, commands, additional_data=None):

    """
    command_name used only for help rendering purposes, so if not given --
    program name will not be rendered in help.

    this function uses command_processor() for command_processing, see it's
    documentation for explanations on parameters
    """

    ret = command_processor(
        command_name,
        commands,
        sys.argv[1:],
        additional_data
        )

    print(ret['message'])

    logging.info("Exit Code: {}".format(ret['code']))

    return ret['code']


def _get_subcommands_text(commands_dict, command, warnings=False):

    commands_dict = copy.copy(commands_dict)

    if '_help' in commands_dict:
        del commands_dict['_help']

    commands_text = ''

    if not command in commands_dict:
        logging.error("No command '{}' supported by this software")
        commands_text = 1

    else:

        if '_help' in commands_dict[command]:
            del commands_dict[command]['_help']

        order = None

        if '_order' in commands_dict[command]:
            order = commands_dict[command]['_order']
            del commands_dict[command]['_order']

        if order == None:
            if warnings:
                logging.warning("No subcommands order")
            order = []

        kl = list(commands_dict[command].keys())
        kl.sort()

        for i in kl:
            if not i in order:
                if warnings:
                    logging.warning("subcommand not ordered: {}".format(i))
                order.append(i)

        for i in order:
            command_help_text = inspect.getdoc(commands_dict[command][i])

            if isinstance(command_help_text, str):
                command_help_text = command_help_text.splitlines()[0].strip()

            if not isinstance(command_help_text, str):
                command_help_text = NO_DOCUMENTATION

            commands_text += "    {command}\n        {doc}\n\n".format(
                command=i,
                doc=command_help_text
                )

    return commands_text


def _get_commands_text(commands_dict, warnings=False):

    commands_dict = copy.copy(commands_dict)

    if '_help' in commands_dict:
        del commands_dict['_help']

    commands_text = ''

    order = None
    if '_order' in commands_dict:
        order = commands_dict['_order']
        del commands_dict['_order']

    if order == None:
        if warnings:
            logging.warning("No commands order")
        order = []

    kl = list(commands_dict.keys())
    kl.sort()

    for i in kl:
        if not i in order:
            if warnings:
                logging.warning("command not ordered: {}".format(i))
            order.append(i)

    for i in order:
        command_help_text = ''
        if not '_help' in commands_dict[i]:
            command_help_text = NO_DOCUMENTATION
        else:
            command_help_text = \
                commands_dict[i]['_help'].splitlines()[0].strip()

        commands_text += "    {command}\n        {doc}\n\n".format(
            command=i,
            doc=command_help_text
            )

    return commands_text


def program_help(command_name, commands, command, subcommand, warnings=False):
    """
    Return help for program, it's module or module's command

    command_name - if not given -- not added to render
    """

    command_name_text = ''
    if command_name != None:
        command_name_text = '{} '.format(command_name)

    ret = ''

    if command != None:

        if not command in commands:
            logging.error("No such command: {}".format(command))
            ret = 1
        else:
            if subcommand != None:
                if not subcommand in commands[command]:
                    logging.error(
                        "No such subcommand: {}::{}".format(
                            command, subcommand
                            )
                        )
                    ret = 1

    if not isinstance(ret, str):
        pass
    else:
        if command == subcommand == None:

            commands_text = _get_commands_text(commands, warnings)

            ret = """\
Usage: {command_name} [command] [subcommand] [options] [parameters]

commands:

{}

    --help          see this help or help for command or subcommand
    --version       version Info
""".format(commands_text, command_name=command_name_text)

        elif subcommand == None:
            commands_text = _get_subcommands_text(commands, command, warnings)

            command_help = NO_DOCUMENTATION

            if '_help' in commands[command]:
                command_help = commands[command]['_help']

            ret = """\
Usage: {command_name} {command} [subcommand] [options] [parameters]

{command_help}

subcommands:

{commands_text}

    --help          see this help or help for command or subcommand
    --version       version Info
""".format(
               command=command,
               commands_text=commands_text,
               command_help=command_help,
               command_name=command_name_text
               )
        else:
            commands_text = inspect.getdoc(commands[command][subcommand])

            if not isinstance(ret, str):
                commands_text = NO_DOCUMENTATION

            ret = """\
Usage: {command_name} {command} {subcommand} [options] [parameters]

{commands_text}

""".format(
               command=command,
               subcommand=subcommand,
               commands_text=commands_text,
               command_name=command_name_text
               )

    return ret
