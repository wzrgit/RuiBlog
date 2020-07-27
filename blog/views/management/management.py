from django.http import HttpRequest
from django.shortcuts import render
from blog.models import Options
from blog.views import common


def dashboard(request):
    # TODO check auth
    content = {'common': common.GetCommons()}
    return render(request, 'management/dashboard.html', content)


