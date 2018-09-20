# Generated by Django 2.1.1 on 2018-09-18 06:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import kernel.utils.upload_to


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.KERNEL_PERSON_MODEL),
        ('comments', '__first__'),
        migrations.swappable_dependency(settings.KERNEL_MAINTAINER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Query',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('removed', models.DateTimeField(blank=True, default=None, editable=False, null=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('datetime_modified', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=127)),
                ('app_name', models.CharField(max_length=63)),
                ('query', models.TextField()),
                ('uploaded_file', models.FileField(blank=True, null=True, upload_to=kernel.utils.upload_to.UploadTo('helpcentre', 'queries'))),
                ('is_closed', models.BooleanField(default=False)),
                ('assignee', models.ManyToManyField(blank=True, to=settings.KERNEL_MAINTAINER_MODEL)),
                ('comments', models.ManyToManyField(blank=True, to='comments.Comment')),
                ('uploader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.KERNEL_PERSON_MODEL)),
            ],
            options={
                'verbose_name_plural': 'queries',
            },
        ),
    ]
