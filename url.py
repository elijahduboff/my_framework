from datetime import datetime

import views

urlpatterns = {
    '/': views.Index(),
    '/about/': views.About(),
    '/study-programs/': views.StudyPrograms(),
    '/course-list/': views.CourseList(),
    '/create-course/': views.CreateCourse(),
    '/category-list/': views.CategoryList(),
    '/create-category/': views.CreateCategory(),
    '/copy-course/': views.CopyCourse()
}


def author_front(request):
    request['author'] = 'Elijah Duboff'


def year_controller(request):
    request['year'] = datetime.now().year

front_controllers = [author_front, year_controller]
