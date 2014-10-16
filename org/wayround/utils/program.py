
import copy
import inspect
import logging
import sys

import org.wayround.utils.error
import org.wayround.utils.getopt
import org.wayround.utils.logging


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

        if not log_level_u in org.wayround.utils.logging.LEVEL_NAMES:
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
        command_name,
        commands,
        opts_and_args_list,
        additional_data
        ):

    opts, args = org.wayround.utils.getopt.getopt_keyed(opts_and_args_list)

    ret = dict(
        code=0,
        message='Default Exit',
        main_message="No Error"
        )

    args_l = len(args)

    subtree = commands

    level_depth = []

    for i in range(args_l):

        ii = args[i]

        if not ii in subtree:
            ret = dict(
                code=100,
                message='error',
                main_message="invalid command or subsection name"
                )
            break

        subtree = subtree[ii]
        level_depth.append(ii)

        if callable(subtree):
            break

    if ret['code'] != 0:
        pass
    else:

        args = args[len(level_depth):]

        args_l = len(args)

        show_help = '--help' in opts

        if callable(subtree):

            if not show_help:

                try:
                    res = subtree(
                        level_depth,
                        opts,
                        args,
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
                        message='error',
                        main_message="Interrupted Using Keyboard"
                        )
                except:
                    e = sys.exc_info()

                    ex_txt = org.wayround.utils.error.return_exception_info(
                        e,
                        tb=True
                        )

                    ret = dict(
                        code=1,
                        message='error',
                        main_message=(
                            "Error while executing command: {}\n{}".format(
                                ' '.join(level_depth),
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
                            txt = 'Some error'

                        ret = dict(
                            code=res,
                            message=txt
                            )
                    elif isinstance(res, dict):

                        ret = dict(
                            code=res['code'],
                            message='error',
                            main_message=res['message']
                            )

                    else:
                        ret = dict(
                            code=1,
                            message='error',
                            main_message=(
                                "Command returned not integer and not "
                                "dict (resetting to 1)."
                                " It has returned(type:{}):\n{}".format(
                                    type(res),
                                    res
                                    )
                                )
                            )
            else:

                # show help

                ret = {
                    'code': 0,
                    'message': "showing help",
                    'main_message': _format_command_help(level_depth, subtree)
                    }

        elif isinstance(subtree, dict):

            if not show_help:
                ret = dict(
                    code=1,
                    message='error',
                    main_message=(
                        "Callable command not supplied. "
                        "May be try use --help param."
                        )
                    )
            else:

                ret = {
                    'code': 0,
                    'message': "showing help",
                    'main_message': _format_command_level_help(
                        subtree,
                        level_depth
                        )
                    }

        else:
            raise ValueError("invalid command tree")

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

    if 'main_message' in ret and ret['main_message']:
        print('{}'.format(ret['main_message']))

    logging.info(
        "Exit Code: {} ({})".format(ret['code'], ret['message'])
        )

    return ret['code']


def _format_command_help(level_depth, function):

    command_text = inspect.getdoc(function)

    if not isinstance(command_text, str):
        command_text = NO_DOCUMENTATION

    command_name_text = ' '.join(level_depth)

    ret = """\
Usage: {command_name_text} [options] [parameters]

{command_text}

""".format(
        command_text=command_text,
        command_name_text=command_name_text
        )

    return ret


def _format_command_level_help(subtree, level_depth):

    this_tree_help = NO_DOCUMENTATION
    command_name_text = ' '.join(level_depth)
    sections_text = ''
    subcommands_text = ''
    commands_text = ''

    if '_help' in subtree:
        this_tree_help = subtree['_help']

    for i in subtree.keys():

        if i == '_help':
            continue

        if callable(subtree[i]) or not isinstance(subtree[i], dict):
            continue

        command_help_text = NO_DOCUMENTATION

        if '_help' in subtree[i]:
            command_help_text = subtree[i]['_help']

        if isinstance(command_help_text, str):
            command_help_text = command_help_text.splitlines()[0].strip()

        sections_text += """\
    {cmd_name}
        {cmd_short_descr}
        
""".format(
            cmd_name=i,
            cmd_short_descr=command_help_text)

    for i in subtree.keys():

        if i == '_help':
            continue

        if not callable(subtree[i]):
            continue

        command_help_text = inspect.getdoc(subtree[i])

        if isinstance(command_help_text, str):
            command_help_text = command_help_text.splitlines()[0].strip()

        if not isinstance(command_help_text, str):
            command_help_text = NO_DOCUMENTATION

        commands_text += """\
    {cmd_name}
        {cmd_short_descr}
        
""".format(
            cmd_name=i,
            cmd_short_descr=command_help_text)

    ret = """\
Usage: {command_name_text} [options] [parameters]

{this_tree_help}

subsections:

{sect_text}

commands:

{cmds_text}
""".format(
        this_tree_help=this_tree_help,
        command_name_text=command_name_text,
        sect_text=sections_text,
        cmds_text=commands_text
        )

    return ret
