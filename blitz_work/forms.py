from blitz_work.fields import BText
from django import forms
from django.forms.widgets import Input, Select, SelectMultiple, TextInput, Textarea


def _update_class(attrs, css_classes:list):
    if attrs is None:
        attrs = {}
    if attrs.get("class", None) is None:
        attrs.update({"class": " ".join(css_classes)})
    else:
        new_value = attrs['class']
        for css_class in css_classes:
            if attrs['class'].find(css_class) == -1:
                new_value+= f" {css_class}"
        attrs.update({"class": new_value})

def _update_input_class(attrs):
    _update_class(attrs, ["form-control"])

def _update_select_class(attrs):
    _update_class(attrs, ["blitzSelect", "form-control"])

def _customize_widgets(form):
    for field_name in form.fields:
        if form.mutate_text_area and issubclass(form.fields[field_name].widget.__class__, Textarea):
            _update_input_class(form.fields[field_name].widget.attrs)
        if form.mutate_inputs and issubclass(form.fields[field_name].widget.__class__, Input):
            _update_input_class(form.fields[field_name].widget.attrs)
        if issubclass(form.fields[field_name].widget.__class__, Select) and form.mutate_select and not isinstance(form.fields[field_name].widget, SelectMultiple):
            _update_select_class(form.fields[field_name].widget.attrs)
        if form.mutate_select_multiple and isinstance(form.fields[field_name].widget, SelectMultiple):
            _update_select_class(form.fields[field_name].widget.attrs)

class BlitzModelForm(forms.ModelForm):
    mutate_inputs = True
    mutate_text_area = True
    mutate_select = True
    mutate_select_multiple = True

    def __init__(self, *args, **kwargs):
        super(BlitzModelForm, self).__init__(*args, **kwargs)
        _customize_widgets(self)
            
class BlitzForm(forms.Form):
    mutate_inputs = True
    mutate_text_area = True
    mutate_select = True
    mutate_select_multiple = True

    def __init__(self, *args, **kwargs):
        super(BlitzForm, self).__init__(*args, **kwargs)
        _customize_widgets(self)
