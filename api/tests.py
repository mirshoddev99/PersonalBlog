from rest_framework.test import APITestCase, APIClient
from rest_framework.reverse import reverse
from blog.models import Blog
from members.models import CustomUser


class PostsAPITestCase(APITestCase):
    client = APIClient()

    def setUp(self):
        self.user = CustomUser.objects.create_superuser(username="Mirshod", email="oripov123@gmail.com",
                                                        password="somepass")
        self.user.save()
        self.client.login(username='Mirshod', password='somepass')
        self.assertTrue(self.user.is_superuser)


    def test_posts(self):
        post1 = Blog.objects.create(title="New post", text="New body of the post")
        post2 = Blog.objects.create(title="next post", text="next body of the next post")

        all_posts = Blog.objects.count()
        self.assertEqual(all_posts, 2)

        req = self.client.get(reverse("posts"))
        self.assertEqual(req.status_code, 200)
        self.assertEqual(len(req.data['results']), 2)

        self.assertEqual(req.data["count"], 2)
        self.assertEqual(req.data['results'][0]['title'], post2.title)
        self.assertEqual(req.data['results'][0]['text'], post2.text)
        self.assertEqual(req.data['results'][1]['title'], post1.title)
        self.assertEqual(req.data['results'][1]['text'], post1.text)


    def test_pagination(self):
        post1 = Blog.objects.create(title="New post", text="New body of the post")
        post2 = Blog.objects.create(title="next post", text="next body of the next post")
        post3 = Blog.objects.create(title="last post", text="last body of the last post")

        all_posts = Blog.objects.count()
        self.assertEqual(all_posts, 3)

        response = self.client.get(reverse("posts"))
        self.assertEqual(response.status_code, 200)

        for idx, post in enumerate([post3, post2]):
            self.assertEqual(response.data['results'][idx]['title'], post.title)
            self.assertEqual(response.data['results'][idx]['text'], post.text)
            self.assertEqual(response.data['results'][idx]['id'], post.id)

        res = self.client.get(reverse("posts") + "?page=2")
        self.assertEqual(response.status_code, 200)

        self.assertEqual(res.data['results'][0]['title'], post1.title)
        self.assertEqual(res.data['results'][0]['text'], post1.text)
        self.assertEqual(res.data['results'][0]['id'], post1.id)


