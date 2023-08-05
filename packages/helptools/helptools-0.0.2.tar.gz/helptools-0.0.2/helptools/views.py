import sys, os, re
from django.http import HttpResponse
import helptools

formats = {
    'svg': 'image/svg+xml',
    'js': 'text/javascript',
    'html': 'text/html',
}

def read_and_close(path):
    with open(path, encoding="utf-8") as r: text = r.read()
    return text

def get_file(name, mime):
    try: response = read_and_close(f'{sys.path[-1]}/helptools/files/{name}')
    except FileNotFoundError:
        for i in sys.path:
            if i[len(i)-13:len(i)] == 'site-packages':
                response = read_and_close(f'{i}/helptools/files/{name}')
    get_file.only_text = response
    response = HttpResponse(response)
    response._headers['content-type'] = ('Content-Type', f'{mime}; charset=utf-8')
    return response

def file(request, file_name):
    if file_name.replace('docs', '') != file_name: return None
    file_format = re.search('.+\.',file_name).group()
    file_format = file_name.replace(file_format, '')
    return get_file(file_name, formats[file_format])

def docs(request):
    if helptools.show_docs:
        get_file('docs/index.html', 'text/html')
        file = get_file.only_text
        try:
            if request.GET['lang'] == 'ru':
                get_file('docs/ru.html', 'text/html')
            elif request.GET['lang'] == 'eng':
                get_file('docs/eng.html', 'text/html')
            else: raise KeyError
        except KeyError:
            get_file(f'docs/{helptools.lang}.html', 'text/html')
        file = file.replace('{{body}}', get_file.only_text)

        return HttpResponse(file)
