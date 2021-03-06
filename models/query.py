import swapper
from django.db import models

from comments.mixins import CommentableMixin
from formula_one.models.base import Model
from formula_one.utils.upload_to import UploadTo


class Query(CommentableMixin, Model):
    """
    This model holds the information about a query asked by a user of Omniport
    """

    title = models.CharField(
        max_length=127,
    )

    uploader = models.ForeignKey(
        to=swapper.get_model_name('kernel', 'Person'),
        on_delete=models.CASCADE,
    )

    app_name = models.CharField(
        max_length=63,
    )

    query = models.TextField()

    uploaded_file = models.FileField(
        upload_to=UploadTo('helpcentre', 'queries'),
        blank=True,
        null=True,
    )

    is_closed = models.BooleanField(
        default=False,
    )

    assignees = models.ManyToManyField(
        to=swapper.get_model_name('kernel', 'Maintainer'),
        blank=True,
    )

    class Meta:
        """
        Meta class for model Query
        """

        verbose_name_plural = 'queries'

    def __str__(self):
        """
        Return the string representation of the model
        :return: the string representation of the model
        """

        uploader = self.uploader
        app_name = self.app_name
        title = self.title

        return f'{uploader} ({app_name}): {title}'
