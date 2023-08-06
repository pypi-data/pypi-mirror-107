import os
from string import Template

import yaml
from polidoro_argument import Command

from polidoro_cli import CLI


class Docker(object):
    @staticmethod
    def _get_main_docker_compose_service():
        for name, info in Docker._gel_all_docker_compose_services().items():
            if 'build' in info:
                return name

    @staticmethod
    def _gel_all_docker_compose_services():
        if os.path.exists('docker-compose.yml'):
            with open('docker-compose.yml') as file:
                return yaml.load(file, Loader=yaml.FullLoader)['services']
        return {}

    @staticmethod
    def command_interceptor(command, *remainders):
        remainders = list(remainders)
        if remainders and remainders[0] in Docker._gel_all_docker_compose_services():
            service = remainders[0]
            remainders.pop(0)
        else:
            service = Docker._get_main_docker_compose_service()
        return Template(command).safe_substitute(service=service), tuple(remainders)

    @staticmethod
    @Command(help='Stop all containers')
    def stop_all():
        services = CLI.execute('docker ps -q', capture_output=True, show_cmd=False).stdout.split()
        if services:
            CLI.execute('docker stop ' + ' '.join(services))
        print('Stopped all containers')

