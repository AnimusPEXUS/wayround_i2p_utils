

import copy
import inspect
import logging

NO_DOCUMENTATION = '(No documentation)'

def get_subcommands_text(commands_dict, command):

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
            logging.warning("No subcommands order")
            order = []

        kl = list(commands_dict[command].keys())
        kl.sort()

        for i in kl:
            if not i in order:
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


def get_commands_text(commands_dict):

    commands_dict = copy.copy(commands_dict)

    if '_help' in commands_dict:
        del commands_dict['_help']

    commands_text = ''

    order = None
    if '_order' in commands_dict:
        order = commands_dict['_order']
        del commands_dict['_order']

    if order == None:
        logging.warning("No commands order")
        order = []

    kl = list(commands_dict.keys())
    kl.sort()

    for i in kl:
        if not i in order:
            logging.warning("command not ordered: {}".format(i))
            order.append(i)

    for i in order:
        command_help_text = ''
        if not '_help' in commands_dict[i]:
            command_help_text = NO_DOCUMENTATION
        else:
            command_help_text = commands_dict[i]['_help'].splitlines()[0].strip()

        commands_text += "    {command}\n        {doc}\n\n".format(
            command=i,
            doc=command_help_text
            )

    return commands_text

def program_help(command_name, commands, command, subcommand):
    """
    Show help for program, it's module or module's command
    """

    ret = ''

    if command != None:

        if not command in commands:
            logging.error("No such command: {}".format(command))
            ret = 1
        else:
            if subcommand != None:
                if not subcommand in commands[command]:
                    logging.error(
                        "No such subcommand: {}::{}".format(command, subcommand)
                        )
                    ret = 1

    if not isinstance(ret, str):
        pass
    else:
        if command == subcommand == None:

            commands_text = get_commands_text(commands)

            ret = """\
Usage: {command_name} [command] [subcommand] [options] [parameters]

commands:

{}

    --help          see this help or help for command or subcommand
    --version       version Info
""".format(commands_text, command_name=command_name)


        elif subcommand == None:
            commands_text = get_subcommands_text(commands, command)

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
""".format(command=command, commands_text=commands_text, command_help=command_help, command_name=command_name)
        else:
            commands_text = inspect.getdoc(commands[command][subcommand])

            if not isinstance(ret, str):
                commands_text = NO_DOCUMENTATION

            ret = """\
Usage: {command_name} {command} {subcommand} [options] [parameters]

{commands_text}

""".format(command=command, subcommand=subcommand, commands_text=commands_text, command_name=command_name)

    return ret
