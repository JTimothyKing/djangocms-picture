# -*- coding: utf-8 -*-
from django.test import TestCase
from django.test.client import RequestFactory

from cms.api import add_plugin
from cms.models import Placeholder
from cms.plugin_rendering import ContentRenderer

from djangocms_picture.cms_plugins import PicturePlugin

from django.utils.html_parser import HTMLParser

import re


class _NormalizedHTML(HTMLParser):
    def __init__(self, html):
        HTMLParser.__init__(self)
        self.segments = []
        self.feed(html)
        self.close()

    def handle_starttag(self, tag, attrs):
        normalized_attrs = [
            (name, " ".join(sorted(value.split(" "))))
            if name == "class"
            else (name, value)
            for name, value in sorted(attrs)
        ]
        attr_str = " ".join([
            '%s="%s"' % (name, value)
            if value
            else "%s" % name
            for name, value in normalized_attrs
        ])
        tag_str = "<%s %s>" % (tag, attr_str)
        self.segments.append(tag_str)

    def handle_endtag(self, tag):
        tag_str = "</%s>" % tag
        self.segments.append(tag_str)

    def handle_data(self, data):
        normalized_data = re.sub(r'\s+', " ", data)
        self.segments.append(normalized_data)

    def __str__(self):
        return ("".join(self.segments)).strip()

def _normalized(html):
    normalized_html = _NormalizedHTML(html)
    return str(normalized_html)


class PicturePluginTestCase(TestCase):
    def setUp(self):
        self.renderer = ContentRenderer(request=RequestFactory())

    # Override with our version.
    def assertHTMLEqual(self, html1, html2, msg=None):
        self.assertEqual(_normalized(html1), _normalized(html2), msg)

    def _create_instance(self, **data):
        placeholder = Placeholder.objects.create(slot='test')
        instance = add_plugin(
            placeholder,
            PicturePlugin,
            'en',
            **data
        )
        return instance

    def test_rendered_HTML(self):
        """
        Creates plugin instances using a series of setups, and verifies
        that each renders correctly.
        """

        link_url = 'https://www.google.com/'
        image_url = 'https://www.google.com/images/logo.png'

        cases = [
            {
                'name': 'external_picture',
                'data': {
                    'external_picture': image_url,
                },
                'expected_html': '<img src="%s">' % image_url,
            },
            {
                'name': 'external_picture with link_url',
                'data': {
                    'link_url': link_url,
                    'external_picture': image_url,
                },
                'expected_html': '<a href="%s"><img src="%s"></a>' % (link_url, image_url),
            },
        ]

        for case in cases:
            instance = self._create_instance(**case['data'])

            html = self.renderer.render_plugin(instance, {})

            self.assertHTMLEqual(html, case['expected_html'], case['name'])
