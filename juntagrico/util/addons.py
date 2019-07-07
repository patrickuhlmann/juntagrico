from django.utils.functional import LazyObject
from django.utils.module_loading import autodiscover_modules


class AddonNotConfigured(Exception):
    pass


class AddonsConfig:

    def __init__(self):
        self._admin_menus = []
        self._user_menus = []
        self._registry = {}

    def register_admin_menu(self, template):
        self._admin_menus.append(template)

    def get_admin_menus(self):
        return self._admin_menus

    def register_user_menu(self, template):
        self._user_menus.append(template)

    def get_user_menus(self):
        return self._user_menus

    def register_model_inline(self, model, inline):
        inline_list = self._registry.get(model, [])
        inline_list.append(inline)
        self._registry[model] = inline_list

    def get_model_inlines(self, model):
        return self._registry.get(model, [])


class DefaultAddonsConfig(LazyObject):
    def _setup(self):
        self._wrapped = AddonsConfig()


config = DefaultAddonsConfig()


def load_addons():
    autodiscover_modules('juntagricoapp', register_to=config)
