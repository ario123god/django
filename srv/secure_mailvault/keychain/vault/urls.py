from rest_framework.routers import DefaultRouter

from vault.views import VaultEntryViewSet

router = DefaultRouter()
router.register(r"vault-entries", VaultEntryViewSet, basename="vaultentry")

urlpatterns = router.urls
