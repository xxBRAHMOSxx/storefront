from typing import Any
from django.contrib import admin, messages
from django.db.models.aggregates import Count
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.utils.html import format_html, urlencode
from django.urls import reverse


from . import models

# Register your models here.
# to know more go to 'django model admin' website in model admin actions


class InventoryFilter(admin.SimpleListFilter):
    title = "inventory"
    parameter_name = "inventory"

    def lookups(self, request, model_admin: Any) -> list[tuple[Any, str]]:
        return [
            ("<10", "low")
        ]

    def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ("title", "products_count")
    search_fields = ["title"]

    @admin.display(ordering="products_count")
    def products_count(self, collection):
        url = (
            reverse("admin:store_product_changelist")
            + "?"  # it marks the beginning os a query string
            + urlencode({
                "collection__id": str(collection.id)
            }))
        return format_html("<a href={}>{} </a>", url,
                           collection.products_count)

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(products_count=Count("product"))


# we can specify ho we wanna view or edit our product with custom class


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):

    autocomplete_fields = ["collection"]
    search_fields = ["products"]
    prepopulated_fields = {
        "slug": ["title"]
    }
    actions = ['clear_inventory']
    list_display = ["title", "unit_price",
                    "inventory_status", "collection_title"]
    list_editable = ["unit_price"]
    list_filter = ["collection", "last_update", InventoryFilter]
    list_per_page = 100

    list_select_related = ["collection"]

    def collection_title(self, product):
        return product.collection.title

    @admin.display(ordering="inventory")
    def inventory_status(self, product):
        if product.inventory < 10:
            return "low"
        return "ok"

    @admin.action(description="Clear Inventory")
    def clear_inventory(self, request, queryset):
        update_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{update_count} products count were successfully updated'
        )


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "membership", "orders"]
    list_editable = ["membership"]
    list_per_page = 100
    search_fields = ["first_name__istartswith", "last_name__istartswith"]
    ordering = ["first_name", "last_name"]

    @admin.display(ordering="order_count")
    def orders(self, customers):
        url = (reverse("admin:store_order_changelist")
               + "?"
               + urlencode({
                   "order__id": str(customers.id)
               }))
        return format_html("<a href={}>{} </a>", url,
                           customers.order_count)

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(order_count=Count("order"))


class OrderItemsInline(admin.StackedInline):
    autocomplete_fields = ["product"]
    model = models.OrderItems
    extra = 0
    min_num = 1
    max_num = 10


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ["customer"]
    inlines = [OrderItemsInline]
    list_display = ["id", "customer", "placed_at", "payment_status"]
    list_editable = ["payment_status"]
    list_per_page = 100
    ordering = ["payment_status"]
