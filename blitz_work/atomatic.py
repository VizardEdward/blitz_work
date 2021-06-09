from django.apps import apps
from .blitzcrud import get_urls
from .blitzcrud import BlitzCRUD
from .internationalization import *


def automatic_crud(app_names: list, language: int = 0, extend_template_name: str = "blitz_base_offline.html",
                   exclude_columns: str = {}):
    models = [model for app in app_names for model in apps.get_app_config(
        app).get_models()]
    cruds = []
    for model_name in models:
        class AutomaticCRUDHelper(BlitzCRUD):
            model = model_name
            exclude = exclude_columns.get(model._meta.verbose_name,['id', ])
            extend_template = extend_template_name
            create_title = CREATE_TITLE[language]
            delete_messages = DELETE_MESSAGES[language]
            delete_title = DELETE_TITLE[language]
            update_title = UPDATE_TITLE[language]
            detail_title = DETAIL_TITLE[language]
            delete_text = DELETE_TEXT[language]
            crud_buttons = CRUD_BUTTONS[language]
        cruds.append(AutomaticCRUDHelper)
    return [path for crud in cruds for path in get_urls(crud, prefix=crud.model._meta.verbose_name.replace(' ', '_') + '/')]
