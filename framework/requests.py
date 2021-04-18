class GetRequests:
    """
    Класс для обработки GET запросов к фреймворку
    """

    @staticmethod
    def parse_input_data(data: str):
        """
        Статический метод, обрабатывающий данные из запроса и возвращающий словарь
        :param data: данные, которые приходят из запроса
        :return: result - словарь с обработанными данными
        """
        result = {}
        if data:
            params = data.split('&')
            for param in params:
                # делим ключ и значение через =
                key, value = param.split('=')
                result[key] = value
        return result

    @staticmethod
    def get_request_params(environ):
        """
        Статический метод, читает параметры запроса и возвращает словарь с параметрами
        :param environ: байты запросы
        :return: request_params словарь с параметрами запроса
        """
        # получаем параметры запроса
        query_string = environ['QUERY_STRING']
        # превращаем параметры в словарь
        request_params = GetRequests.parse_input_data(query_string)
        return request_params


class PostRequests:
    """
    Класс обработчик POST запросов
    """

    @staticmethod
    def parse_input_data(data: str):
        """
        Статический метод, обрабатывающий данные из запроса и возвращающий словарь
        :param data: данные, которые приходят из запроса
        :return: result - словарь с обработанными данными
        """
        result = {}
        if data:
            params = data.split('&')
            for param in params:
                # делим ключ и значение через =
                key, value = param.split('=')
                result[key] = value
        return result

    @staticmethod
    def get_wsgi_input_data(environ) -> bytes:
        """
        Статический метод. Получает wsgi данные из запроса
        :param environ: запрос
        :return: data - wsgi данные из запроса
        """
        content_lenght_data = environ.get('CONTENT_LENGTH')
        content_lenght = int(content_lenght_data) if content_lenght_data else 0
        data = environ['wsgi.input'].read(content_lenght) if content_lenght_data > 0 else b''
        return data

    def parse_wsgi_input_data(self, data: bytes) -> dict:
        """
        Метод, который преобразует байты в словарь
        :param data:
        :return: result словарь с данными
        """
        result = {}
        if data:
            data_str = data.decode(encoding='utf-8')
            result = self.parse_input_data(data_str)
        return result

    def get_request_params(self, environ) -> dict:
        """
        Метод, который собирает параметры из запроса
        :param environ: байты с запросом
        :return: data тело запроса в словаре
        """
        data = self.get_wsgi_input_data(environ)
        data = self.get_wsgi_input_data(data)
        return data

