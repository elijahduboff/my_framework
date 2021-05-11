from datetime import date

from framework.render import render
from patterns.behavioural_patterns import EmailNotifier, SMSNotifier, ListView, CreateView, BaseSerializer
from patterns.creational_patterns import University, Logger
from patterns.structural_patterns import AppRoute, Debug

site = University()
logger = Logger('main')
email_notifier = EmailNotifier()
sms_notifier = SMSNotifier()

views = {}


@AppRoute(views=views, url='/')
class Index:
    """ Контроллер - главная старница"""

    @Debug(name='index')
    def __call__(self, request):
        return '200 OK', render('index.html', objects_list=site.categories)


@AppRoute(views=views, url='/about/')
class About:
    """ Контроллер о компании """

    @Debug(name='about')
    def __call__(self, request):
        return '200 OK', render('about.html')


@AppRoute(views=views, url='/study-programs/')
class StudyPrograms:
    """ Контроллер с учебными программами """

    @Debug(name='study_programs')
    def __call__(self, request):
        return '200 OK', render('study_programs.html', data=date.today())


@AppRoute(views=views, url='/course-list/')
class CourseList:
    """ Контроллер списка курсов"""

    @Debug(name='course_list')
    def __call__(self, request):
        logger.log('Список курсов')
        try:
            category = site.find_category_by_id(int(request['request_params']['id']))
            return '200 OK', render('course_list.html', objects_list=category.courses, name=category.name,
                                    id=category.id)
        except KeyError:
            return '200 OK', 'No course have been added yet'


@AppRoute(views=views, url='/create-course/')
class CreateCourse:
    """ Контроллер создания курса """
    category_id = -1

    @Debug(name='create_course')
    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            name = site.decode_value(name)
            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))
                course = site.create_course('video', name, category)
                site.courses.append(course)
            return '200 OK', render('course_list.html', objects_list=category.courses, name=category.name,
                                    id=category.id)
        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.find_category_by_id(self.category_id)
                return '200 OK', render('create_course.html', name=category.name, id=category.id)
            except KeyError:
                return '200 OK', 'No categories have been added yet'


@AppRoute(views=views, url='/category-list/')
class CategoryList:
    """ Контроллер для списка категорий """

    @Debug(name='category_list')
    def __call__(self, request):
        logger.log('Список категорий')
        return '200 OK', render('category_list.html', objects_list=site.categories)


@AppRoute(views=views, url='/create-category/')
class CreateCategory:
    """ Контроллер для создания категории """

    @Debug(name='create_category')
    def __call__(self, request):
        print(request)
        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            name = site.decode_value(name)
            category_id = data.get('category_id')
            category = None
            if category_id:
                category = site.find_category_by_id(int(category_id))
            new_category = site.create_category(name, category)
            site.categories.append(new_category)
            return '200 OK', render('index.html', objects_list=site.categories)
        else:
            categories = site.categories
            return '200 OK', render('create_category.html', categories=categories)


@AppRoute(views=views, url='/copy-course/')
class CopyCourse:
    """ Контроллер для копирования курса """

    @Debug(name='copy_course')
    def __call__(self, request):
        request_params = request['request_params']
        try:
            name = request_params['name']
            old_course = site.get_course(name)
            if old_course:
                new_name = f'copy_{name}'
                new_course = old_course.clone()
                new_course.name = new_name
                site.courses.append(new_course)

            return '200 OK', render('course_list.html', objects_list=site.courses)
        except KeyError:
            return '200 OK', 'No courses have been added yet'


@AppRoute(views=views, url='/student-list/')
class StudentListView(ListView):
    queryset = site.students
    template_name = 'student_list.html'


@AppRoute(views=views, url='/create-student/')
class StudentCreateView(CreateView):
    template_name = 'create_student.html'

    def create_obf(self, data: dict):
        name = data['name']
        name = site.decode_value(name)
        new_obj = site.create_user('student', name)
        site.students.append(new_obj)


@AppRoute(views=views, url='/add-student/')
class AddStudentByCourseCreateView(CreateView):
    template_name = 'add_student.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['courses'] = site.courses
        context['students'] = site.students
        return context

    def create_obf(self, data):
        course_name = data['course_name']
        course_name = site.decode_value(course_name)
        course = site.get_course(course_name)
        student_name = data['student_name']
        student_name = site.decode_value(student_name)
        student = site.get_student(student_name)
        course.add_student(student)


@AppRoute(views=views, url='/api/v1')
class CourseApi:
    @Debug(name='CourseApi')
    def __call__(self, request):
        return '200 OK', BaseSerializer(site.courses).save()
