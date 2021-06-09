import ast

from django.conf import settings
from django.contrib import messages
from django.db.models import Model, Q
from django.forms.models import modelformset_factory
from django.http.response import HttpResponseForbidden, HttpResponseNotAllowed
from django.shortcuts import redirect, render
from django.urls import path, resolve
from django.views import View
from .internationalization import *
from blitz_work.forms import BlitzModelForm


def default_concatenation(self, list):
    """
    Default concatenation function
    """
    return ", ".join(list)


class BlitzCRUD(View):
    template_name = "blitz_base_crud.html"
    extend_template = "blitz_base_offline.html"
    table_template = "blitz_crud_table.html"
    create_template = "blitz_crud_create.html"
    update_template = "blitz_crud_update.html"
    delete_template = "blitz_crud_delete.html"
    detail_template = "blitz_crud_detail.html"
    model = None
    paginate_by = 20
    title = None
    form = None
    formset = None
    show_caption = False
    show_title = True
    caption_is_title = True
    concat_function = default_concatenation
    exclude = ['id', ]
    dark_mode_switch_label = None
    crud_base_name = ""
    create_title = CREATE_TITLE[0]
    delete_messages = DELETE_MESSAGES[0]
    delete_title = DELETE_TITLE[0]
    update_title = UPDATE_TITLE[0]
    detail_title = DETAIL_TITLE[0]
    delete_text = DELETE_TEXT[0]
    crud_buttons = CRUD_BUTTONS[0]
    allow_anonimous_in_debug = True
    __header_field_map = None
    __deletion_query = None
    __optim_query = None
    __fields = None
    __headers = None
    __foreignkey_fields = None
    __many_to_many_fields = None
    __caption = ""
    __model = None
    __app_name = None
    __model_name = None

    def __init__(self, **kwargs):
        if getattr(self,"data", None):
            self.model = getattr(self,"data")
            print("\033[93mPlease use model intead of data to specify the model. Blitz Work no longer support Queryset\033[0m")
        if issubclass(self.model, Model):
            self.__fields, self.__headers, self.__foreignkey_fields, self.__many_to_many_fields = self.extract_model_fields(
                self.model._meta.get_fields())
            self.__caption = self.model._meta.verbose_name_plural.capitalize()
            self.__app_name = self.model._meta.app_label
            self.__deletion_query = self.model.objects
            self.__model_name = self.model._meta.model_name
            self.__optim_query = self.optimice_query(
                self.__foreignkey_fields, self.__many_to_many_fields)
            self.__model = self.model
        else:
            raise TypeError(f"{self.model} is not {Model}")  # or {QuerySet}")
        if self.form is None:
            self.form = self.get_utility_form(self.__model)
        if self.formset is None:
            self.formset = modelformset_factory(
                self.__model, form=self.form, extra=0)
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
        if request.user.has_perm(f'{self.__app_name}.add_{self.__model_name}') or (settings.DEBUG and self.allow_anonimous_in_debug):
            view = resolve(request.path_info).url_name
            if view.endswith("create"):
                form = self.form(request.POST)
                if form.is_valid():
                    form.save()
                    return redirect(self.crud_base_name+"/view")
                else:
                    return render(request, self.create_template, context={
                        "form": form, "crud_url": self.get_crud_url(), "crud_button": self.crud_buttons, "extend_template": self.extend_template, "dark_mode_switch_label":self.dark_mode_switch_label, "context": {"title": self.create_title}})
            else:
                return HttpResponseNotAllowed(["POST"])
        else:
            return HttpResponseForbidden()

    def put(self, request, *args, **kwargs):
        if request.user.has_perm(f'{self.__app_name}.change_{self.__model_name}') or (settings.DEBUG and self.allow_anonimous_in_debug):
            view = resolve(request.path_info).url_name
            if view.endswith("update"):
                formset = self.formset(request.PUT)
                if formset.is_valid():
                    formset.save()
                    return redirect(self.crud_base_name+"/view")
                else:
                    return render(request, self.update_template, context={"formset": formset, "crud_url": self.get_crud_url(), "crud_button": self.crud_buttons, "extend_template": self.extend_template, "dark_mode_switch_label":self.dark_mode_switch_label, "context": {"title": self.update_title}})
            else:
                return HttpResponseNotAllowed(["POST"])
        else:
            return HttpResponseForbidden()

    def delete(self, request, *args, **kwargs):
        if request.user.has_perm(f'{self.__app_name}.delete_{self.__model_name}') or (settings.DEBUG and self.allow_anonimous_in_debug):
            try:
                items = ast.literal_eval(request.DELETE.get("items"))
                self.__deletion_query.filter(pk__in=items).delete()
                messages.success(request, self.delete_messages.get(
                    "success", "Element deleted"))
            except:
                messages.error(request, self.delete_messages.get(
                    "error", "Error on delete"))
            return redirect(self.crud_base_name+"/view")
        else:
            return HttpResponseForbidden()

    def create_view(self, request, *args, **kwargs):
        if request.user.has_perm(f'{self.__app_name}.add_{self.__model_name}') or (settings.DEBUG and self.allow_anonimous_in_debug):
            return render(request, self.create_template, context={"form": self.form(), "crud_url": self.get_crud_url(), "crud_button": self.crud_buttons, "extend_template": self.extend_template, "dark_mode_switch_label":self.dark_mode_switch_label, "context": {"title": self.create_title}})
        else:
            return HttpResponseForbidden()

    def list_view(self, request, *args, **kwargs):
        if request.user.has_perm(f'{self.__app_name}.view_{self.__model_name}') or (settings.DEBUG and self.allow_anonimous_in_debug):
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
                    order, self.__fields, self.__many_to_many_fields)
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

            return render(request, self.template_name, context={"crud_url": self.get_crud_url(), "crud_button": self.crud_buttons, "extend_template": self.extend_template, "table_template": self.table_template, "dark_mode_switch_label":self.dark_mode_switch_label, "context": {"search_text": search, "search": "" if search is None else "&search=" + search, "title_as_caption": self.caption_is_title, "show_caption": self.show_caption, "show_title": self.show_title, "title": self.title, "current_order": order, "caption": self.__caption, "headers": headers, "values": values, "page": current_page}})
        else:
            return HttpResponseForbidden()

    def update_view(self, request, *args, **kwargs):
        if request.user.has_perm(f'{self.__app_name}.change_{self.__model_name}') or (settings.DEBUG and self.allow_anonimous_in_debug):
            items = request.GET.getlist("item")
            query = self.__optim_query
            return render(request, self.update_template, context={"formset": self.formset(queryset=query.filter(pk__in=items)), "crud_url": self.get_crud_url(), "extend_template": self.extend_template, "crud_button": self.crud_buttons, "dark_mode_switch_label":self.dark_mode_switch_label, "context": {"title": self.update_title}})
        else:
            return HttpResponseForbidden()

    def detail_view(self, request, *args, **kwargs):
        if request.user.has_perm(f'{self.__app_name}.view_{self.__model_name}') or (settings.DEBUG and self.allow_anonimous_in_debug):
            items = request.GET.getlist("item")
            query = self.__optim_query
            return render(request, self.detail_template, context={"formset": self.formset(queryset=query.filter(pk__in=items)), "crud_url": self.get_crud_url(), "crud_button": self.crud_buttons, "extend_template": self.extend_template, "dark_mode_switch_label":self.dark_mode_switch_label, "context": {"title": self.detail_title}})
        else:
            return HttpResponseForbidden()

    def delete_view(self, request, *args, **kwargs):
        if request.user.has_perm(f'{self.__app_name}.delete_{self.__model_name}') or (settings.DEBUG and self.allow_anonimous_in_debug):
            items = request.GET.getlist("item")
            query = self.__optim_query
            return render(request, self.delete_template, context={"crud_url": self.get_crud_url(), "crud_button": self.crud_buttons, "extend_template": self.extend_template, "dark_mode_switch_label":self.dark_mode_switch_label, "context": {"title": self.delete_title, "message": self.delete_text, "pk": items, "items": query.filter(pk__in=items)}})
        else:
            return HttpResponseForbidden()

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
        query = self.model.objects.select_related(*foreignkey_fields) if len(foreignkey_fields) else self.model.objects
        query = query.prefetch_related(*many_to_many_fields) if len(many_to_many_fields) else query
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
                exclude = ('id', 'pk',)
        return UtilityForm

    def get_crud_url(self):
        return {"view": self.crud_base_name+"/view",
                "create": self.crud_base_name+"/create",
                "detail": self.crud_base_name+"/detail",
                "update": self.crud_base_name+"/update",
                "delete": self.crud_base_name+"/delete",
                }


def get_urls(crud_class: BlitzCRUD, crud_name=None, prefix:str=''):
    """
        Return a list of paths for the class

    Args:
        crud_class BlitzCRUD: CRUD Class
        crud_name str, None: name of the CRUD

    Returns:
        list: list of paths for the CRUD
    """
    
    if crud_class.model is None:
        if getattr(crud_class,"data", None):
            crud_name = getattr(crud_class,"data")._meta.verbose_name
            print('\033[93mPlease use model intead of data to specify the model. Blitz Work no longer support Queryset\033[0m')
        else:
            raise Exception("No model provided")
    else:
        crud_name = crud_name or crud_class.model._meta.verbose_name
    crud_view = crud_class.as_view(crud_base_name=crud_name)
    return [path(prefix + "view/", crud_view,
                 name=crud_name+"/view"),
            path(prefix + "detail/", crud_view,
                 name=crud_name+"/detail"),
            path(prefix + "create/", crud_view,
                 name=crud_name+"/create"),
            path(prefix + "update/", crud_view,
                 name=crud_name+"/update"),
            path(prefix + "delete/", crud_view,
                 name=crud_name+"/delete"),
            ]
