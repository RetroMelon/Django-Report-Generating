from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader, RequestContext
from django_xhtml2pdf.utils import generate_pdf
from xhtml2pdf import pisa
import StringIO, logging
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


def fetch_resources(uri, rel):
    logger.debug("uri "+ uri)
    print "media_root", settings.REPORT_STATICFILES_ROOT, "    media_url", settings.REPORT_STATICFILES_URL
    path = os.path.join("s", uri.replace("a", ""))
    print 'returning path', path
    return path

def generate_html(request, template_name, data):
    template_name+=".html"
    report_data = {'message': data}

    report_context = RequestContext(request, report_data)
    template = loader.get_template(template_name)

    rendered_html = template.render(report_context)
    return render(request, 'editpage.html', {'report_html':rendered_html})
