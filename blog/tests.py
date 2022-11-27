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

        post = self.client.post(reverse("new_post"), data={"title":"nice post", "text":"I have just written this post"})
        post1= self.client.post(reverse("new_post"), data={"title":"good post", "text":"I have just written next post"})

        self.assertEqual(Blog.objects.count(), 2)
        response = self.client.get(reverse("home"))
        all_posts = Blog.objects.all()

        for i in range(1):
            self.assertContains(response, all_posts[i].title)
            self.assertContains(response, all_posts[i].text)


    def test_update_post_and_pagination(self):

        super_user = CustomUser.objects.create_superuser(username="Mirshod", email="oripovmirshod9@gmail.com", password="mirshod@99!")
        self.client.login(username="Mirshod", password="mirshod@99!")

        post = self.client.post(reverse("new_post"), data={"title":"nice post", "text":"I have just written this post"})
        post1= self.client.post(reverse("new_post"), data={"title":"good post", "text":"I have just written next post"})
        post2= self.client.post(reverse("new_post"), data={"title":"great post", "text":"Great post!!!!!"})

        all_posts = Blog.objects.all()
        self.assertEqual(Blog.objects.count(), 3)
        get_last_post = Blog.objects.get(id=3)

        detail = self.client.patch(reverse("post_edit", kwargs={"pk":get_last_post.id}), data={"title":"Update", "text":"I have edited this post"})

        response = self.client.get(reverse("home"))
        self.assertContains(response, get_last_post.title)
        self.assertContains(response, get_last_post.text)

        # check pagination
        for i in range(2):
            self.assertContains(response, all_posts[i].title)
            self.assertContains(response, all_posts[i].text)

        req = self.client.get(reverse("home") + "?page=2")
        self.assertEqual(req.status_code, 200)
        self.assertContains(req, "nice post")
