from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


from notes.models import Note

User = get_user_model()


class TestContent(TestCase):
    NOTES_URL = reverse('notes:list')
    TITLE = 'Заголовок'
    NOTE_TEXT = 'Текст'
    SLUG = 'slug'

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='testUser')
        cls.user_client_1 = Client()
        cls.user_client_1.force_login(cls.user)
        cls.note = Note.objects.create(
            title='Заголовок', text='Текст',
            author=cls.user, slug=cls.SLUG
        )
        cls.new_user = User.objects.create(username='newUser')
        cls.user_client_2 = Client()
        cls.user_client_2.force_login(cls.new_user)
        cls.url = reverse('notes:add', None)

    def test_note_list_page_show_correct_context(self):
        response = self.client.get(self.NOTES_URL)
        object_list = response.context['object_list']
        self.assertIn(self.note, object_list)