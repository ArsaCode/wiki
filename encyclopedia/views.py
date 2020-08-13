from django.shortcuts import render
from markdown2 import Markdown
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })

def page(request, title):
    title = util.get_entry(title)
    return render(request, "encyclopedia/page.html", {
        "title": title,
        "page": title
    })