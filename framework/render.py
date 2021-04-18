import os

from jinja2 import Template


def render(template_name, folder='templates', **kwars):
    """
    Функция рендеринга шаблона html.
    :param template_name имя шаблона
    :param folder папка с шаблонами
    :param kwars параметры для рендеринга
    :return Рендер шаблона
    """
    file_path = os.path.join(folder, template_name)
    with open(file_path, encoding='utf-8') as file:
        template = Template(file.read())
        # Рендерим шаблон с параметрами
    return template.render(**kwars)
