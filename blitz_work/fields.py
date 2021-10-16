from django.forms import TextInput
from django.forms.models import ModelChoiceField
from django.forms.widgets import Select


def custom_control(attrs):
    if attrs is None:
        attrs = {}
    if attrs.get('class') is None:
        attrs['class'] = 'form-control'
    return attrs


class BText(TextInput):
    def __init__(self, attrs=None):
        super().__init__(custom_control(attrs))


class BModelChoice(Select):
    template_name = 'components/select.html'
    model_name = ""
    related_crud_url = None
    redirect = None
    extra_url = None

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['model_name'] = self.model_name
        context['related_crud_url'] = self.related_crud_url
        context['redirect'] = self.redirect
        context['extra_url'] = self.extra_url
        return context
class BModelMultipleChoice(BModelChoice):
    allow_multiple_selected = True