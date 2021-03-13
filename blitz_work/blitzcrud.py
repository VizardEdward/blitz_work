import ast
import inspect

from blitz_work.forms import BlitzModelForm
from django.contrib import messages
from django.db.models import Model, Q
from django.db.models.query import QuerySet
from django.forms.models import modelformset_factory
from django.http.response import HttpResponseNotAllowed
from django.shortcuts import redirect, render
from django.urls import path, resolve
from django.views import View



def default_concatenation(self, list):
    """
    Default concatenation function
    """
    return ", ".join(list)

class BlitzCRUD(View):
    template_name = "blitz_base_crud.html"  # template for render
    extend_template = "blitz_base_offline.html"
    table_template = "blitz_crud_table.html"
    create_template = "blitz_crud_create.html"
    update_template = "blitz_crud_update.html"
    delete_template = "blitz_crud_delete.html"
    detail_template = "blitz_crud_detail.html"
    data = None  # Model or QuerySet
    paginate_by = 20
    title = None
    form = None
    formset = None
    show_caption = True
    create_title = "Create"
    show_title = True
    caption_is_title = False
    concat_function = default_concatenation
    exclude = ['id', ]
    crud_base_name = ""
    delete_messages = {"success":"Element deleted","error":"Error on delete"}
    delete_title = "Delete"
    update_title = "Edit"
    detail_title = "Detail"
    delete_text = "The following elements will be deleted, do you want to delete them?"
    crud_buttons = {"add":"Add", "create":"Create", "details":"Details", "update":"Update", "edit":"Edit", "delete":"Delete", "cancel":"Cancel", "return":"Return"}
    __header_field_map = None
    __deletion_query = None
    __optim_query = None
    __fields = None
    __headers = None
    __foreignkey_fields = None
    __many_to_many_fields = None
    __caption = ""
    __model = None

    def __init__(self, **kwargs):
        if isinstance(self.data, QuerySet):
            self.__fields, self.__headers, self.__foreignkey_fields, self.__many_to_many_fields = self.extract_model_fields(
                self.data.model._meta.get_fields())
            self.__deletion_query = self.data
            self.__optim_query = self.data
            self.__caption = self.data.model._meta.verbose_name_plural
            self.__model = self.data.model
        elif inspect.isclass(self.data):
            if issubclass(self.data, Model):
                self.caption = self.data._meta.verbose_name_plural
                self.__fields, self.__headers, self.__foreignkey_fields, self.__many_to_many_fields = self.extract_model_fields(
                    self.data._meta.get_fields())
                self.__caption = self.data._meta.verbose_name_plural
                self.__deletion_query = self.data.objects
                self.__optim_query = self.optimice_query(
                    self.__foreignkey_fields, self.__many_to_many_fields)
                self.__model = self.data
            else:
                raise TypeError(f"{self.data} is not {Model} or {QuerySet}")
        else:
            raise TypeError(f"{self.data} is not {Model} or {QuerySet}")
        if self.form is None:
            self.form = self.get_utility_form(self.__model)
        if self.formset is None:
            self.formset = modelformset_factory(self.__model,form=self.form, extra=0)
        self.__header_field_map = zip(self.__fields, self.__headers)
        super().__init__(**kwargs)

    @staticmethod
    def get_urls(crud_class, crud_name=None):
        return get_urls(crud_class, crud_name)

    def dispatch(self, request, *args, **kwargs):
        method = request.POST.get('_method', '').lower()
        if method == "delete":
            request.method = "DELETE"
            request.DELETE = request.POST
        if method == "put":
            request.method = "PUT"
            request.PUT = request.POST
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        view = resolve(request.path_info).url_name
        if view.endswith("view"):
            return self.list_view(request, *args, **kwargs)
        if view.endswith("detail"):
            return self.detail_view(request, *args, **kwargs)
        elif view.endswith("create"):
            return self.create_view(request, *args, **kwargs)
        elif view.endswith("update"):
            return self.update_view(request, *args, **kwargs)
        elif view.endswith("delete"):
            return self.delete_view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = resolve(request.path_info).url_name
        if view.endswith("create"):
            form = self.form(request.POST)
            if form.is_valid():
                form.save()
                return redirect(self.crud_base_name+"/view")
            else:
                return render(request, self.create_template, context={
                       "form": form, "crud_url": self.get_crud_url(), "context": {"title": self.create_title}})
        else:
            return HttpResponseNotAllowed(["POST"])

    def put(self, request, *args, **kwargs):
        view = resolve(request.path_info).url_name
        if view.endswith("update"):
            formset = self.formset(request.PUT)
            if formset.is_valid():
                formset.save()
                return redirect(self.crud_base_name+"/view")
            else:
                return render(request, self.update_template, context={"formset": formset , "crud_url": self.get_crud_url(), "context": {"title": self.update_title}})
        else:
            return HttpResponseNotAllowed(["POST"])

    def delete(self, request, *args, **kwargs):
        try:
            items = ast.literal_eval(request.DELETE.get("items"))
            self.__deletion_query.filter(pk__in=items).delete()
            messages.success(request, self.delete_messages.get("success","Element deleted"))
        except:
            messages.error(request, self.delete_messages.get("error","Error on delete"))
        return redirect(self.crud_base_name+"/view")

    def create_view(self, request, *args, **kwargs):
        return render(request, self.create_template, context={"form": self.form(), "crud_url": self.get_crud_url(), "crud_button":self.crud_buttons, "extend_template": self.extend_template, "context": {"title": self.create_title}})

    def list_view(self, request, *args, **kwargs):
        table = request.GET.get('table', '')
        page = request.GET.get('page', 1)
        order = request.GET.get('order', 'pk')
        search = request.GET.get('search', None)
        direction = ''
        field = ''
        query = self.__optim_query

        if search:
            search_query = Q()
            for field in self.__fields:
                if(field not in self.__many_to_many_fields and field not in self.__foreignkey_fields):
                    search_query |= Q(**{field + "__icontains": search})
            query = query.filter(search_query)

        if table == self.__caption:
            direction, field, order = self.get_order(
                order,self.__fields, self.__many_to_many_fields)
            query = query.order_by(order)
            order = order[1:] if order[:1] == '-' else order
        else:
            query = query.order_by("pk")
            page = 1

        headers = [{"text": header, "column": name, "direction": direction if name ==
                    field else '-'} for name, header in self.__header_field_map]
        from django.core.paginator import Paginator
        current_page = Paginator(query, self.paginate_by).get_page(page)

        values = [{"values": [getattr(value, key) if key not in self.__many_to_many_fields else self.concat_function(
            [element.__str__() for element in getattr(value, key).all()]) for key in self.__fields], "pk":getattr(value, "pk")} for value in current_page.object_list]
        # print(self.data.query.annotations.keys())

        return render(request, self.template_name, context={"crud_url": self.get_crud_url(), "crud_button":self.crud_buttons, "extend_template": self.extend_template, "table_template": self.table_template, "context": {"search_text": search, "search": "" if search is None else "&search=" + search, "title_as_caption": self.caption_is_title, "show_caption": self.show_caption, "show_title": self.show_title, "title": self.title, "current_order": order, "caption": self.__caption, "headers": headers, "values": values, "page": current_page}})

    def update_view(self, request, *args, **kwargs):
        items = request.GET.getlist("item")
        query = self.__optim_query
        return render(request, self.update_template, context={"formset": self.formset(queryset=query.filter(pk__in=items)), "crud_url": self.get_crud_url(), "extend_template": self.extend_template, "crud_button":self.crud_buttons, "context": {"title": self.update_title}})

    def detail_view(self, request, *args, **kwargs):
        items = request.GET.getlist("item")
        query = self.__optim_query
        return render(request, self.detail_template, context={"formset": self.formset(queryset=query.filter(pk__in=items)), "crud_url": self.get_crud_url(), "crud_button":self.crud_buttons, "extend_template": self.extend_template, "context": {"title": self.detail_title}})

    def delete_view(self, request, *args, **kwargs):
        items = request.GET.getlist("item")
        query = self.__optim_query
        return render(request, self.delete_template, context={"crud_url": self.get_crud_url(), "crud_button":self.crud_buttons, "extend_template": self.extend_template, "context": {"title": self.delete_title,"message":self.delete_text, "pk":items, "items": query.filter(pk__in=items)}})

    def get_order(self, order, fields_name, many_to_many_fields):
        """
        Returns the next_direction of the ordering,\\
        the current field ordering and the current order for the query
        """
        next_direction = '' if order[:1] == '-' else '-'
        real_order = ''
        field = ''
        if order[1:] == 'pk' or order == 'pk':
            real_order = order
            field = 'pk'
        else:
            if order[1:] in fields_name or order in fields_name:
                if order[1:] in many_to_many_fields or order in many_to_many_fields:
                    real_order = 'pk'
                    field = 'pk'
                else:
                    real_order = order
                    field = order if next_direction == '-' else order[1:]
            else:
                real_order = 'pk'
                field = 'pk'
        return next_direction, field, real_order

    def optimice_query(self, foreignkey_fields, many_to_many_fields):
        """
        Return an optimal query
        """
        query = self.data.objects.select_related(
            ",".join(foreignkey_fields)) if len(foreignkey_fields) else self.data.objects
        query = query.prefetch_related(
            ",".join(many_to_many_fields)) if len(many_to_many_fields) else query
        return query

    def extract_model_fields(self, model):
        """
        Returns the fields name, verbose_name, \\
        and foreignkey_fields many_to_many_fields form the given model\\
        :note: foreignkey_fields may content OneToOneField and ForeignKey
        """
        from django.db.models import ForeignKey, ManyToManyField, OneToOneField
        from django.db.models.fields import Field

        id = []
        headers = []
        many_to_many_fields = []
        foreignkey_fields = []
        for field in model:
            if isinstance(field, Field):
                if field.name not in self.exclude:
                    id.append(field.name)
                    headers.append(field.verbose_name)
                    if isinstance(field, ForeignKey) or isinstance(field, OneToOneField):
                        foreignkey_fields.append(field.name)
                    elif isinstance(field, ManyToManyField):
                        many_to_many_fields.append(field.name)

        return id, headers, foreignkey_fields, many_to_many_fields

    def get_utility_form(self, real_model):
        class UtilityForm(BlitzModelForm):
                class Meta:
                    model = real_model
                    fields = '__all__'
                    exclude = ('id','pk',)
        return UtilityForm

    def get_crud_url(self):
        return {"view": self.crud_base_name+"/view",
                "create": self.crud_base_name+"/create",
                "detail": self.crud_base_name+"/detail",
                "update": self.crud_base_name+"/update",
                "delete": self.crud_base_name+"/delete",
                }


def get_urls(crud_class: BlitzCRUD, crud_name):
    """
        Return a list of paths for the class

    Args:
        crud_class BlitzCRUD: CRUD Class
        crud_name str, None: name of the CRUD

    Returns:
        list: list of paths for the CRUD
    """
    crud_view = crud_class.as_view(crud_base_name=crud_name)
    return [path("view/", crud_view,
                 name=crud_name+"/view"),
            path("detail/", crud_view,
                name=crud_name+"/detail"),
            path("create/", crud_view,
                 name=crud_name+"/create"),
            path("update/", crud_view,
                 name=crud_name+"/update"),                 
            path("delete/", crud_view,
                 name=crud_name+"/delete"),
            ]
