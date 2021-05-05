from time import time


class AppRoute:
    """
    Структурный паттерн - декоратор.
    Декатор используется для добавление связки url-view в приложение.
    """

    def __init__(self, views, url):
        # Сохраняем view и url в соответсвующие переменные
        self.views = views
        self.url = url

    def __call__(self, cls):
        """
        Сам декоратор
        :param cls: декорируемый класс view
        :return:

        """
        # Сохраняем словарь в связку при обращении к декорируемому методу класса
        self.views[self.url] = cls()


class Debug:
    """
    Структурный паттерн - декоратор.
    Используется для подсчета времени выполнения функций во фреймворке.
    """

    def __init__(self, name):
        # Сохраняемым имя декорируемого объекта
        self.name = name

    def __call__(self, cls):
        """
        Сам декоратор
        :param cls: принимает декорируемый лкасс
        :return: timeit - запись о времени выполнения метода класса
        """

        def timeit(method):
            def timed(*args, **kwargs):
                ts = time()
                result = method(*args, **kwargs)
                te = time()
                delta = te - ts
                print(f'DEBUG Method {self.name} was running in {delta:2.2f} ms')
                return result
            return timed

        return timeit(cls)
