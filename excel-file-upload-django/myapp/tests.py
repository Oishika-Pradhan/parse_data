from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

class Test(TestCase):

    # def test_url(self):
    #     self.assertEqual(1 + 1, 3)

    def test_urls(self):
        response1 = self.client.get(reverse('myapp:mean'))
        self.assertEqual(response1.status_code, 200)
        response2 = self.client.get(reverse('myapp:index'))
        self.assertEqual(response2.status_code, 200)
        response3 = self.client.get(reverse('myapp:retention'))
        self.assertEqual(response3.status_code, 200)
        response4 = self.client.get(reverse('myapp:downloadexcel'))
        self.assertEqual(response4.status_code, 200)
        response5 = self.client.get(reverse('myapp:compound'))
        self.assertEqual(response5.status_code, 200)
    
    # def test_upload_video(self):
    #     video = SimpleUploadedFile("file.xlsx", b"file_content", content_type="xlsx")
    #     self.client.post(reverse('myapp:index'), {'xlsx': xlsx})