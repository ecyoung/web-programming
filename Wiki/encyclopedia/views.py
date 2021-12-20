from django.shortcuts import render, redirect
from markdown2 import markdown
from random import randint
from . import util

def entry(request, title):
    content = util.get_entry(title.strip())
    if content == None:
        content = "The requested page was not found..."
    content = markdown(content)
    return render(request, "encyclopedia/entry.html", {"content": content, "title": title})

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def search(request):
    q = request.GET.get("q").strip()
    if q in util.list_entries():
        return redirect("entry", title=q)
    return render(request, "encyclopedia/search.html", {"entries": util.search(q), "q": q})

def new(request):
    if request.method == "POST":
        title = request.POST.get("title").strip()
        content = request.POST.get("content").strip()
        if title == "" or content == "":
            return render(request, "encyclopedia/new.html", {"message": "Unable to create new page with empty title/content field(s)...", "title": title, "content": content})
        if title in util.list_entries():
            return render(request, "encyclopedia/new.html", {"message": "The title already exists...", "title": title, "content": content})
        util.save_entry(title, content)
        return redirect("entry", title=title)
    return render(request, "encyclopedia/new.html")

def edit(request, title):
    content = util.get_entry(title.strip())
    if content == None:
        return render(request, "encyclopedia/edit.html", {"error": "404 Not Found"})
    if request.method == "POST":
        content = request.POST.get("content").strip()
        if content == "":
            return render(request, "encyclopedia/edit.html", {"message": "Unable to save empty page...", "title": title, "content": content})
        util.save_entry(title, content)
        return redirect("entry", title=title)
    return render(request, "encyclopedia/edit.html", {"content": content, "title": title})

def random(request):
    all_entries = util.list_entries()
    random_title = all_entries[randint(0, len(all_entries)-1)]
    return redirect("entry", title=random_title)