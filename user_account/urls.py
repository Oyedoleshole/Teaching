from django.urls import path
from .views import RegisterUser, login_user, Task_added_by_admin, email_verification,delete_any_account, resend_otp
from teacher.views import TeacherList, show_student_relate_to_teacher_, task_assign_to_student_by_teacher, TaskAssignToStudentByTeacher \
, TeacherRemarkAfterPostedTaskForStudent, GetTheTeacherData, AfterHomeScreenTask, homeforteacher, ActivityProgressForTeacher, task_progress_for_teacher_app \

from student.views import Student_class, StudentLogin, show_student_details, get_student_profile_details, FilterTaskForStudent, TaskDoneByStudentAPI
from task_app.views import ShowTaskBasedOnDateAndCategory, create_task_type, create_age_group, update_the_task \
, ShowActivityProgressofTask
from parent.views import CreateSudentUniqueID
urlpatterns = [
    path('email/verification/',email_verification),
    path('task_creation/',Task_added_by_admin.as_view()),
    path('register/',RegisterUser.as_view(), name="register_the_user"),
    path('login/', login_user, name='login_user'),
    path('resend-otp/',resend_otp),
    path('list-of-teachers/',TeacherList.as_view()),
    path('list-of-students/',Student_class.as_view()),
    path('show-student-relate-to-teachers/',show_student_relate_to_teacher_),
    path('past-task/',ShowTaskBasedOnDateAndCategory.as_view()),
    path('create-unique-student-id/', CreateSudentUniqueID),
    path('task-assigned-to-student-by-teacher/',task_assign_to_student_by_teacher.as_view()),
    path('student-login/',StudentLogin.as_view()),
    path('student-details/',show_student_details),
    path('teacher-add-remark-and-file/',TeacherRemarkAfterPostedTaskForStudent.as_view()),
    path('create-task-type/',create_task_type),
    path('create-age-group/',create_age_group),
    path('get-the-teacher-data/',GetTheTeacherData.as_view()),
    path('update-the-existence-task/',update_the_task),
    path('show-activity-progress-of-task/',ShowActivityProgressofTask.as_view()),
    path('home-screen-for-teacher/',homeforteacher),
    path('teacher-selection-task/',AfterHomeScreenTask.as_view()),
    path('show-activity-progress-of-task-for-requested-teacher/',ActivityProgressForTeacher.as_view()),
    path('show-task-progress-of-task-for-requested-teacher/',task_progress_for_teacher_app),
    path('get-student-profile-details/',get_student_profile_details),
    path('delete-any-account/',delete_any_account),
    path('filter-task-for-student/',FilterTaskForStudent.as_view()),
    path('task-completion/',TaskDoneByStudentAPI.as_view())
]