from blitz_work.fields import BText
from django import forms
from django.forms.widgets import DateInput, Input, NumberInput, Select, SelectDateWidget, SelectMultiple, Textarea


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
        elif issubclass(form.fields[field_name].widget.__class__, Select) and form.mutate_select and not isinstance(form.fields[field_name].widget, SelectMultiple):
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
