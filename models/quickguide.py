import swapper
from django.db import models
from formula_one.models.base import Model
from formula_one.utils.upload_to import UploadTo

class quickguide(models.Model):
    title=models.CharField(
        max_length=200,
    )
    description=models.TextField()

    description_file=models.FileField(
        upload_to=UploadTo('helpcentre','quickguide'),
        blank=False,
        null=False,
    )