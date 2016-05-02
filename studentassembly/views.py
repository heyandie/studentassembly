import re
from uuid import UUID

from django.views.generic import TemplateView
from django.conf import settings

from report.models import Report, Category, School


REPORT_VIEW_REGEX = re.compile(r'/report/view/([a-z0-9\-]+)')


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['title'] = 'Student Assembly'
        context['description'] = 'Student Assembly is a tool that aims to reduce quiet and hard corruption in universities. It is a safe anonymous reporting platform for students and an efficient report management platform for school administrations.'

        report_view_path = re.findall(REPORT_VIEW_REGEX, self.request.path)

        if report_view_path:
            try:
                report = Report.objects.get(pk=UUID(report_view_path[0]))
                category = Category.objects.get(pk=report.category)
                school = School.objects.get(pk=report.school)
                description = report.text[:75] + '..' if len(report.text) > 75 else report.text

                og_tags = {
                    'fb:app_id': settings.FB.get('APP_ID'),
                    'og:type': 'article',
                    'article:publisher': 'https://www.facebook.com/Student-Assembly-501349423323098/',
                    'article:tag': 'report',
                    'og:site_name': 'StudentAssembly',
                    'og:title': 'Report on ' + category.name + ' | ' + school.name,
                    'og:description': description,
                    'og:url': self.request.META['HTTP_HOST'] + '/report/view/' + report_view_path[0],
                }

                tw_cards = {
                    'twitter:card': 'summary_large_image',
                    'twitter:site': '@studentassemblyph',
                    'twitter:title':  'Report on ' + category.name + ' | ' + school.name
                }

                context['og_tags'] = og_tags
                context['tw_cards'] = tw_cards
                context['title'] = ' | '.join([category.name.title(), school.name.title(), 'Student Assembly'])
            except:
                raise

        print(context.get('og_tags'))

        return context
