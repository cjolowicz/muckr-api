import importlib

import muckr.app

app = muckr.app.create_app()


def _import(name):
    module, attribute = name.rsplit('.', 1)
    value = getattr(importlib.import_module(module), attribute)
    return attribute, value


@app.shell_context_processor
def make_shell_context():
    return dict(map(_import, [
        'muckr.extensions.database',
        'muckr.models.User',
    ]))
