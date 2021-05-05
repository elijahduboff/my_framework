import quopri

from framework.requests import PostRequests, GetRequests


class MyFramework:
    def __init__(self, urlpatterns, front_controllers):
        """
        :param urlpatterns: словарь связок url -> view
        :param front_controllers: список middlewares
        """
        self.urlpatterns = urlpatterns
        self.front_controllers = front_controllers

    def __call__(self, environ, start_response):
        # забираем из словаря запроса текущий url
        current_url = environ['PATH_INFO']

        # Обработка слэша в пути
        if not current_url.endswith('/'):
            current_url = f'{current_url}/'

        # Формируем словарь запроса и получаем его тип
        request = {}
        method = environ['REQUEST_METHOD']
        request['method'] = method
        # Обработка POST и  GET запросов
        if method == 'POST':
            data = PostRequests().get_request_params(environ)
            request['data'] = MyFramework.decode_value(data)
            print(f'Нам пришел POST запрос {MyFramework.decode_value(data)}')
        if method == 'GET':
            request_params = GetRequests.get_request_params(environ)
            request['request_params'] = request_params
            print(f'Нам пришел GET запрос {request_params}')
        if current_url in self.urlpatterns:
            # Получаем view из словаря urlpatterns
            view = self.urlpatterns[current_url]
            # Добавляем в запрос данные из front_controllers
            for controller in self.front_controllers:
                controller(request)
            # Вызываем view
            code, text = view(request)
            # Возрвращаем http заголовки
            start_response(code, [('Content-Type', 'text/html')])
            # Вовзращаем тело ответа
            print(request)
            return [text.encode('utf-8')]
        else:
            # Если url нет в словаре, то вернем ошибку 404 - not found
            start_response('404 NOT FOUND', [('Content-Type', 'text/html')])
            return [b'Not Found']

    @staticmethod
    def decode_value(data):
        print(data)
        new_data = {}
        for k, v in data.items():
            val = bytes(v.replace('%', '=').replace("+", " "), 'UTF-8')
            val_decode_str = quopri.decodestring(val).decode('UTF-8')
            new_data[k] = val_decode_str
        print(new_data)
        return new_data


class DebugApplication(MyFramework):
    """
    Класс приложения для дебага. Наследуется от основного приложения фреймворка. Выводит данные запроса в консоль.
    """

    def __init__(self, urlpatterns, front_controllers):
        self.application = MyFramework(urlpatterns, front_controllers)
        super().__init__(urlpatterns, front_controllers)

    def __call__(self, environ, start_response):
        print('DEBUG MODE')
        print(environ)
        return self.application(environ, start_response)


class FakeApplication(MyFramework):
    """
    Класс фейкового приложения. Наследуется от основного приложения фреймворка. Отвечает на все запросы одинаково.
    """

    def __init__(self, urlpatterns, front_controllers):
        self.application = MyFramework(urlpatterns, front_controllers)
        super().__init__(urlpatterns, front_controllers)

    def __call__(self, environ, start_response):
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [b'Hello from Fake']
