from django.contrib import admin

from vault.models import VaultEntry


@admin.register(VaultEntry)
class VaultEntryAdmin(admin.ModelAdmin):
    list_display = ("label", "owner", "date_modified")
    search_fields = ("label", "owner__username", "owner__email")
    readonly_fields = ("password_encrypted", "note_encrypted", "date_created", "date_modified")
