from rest_framework import serializers

from paperless_documenso.models import DocumensoGroupLink
from paperless_documenso.models import DocumensoUserSync


class DocumensoGroupLinkSerializer(serializers.ModelSerializer):
    documenso_org_name = serializers.CharField(required=False, allow_blank=True)
    group_name = serializers.CharField(source="group.name", read_only=True)
    is_configured = serializers.BooleanField(read_only=True)
    has_token = serializers.SerializerMethodField()

    def get_has_token(self, obj):
        return bool(obj.documenso_team_token)

    class Meta:
        model = DocumensoGroupLink
        fields = [
            "id",
            "group",
            "group_name",
            "documenso_org_name",
            "is_configured",
            "has_token",
        ]


class DocumensoUserSyncSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.CharField(source="user.email", read_only=True)
    group_name = serializers.CharField(
        source="group_link.group.name", read_only=True
    )

    class Meta:
        model = DocumensoUserSync
        fields = [
            "id",
            "user",
            "username",
            "email",
            "group_link",
            "group_name",
            "synced",
            "synced_at",
        ]
        read_only_fields = ["synced", "synced_at"]

