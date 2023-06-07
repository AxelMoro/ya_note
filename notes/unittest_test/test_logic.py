from django.test import Client, TestCase
from django.urls import reverse
from notes.forms import WARNING
from notes.models import Note
from django.contrib.auth import get_user_model

User = get_user_model()


class TestNoteCreation(TestCase):
    TITLE = 'Заголовок'
    NOTE_TEXT = 'Текст'
    SLUG = 'slug'

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='testUser')
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.user)
        cls.note = Note.objects.create(
            title='Заголовок', text='Текст',
            author=cls.user, slug=cls.SLUG
        )
        cls.url = reverse('notes:add')
        cls.success_url = reverse('notes:success')
        cls.form_data = {
            'title': cls.TITLE, 'text': cls.NOTE_TEXT,
            'slug': cls.SLUG, 'author': cls.auth_client
        }

    def test_user_can_create_note(self):
        response = self.auth_client.post(self.url, data=self.form_data)
        self.assertRedirects(response, self.success_url)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)
        note = Note.objects.get()
        self.assertEqual(note.title, self.TITLE)
        self.assertEqual(note.text, self.NOTE_TEXT)
        self.assertEqual(note.author, self.auth_client)

    def test_anonymous_user_cant_create_comment(self):     
        self.client.post(self.url, data=self.form_data)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 0)





    def test_not_unique_slug(self):
        """Проверка на невозможность создать две заметки с одинаковым slug."""
        notes_count = Note.objects.count()
        new_data = {
            'text': self.NOTE_TEXT,
            'title': self.TITLE,
            'slug': self.note.slug,
            'author': self.auth_client,
        }
        response = self.auth_client.post(self.url, data=new_data)
        self.assertFormError(
            response,
            form='form',
            field='slug',
            errors=(self.note.slug + WARNING)
        )
        self.assertEqual(Note.objects.count(), notes_count)
        note_dict_objects = {
            Note.objects.get().text: self.note.text,
            Note.objects.get().title: self.note.title,
            Note.objects.get().slug: self.note.slug,
            Note.objects.get().author: self.note.author,
        }
        for note_field, init_note_field in note_dict_objects.items():
            with self.subTest(
                note_field=note_field,
                init_note_field=init_note_field,
            ):
                self.assertEqual(note_field, init_note_field)
