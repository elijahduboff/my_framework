import copy
import quopri

from patterns.behavioural_patterns import ConsoleLogger


class User:
    """ Класс абстрактного пользователя """
    auto_id = 0

    def __init__(self, name):
        self.id = User.auto_id
        User.auto_id += 1
        self.name = name


class Student(User):
    """ Класс студента курсов """
    pass


class Teacher(User):
    """ Класс преподавателя курсов """
    pass


class UserFactory:
    """ Порождающий паттерн абстрактная фабрика для создания объектов с классом пользователь """
    types = {
        'student': Student,
        'teacher': Teacher
    }

    @classmethod
    def create(cls, type_, name):
        """ Пораждающий паттерн фабричный метод """
        return cls.types[type_](name)


class CoursePrototype:
    """ Порождающий паттерн-прототип курсов """

    def clone(self):
        return copy.deepcopy(self)


class Course(CoursePrototype):
    """ Конструктор создания нового курса из прототипа """

    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)


class InteractiveCourse(Course):
    """ Интерактивный курс """
    pass


class VideoCourse(Course):
    """ Видео курс """
    pass


class Category:
    """ Класс для категории курсов """
    auto_id = 0

    def __init__(self, name, category):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.category = category
        self.courses = []

    def course_count(self):
        result = len(self.courses)
        if self.category:
            result += self.category.course_count()
        return result


class CourseFactory:
    """ Порождающий паттерн абстрактная фабрика для категорий курсов """
    types = {
        'interactive': InteractiveCourse,
        'video': VideoCourse
    }

    @classmethod
    def create(cls, type_, name, category):
        """ Фабричный метод"""
        return cls.types[type_](name, category)


class University:
    """ Основной класс проекта """

    def __init__(self):
        self.teachers = []
        self.students = []
        self.courses = []
        self.categories = []

    @staticmethod
    def create_user(type_, name):
        return UserFactory.create(type_, name)

    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)

    def find_category_by_id(self, category_id):
        for category in self.categories:
            if category.id == category_id:
                return category
        raise Exception(f'Категория с {category_id} не найдена')

    @staticmethod
    def create_course(type_, name, category):
        return CourseFactory.create(type_, name, category)

    def get_course(self, name):
        for course in self.courses:
            if course.name == name:
                return course
        return None

    def get_student(self, name) -> Student:
        for item in self.students:
            if item.name == name:
                return item

    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = quopri.decodestring(val_b)
        return val_decode_str.decode('utf-8')


class SingletoneByName(type):
    """ Порождающий паттерн Синглтон """

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']
        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=SingletoneByName):
    """ Класс логирования с использованием порождающего паттерна Синглтон """

    def __init__(self, name, writer=ConsoleLogger()):
        self.name = name
        self.writer = writer

    def log(self, text):
        self.writer.write(text)
