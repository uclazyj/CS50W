from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from . import util

from markdown import markdown
from random import randint


def index(request):
    query = request.GET.get("q","")
    if query != "":
        all_entries = util.list_entries()
        all_entries_lowercase = [entry.lower() for entry in all_entries]
        # Exact match (case-insensitive)
        if query.lower() in all_entries_lowercase:
            return redirect("title", title=query)
        # Match to a substring of an entry / entries
        matched_entries = [entry for entry in all_entries if query.lower() in entry.lower()]
        return render(request, "encyclopedia/search_results_page.html", {
            "matched_entries": matched_entries
        })
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, title):
    if title == "_random":
        all_entries = util.list_entries()
        if len(all_entries) == 0:
            return render(request, "encyclopedia/index.html", {
            "entries": all_entries
        })
        idx = randint(0, len(all_entries) - 1)
        entry = all_entries[idx]
        return redirect("title", title=entry)
        
    entry = util.get_entry(title)
    if not entry:
        return render(request, "encyclopedia/error.html")
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "body": markdown(entry)
    })