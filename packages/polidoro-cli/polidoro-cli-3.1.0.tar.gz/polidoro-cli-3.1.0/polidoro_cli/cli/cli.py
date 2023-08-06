import os
from string import Template
from subprocess import run

import sys
import re

from polidoro_argument import Command


class CLI:
    """
    Class to create CLI commands
    """

    @staticmethod
    def create_file_commands(full_path):
        """
        Create commands reading from file
        """
        file = full_path.split('/')[-1]
        clazz_name = file.split('.')[0].title()
        clazz = getattr(sys.modules.get(clazz_name.lower(), None), clazz_name, None)
        if clazz is None:
            clazz = type(clazz_name, (object,), {})

        if not hasattr(clazz, 'help'):
            setattr(clazz, 'help', clazz.__qualname__ + ' CLI commands')

        local_vars = {}
        with open(full_path, 'r', newline='') as file:
            for line in file.readlines():
                line = line.strip()
                if line and not line.startswith('#'):
                    # set local variables defined in .cli file with `set VAR`
                    if line.startswith("set"):
                        local_var, _, value = line[4:].partition('=')
                        local_vars[local_var] = value.split(',')
                    else:
                        name, _, command = line.partition('=')
                        CLI._create_command(name, command, clazz, **local_vars)

    @staticmethod
    def _create_command(name, command, clazz, **local_vars):
        run_cmd = getattr(clazz, 'get_cmd_method', CLI._get_cmd_method)(command, clazz, **local_vars)
        command_alias = name.replace(' ', '').split(',')
        name = command_alias.pop(0)
        # Parser full name
        setattr(run_cmd, '__qualname__', '%s.%s' % (clazz.__qualname__, name))
        # Command name
        setattr(run_cmd, '__name__', name)
        # Command class
        setattr(run_cmd, '__objclass__', clazz)
        Command(help='Run "%s"' % command, command_alias=command_alias)(run_cmd)

    @staticmethod
    def _get_cmd_method(command, clazz, **local_vars):
        def run_cmd_method(*_remainder, docker=False):
            docker_class = getattr(sys.modules['docker'], 'Docker', None)
            interceptors = []
            substituted_command = Template(command).safe_substitute(**local_vars)
            if docker_class:
                if docker:
                    # If the argument --docker/-d in arguments, replace "$docker" (if exists) in command
                    interceptors.append(docker_class.command_interceptor)
                    substituted_command = Template(substituted_command).safe_substitute(docker='docker-compose exec $service')
                else:
                    substituted_command = Template(substituted_command).safe_substitute(docker='')

            if hasattr(clazz, 'command_interceptor'):
                interceptors.append(clazz.command_interceptor)

            for interceptor in interceptors:
                substituted_command, _remainder = interceptor(substituted_command, *_remainder)

            for cmd in substituted_command.split(';'):
                cmd = cmd.replace('  ', ' ').strip()
                # cmd = ' '.join([cmd.replace('  ', ' ').strip()] + list(_remainder))
                compiled = compile_command(cmd, *_remainder)
                run_command(compiled)

        def compile_command(cmd, *_remainder):
            cmd = cmd.strip()
            _for = re.search(r'(.*) for (\w+) in (.*)', cmd.lower())
            if _for:
                for_cmd = _for.groups()[0]
                for_var = _for.groups()[1]
                for_in = _for.groups()[2]

                # Replacing for var for '%s'
                for_cmd = ' '.join(['$for_var' if c == for_var else c for c in for_cmd.split()] + list(_remainder))
                return eval('[Template(\'' + for_cmd + '\').safe_substitute(for_var=' + for_var + ') for ' +
                            for_var + ' in ' + for_in + ']')
            elif cmd.lower().startswith('run'):
                cmds = re.search('run(.*)in(.*)done', cmd).groups()
                return 'cd %s; %s; cd..' % (cmds[1], cmds[0])

            return cmd

        def run_command(cmd):
            if isinstance(cmd, list):
                for c in cmd:
                    CLI.execute(c)
            elif isinstance(cmd, str):
                if cmd.lower().startswith('cd'):
                    os.chdir(cmd[2:].strip())
                else:
                    CLI.execute(cmd)
            else:
                raise Exception

        # method without "docker" argument
        def run_docker_cmd_method(*_remainder):
            run_cmd_method(*_remainder)

        if clazz.__name__ == 'Docker':
            return run_docker_cmd_method
        else:
            setattr(run_cmd_method, 'aliases', {'docker': 'd'})
            return run_cmd_method

    @staticmethod
    def execute(command, exit_on_fail=True, capture_output=False, show_cmd=True):
        """
        Run a shell command

        :param command: command as string
        :param exit_on_fail: If True, exit script if command fails
        :param capture_output: Return the command output AND not print in terminal
        :param show_cmd: Show command in terminal
        :return: subprocess.CompletedProcess
        """
        if show_cmd:
            print('+ %s' % command.strip())

        resp = run(command, shell=True, text=True, capture_output=capture_output)
        if exit_on_fail and resp.returncode:
            exit(resp.returncode)
        return resp
