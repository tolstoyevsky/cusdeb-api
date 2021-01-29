"""Module for the admin interface of the application. """

from django.contrib import admin

from .models import EmailConfirmationToken, Person


class HiddenModelAdmin(admin.ModelAdmin):
    """Admin class for all the modules supposed to be hidden in the Django admin. """

    def get_model_perms(self, request):
        """Returns empty permissions dict to hide the target model in the Django admin. """

        return {}


admin.site.register(EmailConfirmationToken, HiddenModelAdmin)
admin.site.register(Person)
