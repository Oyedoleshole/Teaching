from django.urls import path
from .views import RegisterUser, login_user, Task_added_by_admin, email_verification,ParentCreateKidUniqueId
from teacher.views import TeacherList, show_student_relate_to_teacher_, task_assign_to_student_by_teacher, TaskAssignToStudentByTeacher \
, TeacherRemarkAfterPostedTaskForStudent
from student.views import Student_class, StudentLogin, show_student_details
from task.views import ShowTaskBasedOnDateAndCategory, TaskProgress_orDone, create_task_type, create_age_group
from parent.views import CreateSudentUniqueID
urlpatterns = [
    path('email/verification/',email_verification),
    path('task_creation/',Task_added_by_admin.as_view()),
    path('register/',RegisterUser.as_view(), name="register_the_user"),
    path('login/', login_user, name='login_user'),
    path('list-of-teachers/',TeacherList.as_view()),
    path('list-of-students/',Student_class.as_view()),
    path('show-student-relate-to-teachers/',show_student_relate_to_teacher_),
    path('past-task/',ShowTaskBasedOnDateAndCategory.as_view()),
    path('task-completion/',TaskProgress_orDone.as_view()),
    path('create-parent/',ParentCreateKidUniqueId),
    path('create-unique-student-id/', CreateSudentUniqueID),
    path('task-assigned-to-student-by-teacher/',task_assign_to_student_by_teacher.as_view()),
    path('student-login/',StudentLogin.as_view()),
    path('student-details/',show_student_details),
    path('teacher-add-remark-and-file/',TeacherRemarkAfterPostedTaskForStudent.as_view()),
    path('create-task-type/',create_task_type),
    path('create-age-group/',create_age_group)
]