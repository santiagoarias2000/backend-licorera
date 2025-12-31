from django.db import models
from datetime import date


class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, db_index=True)
    email = models.EmailField(unique=True, db_index=True)
    password = models.CharField(max_length=128)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True, db_index=True)

    def __str__(self):
        return f"{self.name} ({self.email})"
    
    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['email']),
            models.Index(fields=['active']),
        ]


class Customer(models.Model):
    DOCUMENT_TYPE_CHOICES = [
        ('CC', 'Cédula de ciudadanía'),
        ('TI', 'Tarjeta de identidad'),
        ('CE', 'Cédula de extranjería'),
        ('PAS', 'Pasaporte'),
        ('NIT', 'NIT'),
    ]

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, db_index=True)
    document_type = models.CharField(max_length=10, choices=DOCUMENT_TYPE_CHOICES)
    document_number = models.CharField(max_length=20, unique=True)
    birthdate = models.DateField()
    address = models.CharField(max_length=150)
    entry_date = models.DateField(default=date.today)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    delivered = models.BooleanField(default=False, db_index=True)

    def __str__(self):
        return f"{self.name} ({self.document_type} {self.document_number})"

    class Meta:
        indexes = [
            models.Index(fields=['delivered']),
            models.Index(fields=['name']),
        ]


class Product(models.Model):
        
    CATEGORY_CHOICES = [
        ('CERVEZAS', 'CERVEZAS'),
        ('CIGARILLOS', 'CIGARILLOS'),
        ('GOLOSINAS', 'GOLOSIONAS'),
        ('LICORES', 'LICORES'),
        ('OTROS', 'OTROS'),
    ]

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, db_index=True)
    otros = models.CharField(max_length=100, db_index=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, db_index=True)
    stock = models.PositiveIntegerField(default=0)
    imagen = models.TextField(blank=True, null=True)
    size = models.CharField(max_length=20, blank=True, null=True)
    active = models.BooleanField(default=True, db_index=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=['price']),
            models.Index(fields=['name']),
            models.Index(fields=['otros']),
            models.Index(fields=['category']),
            models.Index(fields=['active']),
        ]


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('EFECTIVO', 'Efectivo'),
        ('TARJETA', 'Tarjeta'),
        ('TRANSFERENCIA', 'Transferencia'),
        ('OTRO', 'Otro'),
    ]

    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='payments')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False, db_index=True)

    def __str__(self):
        return f"Payment {self.id} - {self.payment_method} - ${self.amount}"

    class Meta:
        indexes = [
            models.Index(fields=['customer']),
            models.Index(fields=['product']),
            models.Index(fields=['payment_method']),
            models.Index(fields=['paid']),
        ]