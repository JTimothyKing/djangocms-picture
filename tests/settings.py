#!/usr/bin/env python
# -*- coding: utf-8 -*-

HELPER_SETTINGS = {
    'INSTALLED_APPS': [
        'easy_thumbnails',
        'filer',
        'mptt',
    ],
    'ALLOWED_HOSTS': ['localhost'],
    'CMS_LANGUAGES': {
        1: [{
            'code': 'en',
            'name': 'English',
        }]
    },
    'LANGUAGE_CODE': 'en',
    'THUMBNAIL_PROCESSORS': [
        'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    ],
}

def run():
    from djangocms_helper import runner
    runner.cms('djangocms_picture')

if __name__ == '__main__':
    run()
