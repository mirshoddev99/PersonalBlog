# Generated by Django 4.1 on 2022-09-06 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_remove_blog_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='date',
            field=models.DateField(auto_created=True),
        ),
    ]