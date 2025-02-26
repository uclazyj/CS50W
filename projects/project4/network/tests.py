from django.test import TestCase

from .models import User, Post

# Create your tests here.
class NetworkTestCase(TestCase):

    def setUp(self):
        u1 = User.objects.create(username="u1")
        u2 = User.objects.create(username="u2")
        u3 = User.objects.create(username="u3")
    
    def test_no_followers_initially(self):
        u1 = User.objects.get(username="u1")
        self.assertEqual(u1.followers.count(), 0)

    def test_add_followers(self):
        u1 = User.objects.get(username="u1")
        u2 = User.objects.get(username="u2")
        u3 = User.objects.get(username="u3")

        u1.followers.add(u2)
        u1.followers.add(u3)
        self.assertEqual(u1.followers.count(), 2)

    def test_add_same_follower_twice(self):
        u1 = User.objects.get(username="u1")
        u2 = User.objects.get(username="u2")

        u1.followers.add(u2)
        u1.followers.add(u2)
        self.assertEqual(u1.followers.count(), 1)

    def test_add_followees(self):
        u1 = User.objects.get(username="u1")
        u2 = User.objects.get(username="u2")
        u3 = User.objects.get(username="u3")

        u2.followees.add(u1)
        u3.followees.add(u1)
        self.assertEqual(u1.followers.count(), 2)

    def test_add_follower_then_remove(self):
        u1 = User.objects.get(username="u1")
        u2 = User.objects.get(username="u2")
        u3 = User.objects.get(username="u3")

        u1.followers.add(u2)
        u1.followers.add(u3)
        u1.followers.remove(u2)
        self.assertEqual(u1.followers.count(), 1)

    def test_add_follower_then_remove_followee(self):
        u1 = User.objects.get(username="u1")
        u2 = User.objects.get(username="u2")

        u1.followers.add(u2)
        u2.followees.remove(u1)
        self.assertEqual(u1.followers.count(), 0)

    def test_add_posts(self):
        u1 = User.objects.get(username="u1")
        p1 = Post.objects.create(author=u1, content="foo")
        p2 = Post.objects.create(author=u1, content="bar")
        self.assertEqual(Post.objects.filter(author=u1).count(), 2)

    def test_like_posts(self):
        u1 = User.objects.get(username="u1")
        u2 = User.objects.get(username="u2")
        u3 = User.objects.get(username="u3")

        # u1 creates a post p1, u2 and u3 like it.
        p1 = Post.objects.create(author=u1, content="foo")
        p1.likes.add(u2)
        p1.likes.add(u3)
        self.assertEqual(Post.objects.get(author=u1).likes.count(), 2)
