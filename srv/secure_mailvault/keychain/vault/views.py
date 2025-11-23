from rest_framework import permissions, viewsets

from vault.models import VaultEntry
from vault.serializers import VaultEntrySerializer


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class VaultEntryViewSet(viewsets.ModelViewSet):
    serializer_class = VaultEntrySerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return VaultEntry.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
