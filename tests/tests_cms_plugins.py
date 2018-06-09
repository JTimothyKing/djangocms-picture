# -*- coding: utf-8 -*-
from django.test import TestCase
from django.test.client import RequestFactory

from cms.api import add_plugin
from cms.models import Placeholder
from cms.plugin_rendering import ContentRenderer

from djangocms_picture.cms_plugins import PicturePlugin


class PicturePluginTestCase(TestCase):
    def setUp(self):
        self.renderer = ContentRenderer(request=RequestFactory())

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
