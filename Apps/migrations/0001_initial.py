# Generated by Django 4.1 on 2023-01-12 13:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('Category_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('contact_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField()),
                ('time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('profile', models.ImageField(upload_to='images/UserProfiles')),
                ('post_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('date_timeStamp', models.DateTimeField(auto_now_add=True)),
                ('thumbnail', models.URLField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Apps.category')),
                ('favourite', models.ManyToManyField(blank=True, related_name='favourite', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]