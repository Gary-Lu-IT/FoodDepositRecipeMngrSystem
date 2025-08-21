from django.db import models
from core.models import HexIdModel
from recipes.models import Recipe


class MealPlan(HexIdModel):
    title = models.CharField(max_length=120)
    start_date = models.DateField()
    end_date = models.DateField()


class MealPlanItem(HexIdModel):
    plan = models.ForeignKey(MealPlan, on_delete=models.CASCADE, related_name="items")
    date = models.DateField()
    recipe = models.ForeignKey(Recipe, on_delete=models.PROTECT)
    servings = models.IntegerField(default=1)


class ShoppingList(HexIdModel):
    plan = models.ForeignKey(MealPlan, on_delete=models.SET_NULL, null=True, blank=True)
    created_from = models.CharField(max_length=60, blank=True) # 任務來源標註
    is_completed = models.BooleanField(default=False)


class ShoppingListItem(HexIdModel):
    list = models.ForeignKey(ShoppingList, on_delete=models.CASCADE, related_name="items")
    ingredient_name = models.CharField(max_length=120) # 預留自由輸入
    ingredient = models.ForeignKey("pantry.Ingredient", on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.DecimalField(max_digits=12, decimal_places=3)
    unit = models.CharField(max_length=8)
    fulfilled = models.BooleanField(default=False)
