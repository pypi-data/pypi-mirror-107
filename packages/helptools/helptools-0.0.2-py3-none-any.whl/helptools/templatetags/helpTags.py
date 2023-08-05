from django.template import Library, TemplateSyntaxError
from django.utils.html import format_html
register = Library()

def validate_id(id:str):
    if id == '': raise TemplateSyntaxError('The id argument can\'t be empty.')
    try:
        int(id[0])
        raise TemplateSyntaxError('The id argument can\'t start with a number')
    except ValueError: pass
    banned = ['null','false','true','typeof','new','let','var','const','for','while','function','class']
    for i in banned:
        if id == i: raise TemplateSyntaxError('The id argument can\'t contain any JavaScript keywords.')

@register.simple_tag()
def help_tools_load(minify=True, cdn=False):
    """
    This tag loads helpTools even if you haven't configured static files!
    Don't forget to include helpTools.urls:
    urlpatterns = [
        path('admin/', admin.site.urls),
        path('hlptls/', include('helptools.urls')),
    ]
    """
    if minify: minify='min.'
    else: minify=''

    if cdn: url = f'https://cdn.jsdelivr.net/gh/ElouLeol/helpTools@main/helpTools.{minify}js'
    else: url = f'/hlptls/files/helpTools.{minify}js'

    return format_html(f'<script src="{url}"></script>')

@register.simple_tag()
def timer(id:str, tag='span', classes='', auto_run=False):
    """
    This tag creates a simple timer.
    "id" is a required argument, it will become a variable in javascript and the id of the html element.
    """
    validate_id(id)
    if auto_run: auto_run = f'{id}.start()'
    else: auto_run = ''
    timer = f'<{tag} id="{id}" class="{classes}">0:00</{tag}>'
    return format_html(f'{timer}<script>let {id} = new helpTools.timer("#{id}");{auto_run}</script>')

@register.simple_tag()
def recorder(id:str, image='/hlptls/files/mic.svg', onstop=''):
    """
    This tag creates a simple voice recorder.

    "id" is a required argument, it will become a variable in javascript and the id of the html element.
    "image" is the path to the image that will become the voice recorder. This is an optional argument.
    "onstop" is a javascript function, but for Python it is just a string.
    """
    validate_id(id)
    image = f'<img alt="microphone" src="{image}">'
    script = f'<script>let {id} = new VoiceRecorder;{id}.recordOnclick("#{id}", {onstop});helpTools.rd("{id}")</script>'
    return format_html(f'<a href="#" id="{id}">{image}{script}</a>')
