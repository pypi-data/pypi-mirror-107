import logging
import sys

from django_doctor.staticanalysis.commands import helpers

from pylint.reporters.text import ColorizedTextReporter


logger = logging.getLogger(__name__)


def handle(project_root, ignore, output=sys.stdout):
    sys.path.insert(0, project_root)
    reporter = ColorizedTextReporter(output=output)

    reporter._template = "{path}:{line}\n{msg}"

    message = None
    with helpers.chdir(project_root):
        for message in helpers.get_messages(project_root=project_root, ignore=ignore):
            reporter.handle_message(message)

    exit_code = 0 if message is None else 1
    sys.exit(exit_code)
