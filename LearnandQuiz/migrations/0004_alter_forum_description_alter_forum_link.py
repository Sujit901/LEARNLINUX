# Generated by Django 4.1.5 on 2023-06-16 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LearnandQuiz', '0003_alter_discussion_discuss_alter_forum_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forum',
            name='description',
            field=models.TextField(blank=True, max_length=1000000),
        ),
        migrations.AlterField(
            model_name='forum',
            name='link',
            field=models.CharField(max_length=100000, null=True),
        ),
    ]
