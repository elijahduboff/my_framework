import os

from jinja2 import Template, FileSystemLoader, Environment


def render(template_name, folder='templates', **kwars):
    """
    Функция рендеринга шаблона html.
    :param template_name имя шаблона
    :param folder папка с шаблонами
    :param kwars параметры для рендеринга
    :return Рендер шаблона
    """
    environ = Environment()
    environ.loader = FileSystemLoader(folder)
    template = environ.get_template(template_name)
    return template.render(**kwars)
