from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader, RequestContext
from xhtml2pdf import pisa
import StringIO, logging, os
from project import settings

logger = logging.getLogger(__name__)

def render_to_pdf(request):
    html = request.POST.get("data", "")
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(
            StringIO.StringIO(html.encode("UTF-8")),
            result,
            link_callback=fetch_resources
    )

    if not pdf.err:
        return HttpResponse(
                result.getvalue(),
                content_type='application/pdf'
        )
    else:
        return HttpResponse('We had some errors')


class UnsupportedMediaPathException(Exception):
    pass

def fetch_resources(uri, rel):
    """
    Callback to allow xhtml2pdf/reportlab to retrieve Images,Stylesheets, etc.
    `uri` is the href attribute from the html link element.
    `rel` gives a relative path, but it's not used here.
    """
    # if settings.MEDIA_URL and uri.startswith(settings.MEDIA_URL):
    #      path = os.path.join(settings.MEDIA_ROOT,
    #                          uri.replace(settings.MEDIA_URL, ""))
    if settings.STATIC_URL and settings.STATICFILES_DIRS and uri.startswith(settings.STATIC_URL):
        # path = os.path.join(settings.STATIC_ROOT,
        #                     uri.replace(settings.STATIC_URL, ""))
        # if not os.path.exists(path):
        for d in settings.STATICFILES_DIRS:
            path = os.path.join(d, uri.replace(settings.STATIC_URL, ""))
            if os.path.exists(path):
                break
    elif uri.startswith("http://") or uri.startswith("https://"):
        path = uri
    else:
        raise UnsupportedMediaPathException(
                                'media urls must start with %s or %s' % (
                                settings.MEDIA_URL, settings.STATIC_URL))

    print path
    return path

def generate_html(request, template_name, data):
    template_name+=".html"
    report_data = {'message': data}

    report_context = RequestContext(request, report_data)
    template = loader.get_template(template_name)

    rendered_html = template.render(report_context)
    return render(request, 'editpage.html', {'report_html':rendered_html})
