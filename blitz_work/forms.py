from django.forms.models import ModelChoiceField
from django.urls.base import reverse
from blitz_work.fields import BModelChoice, BText
from importlib import import_module
from django import forms
from django.forms.widgets import DateInput, Input, NumberInput, Select, SelectDateWidget, SelectMultiple, Textarea
from django.urls import get_resolver, resolve
from django.urls.exceptions import NoReverseMatch, Resolver404

def _update_class(attrs, css_classes: list):
    if attrs is None:
        attrs = {}
    if attrs.get("class", None) is None:
        attrs.update({"class": " ".join(css_classes)})
    else:
        new_value = attrs['class']
        for css_class in css_classes:
            if attrs['class'].find(css_class) == -1:
                new_value += f" {css_class}"
        attrs.update({"class": new_value})


def _update_input_class(attrs):
    _update_class(attrs, ["form-control"])


def _update_select_class(attrs):
    _update_class(attrs, ["blitzSelect", "form-control"])


def _customize_widgets(form):
    for field_name in form.fields:
        if form.model_related_crud_add and issubclass(form.fields[field_name].__class__, ModelChoiceField):
            related_model = getattr(
                form._meta.model, field_name).field.related_model
            form.fields[field_name].widget = BModelChoice(
                choices=[(item.pk, str(item))for item in related_model.objects.all()])
            form.fields[field_name].widget.model_name = related_model._meta.verbose_name
            def get_class(path):
                module_path,_,class_name=path.rpartition('.')
                module = import_module(module_path)
                return getattr(module,class_name)
            for item in get_resolver().reverse_dict.keys():
                if type(item) == str and item.endswith("create"):
                    try:
                        resolver_match = resolve(reverse(item))
                        if get_class(resolver_match._func_path).model == related_model:
                            form.fields[field_name].widget.related_crud_url = item
                            form.fields[field_name].widget.redirect = resolve(form.request.path_info).url_name
                    except Resolver404:
                        pass
                    except NoReverseMatch:
                        pass
        if form.mutate_date_input and issubclass(form.fields[field_name].widget.__class__, DateInput):
            form.fields[field_name].widget = NumberInput(
                attrs={"type": "date"}) if form.number_input_for_date else SelectDateWidget()
        if form.mutate_inputs and issubclass(form.fields[field_name].widget.__class__, SelectDateWidget):
            _update_select_class(form.fields[field_name].widget.attrs)
        elif form.mutate_inputs and issubclass(form.fields[field_name].widget.__class__, NumberInput):
            _update_input_class(form.fields[field_name].widget.attrs)
        elif form.mutate_text_area and issubclass(form.fields[field_name].widget.__class__, Textarea):
            _update_input_class(form.fields[field_name].widget.attrs)
        elif form.mutate_inputs and issubclass(form.fields[field_name].widget.__class__, Input):
            _update_input_class(form.fields[field_name].widget.attrs)
        elif issubclass(form.fields[field_name].widget.__class__, (Select, BModelChoice)) and form.mutate_select and not isinstance(form.fields[field_name].widget, SelectMultiple):
            _update_select_class(form.fields[field_name].widget.attrs)
        elif form.mutate_select_multiple and isinstance(form.fields[field_name].widget, SelectMultiple):
            _update_select_class(form.fields[field_name].widget.attrs)


class BlitzModelForm(forms.ModelForm):
    mutate_inputs = True
    mutate_text_area = True
    mutate_select = True
    mutate_select_multiple = True
    mutate_date_input = True
    number_input_for_date = True
    model_related_crud_add = True

    def __init__(self, *args, **kwargs):
        super(BlitzModelForm, self).__init__(*args, **kwargs)
        _customize_widgets(self)


class BlitzForm(forms.Form):
    mutate_inputs = True
    mutate_text_area = True
    mutate_select = True
    mutate_select_multiple = True
    mutate_date_input = True
    number_input_for_date = True

    def __init__(self, *args, **kwargs):
        super(BlitzForm, self).__init__(*args, **kwargs)
        _customize_widgets(self)
