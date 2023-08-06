import json
import os
from django.conf import settings
from django.contrib.admindocs.views import simplify_regex
from django.core.exceptions import ImproperlyConfigured, ViewDoesNotExist
from django.core.management.base import BaseCommand
from django.template import loader
from django.urls.resolvers import URLPattern, URLResolver

from ... import settings as default_settings

def describe_pattern(p):
    return str(p.pattern)

class Command(BaseCommand):
    def handle(self, *args, **options):
        views = self.extract_views_from_urlpatterns()
        urls = {}
        for (_, regex, url_name) in views:
            urls[url_name] = simplify_regex(regex)
        included_urls = {}
        if not hasattr(settings, 'DJANGO_TS_BRIDGE_INCLUDE_URL_NAMESPACES'):
            raise ImproperlyConfigured('DJANGO_TS_BRIDGE_INCLUDE_URL_NAMESPACES must be set to generate URLs')
        namespaces = tuple(f'{namespace}:' for namespace in settings.DJANGO_TS_BRIDGE_INCLUDE_URL_NAMESPACES)
        for url_name, url in urls.items():
            if url_name is not None and url_name.startswith(namespaces):
                included_urls[url_name] = url
        url_file_location = self.get_location()
        with open(url_file_location, 'w') as url_file:
            url_file.write(json.dumps(included_urls))
        self.stdout.write(self.style.SUCCESS(f'URL file sucessfully generated at {url_file_location}'))


    def get_location(self):
        output_path = getattr(settings, 'DJANGO_TS_BRIDGE_URL_OUTPUT_PATH', default_settings.DJANGO_TS_BRIDGE_URL_OUTPUT_PATH)
        return os.path.join(settings.BASE_DIR, output_path)

    def extract_views_from_urlpatterns(self, urlpatterns=None, base='', namespace=None):
        """
        Return a list of views from a list of urlpatterns.
        Each object in the returned list is a three-tuple: (view_func, regex, name)
        """
        if urlpatterns is None:
            urlconf = __import__(settings.ROOT_URLCONF, {}, {}, [''])
            urlpatterns = urlconf.urlpatterns
        views = []
        for p in urlpatterns:
            if isinstance(p, URLPattern):
                try:
                    if not p.name:
                        name = p.name
                    elif namespace:
                        name = '{0}:{1}'.format(namespace, p.name)
                    else:
                        name = p.name
                    pattern = describe_pattern(p)
                    views.append((p.callback, base + pattern, name))
                except ViewDoesNotExist:
                    continue
            elif isinstance(p, URLResolver):
                try:
                    patterns = p.url_patterns
                except ImportError:
                    continue
                if namespace and p.namespace:
                    _namespace = '{0}:{1}'.format(namespace, p.namespace)
                else:
                    _namespace = (p.namespace or namespace)
                pattern = describe_pattern(p)
                views.extend(self.extract_views_from_urlpatterns(patterns, base + pattern, namespace=_namespace))
            elif hasattr(p, '_get_callback'):
                try:
                    views.append((p._get_callback(), base + describe_pattern(p), p.name))
                except ViewDoesNotExist:
                    continue
            elif hasattr(p, 'url_patterns') or hasattr(p, '_get_url_patterns'):
                try:
                    patterns = p.url_patterns
                except ImportError:
                    continue
                views.extend(self.extract_views_from_urlpatterns(patterns, base + describe_pattern(p), namespace=namespace))
            else:
                raise TypeError("%s does not appear to be a urlpattern object" % p)
        return views
