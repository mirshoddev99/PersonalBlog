# Generated by Django 4.1.1 on 2022-09-24 22:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0016_alter_comment_article'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blog',
            options={'ordering': ['-add_time']},
        ),
    ]
