from django.shortcuts import render, redirect
from core.models import Student_Notification, Student, Student_Feedback, Result
from django.contrib import messages

def STUDENT_HOME(request):
    return render(request, 'student/home.html')

def STUDENT_NOTIFICATION(request):
    student = Student.objects.get(admin=request.user.id)
    notification = Student_Notification.objects.filter(student_id=student.id)
    context = {
        'notification': notification,
    }
    return render(request, 'student/notification.html', context)

def STUDENT_NOTIFICATION_MARK_AS_DONE(request, status):
    notification = Student_Notification.objects.get(id=status)
    notification.status = 1
    notification.save()
    return redirect('student_notification')

def STUDENT_FEEDBACK(request):
    student_id = Student.objects.get(admin=request.user.id)
    feedback_history = Student_Feedback.objects.filter(student_id=student_id)
    context = {
        'feedback_history': feedback_history,
    }
    return render(request, 'student/feedback.html', context)

def STUDENT_FEEDBACK_SAVE(request):
    if request.method == "POST":
        student_id = Student.objects.get(admin=request.user.id)
        feedback = request.POST.get('feedback')
        feedback_query = Student_Feedback(
            student_id = student_id,
            feedback = feedback,
            feedback_reply = "",
        )
        feedback_query.save()
        messages.success(request, "Feedback Sent Successfully")
        return redirect('student_feedback')
    
def VIEW_RESULT(request):
    mark = None
    student = Student.objects.get(admin=request.user.id)
    result = Result.objects.filter(student_id=student)
    for i in result:
        assignment_mark = i.assignment_mark
        exam_mark = i.exam_mark
        mark = assignment_mark + exam_mark

    context = {
        'result': result,
        'mark': mark
    }
    return render(request, 'student/view_result.html', context)