"""Data models for the CusDeb API Images application. """

from django.contrib.auth.models import User
from django.db import models, transaction
from django.utils.timezone import now


class ImageManager(models.Manager):
    """Image model manager. """

    def get_any(self):
        """
        * Fetches a pending for building image from the database.
        * Changes the image status to 'BUILDING'.
        * Returns the image.
        """

        with transaction.atomic():
            image = self.select_for_update().filter(status=Image.PENDING).first()
            if not image:
                return None

            image.status = Image.BUILDING
            image.save(update_fields=['status'])

        return image


class Image(models.Model):
    """Model representing an image which has been built (or is being built) by CusDeb. """

    CLASSIC = 'C'
    MENDER = 'M'
    ARTIFACT = 'A'

    FLAVOUR_CHOICES = {
        (CLASSIC, 'Classic'),
        (MENDER, 'Mender'),
        (ARTIFACT, 'Artifact'),
    }

    UNDEFINED = 'U'
    PENDING = 'P'
    BUILDING = 'B'
    FAILED = 'F'
    INTERRUPTED = 'I'
    SUCCEEDED = 'S'

    STATUS_CHOICES = (
        (UNDEFINED, 'Undefined'),
        (PENDING, 'Pending'),
        (BUILDING, 'Building'),
        (FAILED, 'Failed'),
        (INTERRUPTED, 'Interrupted'),
        (SUCCEEDED, 'Succeeded'),
    )

    def change_status_to(self, status):
        """Changes the current status to the specified one. """

        self.status = status
        self.save(update_fields=['status'])

    def set_started_at(self):
        """Sets the 'started_at' field to now. """

        self.started_at = now()
        self.save(update_fields=['started_at'])

    def set_finished_at(self):
        """Sets the 'finished_at' field to now. """

        self.finished_at = now()
        self.save(update_fields=['finished_at'])

    def store_build_log(self, build_log):
        """Stores the build log in the 'build_log' field. """

        self.build_log = build_log
        self.save(update_fields=['build_log'])

    user = models.ForeignKey(User, models.PROTECT)
    image_id = models.CharField(max_length=36)
    device_name = models.CharField(max_length=64)
    distro_name = models.CharField(max_length=64)
    flavour = models.CharField(max_length=1, choices=FLAVOUR_CHOICES, default=CLASSIC)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    started_at = models.DateTimeField(blank=True, null=True)
    finished_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=UNDEFINED)
    notes = models.TextField(default='')
    build_log = models.TextField(default='')
    objects = ImageManager()

    def __str__(self):
        return '{} on {}'.format(self.distro_name, self.device_name)
