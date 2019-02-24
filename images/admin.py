from django.contrib import admin

from .models import (BuildType, BuildTypeName, CodeName, Device, DeviceName,
                     DistroName, Image, OS, Port)


class HiddenModelAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}


admin.site.register(BuildType)
admin.site.register(BuildTypeName, HiddenModelAdmin)
admin.site.register(CodeName, HiddenModelAdmin)
admin.site.register(Device)
admin.site.register(DeviceName, HiddenModelAdmin)
admin.site.register(DistroName, HiddenModelAdmin)
admin.site.register(Image)
admin.site.register(OS)
admin.site.register(Port, HiddenModelAdmin)
