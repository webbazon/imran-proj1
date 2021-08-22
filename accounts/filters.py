from django.db.models.fields import IntegerField
import django_filters
from django_filters import DateFilter
from .models import *
from .forms import *


class CustomerFilter(django_filters.FilterSet):
    class Meta:
        model = Customer
        fields = ['customer_city']


class VendorFilter(django_filters.FilterSet):
    class Meta:
        model = Vendor
        fields = ['vendor_city']


class OrderFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(widget=DateTypeInput(attrs={'placeholder': 'dd/mm/yyyy'}), field_name='order_date',
                                           lookup_expr='gte', label="Start Date")
    end_date = django_filters.DateFilter(widget=DateTypeInput(attrs={'placeholder': 'dd/mm/yyyy'}), field_name='order_date',
                                         lookup_expr='lte', label="End Date")

    class Meta:
        model = Order
        fields = []


class GeneralExpenseFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(widget=DateTypeInput(attrs={'placeholder': 'dd/mm/yyyy'}), field_name='expense_date',
                                           lookup_expr='gte', label="Start Date")
    end_date = django_filters.DateFilter(widget=DateTypeInput(attrs={'placeholder': 'dd/mm/yyyy'}), field_name='expense_date',
                                         lookup_expr='lte', label="End Date")

    class Meta:
        model = GeneralExpense
        fields = []


class OrderExpenseFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(widget=DateTypeInput(attrs={'placeholder': 'dd/mm/yyyy'}), field_name='expense_date',
                                           lookup_expr='gte', label="Start Date")
    end_date = django_filters.DateFilter(widget=DateTypeInput(attrs={'placeholder': 'dd/mm/yyyy'}), field_name='expense_date',
                                         lookup_expr='lte', label="End Date")

    class Meta:
        model = OrderExpense
        fields = []


class PaymentReceiptFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(
        widget=DateTypeInput(attrs={'placeholder': 'dd/mm/yyyy'}), field_name='payment_received_date', lookup_expr='gte', label="Start Date")
    end_date = django_filters.DateFilter(widget=DateTypeInput(
        attrs={'placeholder': 'dd/mm/yyyy'}), field_name='payment_received_date', lookup_expr='lte', label="End Date")

    class Meta:
        model = PaymentReceipt
        fields = []
