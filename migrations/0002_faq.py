# Generated by Django 3.0.3 on 2020-11-02 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
        ('helpcentre', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Faq',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('datetime_modified', models.DateTimeField(auto_now=True)),
                ('app_name', models.CharField(max_length=63)),
                ('question', models.TextField()),
                ('answer', models.TextField()),
                ('comments', models.ManyToManyField(blank=True, to='comments.Comment')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
