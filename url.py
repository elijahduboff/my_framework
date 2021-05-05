from datetime import datetime


def author_front(request):
    request['author'] = 'Elijah Duboff'


def year_controller(request):
    request['year'] = datetime.now().year


front_controllers = [author_front, year_controller]
