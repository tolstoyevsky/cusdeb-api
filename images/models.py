from django.db import models


class DistroName(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return '{}'.format(self.name)


class CodeName(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return '{}'.format(self.name)


class Port(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return '{}'.format(self.name)


class OS(models.Model):
    name = models.ForeignKey(DistroName, models.PROTECT)
    codename = models.ForeignKey(CodeName, models.PROTECT)
    # Version can be 1, 10, 18.04, 2019.01, etc.
    # 32 characters should be enough to store any exotic verison.
    version = models.CharField(max_length=32)
    port = models.ForeignKey(Port, models.PROTECT)
    active = models.BooleanField(default=False)

    def __str__(self):
        return '{} {} "{}" ({})'.format(self.name, self.version, self.codename,
                                        self.port)


class DeviceName(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return '{}'.format(self.name)


class Device(models.Model):
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
    name = models.CharField(max_length=32)

    def __str__(self):
        return '{}'.format(self.name)


class BuildType(models.Model):
    device = models.ForeignKey(Device, models.PROTECT)
    os = models.ForeignKey(OS, models.PROTECT)
    build_type = models.ManyToManyField(BuildTypeName)

    def __str__(self):
        return '{} on {}'.format(self.os, self.device)
