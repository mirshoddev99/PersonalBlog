from django.test import TestCase
from django.urls import reverse

from blog.models import Blog
from members.models import CustomUser


class PostsTestCase(TestCase):
    def test_posts(self):
        super_user = CustomUser.objects.create_superuser(username="Mirshod", email="oripovmirshod9@gmail.com", password="mirshod@99!")
        self.client.login(username="Mirshod", password="mirshod@99!")

        res = self.client.get(reverse("home"))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, super_user.username)
        self.assertTrue(super_user.is_superuser)

        req = self.client.post(reverse("new_post"), data={"title":"nice post", "text":"I have just written this post"})
        count_posts = Blog.objects.count()
        self.assertEqual(count_posts, 1)

        response = self.client.get(reverse("home"))
        self.assertContains(response, "nice post")
        self.assertContains(response, "I have just written this post")



    def test_user_not_add_post(self):

        user = CustomUser.objects.create_user(username="Sitora", email="Sitora9@gmail.com", password="sitora@99!")
        self.client.login(username="Sitora", password="sitora@99!")

        res = self.client.get(reverse("home"))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, user.username)
        self.assertFalse(user.is_superuser)
