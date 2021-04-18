from wsgiref.simple_server import make_server

from framework.framework_core import MyFramework
from url import urlpatterns, front_controllers

framework = MyFramework(urlpatterns=urlpatterns, front_controllers=front_controllers)

with make_server('', 8080, framework) as httpd:
    print('Запуск сервера на порту 8080...')
    httpd.serve_forever()
