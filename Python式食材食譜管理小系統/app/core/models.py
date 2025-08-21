import secrets
from django.db import models, IntegrityError, transaction
from django.core.validators import RegexValidator


HEX19_VALIDATOR = RegexValidator(
    regex=r"^[0-9a-fA-F]{4}(-[0-9a-fA-F]{4}){3}$",
    message="ID must be like XXXX-XXXX-XXXX-XXXX (hex segments)."
)


class HexIdModel(models.Model):
    """��H�򩳡G�H�ۭq 8-byte hex ���qID���D��C"""
    id = models.CharField(
        primary_key=True,
        max_length=19,
        validators=[HEX19_VALIDATOR],
        editable=False,)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

        @staticmethod
        def new_hex19() -> str:
            h = secrets.token_hex(8) # 16 hex chars
            return f"{h[0:4]}-{h[4:8]}-{h[8:12]}-{h[12:16]}"

        def save(self, *args, **kwargs):
            if not self.id:
                # �C���v�I���A�O�I����
                for _ in range(5):
                    candidate = self.new_hex19()
                    try:
                        with transaction.atomic():
                            self.id = candidate
                            return super().save(*args, **kwargs)
                    except IntegrityError:
                        continue
                raise IntegrityError("Failed to generate unique hex19 id after retries")
            return super().save(*args, **kwargs)

class Unit(models.TextChoices):
    G = "g", "�J"
    KG = "kg", "����"
    ML = "ml", "�@��"
    L = "l", "����"
    PC = "pc", "��/��"


class Tag(HexIdModel):
    name = models.CharField(max_length=50, unique=True)


class LabeledMixin(models.Model):
    name = models.CharField(max_length=120, db_index=True)
    description = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    class Meta:
        abstract = True