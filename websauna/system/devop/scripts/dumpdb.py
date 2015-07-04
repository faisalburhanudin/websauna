"""ws-dump-db command entry point.

Wrapper for pgsql-dump.bash script. Extract database settings from registry and pass to Bash script.
"""

import subprocess

import os
import sys

from pyramid.paster import bootstrap

from websauna.utils.configincluder import monkey_patch_paster_config_parser
from websauna.utils.exportenv import create_settings_env


DUMP_SCRIPT = os.path.join(os.path.dirname(__file__), "psql-dump.bash")


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [ARG1, ARG2]\n'
          '(example: "%s development.ini") \n'
          'All arguments are passed to pg_dump command' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):

    monkey_patch_paster_config_parser()

    if len(argv) < 2:
        usage(argv)

    config_uri = argv[1]
    args = argv[2:]

    env = bootstrap(config_uri, options=dict(sanity_check=False))

    # Export all secrets and settings
    bash_env = create_settings_env(env["registry"])

    # subprocess.check_output([DUMP_SCRIPT] + args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env)
    cmd = [DUMP_SCRIPT] + args
    with subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=1, env=bash_env, universal_newlines=True) as p:
        for line in p.stdout:
            print(line, end='')


if __name__ == "__main__":
    main()