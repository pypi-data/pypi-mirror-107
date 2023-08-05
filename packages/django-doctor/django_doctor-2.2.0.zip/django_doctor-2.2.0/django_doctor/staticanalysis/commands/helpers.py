from contextlib import contextmanager
import difflib
import functools
import logging
import pathlib
import textwrap
import os

from pylint.reporters.text import colorize_ansi

from django_doctor.staticanalysis import checker, meta, render, transformer, message_templates


logger = logging.getLogger(__name__)

blue = functools.partial(colorize_ansi, color="blue")
red = functools.partial(colorize_ansi, color="red")
green = functools.partial(colorize_ansi, color="green")


def color_diff(line):
    if line.startswith('+'):
        color = "green"
    elif line.startswith('-'):
        color = "red"
    else:
        color = None
    return colorize_ansi(line, color=color)


class Message(dict):
    def __getattr__(self, key):
        return self.get(key)

    def _replace(self, **msg):
        self.update(msg)
        return self

    def format(self, template):
        rendered = template.format(**self)
        if self['diff']:
            diff = difflib.unified_diff(
                a=[line for number, line in self['diff']['before']],
                b=[line for number, line in self['diff']['after']],
                lineterm='',
                n=0,
            )
            # skipping the headers "+++" and "---"
            next(diff)
            next(diff)
            joined_diff = '\n'.join([color_diff(item) for item in diff])
            rendered += ('\n    Consider this change:\n' + textwrap.indent(joined_diff, ' ' * 8)) + '\n'

        return rendered


def get_messages(project_root, ignore):
    files = meta.get_files_to_check_in_project(project_root=project_root, ignore=ignore)

    logger.info(
        f"Found {len(files)} files. HINT: use --log-level=debug to see what files were found, "
        "and use --ignore=foo to skip any directories you don't want to check.\n"
    )

    messages = checker.get_messages(project_root=project_root, files=files)
    rendered_messages = render.render_line_centric_advice(
        messages=messages,
        project_root=project_root,
        settings={"STATIC_URL": meta.get_static_url_setting(project_root)},
        settings_modpath=meta.get_settings_modpath(project_root),
        code_style=meta.get_code_style(project_root),
    )
    for item in rendered_messages:
        line_messages = []
        for message_id in item["message_ids"]:
            template = getattr(message_templates, message_id)
            line_message = render.render_template(
                template=template['report'],
                message={**item, 'message-id': message_id, 'message': item['context']}
            )
            line_messages.append(f'{line_message} ➡ Read more: {get_hyperlink(message_id)}')
        yield Message(
            **item,
            msg=textwrap.indent('\n'.join(f'⚠️  {item}' for item in sorted(line_messages)), '    '),
            module=item["path"],
            C='W'
        )


def trasform_files(project_root, whitelist):
    filepaths = transformer.trasform_files_in_place(project_root=project_root, whitelist=whitelist)
    body = ""
    for path in filepaths:
        if 'models.py' in path:
            body = " models.py has changed, so please run `./manage.py makemigrations`."
    logger.info(green(f"\n\nChanges saved successfully. {body}"))


@contextmanager
def chdir(path):
    origin = pathlib.Path().absolute()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(origin)


def get_hyperlink(message_id):
    return f'https://django.doctor/advice/{message_id}'
