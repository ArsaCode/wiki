from django.shortcuts import render
import markdown2
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
import random
from . import util

class SearchForm(forms.Form):
    search = forms.CharField(label="Search",
                            max_length=100,
                            widget= forms.TextInput
                            (attrs={'class':'search',
				            'placeholder':'Search Encyclopedia'
                            }))

class CreateForm(forms.Form):
    title = forms.CharField(label="Title of the new page",
                            max_length=100,
                            widget= forms.TextInput
                            (attrs={'class':'form-control',
				            'placeholder':'Title'
                            }))
    textarea = forms.CharField(label="Markdown text of the new page",
                            max_length=1000,
                            widget= forms.Textarea
                            (attrs={'class':'form-control',
                            'placeholder':'Text'
                            }))

class EditForm(forms.Form):
    title = forms.CharField(label="Title of the new page",
                            max_length=100,
                            widget= forms.TextInput
                            (attrs={'class':'form-control',
				            'placeholder':'Title'
                            }))
    textarea = forms.CharField(label="Markdown text of the new page",
                            max_length=1000,
                            widget= forms.Textarea
                            (attrs={'class':'form-control',
                            'placeholder':'Text'
                            }))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "searchform": SearchForm()
    })

def title(request, title):
    if util.get_entry(title):
        content = markdown2.markdown(util.get_entry(title))
        return render(request, "encyclopedia/page.html", {
        "title": title,
        "page": content,
        "searchform": SearchForm()
        })
    else:
        return render(request, "encyclopedia/404.html")

def search(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        searchlist = []
        if form.is_valid():
            search = form.cleaned_data["search"]
            if util.get_entry(search):
                return HttpResponseRedirect(f"wiki/{ search }")
            for entry in util.list_entries():
                if search.lower() in entry.lower(): 
                    searchlist.append(entry)
            if searchlist:
                return render(request, "encyclopedia/search.html", {
                        "search": search,
                        "searchlist": searchlist,
                        "searchform": form
                    })
            else:
                return render(request, "encyclopedia/404.html", {
                        "form": form,
                        "searchform": form
                    })
        else:
            return render(request, "encyclopedia/index.html", {
            "searchform": form
            })
    return render(request, "encyclopedia/index.html", {
        "searchform": SearchForm()
    })

def create(request):
    if request.method == "POST":
        form = CreateForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            textarea = form.cleaned_data["textarea"]
            if util.get_entry(title):
                return HttpResponseRedirect(f"wiki/{ title }")
            else:
                util.save_entry(title, textarea)
                return HttpResponseRedirect(f"wiki/{ title }")
        else:
            return render(request, "encyclopedia/search.html", {
                "createform": form,
                "searchform": SearchForm()
            })
    return render(request, "encyclopedia/create.html", {
        "createform": CreateForm(),
        "searchform": SearchForm()
    })

def edit(request, edit):
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            textarea = form.cleaned_data["textarea"]
            util.save_entry(title, textarea)
            return HttpResponseRedirect(f"/wiki/{ title }")
        else:
            return render(request, "encyclopedia/edit.html", {
                "title": edit,
                "editform": form,
                "searchform": SearchForm()
            })
    else:
        if util.get_entry(edit):
            form = EditForm(initial={'title': edit, 'textarea': util.get_entry(edit)})
            return render(request, "encyclopedia/edit.html", {
                "title": edit,
                "editform": form,
                "searchform": SearchForm()
            })
        else:
            return render(request, "encyclopedia/404.html", {
            "searchform": SearchForm() 
            })

def rand(request):
    pick = random.choice(util.list_entries())
    return HttpResponseRedirect(f"/wiki/{ pick }")