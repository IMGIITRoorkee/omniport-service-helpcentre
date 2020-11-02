import swapper
from django.db import models
from comments.mixins import CommentableMixin
from formula_one.models.base import Model


class Faq(CommentableMixin, Model):
    """ 
    This model holds the information about the FaQ of all particular App 
    """

    app_name = models.CharField(
        max_length=63,
    )

    question = models.TextField()
    answer = models.TextField()

    # def __str__(self):
    #     app_name = self.app_name
