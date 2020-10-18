"""Data models for the CusDeb API Images application. """

from django.db import models


class DistroName(models.Model):
    """Distribution name (i.e. Debian, Devuan, Kali, Raspbian, Ubuntu). """

    name = models.CharField(max_length=255)

    def __str__(self):
        return '{}'.format(self.name)


class CodeName(models.Model):
    """Distribution code name. """

    name = models.CharField(max_length=255)

    def __str__(self):
        return '{}'.format(self.name)


class Port(models.Model):
    """Operating system port name (i.e. armhf, arm64). """

    name = models.CharField(max_length=32)

    def __str__(self):
        return '{}'.format(self.name)


class OS(models.Model):
    """Model representing an operation system supported by CusDeb. """

    name = models.ForeignKey(DistroName, models.PROTECT)
    codename = models.ForeignKey(CodeName, models.PROTECT)
    # Version can be 1, 10, 18.04, 2019.01, etc.
    # 32 characters should be enough to store any exotic verison.
    version = models.CharField(max_length=32)
    port = models.ForeignKey(Port, models.PROTECT)
    packages_url = models.CharField(max_length=64, blank=True)
    active = models.BooleanField(default=False)

    def get_short_name(self):
        """Gets the short name of the operating system intended for Pieman. """

        name = str(self.name).lower()
        codename = str(self.codename).split(' ')[0].lower()  # "Bionic Beaver" -> "bionic"
        return f'{name}-{codename}-{self.port}'

    def __str__(self):
        port = '64-bit' if str(self.port) == 'arm64' else '32-bit'
        return '{} {} "{}" ({})'.format(self.name, self.version, self.codename, port)


class DeviceName(models.Model):
    """Device name (i.e. Raspberry Pi, Orange Pi). """

    name = models.CharField(max_length=32)

    def __str__(self):
        return '{}'.format(self.name)


class Device(models.Model):
    """Model representing a device supported by CusDeb. """

    name = models.ForeignKey(DeviceName, models.PROTECT)
    generation = models.CharField(max_length=32, blank=True)
    model = models.CharField(max_length=255)
    supported_os = models.ManyToManyField(OS)
    active = models.BooleanField(default=False)

    def __str__(self):
        if self.generation:
            return '{} {} {}'.format(self.name, self.generation, self.model)

        return '{} {}'.format(self.name, self.model)


class Image(models.Model):
    name = models.CharField(max_length=255)
    device = models.ForeignKey(Device, models.PROTECT)
    os = models.ForeignKey(OS, models.PROTECT)

    def __str__(self):
        return '{}'.format(self.name)


class BuildTypeName(models.Model):
    """Build type name (i.e. Classic image, Mender-compatible image, Mender artifact). """

    name = models.CharField(max_length=32)

    def __str__(self):
        return '{}'.format(self.name)


class BuildType(models.Model):
    """Model representing a build type supported by CusDeb. """

    device = models.ForeignKey(Device, models.CASCADE)
    os = models.ForeignKey(OS, models.PROTECT)
    build_type = models.ManyToManyField(BuildTypeName)

    class Meta:
        unique_together = (('device', 'os'), )

    def __str__(self):
        return '{} on {}'.format(self.os, self.device)
