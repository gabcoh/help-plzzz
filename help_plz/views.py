from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from rules.contrib.views import permission_required, objectgetter
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404, redirect
from django.db import IntegrityError
from .models import HelpRequest, Class

def recent_requests(user):
    return HelpRequest.objects.filter(creator=user).order_by('-pub_datetime')

@permission_required('class.can_view', fn=objectgetter(Class, 'class_pk'))
def get_class(request, class_pk):
    klass = get_object_or_404(Class, pk=class_pk)
    requests = HelpRequest.objects.filter(klass=Class.objects.get(pk=class_pk))
    if klass.can_view_private(request.user):
        request_list = requests.order_by('-pub_datetime')[:]
    else:
        request_list = requests.filter(
            public=True).order_by('-pub_datetime')[:]
    if request.user.is_authenticated:
        request_list = request_list | requests.filter(creator=request.user.pk)
    context = {
        'requests_list': request_list,
        'klass': klass,
    }
    if request.user.has_perm('class.add_help_request'):
        context['urgency_choices'] = map(lambda x: x[0].title(),
                                         list(HelpRequest.URGENCY_CHOICES))
    return render(request, 'help_plz/class.html', context)


@permission_required('help_request.delete_help_request',
                     fn=objectgetter(HelpRequest,
                                     'pk'))
def delete_request(request, pk):
    request_object = get_object_or_404(HelpRequest, pk=pk)
    request_object.delete()
    return redirect('help_plz:class', class_pk=request_object.klass.pk)


@require_http_methods("POST")
@permission_required('class.add_help_request', fn=objectgetter(Class,
                                                               'class_pk'))
def request_help(request, class_pk):
    help_request = HelpRequest(topic=request.POST['topic'],
                               creator=request.user, public=(
                                   'public' in request.POST),
                               klass=Class.objects.get(pk=class_pk))
    if 'urgency' in request.POST and request.POST['urgency'] != 'None':
        help_request.urgency = request.POST['urgency'].upper()
    help_request.save()
    return redirect('help_plz:class', class_pk=help_request.klass.pk)


@permission_required('help_request.can_mark_started',
                     fn=objectgetter(HelpRequest, 'pk'))
def start_request(request, pk):
    request_object = get_object_or_404(HelpRequest, pk=pk)
    request_object.started = True
    request_object.helper = request.user
    request_object.save()
    return redirect('help_plz:class', class_pk=request_object.klass.pk)


@permission_required('help_request.can_mark_done', fn=objectgetter(HelpRequest,
                                                                   'pk'))
def finish_request(request, pk):
    request_object = get_object_or_404(HelpRequest, pk=pk)
    request_object.delete()
    return redirect('help_plz:class', class_pk=request_object.klass.pk)


@login_required()
@permission_required('help_request.can_concur', fn=objectgetter(HelpRequest,
                                                                'pk'))
def concur_with_request(request, pk):
    request_object = get_object_or_404(HelpRequest, pk=pk)
    request_object.concurers.add(request.user)
    return redirect('help_plz:class', class_pk=request_object.klass.pk)


@login_required()
def account(request, context=None):
    context = {
            'recent_requests':recent_requests(request.user)
    }
    return render(request, 'help_plz/account.html', context)


@require_http_methods(["GET", "POST"])
@login_required()
def join_class(request):
    if request.method == "GET":
        return render(request, 'help_plz/account.html',
                      {'recent_requests': recent_requests(request.user)})
    fields = ["join_name", "join_role",
              "join_password"]
    if not all(map(lambda field: field in request.POST, fields)):
        context = {
            'error_message': 'Not all fields provided',
            'recent_requests': recent_requests(request.user)
        }
        return render(request, "help_plz/account.html", context)
    else:
        try:
            klass = Class.objects.get(name=request.POST['join_name'])
        except Class.DoesNotExist:
            context = {
                'error_message': 'Class does not exist',
                'recent_requests': recent_requests(request.user)
            }
            return render(request, "help_plz/account.html", context)
        if (request.user in klass.teachers.all()) or (request.user in
                                                      klass.tutors.all()) or (request.user in klass.students.all()):
            context = {
                'error_message': 'You are already a member of this class',
                'recent_requests': recent_requests(request.user)
            }
            return render(request, "help_plz/account.html", context)
        if request.POST['join_role'] == "Student":
            klass.students.add(request.user)
        elif request.POST['join_role'] == "Tutor":
            klass.tutors.add(request.user)
        elif request.POST['join_role'] == "Teacher":
            klass.teachers.add(request.user)
        klass.save()
        return render(request, "help_plz/account.html",
                      {'recent_requests': recent_requests(request.user)})


@require_http_methods(["GET", "POST"])
@login_required()
def create_class(request):
    if request.method == "GET":
        context = {
            'recent_requests': recent_requests(request.user)
        }
        return render(request, 'help_plz/account.html', context)
    else:
        fields = ["create_class_name", "create_student_password",
                  "create_tutor_password", "create_teacher_password"]
        if not all(map(lambda field: field in request.POST, fields)):
            context = {
                'error_message': 'Not all fields provided',
                'recent_requests': recent_requests(request.user)
            }
            return render(request, "help_plz/account.html", context)
        elif len(request.POST['create_class_name'].strip()) == 0:
            context = {
                'error_message': 'Name must not be blank',
                'recent_requests': recent_requests(request.user)
            }
            return render(request, "help_plz/account.html", context)
        else:
            try:
                new_class = Class()
                new_class.name = request.POST['create_class_name']
                new_class.student_password = request.POST['create_student_password']
                new_class.tutor_password = request.POST['create_tutor_password']
                new_class.teacher_password = request.POST['create_teacher_password']
                new_class.save()
                new_class.teachers.add(request.user)
            except IntegrityError:
                context = {
                    'recent_requests': recent_requests(request.user),
                    'error_message': 'Class name is already taken',
                }
                return render(request, "help_plz/account.html", context)
            context = {
                'recent_requests': recent_requests(request.user)
            }
            return render(request, 'help_plz/account.html', context)
