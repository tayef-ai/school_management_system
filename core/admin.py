from django.contrib import admin
from .models import CustomUser, Course, Session, Student, Student_Notification, Student_Feedback, Attendance, Attendance_Report, Result
from django.contrib.auth.admin import UserAdmin

class UserModel(UserAdmin):
    list_display = ['username', 'user_type']
admin.site.register(CustomUser, UserModel)
admin.site.register(Course)
admin.site.register(Session)
admin.site.register(Student)
admin.site.register(Student_Notification)
admin.site.register(Student_Feedback)
admin.site.register(Attendance)
admin.site.register(Attendance_Report)
admin.site.register(Result)