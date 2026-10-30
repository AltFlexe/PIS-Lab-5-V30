from django.contrib import admin
from .models import Article, Space, Tenant, Contract, ContractSpace, Payment


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'get_excerpt', 'created_date')


@admin.register(Space)
class SpaceAdmin(admin.ModelAdmin):
    list_display = ('number', 'floor', 'area', 'air_conditioner', 'daily_price')


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'contact')


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('number', 'tenant', 'signed_date')


@admin.register(ContractSpace)
class ContractSpaceAdmin(admin.ModelAdmin):
    list_display = ('contract', 'space', 'start_date', 'end_date')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('contract', 'month', 'paid_date', 'amount')
