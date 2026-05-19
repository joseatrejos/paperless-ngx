import logging

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.viewsets import ReadOnlyModelViewSet

from documents.permissions import PaperlessAdminPermissions
from paperless.views import StandardPagination
from paperless_documenso.models import DocumensoGroupLink
from paperless_documenso.models import DocumensoUserSync
from paperless_documenso.serialisers import DocumensoGroupLinkSerializer
from paperless_documenso.serialisers import DocumensoUserSyncSerializer
from paperless_documenso.tasks import sync_all_group_users

logger = logging.getLogger("paperless.documenso.views")


class DocumensoGroupLinkViewSet(ModelViewSet):
    queryset = DocumensoGroupLink.objects.select_related("group").order_by(
        "group__name"
    )
    serializer_class = DocumensoGroupLinkSerializer
    pagination_class = StandardPagination
    permission_classes = (IsAuthenticated, PaperlessAdminPermissions)
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ["group"]
    ordering_fields = ("group__name",)

    @action(detail=False, methods=["get"], url_path="my-teams", permission_classes=[IsAuthenticated])
    def my_teams(self, request):
        """
        Returns the DocumensoGroupLinks for the groups the current user belongs to
        that have a configured team token. Used to allow the user to select which
        team to send a document to when they belong to multiple Documenso groups.
        """
        links = DocumensoGroupLink.objects.filter(
            group__user=request.user,
            documenso_team_token__gt="",
        ).select_related("group").order_by("group__name")
        serializer = self.get_serializer(links, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], url_path="sync")
    def trigger_sync(self, request, pk=None):
        """
        Triggers a bulk synchronisation of all users in the group to Documenso
        asynchronously.
        """
        group_link = self.get_object()
        if not group_link.is_configured:
            return Response(
                {"detail": "Este grupo no tiene nombre de organización Documenso configurado."},
                status=400,
            )
        sync_all_group_users.delay(group_link.pk)
        return Response(
            {
                "detail": f"Sincronización iniciada para el grupo '{group_link.group.name}'."
            }
        )


class DocumensoUserSyncViewSet(ReadOnlyModelViewSet):
    queryset = DocumensoUserSync.objects.select_related(
        "user", "group_link", "group_link__group"
    ).order_by("user__username")
    serializer_class = DocumensoUserSyncSerializer
    pagination_class = StandardPagination
    permission_classes = (IsAuthenticated, PaperlessAdminPermissions)
    filter_backends = (OrderingFilter,)
    ordering_fields = ("user__username", "synced", "synced_at")
