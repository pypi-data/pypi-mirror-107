from jinja2 import Environment, FileSystemLoader, select_autoescape
import pathlib

def render(template_path, params):
    env = Environment(
        loader=FileSystemLoader(searchpath=pathlib.Path().absolute(), encoding='UTF-8', followlinks=False),
        autoescape=select_autoescape()
    )
    template = env.get_template(template_path)
    return template.render(**params)

