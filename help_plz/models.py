from django.db import models
from django.contrib.auth.models import User
import rules


@rules.predicate
def is_teacher(user, klass):
    if klass == None or user == None:
        return False
    return user in klass.teachers.all()


@rules.predicate
def is_tutor(user, klass):
    if klass == None or user == None:
        return False
    return user in klass.tutors.all()


@rules.predicate
def is_student(user, klass):
    if klass == None or user == None:
        return False
    return user in klass.students.all()


@rules.predicate
def class_member(user, klass):
    if klass == None or user == None:
        return False
    return (is_tutor | is_teacher | is_student)(user, klass)


@rules.predicate
def concur_request(user, request):
    if request == None or user == None:
        return False
    return class_member(user, request.klass)


@rules.predicate
def start_request(user, request):
    if request == None or user == None:
        return False
    return (is_teacher | is_tutor)(user, request.klass)


@rules.predicate
def mark_done_request(user, request):
    if request == None or user == None:
        return False
    return (is_teacher | is_tutor)(user, request.klass)


@rules.predicate
def view_private_request(user, request):
    if request == None or user == None:
        return False
    return (is_teacher | is_tutor)(user, request.klass)


@rules.predicate
def add_help_request(user, klass):
    if klass == None or user == None:
        return False
    return class_member(user, klass)


@rules.predicate
def delete_help_request(user, request):
    if request == None or user == None:
        return False
    return (is_teacher | is_tutor)(user, request.klass)


rules.add_perm('help_request.can_concur', concur_request)
rules.add_perm('help_request.can_mark_started', start_request)
rules.add_perm('help_request.can_mark_done', mark_done_request)
rules.add_perm('help_request.can_view_private', view_private_request)
rules.add_perm('class.add_help_request', class_member)
rules.add_perm('class.can_view', class_member)
rules.add_perm('help_request.delete_help_request', delete_help_request)


class Class(models.Model):
    teachers = models.ManyToManyField(User, related_name="teaching_set")
    tutors = models.ManyToManyField(User, related_name="tutoring_set")
    students = models.ManyToManyField(User, related_name="class_set")
    name = models.CharField(max_length=50, default="default_name", unique=True)
    student_password = models.CharField(max_length=50, default="password")
    tutor_password = models.CharField(max_length=50, default="password")
    teacher_password = models.CharField(max_length=50, default="password")

    def in_class(self, user):
        return (user in self.teachers.all()) or (user in self.tutors.all()) or (user in self.student.all())

    def can_mark_started(self, user):
        return (user in self.teachers.all()) or (user in self.tutors.all())

    def can_mark_done(self, user):
        return (user in self.teachers.all()) or (user in self.tutors.all())

    def can_view_private(self, user):
        return (user in self.teachers.all()) or (user in self.tutors.all())

    def __str__(self):
        return self.name

# Create your models here.


class HelpRequest(models.Model):
    #name = models.CharField('your name', max_length=20)
    klass = models.ForeignKey(Class, default=1, on_delete=models.CASCADE)
    topic = models.CharField(max_length=50)
    HIGH = ("HIGH", "H")
    LOW = ("LOW", "L")
    MEDIUM = ("MEDIUM", "M")
    URGENCY_CHOICES = (
        HIGH, MEDIUM, LOW
    )
    urgency = models.CharField(max_length=1, choices=URGENCY_CHOICES,
                               blank=True)
    pub_datetime = models.DateTimeField('request time', auto_now=True)
    public = models.BooleanField(default=True)
    started = models.BooleanField(default=False)
    helper = models.ForeignKey(User, related_name="helped", blank=True, null=True)
    request_teacher = models.BooleanField(default=False)
    creator = models.ForeignKey(User, related_name="created", on_delete=models.CASCADE, default=1)
    concurers = models.ManyToManyField(User, related_name="concurers")

    def __str__(self):
        x = self.creator.username + ' needs help'
        if not self.topic.__str__() == '':
            x += ' with ' + self.topic.__str__()
        return x
