import logging
import subprocess

from cliwrap import utils


def run(command, options, on_success=utils.do_nothing, on_error=utils.do_nothing):
    try:
        command.extend(options)

        logging.info(f'running {command}')

        subprocess.run(command, check=True)

        on_success()
        return True
    except subprocess.CalledProcessError as e:
        on_error()
        return False


def run_or_exit(command, options, on_success=utils.do_nothing, on_error=utils.do_nothing):
    has_succeeded = run(command=command, options=options, on_success=on_success, on_error=on_error)
    utils.exit_if_false(has_succeeded)
