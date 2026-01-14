from flask import render_template


def template(name, *args, **kwargs):
    if not name.endswith('.j2'):
        name = name + '.j2'
    context = {}
    for arg in args:
        if isinstance(arg, dict):
            context.update(arg)
        else:
            raise TypeError("template() only accepts dict positional args")
    context.update(kwargs)
    return render_template(name, **context)
