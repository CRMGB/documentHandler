# Generated by Django 4.0 on 2023-02-14 14:16

import uuid
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fileManagement', '0002_uploadcsvfilemodel_created_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CSVFileModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('file_name', models.CharField(max_length=200)),
                ('row_count', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='CSVRowsModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('book_title', models.CharField(max_length=150)),
                ('book_author', models.CharField(max_length=200)),
                ('publisher_name', models.CharField(max_length=150)),
                ('date_published', models.DateField()),
                ('book_id', models.CharField(max_length=150, unique=True)),
                ('file', models.ForeignKey(help_text='File owning this row content', on_delete=django.db.models.deletion.CASCADE, to='fileManagement.csvfilemodel')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='UploadCSVFileModel',
        ),
    ]
