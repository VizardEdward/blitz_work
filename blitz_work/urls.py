from django.urls import path
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_sameorigin

def blitz_doc(request):
    return render(request, "doc/index.html")

def blitz_doc_blitz(request):
    return render(request, "doc/content/blitz.html")

def blitz_doc_blitz_js(request):
    return render(request, "doc/content/blitzjs.html")

def blitz_doc_crud(request):
    return render(request, "doc/content/crud.html")

def blitz_doc_url(request):
    return render(request, "doc/content/urls.html")

def blitz_doc_table(request):
    return render(request, "doc/content/table.html")

def blitz_doc_search(request):
    return render(request, "doc/content/search.html")

def blitz_doc_create(request):
    return render(request, "doc/content/create.html")

def blitz_doc_detail(request):
    return render(request, "doc/content/detail.html")

def blitz_doc_update(request):
    return render(request, "doc/content/update.html")

def blitz_doc_delete(request):
    return render(request, "doc/content/delete.html")

def blitz_doc_blitz_crud(request):
    return render(request, "doc/content/blitzcrud.html")

def blitz_doc_blitz_form(request):
    return render(request, "doc/content/form.html")

urlpatterns = [
    path("blitz-doc/",blitz_doc,name="blitz-doc"),
    path("blitz-doc-blitz/",blitz_doc_blitz,name="blitz-doc-blitz"),
    path("blitz-doc-blitz-js/",blitz_doc_blitz_js,name="blitz-doc-blitz-js"),
    path("blitz-doc-crud/",blitz_doc_crud,name="blitz-doc-crud"),
    path("blitz-doc-url/",blitz_doc_url,name="blitz-doc-url"),
    path("blitz-doc-table/",blitz_doc_table,name="blitz-doc-table"),
    path("blitz-doc-search/",blitz_doc_search,name="blitz-doc-search"),
    path("blitz-doc-create/",blitz_doc_create,name="blitz-doc-create"),
    path("blitz-doc-detail/",blitz_doc_detail,name="blitz-doc-detail"),
    path("blitz-doc-update/",blitz_doc_update,name="blitz-doc-update"),
    path("blitz-doc-delete/",blitz_doc_delete,name="blitz-doc-delete"),
    path("blitz-doc-blitz-crud/",blitz_doc_blitz_crud,name="blitz-doc-blitz-crud"),
    path("blitz-doc-blitz-form/",blitz_doc_blitz_form,name="blitz-doc-blitz-form"),
]