# gestion_blog/tests.py

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post, Comment

class GestionBlogTestCase(TestCase):
    TEST_POST_TITLE = 'Test Post'

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a test post
        self.post = Post.objects.create(
            title=self.TEST_POST_TITLE,
            content='This is a test post content.',
            author=self.user,
            slug='test-post'
        )

        # Create a test comment
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            text='This is a test comment.'
        )

    def test_post_model(self):
        self.assertEqual(str(self.post), self.TEST_POST_TITLE)
        self.assertEqual(self.post.author, self.user)

    def test_comment_model(self):
        expected_comment_str = f"Comment by {self.user} on {self.post}"
        self.assertEqual(str(self.comment), expected_comment_str)
        self.assertEqual(self.comment.author, self.user)

    def test_post_detail_view(self):
        url = reverse('post_detail', args=[self.post.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.TEST_POST_TITLE)
        self.assertContains(response, 'This is a test post content.')

    def test_add_comment_view(self):
        url = reverse('add_comment', args=[self.post.slug])
        response = self.client.post(url, {'text': 'Another test comment.'})
        self.assertEqual(response.status_code, 302)  # Redirect after adding a comment
        self.assertEqual(self.post.comments.count(), 2)  # Assuming there's already one comment

# Add more tests as needed for your specific views and functionalities.
