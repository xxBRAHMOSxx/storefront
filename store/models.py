from django.core.validators import MinValueValidator
from django.db import models

# Create your models here.
# the class below inherits the model class


class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()

    # products


class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey(
        "Product", on_delete=models.SET_NULL, null=True, related_name="+", primary_key=False)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = [
            "title"
        ]


class Product(models.Model):
    # now we define the fields
    title = models.CharField(max_length=255)
    # either set slug as nullabe value of set a default value
    slug = models.SlugField()
    description = models.TextField()
    # use decimal field for monetary cases cuz float has rounding issues
    unit_price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(1)])
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    promotions = models.ManyToManyField(Promotion, blank=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = [
            "title"
        ]


class Customer(models.Model):
    MEMBERSHIP_BRONZE = "B"
    MEMBERSHIP_SILVER = "S"
    MEMBERSHIP_GOLD = "G"
    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, "Bronze"),
        (MEMBERSHIP_SILVER, "Silver"),
        (MEMBERSHIP_GOLD, "Gold")
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)

    # phone_number=models.PhoneNumberField()
    phone_number = models.CharField(max_length=50)

    birth_date = models.DateField(
        auto_now=False, auto_now_add=False, null=True)
    membership = models.CharField(
        max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)

    class Meta:
        db_table = "store_customers"
        ordering = ["first_name", "last_name"]
        indexes = [
            models.Index(fields=["last_name", "first_name"])
        ]

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Order(models.Model):
    PAYMENT_PENDING = "P"
    PAYMENT_COMPLETED = "C"
    PAYMENT_FAILED = "F"

    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_PENDING, "Pending"),
        (PAYMENT_COMPLETED, "Completed"),
        (PAYMENT_FAILED, "Failed")
    ]

    placed_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_PENDING)

    customer = models.ForeignKey(Customer,
                                 on_delete=models.PROTECT)


class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)


class Address(models.Model):
    street = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zip = models.CharField(max_length=8)
    # now we need to create a one-to-one relation ship between customer class and address class
    customer = models.OneToOneField(
        Customer, on_delete=models.CASCADE, primary_key=True)


class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)


class Cart_Item(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
