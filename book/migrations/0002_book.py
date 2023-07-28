# Generated by Django 4.2.3 on 2023-07-15 05:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=225)),
                ('author', models.CharField(max_length=225)),
                ('publisher', models.CharField(max_length=225)),
                ('publication_year', models.IntegerField()),
                ('price', models.FloatField()),
                ('description', models.TextField()),
                ('is_available', models.BooleanField(default=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.category')),
            ],
        ),
    ]
