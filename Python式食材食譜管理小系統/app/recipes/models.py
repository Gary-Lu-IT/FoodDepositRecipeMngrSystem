from django.db import models
from core.models import HexIdModel, LabeledMixin, Unit
from pantry.models import Ingredient


class Recipe(HexIdModel, LabeledMixin):
    difficulty = models.IntegerField(default=1) # 1~5
    servings = models.IntegerField(default=1)
    minutes = models.IntegerField(default=20)


class RecipeStep(HexIdModel):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="steps")
    order = models.PositiveIntegerField()
    text = models.TextField()
    class Meta:
        ordering = ["order"]


class RecipeIngredient(HexIdModel):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="ingredients")
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=12, decimal_places=3)
    unit = models.CharField(max_length=8, choices=Unit.choices)
    optional = models.BooleanField(default=False)


class IngredientSubstitute(HexIdModel):
    # A 可以被 B 替代；score 代表相似/替代程度（0~1）
    source = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name="subs_sources")
    target = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name="subs_targets")
    score = models.DecimalField(max_digits=3, decimal_places=2, default=0.7)
    note = models.CharField(max_length=120, blank=True)
    class Meta:
        unique_together = ("source", "target")