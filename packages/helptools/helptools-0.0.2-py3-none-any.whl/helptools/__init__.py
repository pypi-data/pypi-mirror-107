from django.conf import settings

try: show_docs = settings.SHOW_HELP_TOOLS_DOCS
except AttributeError: show_docs = True

lang = 'eng'
if settings.LANGUAGE_CODE == 'ru-ru': lang = 'ru'
