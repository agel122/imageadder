from django.core.files.base import ContentFile
from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APITestCase
from PIL import Image
import io
import hashlib

import tempfile
from django.test import override_settings

from .models import PostedPicture

from rename_resize.resizer import resize_rename


def create_image_file1():
    file = io.BytesIO()
    image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
    image.save(file, 'png')
    file.name = 'test.png'
    file.seek(0)
    django_friendly_file = ContentFile(file.read(), 'test.png')
    return django_friendly_file


class ImagePosterTestsPureDjango(TestCase):
    @override_settings(MEDIA_ROOT=tempfile.TemporaryDirectory(prefix='mediatest').name)
    def setUp(self):
        self.image = PostedPicture.objects.create(
            title='testImage',
            cover=create_image_file1(),
        )
        self.client.post(reverse('add'), {
            'title': 'testImage1',
            'cover': create_image_file1(),
        })

    def test_image_content(self):
        image = PostedPicture.objects.get(id=1)
        expected_title = f'{image.title}'
        self.assertEqual(expected_title, 'testImage')

    def test_list_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertContains(response, 'testImage')
        self.assertContains(response, 'testImage1')


class ImagePosterTestsDjangoRestApi(APITestCase):
    @override_settings(MEDIA_ROOT=tempfile.TemporaryDirectory(prefix='mediatest').name)
    def setUp(self):
        self.client.post(reverse('all_pictures-list'), {
            'title': 'testImage3',
            'cover': create_image_file1(),
        })

    def test_list_view(self):
        response = self.client.get(reverse('all_pictures-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testImage3')


class TestFuncRenameResize(TestCase):
    def setUp(self):
        self.file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(self.file, 'png')
        self.file.name = 'test.png'
        self.file.seek(0)
        self.name_to_hash = self.file.name.split('.')[0]
        self.hash_name = hashlib.md5(self.name_to_hash.encode()).hexdigest()
        self.name_to_save = f'{self.hash_name}_200x200.png'
        self.resized_image1 = resize_rename(self.file, 200, 200)
        self.resized_image2 = resize_rename(self.file, 200)

    def test_resize_name(self):
        self.assertEqual(self.resized_image1['name'], self.name_to_save)

    def test_resize_height(self):
        self.assertEqual(self.resized_image2['name'], self.name_to_save)





















