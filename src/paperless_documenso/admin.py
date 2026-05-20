from django.contrib import admin

from paperless_documenso.models import DocumensoGroupLink
from paperless_documenso.models import DocumensoUserSync


@admin.register(DocumensoGroupLink)
class DocumensoGroupLinkAdmin(admin.ModelAdmin):
    list_display = ("group", "is_configured")
    search_fields = ("group__name",)


@admin.register(DocumensoUserSync)
class DocumensoUserSyncAdmin(admin.ModelAdmin):
    list_display = ("user", "group_link", "synced", "email_sent", "synced_at")
    list_filter = ("synced", "email_sent")
    search_fields = ("user__username", "user__email")
    readonly_fields = ("synced_at",)
