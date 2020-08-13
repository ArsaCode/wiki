from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })

def page(request, title):
    return render(request, "encyclopedia/page.html", {
        "title": title,
        "page": util.get_entry(title)
    })