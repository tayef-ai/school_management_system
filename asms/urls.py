from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .import views, hod_views, staff_views, student_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/', views.BASE, name='base'),
    path('', views.LOGIN, name='login'),
    path('dologin/', views.doLogin, name='doLogin'),
    path('profile/', views.PROFILE, name='profile'),
    path('profile/update/', views.PROFILE_UPDATE, name='profile_update'),
    path('dologout/', views.doLogout, name='doLogout'),
    #hod
    path('hod/home/', hod_views.HOME, name='hod_home'),
    path('hod/student/add/', hod_views.ADD_STUDENT, name='add_student'),
    path('hod/student/view/', hod_views.VIEW_STUDENT, name='view_student'),
    path('hod/student/edit/<str:id>/', hod_views.EDIT_STUDENT, name='edit_student'),
    path('hod/student/delete/<str:id>/', hod_views.DELETE_STUDENT, name='delete_student'),
    path('hod/student/update/', hod_views.UPDATE_STUDENT, name='update_student'),
    path('hod/student/send_notification/', hod_views.STUDENT_SEND_NOTIFICATION, name='student_send_notification'),
    path('hod/student/save_notification/', hod_views.STUDENT_SAVE_NOTIFICATION, name='student_save_notification'),
    path('hod/student/feedback/', hod_views.STUDENT_FEEDBACK, name='hod_student_feedback'),
    path('hod/student/feedback/reply/save/', hod_views.REPLY_STUDENT_FEEDBACK, name='hod_reply_student_feedback'),
    path('hod/take_attendance/', hod_views.HOD_TAKE_ATTENDANCE, name='hod_take_attendance'),
    path('hod/save_attendance/', hod_views.HOD_SAVE_ATTENDANCE, name='hod_save_attendance'),
    path('hod/view_attendance/', hod_views.HOD_VIEW_ATTENDANCE, name='hod_view_attendance'),
    path('hod/add/result/', hod_views.HOD_ADD_RESULT, name='hod_add_result'),
    path('hod/save/result/', hod_views.HOD_SAVE_RESULT, name='hod_save_result'),
    #students
    path('student/home/', student_views.STUDENT_HOME, name='student_home'),
    path('student/notification/', student_views.STUDENT_NOTIFICATION, name='student_notification'),
    path('student/feedback/', student_views.STUDENT_FEEDBACK, name='student_feedback'),
    path('student/feedback/save/', student_views.STUDENT_FEEDBACK_SAVE, name='student_feedback_save'),
    path('student/mark_as_done/<str:status>', student_views.STUDENT_NOTIFICATION_MARK_AS_DONE, name='student_notification_mark_as_done'),
    path('student/view_result/', student_views.VIEW_RESULT, name='view_result'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
