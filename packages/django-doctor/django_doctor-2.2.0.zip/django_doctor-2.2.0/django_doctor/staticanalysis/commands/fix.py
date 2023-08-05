import logging
import sys
import webbrowser

from django_doctor.staticanalysis.commands import helpers, wsgi
from django_doctor.staticanalysis import constants


logger = logging.getLogger(__name__)


MESSAGE = (
    "Analyzing your Django code.\n"
    "The suggestion engine will soon open in your browser on http://{address}:{port}\n"
    "Use Ctrl+C or Command+C etc to exit."
)


def handle(project_root, ignore, address, port):
    sys.path.insert(0, project_root)

    logger.info(helpers.blue(MESSAGE.format(address=address, port=port)))

    with helpers.chdir(project_root):
        messages = list(helpers.get_messages(project_root=project_root, ignore=ignore))

        for message in messages:
            if message['message_ids'].intersection(constants.TRANSFORMABLE_RULES):
                break
        else:
            logger.info(helpers.green("\n\nNo autofixable issues detected. Good job.\n"))
            return

        # TODO: somehow resolve from django-doctor package
        server = wsgi.create(
            address=address,
            port=port,
            project_root=project_root,
            messages=messages,
        )
        webbrowser.open_new(f"http://{address}:{port}")
        server.serve_forever()
