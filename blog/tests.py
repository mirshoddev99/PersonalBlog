from django.test import TestCase
from django.urls import reverse

from blog.models import Blog
from members.models import CustomUser


class PostsTestCase(TestCase):

    def test_posts(self):
        super_user = CustomUser.objects.create_superuser(username="Mirshod", email="oripovmirshod9@gmail.com",
                                                         password="mirshod@99!")
        self.client.login(username="Mirshod", password="mirshod@99!")

        res = self.client.get(reverse("home"))
        self.assertEqual(res.status_code, 200)
        # check superuser
        self.assertContains(res, super_user.username)
        self.assertTrue(super_user.is_superuser)

        post = self.client.post(reverse("new_post"),
                                data={"title": "nice post", "text": "I have just written this post"})
        post1 = self.client.post(reverse("new_post"),
                                 data={"title": "good post", "text": "I have just written next post"})

        self.assertEqual(post.status_code, 302)
        self.assertEqual(post1.status_code, 302)
        self.assertEqual(Blog.objects.count(), 2)

        response = self.client.get(reverse("home"))
        all_posts = Blog.objects.all()

        for i in range(1):
            self.assertContains(response, all_posts[i].title)
            self.assertContains(response, all_posts[i].text)

    def test_update_post_and_pagination(self):

        super_user = CustomUser.objects.create_superuser(username="Mirshod", email="oripovmirshod9@gmail.com",
                                                         password="mirshod@99!")
        self.client.login(username="Mirshod", password="mirshod@99!")

        post = self.client.post(reverse("new_post"),
                                data={"title": "nice post", "text": "I have just written this post"})
        post1 = self.client.post(reverse("new_post"),
                                 data={"title": "good post", "text": "I have just written next post"})
        post2 = self.client.post(reverse("new_post"), data={"title": "great post", "text": "Great post!!!!!"})

        self.assertEqual(post.status_code, 302)
        self.assertEqual(post1.status_code, 302)
        self.assertEqual(post2.status_code, 302)

        all_posts = Blog.objects.all()
        self.assertEqual(Blog.objects.count(), 3)
        get_last_post = Blog.objects.get(id=3)

        detail = self.client.patch(reverse("post_edit", kwargs={"pk": get_last_post.id}),
                                   data={"title": "Update", "text": "I have edited this post"})
        self.assertEqual(detail.status_code, 200)

        get_last_post.refresh_from_db()

        response = self.client.get(reverse("home"))
        self.assertContains(response, get_last_post.title)
        self.assertContains(response, get_last_post.text)

        # check pagination
        for i in range(2, 2, -1):
            self.assertContains(response, all_posts[i].title)
            self.assertContains(response, all_posts[i].text)

        req = self.client.get(reverse("home") + "?page=2")
        self.assertEqual(req.status_code, 200)
        self.assertContains(req, "nice post")


class CommentTestCase(TestCase):

    def setUp(self) -> None:
        self.user = CustomUser.objects.create_superuser(username="Mirshod", email="oripovmirshod9@gmail.com",
                                                        password="mirshod@99!")
        self.client.login(username="Mirshod", password="mirshod@99!")

    def test_comment(self):
        post = Blog.objects.create(title="New post", text="New body of the post")

        req = self.client.post(reverse("reviews", kwargs={"id": post.id}),data={"body": "I have left a comment for this post"})
        self.assertEqual(req.status_code, 302)

        response = self.client.get(reverse("post_detail", kwargs={"id": post.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, post.title)
        self.assertContains(response, post.text)
        self.assertContains(response, "I have left a comment for this post")
        self.assertContains(response, self.user.username)
