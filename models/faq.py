import swapper
from django.db import models
from formula_one.models.base import Model
from formula_one.utils.upload_to import UploadTo

class Faq(models.Model):
    app_name=models.CharField(
        max_length=63,
    )
    title=models.CharField(max_length=200)
    query=models.TextField()
    answer=models.TextField()
    answer_file=models.FileField(
        upload_to=UploadTo('helpcentre','faq'),
        blank=True,
        null=True,
    )

    class Meta(object):
        verbose_name_plural='faqs'
        