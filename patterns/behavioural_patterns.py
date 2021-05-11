import json

from framework.render import render


class Observer:
    """
    Поведенческий паттерн - наблюдатель.
    Класс наблюдателя за субъектом.
    """

    def update(self, subject):
        pass


class Subject:
    """
    Поведенческий паттерн - наблюдатель.
    Класс объекта, за которым ведется наблюдение.
    """

    def __init__(self):
        self.observers = []

    def notify(self):
        for item in self.observers:
            item.update(self)


class SMSNotifier(Observer):
    """ Класс наблюдателя, наследуется от абстрактного наблюдателя. Отправляет уведомления через SMS """

    def update(self, subject):
        print(f'SMS ---> К нам присоединился {subject.students[-1].name}')


class EmailNotifier(Observer):
    """ Класс наблюдателя, наследуется от абстрактного наблюдателя. Отправляет уведомления через SMS """

    def update(self, subject):
        print(f'Email ---> К нам присоединился {subject.students[-1].name}')


class BaseSerializer:
    """ Поведенческий паттерн - Хранитель """

    def __init__(self, obj):
        self.obj = obj

    def save(self):
        return json.dumps(self.obj)

    @staticmethod
    def load(data):
        return json.loads(data)


class TemlateView:
    """
    Поведенческий паттерн - шаблонный метод.
    """
    template_name = 'template.html'

    def get_context_data(self):
        return {}

    def get_template(self):
        return self.template_name

    def render_template_with_context(self):
        template_name = self.get_template()
        context = self.get_context_data()
        return '200 OK', render(template_name, **context)

    def __call__(self, request):
        return self.render_template_with_context()


class ListView(TemlateView):
    """
    Поведенческий паттерн - шаблонный метод.
    """
    queryset = []
    template_name = 'list.html'
    context_object_name = 'objects_list'

    def get_queryset(self):
        return self.queryset

    def get_context_object_name(self):
        return self.context_object_name

    def get_context_data(self):
        queryset = self.get_queryset()
        context_object_name = self.get_context_object_name()
        context = {context_object_name: queryset}
        return context


class CreateView(TemlateView):
    """
    Поведенческий паттерн - шаблонный метод.
    """
    template_name = 'create.html'

    @staticmethod
    def get_request_data(request):
        return request['data']

    def create_obf(self, data):
        pass

    def __call__(self, request):
        if request['method'] == 'POST':
            data = self.get_request_data(request)
            self.create_obf(data)
            return self.render_template_with_context()
        else:
            return super().__call__(request)


class ConsoleLogger:
    """
    Поведенческий паттерн - стратегия. Класс определяет стратегию логирования в консоль
    """

    def write(self, text):
        print(text)


class FileLogger:
    """
    Поведенческий паттерн - стратегия. Класс определяет стратегию логирования в файл
    """

    def __init__(self, file):
        self.file = file

    def write(self, text):
        with open(self.file, 'a', encoding='utf-8') as f:
            f.write(f'{text}\n')
