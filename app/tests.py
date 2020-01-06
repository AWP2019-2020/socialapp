from django.test import TestCase
from django.urls import reverse

from app.models import Comment, Post, User


class PostTestCase(TestCase):
    def test_post_detail(self):
        user = User.objects.create_user(username="testuser", password="testpassword")

        post = Post.objects.create(text="Test Post", created_by_id=user.pk)
        comment = Comment.objects.create(text="Test Comment", post=post, created_by_id=user.pk)

        response = self.client.get(reverse('post_detail', args=[post.pk]))

        self.assertEquals(response.context['post'], post)
        self.assertEquals(len(response.context['post'].comments.all()), 1)
        self.assertEquals(response.context['post'].comments.first(), comment)
