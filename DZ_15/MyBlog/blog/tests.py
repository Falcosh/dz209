from django.test import TestCase, Client
from django.urls import reverse
from .models import Post


class PostModelTest(TestCase):
    def setUp(self):
        self.post = Post.objects.create(title='Тест', content='Содержание теста')

    def test_post_creation(self):
        self.assertEqual(self.post.title, 'Тест')
        self.assertEqual(self.post.content, 'Содержание теста')

    def test_post_str(self):
        self.assertEqual(str(self.post), 'Тест')


class HomeViewTest(TestCase):
    def test_home_status_code(self):
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)

    def test_home_template(self):
        resp = self.client.get(reverse('home'))
        self.assertTemplateUsed(resp, 'blog/home.html')


class AboutViewTest(TestCase):
    def test_about_status_code(self):
        resp = self.client.get(reverse('about'))
        self.assertEqual(resp.status_code, 200)

    def test_about_template(self):
        resp = self.client.get(reverse('about'))
        self.assertTemplateUsed(resp, 'blog/about.html')


class PostListViewTest(TestCase):
    def setUp(self):
        Post.objects.create(title='Пост 1', content='Контент 1')
        Post.objects.create(title='Пост 2', content='Контент 2')

    def test_list_status_code(self):
        resp = self.client.get(reverse('post_list'))
        self.assertEqual(resp.status_code, 200)

    def test_list_template(self):
        resp = self.client.get(reverse('post_list'))
        self.assertTemplateUsed(resp, 'blog/post_list.html')

    def test_list_contains_posts(self):
        resp = self.client.get(reverse('post_list'))
        self.assertContains(resp, 'Пост 1')
        self.assertContains(resp, 'Пост 2')


class PostDetailViewTest(TestCase):
    def setUp(self):
        self.post = Post.objects.create(title='Детальный пост', content='Подробный текст')

    def test_detail_status_code(self):
        resp = self.client.get(reverse('post_detail', kwargs={'pk': self.post.pk}))
        self.assertEqual(resp.status_code, 200)

    def test_detail_404(self):
        resp = self.client.get(reverse('post_detail', kwargs={'pk': 9999}))
        self.assertEqual(resp.status_code, 404)

    def test_detail_template(self):
        resp = self.client.get(reverse('post_detail', kwargs={'pk': self.post.pk}))
        self.assertTemplateUsed(resp, 'blog/post_detail.html')


class PostCreateViewTest(TestCase):
    def test_create_status_code(self):
        resp = self.client.get(reverse('post_create'))
        self.assertEqual(resp.status_code, 200)

    def test_create_post_valid(self):
        resp = self.client.post(reverse('post_create'), {
            'title': 'Новый пост',
            'content': 'Текст нового поста',
        })
        self.assertEqual(resp.status_code, 302)  # редирект
        self.assertTrue(Post.objects.filter(title='Новый пост').exists())

    def test_create_post_invalid(self):
        resp = self.client.post(reverse('post_create'), {
            'title': '',
            'content': '',
        })
        self.assertEqual(resp.status_code,200)
        self.assertFalse(Post.objects.filter(title='').exists())


class PostUpdateViewTest(TestCase):
    def setUp(self):
        self.post = Post.objects.create(title='Старый', content='Старый текст')

    def test_update_status_code(self):
        resp = self.client.get(reverse('post_edit', kwargs={'pk': self.post.pk}))
        self.assertEqual(resp.status_code, 200)

    def test_update_post(self):
        resp = self.client.post(reverse('post_edit', kwargs={'pk': self.post.pk}), {
            'title': 'Новый заголовок',
            'content': 'Новый текст',
        })
        self.assertEqual(resp.status_code, 302)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Новый заголовок')


class PostDeleteViewTest(TestCase):
    def setUp(self):
        self.post = Post.objects.create(title='Удалить', content='Этот пост будет удалён')

    def test_delete_status_code(self):
        resp = self.client.get(reverse('post_delete', kwargs={'pk': self.post.pk}))
        self.assertEqual(resp.status_code, 200)

    def test_delete_post(self):
        resp = self.client.post(reverse('post_delete', kwargs={'pk': self.post.pk}))
        self.assertEqual(resp.status_code, 302)
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())
