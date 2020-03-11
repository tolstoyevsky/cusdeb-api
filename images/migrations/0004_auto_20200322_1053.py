# Generated by Django 2.2.9 on 2020-03-22 10:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('images', '0003_auto_20190308_2012'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='name',
        ),
        migrations.AddField(
            model_name='image',
            name='build_type',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='images.BuildTypeName'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='image',
            name='finished_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='image',
            name='format',
            field=models.CharField(choices=[('img.gz', 'Classic img.gz'), ('mender', 'Mender artifact')], default='img.gz', max_length=18),
        ),
        migrations.AddField(
            model_name='image',
            name='notes',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='image',
            name='started_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='image',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('building', 'Building'), ('failed', 'Failed'), ('succeeded', 'Succeeded')], default='pending', max_length=18),
        ),
        migrations.AddField(
            model_name='image',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
