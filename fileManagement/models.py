from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

# Django model utils TimeStampedModel
class TimestampedModel(models.Model):
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True

class CSVFileModel(models.Model):
    file_name = models.CharField(max_length=200)
    file_aws_s3_name = models.CharField(max_length=200, null=True)
    row_count = models.IntegerField(null=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, help_text="User owning this csv file", null=True
    )

    def __str__(self):
        return "File Name: %s.\n Row count: %s" % (self.file_name, self.row_count)

class CSVRowsModel(TimestampedModel):
    """Contents of the CSV file"""
    book_title = models.CharField(max_length=150)
    book_author = models.CharField(max_length=200)
    publisher_name = models.CharField(max_length=150)
    date_published = models.DateField()
    book_id = models.CharField(unique=True, max_length=150)
    file = models.ForeignKey(
        CSVFileModel,
        on_delete=models.CASCADE,
        help_text="File owning this row content",
        null=True,
        blank=True,
    )

    def __str__(self):
        return 'Tittle: %s.\n Author: %s.\n Created: %s.\n Updated: %s' % (
            self.book_title, self.book_author, self.created, self.updated
        )
