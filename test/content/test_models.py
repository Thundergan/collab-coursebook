"""Purpose of this file

This file contains the test cases for /content/models.py.
"""

import os
from django.test import override_settings
from test.test_cases import MediaTestCase
from test import utils
import content.models as model

@override_settings(MEDIA_ROOT=utils.MEDIA_ROOT)
class LatexTestCase(MediaTestCase):  # pylint: disable=too-few-public-methods)
    """LaTeX test case

    Defines the test cases for the model Latex.
    """

    def test_generate_preview_successful(self):
        """Generate preview test case - successful

        Tests that a preview image gets generated in the preview folder
        after calling generate_preview on a LaTeX Content.
        """
        latex = model.Latex.objects.first()
        preview_folder = 'uploads/previews/'

        self.assertFalse(os.path.exists(os.path.join(utils.MEDIA_ROOT, preview_folder)))
        preview_path = latex.generate_preview()
        self.assertTrue(os.path.exists(os.path.join(utils.MEDIA_ROOT, preview_folder)))

        content = model.Content.objects.first()
        content.preview.name = preview_path
        content.save()

        self.assertEqual('uploads/previews/Topic_Category.jpg', content.preview.name)
        self.assertTrue(bool(content.preview))

@override_settings(MEDIA_ROOT=utils.MEDIA_ROOT)
class PanoptoVideoContentTestCase(MediaTestCase): # pylint: disable=too-few-public-methods)
    """PanoptoVideoContent test case

    Defines the test cases for the model PanoptoVideoContent.
    """

    def test_id_property(self):
        """Test id property

        Tests the id property of PanoptoVideoContent.
        """
        panopto_video = model.PanoptoVideoContent(url='https://tu-darmstadt.cloud.panopto.eu/Panopto/Pages/Viewer.aspx?id=143edbe5-b2a1-48bc-bc94-b0fa011f7143')
        self.assertEqual(panopto_video.id, '143edbe5-b2a1-48bc-bc94-b0fa011f7143')

    def test_start_time_property(self):
        """Test start_time property

        Tests the start_time property of PanoptoVideoContent.
        """
        panopto_video = model.PanoptoVideoContent(url='https://tu-darmstadt.cloud.panopto.eu/Panopto/Pages/Viewer.aspx?id=143edbe5-b2a1-48bc-bc94-b0fa011f7143&start=1792.375985')
        self.assertEqual(panopto_video.start_time, '1792.375985')

    def test_start_time_property_default(self):
        """Test start_time property with default value

        Tests the start_time property of PanoptoVideoContent when start time is not present in the URL.
        """
        panopto_video = model.PanoptoVideoContent(url='https://tu-darmstadt.cloud.panopto.eu/Panopto/Pages/Viewer.aspx?id=143edbe5-b2a1-48bc-bc94-b0fa011f7143')
        self.assertEqual(panopto_video.start_time, '0:00:00')

    def test_str_method(self):
        """Test __str__ method

        Tests the __str__ method of PanoptoVideoContent.
        """
        panopto_video = model.PanoptoVideoContent(url='https://tu-darmstadt.cloud.panopto.eu/Panopto/Pages/Viewer.aspx?id=143edbe5-b2a1-48bc-bc94-b0fa011f7143')
        self.assertEqual(str(panopto_video), 'https://tu-darmstadt.cloud.panopto.eu/Panopto/Pages/Viewer.aspx?id=143edbe5-b2a1-48bc-bc94-b0fa011f7143')

    def test_filter_by_own_type(self):
        """Test filter_by_own_type method

        Tests the filter_by_own_type method of PanoptoVideoContent.
        """
        panopto_video = model.PanoptoVideoContent(url='https://tu-darmstadt.cloud.panopto.eu/Panopto/Pages/Viewer.aspx?id=143edbe5-b2a1-48bc-bc94-b0fa011f7143')
        panopto_video.save()

        contents = model.Content.objects.all() # contains only one Latex object
        filtered_contents = model.PanoptoVideoContent.filter_by_own_type(contents)

        self.assertIn(panopto_video, filtered_contents)


class GeneralURLTestCase(MediaTestCase):
    """GeneralURL test case

    Defines the test cases for the model GeneralURL.

    """
    def test_str_method(self):
        """Test __str__ method

        Tests the __str__ method of GeneralURL.

        """
        general_url = model.GeneralURL(url='https://www.google.com/', title='Google')
        self.assertEqual(str(general_url), 'https://www.google.com/')

    def test_filter_by_own_type(self):
        """Test filter_by_own_type method

        Tests the filter_by_own_type method of GeneralURL.

        """
        general_url = model.GeneralURL(url='https://www.google.com/', title='Google')
        general_url.save()

        all_contents = model.Content.objects.all()
        filtered_contents = model.GeneralURL.filter_by_own_type(all_contents)

        self.assertTrue(all(isinstance(content, model.GeneralURL) for content in filtered_contents))
