from rest_framework import serializers

from crypto_utils import decrypt_data, encrypt_data, load_encryption_key
from vault.models import VaultEntry


class VaultEntrySerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)
    note = serializers.CharField(write_only=True, required=False, allow_blank=True)
    password_decrypted = serializers.SerializerMethodField()
    note_decrypted = serializers.SerializerMethodField()

    class Meta:
        model = VaultEntry
        fields = [
            "id",
            "owner",
            "label",
            "username",
            "password_encrypted",
            "note_encrypted",
            "password",
            "note",
            "password_decrypted",
            "note_decrypted",
            "date_created",
            "date_modified",
        ]
        read_only_fields = [
            "id",
            "owner",
            "password_encrypted",
            "note_encrypted",
            "password_decrypted",
            "note_decrypted",
            "date_created",
            "date_modified",
        ]

    def _apply_encryption(self, validated_data):
        """Encrypt cleartext payloads and remove non-model fields."""
        key = load_encryption_key()
        if "password" in validated_data:
            password = validated_data.pop("password", "")
            validated_data["password_encrypted"] = encrypt_data(password, key)
        if "note" in validated_data:
            note = validated_data.pop("note", "")
            validated_data["note_encrypted"] = encrypt_data(note, key)
        return validated_data

    def create(self, validated_data):
        validated_data.setdefault("password", "")
        validated_data.setdefault("note", "")
        validated_data["owner"] = self.context["request"].user
        self._apply_encryption(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Only encrypt when password or note are provided in the update payload
        if "password" in validated_data or "note" in validated_data:
            self._apply_encryption(validated_data)
        return super().update(instance, validated_data)

    def get_password_decrypted(self, obj: VaultEntry) -> str:
        return decrypt_data(obj.password_encrypted)

    def get_note_decrypted(self, obj: VaultEntry) -> str:
        return decrypt_data(obj.note_encrypted)
