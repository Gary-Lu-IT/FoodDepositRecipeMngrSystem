from django.db import models
from core.models import HexIdModel
from pantry.models import Ingredient


class Vendor(HexIdModel):
    name = models.CharField(max_length=120, db_index=True) # 全聯/家樂福/某市場攤商
    address = models.CharField(max_length=200, blank=True)
    note = models.CharField(max_length=200, blank=True)


class Purchase(HexIdModel):
    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT)
    bought_at = models.DateTimeField()
    total_cost = models.DecimalField(max_digits=12, decimal_places=2)


class PurchaseItem(HexIdModel):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name="items")
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.DecimalField(max_digits=12, decimal_places=3)
    unit = models.CharField(max_length=8)
    batch = models.OneToOneField("pantry.InventoryBatch", on_delete=models.PROTECT, related_name="from_purchase", null=True, blank=True)


class PriceSample(HexIdModel):
    # 不一定等同於一次實際購買，用於長期價格追蹤
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    unit = models.CharField(max_length=8)
    sampled_at = models.DateTimeField(db_index=True)
    class Meta:
        indexes = [models.Index(fields=["ingredient", "vendor", "sampled_at"])]
