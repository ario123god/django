from django.contrib.auth import get_user_model
from django.db import models

from crypto_utils import decrypt_data

User = get_user_model()


class VaultEntry(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    label = models.CharField(max_length=255)
    username = models.CharField(max_length=255, blank=True)
    password_encrypted = models.BinaryField()
    note_encrypted = models.BinaryField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Vault entry"
        verbose_name_plural = "Vault entries"
        ordering = ["-date_modified"]

    def __str__(self) -> str:  # pragma: no cover - human-readable
        return f"{self.label} ({self.owner})"

    @property
    def password_plaintext(self) -> str:
        return decrypt_data(self.password_encrypted)

    @property
    def note_plaintext(self) -> str:
        return decrypt_data(self.note_encrypted)
