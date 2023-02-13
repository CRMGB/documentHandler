import uuid
from django.db import models

#Django model utils TimeStampedModel
class TimestampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class UploadCSVFileModel(TimestampedModel):
    book_title = models.CharField(max_length=150)
    book_author = models.CharField(max_length=200)
    publisher_name = models.CharField(max_length=150)
    date_published = models.DateField()
    book_id = models.CharField(unique=True, max_length=150)

    def __str__(self):
        return 'Tittle: %s.\n Author: %s.\n Created: %s.\n Updated: %s' % (
            self.book_title, self.book_author, self.created, self.updated
        )
