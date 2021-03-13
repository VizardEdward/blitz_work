from django.forms import TextInput


def custom_control(attrs):
    if attrs is None:
        attrs = {}
    if attrs.get('class') is None:
        attrs['class'] = 'form-control'
    return attrs


class BText(TextInput):
    def __init__(self, attrs=None):
        super().__init__(custom_control(attrs))
