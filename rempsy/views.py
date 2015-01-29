#!/usr/bin/env python
# -*- coding: utf-8 -*-
import uuid
import json

from django.shortcuts import render, redirect

from django.http import HttpResponse
from django.shortcuts import render_to_response

from django.contrib import auth
from django.contrib.auth.models import User

from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist

from django.utils import translation
from django.utils.translation import ugettext as _


def index(request):
    if request.user.is_authenticated():
        user_name = request.user.first_name

        if request.user.is_superuser:
            return render_to_response('superuser_index.html', locals())
        elif request.user.is_staff:
            return render_to_response('staff_index.html', locals())
        else:
            return render_to_response('user_index.html', locals())
    else:
        return render_to_response('index.html', locals())

@csrf_exempt
def registration(request):
    if request.method != 'POST':
        return render_to_response('registration.html', locals())

    email = request.POST['email']
    passwd = request.POST['password']
    name = request.POST['name']

    try:
        user = User.objects.get(username=email)
        return HttpResponse(reason=_('User %(email)s is already registered!')%{'email':email}, status=500)
    except ObjectDoesNotExist:
        pass

    host = '127.0.0.1:8000' #FIXME
    a_hash = str(uuid.uuid1())

    send_mail(_('Регистрация'), _('Пройдите по ссылке для продолжения регистрации: http://%(host)s/activate_user/%(a_hash)s')%locals(), 'from@example.com',
                [email], fail_silently=False)

    user = User.objects.create_user(email, email, passwd)
    user.first_name = name
    user.is_active = False
    user.last_name = a_hash
    user.save()

    response_data = {}
    response_data['header'] = _(u'Регистрация')
    response_data['message'] = _(u'На ваш email адрес выслано письмо с инструкциями по активации вашего аккаунта.')
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def activate_user(request, a_hash):
    user = User.objects.get(last_name=a_hash)
    if not user:
        return HttpResponse('Invalid request!', status=401)
    user.last_name = ''
    user.is_active = True
    user.save()

    header = _('Регистрация!')
    message = _('Вы успешно зарегистрировались!\nВойдите на сайт, используя ваш email адрес и пароль')
    redirect_to = '/'

    return render_to_response('information.html', locals())


@csrf_exempt
def login(request):
    if request.method != 'POST':
        raise RuntimeError('POST method required')

    email = request.POST['email']
    passwd = request.POST['password']

    user = auth.authenticate(username=email, password=passwd)

    if user is not None:
        if user.is_active:
            auth.login(request, user)
            return HttpResponse()
        else:
            return HttpResponse(status=403)
    else:
        return HttpResponse(status=401)

@csrf_exempt
def logout(request):
    if request.method != 'POST':
        raise RuntimeError('POST method required')

    auth.logout(request)
    return HttpResponse()

def restore_password(request):
    if request.method != 'POST':
        return render_to_response('restore_password.html', locals())

    email = request.POST['email']

    try:
        user = User.objects.get(username=email)
    except ObjectDoesNotExist:
        return HttpResponse(status=404, reason=_('email addresss does not found!'))

    host = '127.0.0.1:8000' #FIXME
    a_hash = str(uuid.uuid1())
    send_mail(_(u'Восстановление пароля'), _(u'Пройдите по ссылке для изменения пароля: http://%(host)s/set_password/%(a_hash)s')%locals(),
            'from@example.com', [email], fail_silently=False)

    user.last_name = a_hash
    user.save()

    response_data = {}
    response_data['header'] = _(u'Восстановление пароля')
    response_data['message'] = _(u'На ваш email адрес выслано письмо с инструкциями по установке нового пароля для вашего аккаунта.')
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def set_password(request, a_hash):
    if request.method != 'POST':
        return render_to_response('set_password.html', locals())

    passwd = request.POST['password']

    user = User.objects.get(last_name=a_hash)
    if not user:
        return HttpResponse('Invalid request!', status=401)
    user.set_password(passwd)
    user.last_name = ''
    user.save()

    response_data = {}
    response_data['header'] = _(u'Восстановление пароля!')
    response_data['message'] = _(u'Ваш пароль успешно изменен. Теперь вы можете использовать его для входа на сайт.')
    return HttpResponse(json.dumps(response_data), content_type="application/json")

