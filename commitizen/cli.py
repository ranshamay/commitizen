import os
import io
import logging
import argparse
import sys
# from pathlib import Path
from configparser import RawConfigParser
from commitizen import (registered, run, set_commiter, show_example,
                        show_info, show_schema)

logger = logging.getLogger(__name__)


def get_parser(config):
    description = (
        'Commitizen is a cli tool to generate conventional commits.\n'
        'For more information about the topic go to '
        'https://conventionalcommits.org/'
    )

    formater = argparse.RawDescriptionHelpFormatter
    parser = argparse.ArgumentParser(prog='cz',
                                     description=description,
                                     formatter_class=formater)
    parser.set_defaults(func=run)
    parser.add_argument('--debug', action='store_true', default=False,
                        help='use debug mode')
    parser.add_argument('-n', '--name', default=config.get('name'),
                        help='use the given commitizen')
    subparser = parser.add_subparsers(title='commands')
    # subparser.add_argument('--debug', default=False)

    lscz = subparser.add_parser('ls', help='show available commitizens')
    lscz.set_defaults(func=registered)

    # commit = subparser.add_parser('commit', aliases=['c'],
    #                               help='create new commit')

    commit = subparser.add_parser('commit',
                                  help='create new commit')
    commit.set_defaults(func=run)

    example = subparser.add_parser('example', help='show commit example')
    example.set_defaults(func=show_example)

    info = subparser.add_parser('info', help='show information about the cz')
    info.set_defaults(func=show_info)

    schema = subparser.add_parser('schema', help='show commit schema')
    schema.set_defaults(func=show_schema)

    return parser


def load_cfg():
    defaults = {
        'name': 'cz_conventional_changelog'
    }
    config = RawConfigParser('')

    home = str(os.path.expanduser("~"))
    config_file = '.cz'

    # load cfg from home folder
    global_cfg = os.path.join(home, config_file)
    if os.path.exists(global_cfg):
        config.readfp(io.open(global_cfg, 'rt', encoding='utf-8'))
        log_config = io.StringIO()
        config.write(log_config)
        defaults.update(dict(config.items("commitizen")))

    # load cfg from current project
    configs = ['setup.cfg', '.cz.cfg']
    for cfg in configs:
        if not os.path.exists(config_file) and os.path.exists(cfg):
            config_file = cfg
            break

    config_file_exists = os.path.exists(config_file)
    if config_file_exists:
        logger.debug('Reading file "%s"', config_file)
        config.readfp(io.open(config_file, 'rt', encoding='utf-8'))
        log_config = io.StringIO()
        config.write(log_config)
        defaults.update(dict(config.items("commitizen")))

    return defaults


def cz(args):
    sys.argv = [sys.argv[0]] + args

    config = load_cfg()
    parser = get_parser(config)
    args = parser.parse_args()

    if args.debug:
        logging.getLogger('commitizen').setLevel(logging.DEBUG)

    set_commiter(config.get('name'))
    change_type = args.func(args)
    return change_type


def main():
    config = load_cfg()
    parser = get_parser(config)
    args = parser.parse_args()

    if args.debug:
        logging.getLogger('commitizen').setLevel(logging.DEBUG)

    set_commiter(args.name)
    args.func(args)
