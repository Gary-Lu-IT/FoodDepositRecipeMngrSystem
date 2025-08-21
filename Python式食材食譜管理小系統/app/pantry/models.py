# pantry/models.py
from django.db import models
from core.models import HexIdModel, Unit, LabeledMixin


class StorageLocation(HexIdModel, LabeledMixin):
    # �ҡG�N��ǡB�N�ëǡB�`���d
    path = models.CharField(max_length=120, blank=True)


class Ingredient(HexIdModel, LabeledMixin):
    category = models.CharField(max_length=60, db_index=True) # ����/����/�\��/�ը��K
    default_unit = models.CharField(max_length=8, choices=Unit.choices)
    min_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0) # �w���w�s�u
    is_active = models.BooleanField(default=True)


class InventoryBatch(HexIdModel):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT, related_name="batches")
    location = models.ForeignKey(StorageLocation, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=12, decimal_places=3)
    unit = models.CharField(max_length=8, choices=Unit.choices)
    expiry_date = models.DateField(null=True, blank=True)
    cost_per_unit = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    note = models.CharField(max_length=200, blank=True)
    class Meta:
        indexes = [models.Index(fields=["expiry_date"]), models.Index(fields=["ingredient"]) ]


class StockTxType(models.TextChoices):
    IN = "IN", "�J�w"
    OUT = "OUT", "�X�w"
    ADJ = "ADJ", "�վ�"


class StockTransaction(HexIdModel):
    batch = models.ForeignKey(InventoryBatch, on_delete=models.PROTECT, related_name="transactions")
    tx_type = models.CharField(max_length=3, choices=StockTxType.choices)
    quantity = models.DecimalField(max_digits=12, decimal_places=3)
    unit = models.CharField(max_length=8, choices=Unit.choices)
    reason = models.CharField(max_length=120, blank=True) # �ҡG�i�ծ���/���o/�L�I
