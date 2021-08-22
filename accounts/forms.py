from django import forms
from django.forms import ModelForm
from .models import *


class CustomerCityForm(ModelForm):
    class Meta:
        model = CustomerCity
        fields = '__all__'


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'


class DeliveryStatusForm(ModelForm):
    class Meta:
        model = DeliveryStatus
        fields = '__all__'


class PaymentTermForm(ModelForm):
    class Meta:
        model = PaymentTerm
        fields = '__all__'


class PaymentStatusForm(ModelForm):
    class Meta:
        model = PaymentStatus
        fields = '__all__'


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        widgets = {
            'order_date': forms.DateInput(attrs={'placeholder': 'dd/mm/yyyy'}),
            'description': forms.TextInput(attrs={'placeholder': 'Details of Products/ Services in Order'}),
            'due_date': forms.DateInput(attrs={'placeholder': 'dd/mm/yyyy'}),
        }


class PaymentModeForm(ModelForm):
    class Meta:
        model = PaymentMode
        fields = '__all__'


class PaymentReceiptForm(ModelForm):
    class Meta:
        model = PaymentReceipt
        fields = '__all__'
        widgets = {
            'payment_received_date': forms.DateInput(attrs={'placeholder': 'dd/mm/yyyy'}),
        }


class EmployeeNameForm(ModelForm):
    class Meta:
        model = EmployeeName
        fields = '__all__'


class OrderExpenseCategoryForm(ModelForm):
    class Meta:
        model = OrderExpenseCategory
        fields = '__all__'


class OrderExpenseModeForm(ModelForm):
    class Meta:
        model = OrderExpenseMode
        fields = '__all__'


class VendorCityForm(ModelForm):
    class Meta:
        model = VendorCity
        fields = '__all__'


class VendorForm(ModelForm):
    class Meta:
        model = Vendor
        fields = '__all__'


class OrderExpenseForm(ModelForm):
    class Meta:
        model = OrderExpense
        fields = '__all__'
        widgets = {
            'expense_date': forms.DateInput(attrs={'placeholder': 'dd/mm/yyyy'}),
        }


class GeneralExpenseCategoryForm(ModelForm):
    class Meta:
        model = GeneralExpenseCategory
        fields = '__all__'


class GeneralExpenseModeForm(ModelForm):
    class Meta:
        model = GeneralExpenseMode
        fields = '__all__'


class GeneralExpenseForm(ModelForm):
    class Meta:
        model = GeneralExpense
        fields = '__all__'
        widgets = {
            'expense_date': forms.DateInput(attrs={'placeholder': 'dd/mm/yyyy'}),
        }


class DateTypeInput(forms.DateInput):
    input_type = 'date'
