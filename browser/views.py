from django.http import HttpResponse
from django.shortcuts import render
from b2_browser.settings import CF_ROOT

from .b2 import b2ls
import os


def strip_slash(p):
    if p.endswith('/'):
        return p[0:-1]
    return p


def ls(request, directory=""):
    d = b2ls(directory)

    if len(d) < 1:
        return HttpResponse(content="404 Not Found", status=404)

    d.sort(key=lambda i: (i['is_file'], i['name']))

    if directory != "":
        up = os.path.dirname(strip_slash(directory))
    else:
        up = ""

    return HttpResponse(
        content=render(request, "dir.html", context={"files": d, "cf_root": CF_ROOT, "is_root": directory == "", "up": up}),
        status=200)
