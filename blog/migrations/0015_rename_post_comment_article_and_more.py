# Generated by Django 4.1.1 on 2022-09-12 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_remove_comment_author_comment_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='post',
            new_name='article',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='date_added',
            new_name='created_on',
        ),
        migrations.AlterField(
            model_name='comment',
            name='name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
