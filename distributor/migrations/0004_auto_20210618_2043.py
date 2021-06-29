# Generated by Django 3.2.4 on 2021-06-18 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('distributor', '0003_review_rating'),
    ]

    operations = [
        migrations.CreateModel(
            name='HashTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='HashTag',
            field=models.ManyToManyField(blank=True, to='distributor.HashTag'),
        ),
    ]
