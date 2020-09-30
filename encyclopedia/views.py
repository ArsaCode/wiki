from django.shortcuts import render
import markdown2
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Max
import random

from .models import User, Entry

class SearchForm(forms.Form):
    search = forms.CharField(label="Recherche",
                            max_length=255,
                            widget= forms.TextInput
                            (attrs={'class':'search',
				            'placeholder':'Chercher une page'
                            }))

class CreateForm(forms.Form):
    title = forms.CharField(label="Titre de la nouvelle page",
                            max_length=255,
                            widget= forms.TextInput
                            (attrs={'class':'form-control',
				            'placeholder':'Titre'
                            }))
    textarea = forms.CharField(label="Texte de la page (format Markdown)",
                            max_length=4000,
                            widget= forms.Textarea
                            (attrs={'class':'form-control',
                            'placeholder':'Texte'
                            }))

class EditForm(forms.Form):
    title = forms.CharField(label="Titre de la page",
                            max_length=255,
                            widget= forms.TextInput
                            (attrs={'class':'form-control',
				            'placeholder':'Titre'
                            }))
    textarea = forms.CharField(label="Texte de la page (format Markdown)",
                            max_length=4000,
                            widget= forms.Textarea
                            (attrs={'class':'form-control',
                            'placeholder':'Texte'
                            }))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": Entry.objects.all(),
        "searchform": SearchForm()
    })

def page(request, entry_id):
    try:
        entry = Entry.objects.get(pk=entry_id)
        content = markdown2.markdown(entry.content)
        return render(request, "encyclopedia/page.html", {
        "title": entry.title,
        "entry_id": entry.id,
        "page": content,
        "searchform": SearchForm()
        })
    except Entry.DoesNotExist:
        return render(request, "encyclopedia/404.html", {
            "searchform": SearchForm(),
        })

def search(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data["search"]
            searchresult = Entry.objects.filter(title__icontains=search)
            if len(searchresult) != 0:
                return render(request, "encyclopedia/search.html", {
                        "search": search,
                        "searchlist": searchresult,
                        "searchform": form
                    })
            else:
                return render(request, "encyclopedia/404.html", {
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
            try:
                entrycheck = Entry.objects.get(title=title)
                return render(request, "encyclopedia/create.html", {
                    "createform": form,
                    "searchform": SearchForm(),
                    "flash": True,
                    "entry_id": entrycheck.id,
                })
            except Entry.DoesNotExist:
                newentry = Entry(title=title, content=textarea)
                newentry.save()
                return HttpResponseRedirect(f"wiki/{newentry.id}")
        else:
            return render(request, "encyclopedia/search.html", {
                "createform": form,
                "searchform": SearchForm()
            })
    return render(request, "encyclopedia/create.html", {
        "createform": CreateForm(),
        "searchform": SearchForm()
    })

def edit(request, entry_id):
    try:
        entry = Entry.objects.get(pk=entry_id)
    except Entry.DoesNotExist:
            return render(request, "encyclopedia/404.html", {
            "searchform": SearchForm() 
            })
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["textarea"]
            entry.title = title
            entry.content = content
            entry.save()
            return HttpResponseRedirect(f"/wiki/{entry.id}")
        else:
            return render(request, "encyclopedia/edit.html", {
                "searchform" : SearchForm(),
                "editform" : form,
                "title" : entry.title,
                "entry_id" : entry.id,
            })
    else:
        form = EditForm(initial={'title': entry.title, 'textarea': entry.content})
        return render(request, "encyclopedia/edit.html", {
            "searchform" : SearchForm(),
            "editform" : form,
            "title" : entry.title,
            "entry_id" : entry.id,
        })

def rand(request):
    max_id = Entry.objects.all().aggregate(max_id=Max("id"))['max_id']
    pk = random.randint(1, max_id)
    return HttpResponseRedirect(f"/wiki/{pk}")
