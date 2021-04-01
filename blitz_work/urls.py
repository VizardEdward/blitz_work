from django.urls import path
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_sameorigin

def blitz_doc(request):
    return render(request, "doc/es/index.html")

def blitz_doc_blitz(request):
    return render(request, "doc/es/content/blitz.html")

def blitz_doc_blitz_js(request):
    return render(request, "doc/es/content/blitzjs.html")

def blitz_doc_crud(request):
    return render(request, "doc/es/content/crud.html")

def blitz_doc_url(request):
    return render(request, "doc/es/content/urls.html")

def blitz_doc_table(request):
    return render(request, "doc/es/content/table.html")

def blitz_doc_search(request):
    return render(request, "doc/es/content/search.html")

def blitz_doc_create(request):
    return render(request, "doc/es/content/create.html")

def blitz_doc_detail(request):
    return render(request, "doc/es/content/detail.html")

def blitz_doc_update(request):
    return render(request, "doc/es/content/update.html")

def blitz_doc_delete(request):
    return render(request, "doc/es/content/delete.html")

def blitz_doc_blitz_crud(request):
    return render(request, "doc/es/content/blitzcrud.html")

def blitz_doc_blitz_form(request):
    return render(request, "doc/es/content/form.html")

def blitz_doc_switch(request):
    return render(request, "doc/es/content/switch.html")

def blitz_doc_en(request):
    return render(request, "doc/en/index.html")

def blitz_doc_blitz_en(request):
    return render(request, "doc/en/content/blitz.html")

def blitz_doc_blitz_js_en(request):
    return render(request, "doc/en/content/blitzjs.html")

def blitz_doc_crud_en(request):
    return render(request, "doc/en/content/crud.html")

def blitz_doc_url_en(request):
    return render(request, "doc/en/content/urls.html")

def blitz_doc_table_en(request):
    return render(request, "doc/en/content/table.html")

def blitz_doc_search_en(request):
    return render(request, "doc/en/content/search.html")

def blitz_doc_create_en(request):
    return render(request, "doc/en/content/create.html")

def blitz_doc_detail_en(request):
    return render(request, "doc/en/content/detail.html")

def blitz_doc_update_en(request):
    return render(request, "doc/en/content/update.html")

def blitz_doc_delete_en(request):
    return render(request, "doc/en/content/delete.html")

def blitz_doc_blitz_crud_en(request):
    return render(request, "doc/en/content/blitzcrud.html")

def blitz_doc_blitz_form_en(request):
    return render(request, "doc/en/content/form.html")

def blitz_doc_switch_en(request):
    return render(request, "doc/en/content/switch.html")

urlpatterns = [
    #!ES
    path("blitz-doc-es/",blitz_doc,name="blitz-doc-es"),
    path("blitz-doc-blitz-es/",blitz_doc_blitz,name="blitz-doc-blitz-es"),
    path("blitz-doc-blitz-js-es/",blitz_doc_blitz_js,name="blitz-doc-blitz-js-es"),
    path("blitz-doc-crud-es/",blitz_doc_crud,name="blitz-doc-crud-es"),
    path("blitz-doc-url-es/",blitz_doc_url,name="blitz-doc-url-es"),
    path("blitz-doc-table-es/",blitz_doc_table,name="blitz-doc-table-es"),
    path("blitz-doc-search-es/",blitz_doc_search,name="blitz-doc-search-es"),
    path("blitz-doc-create-es/",blitz_doc_create,name="blitz-doc-create-es"),
    path("blitz-doc-detail-es/",blitz_doc_detail,name="blitz-doc-detail-es"),
    path("blitz-doc-update-es/",blitz_doc_update,name="blitz-doc-update-es"),
    path("blitz-doc-delete-es/",blitz_doc_delete,name="blitz-doc-delete-es"),
    path("blitz-doc-blitz-crud-es/",blitz_doc_blitz_crud,name="blitz-doc-blitz-crud-es"),
    path("blitz-doc-blitz-form-es/",blitz_doc_blitz_form,name="blitz-doc-blitz-form-es"),
    path("blitz-doc-switch-es/",blitz_doc_switch,name="blitz-doc-switch-es"),
    #!EN
    path("blitz-doc-en/",blitz_doc_en,name="blitz-doc-en"),
    path("blitz-doc-blitz-en/",blitz_doc_blitz_en,name="blitz-doc-blitz-en"),
    path("blitz-doc-blitz-js-en/",blitz_doc_blitz_js_en,name="blitz-doc-blitz-js-en"),
    path("blitz-doc-crud-en/",blitz_doc_crud_en,name="blitz-doc-crud-en"),
    path("blitz-doc-url-en/",blitz_doc_url_en,name="blitz-doc-url-en"),
    path("blitz-doc-table-en/",blitz_doc_table_en,name="blitz-doc-table-en"),
    path("blitz-doc-search-en/",blitz_doc_search_en,name="blitz-doc-search-en"),
    path("blitz-doc-create-en/",blitz_doc_create_en,name="blitz-doc-create-en"),
    path("blitz-doc-detail-en/",blitz_doc_detail_en,name="blitz-doc-detail-en"),
    path("blitz-doc-update-en/",blitz_doc_update_en,name="blitz-doc-update-en"),
    path("blitz-doc-delete-en/",blitz_doc_delete_en,name="blitz-doc-delete-en"),
    path("blitz-doc-blitz-crud-en/",blitz_doc_blitz_crud_en,name="blitz-doc-blitz-crud-en"),
    path("blitz-doc-blitz-form-en/",blitz_doc_blitz_form_en,name="blitz-doc-blitz-form-en"),
    path("blitz-doc-switch-en/",blitz_doc_switch_en,name="blitz-doc-switch-en"),
]