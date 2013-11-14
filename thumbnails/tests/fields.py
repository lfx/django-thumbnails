import os

from django.core.files import File
from django.test import TestCase

from .models import TestModel
from thumbnails.backends.metadata import ImageMeta


class ImageFieldTest(TestCase):

    def setUp(self):
        self.instance = TestModel.objects.create()
        with open('thumbnails/tests/tests.png') as image_file:
            self.instance.avatar = File(image_file)
            self.instance.save()

    def tearDown(self):
        self.instance.avatar.storage.delete_temporary_storage()
        super(ImageFieldTest, self).tearDown()

    def test_image_field(self):
        avatar_folder = \
            os.path.join(self.instance.avatar.storage.temporary_location, 'avatars')

        # 1. Test for thumbnail creation
        self.assertFalse(os.path.isfile(os.path.join(avatar_folder, 'tests_small.png')))
        thumb = self.instance.avatar.create_thumbnail(size='small')
        self.assertTrue(os.path.isfile(os.path.join(avatar_folder, 'tests_small.png')))

        # 2. Test for getting thumbnail
        img_meta = self.instance.avatar.get_thumbnail(size='small')
        self.assertEqual(img_meta, ImageMeta(thumb.source.name ,thumb.name, thumb.size))

        # 3. Test for thumbnail deletion
        self.assertTrue(os.path.isfile(os.path.join(avatar_folder, 'tests_small.png')))
        self.instance.avatar.delete_thumbnail(size='small')
        self.assertFalse(os.path.isfile(os.path.join(avatar_folder, 'tests_small.png')))

