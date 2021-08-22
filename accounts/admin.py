from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(CustomerCity)


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_id', 'customer', 'customer_city')
    list_display_links = ('customer_id', 'customer', 'customer_city')
    list_filter = ('customer_city',)
    search_fields = ('customer_id', 'customer', 'city__customer_city',
                     'contact_person', 'designation', 'email', 'phone')


admin.site.register(Customer, CustomerAdmin)


admin.site.register(DeliveryStatus)
admin.site.register(PaymentTerm)
admin.site.register(PaymentStatus)


class PaymentReceiptInline(admin.StackedInline):
    model = PaymentReceipt
    extra = 1


class OrderExpenseInline(admin.StackedInline):
    model = OrderExpense
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_ref', 'order_date', 'value', 'customer',
                    'customer_city', 'delivery_status', 'payment_status')
    list_display_links = ('order_ref', 'order_date', 'value',
                          'customer', 'customer_city', 'payment_status')
    list_filter = ('customer_city', 'delivery_status', 'payment_status')
    search_fields = ('order_ref', 'order_date', 'value', 'customer', 'customer_city',
                     'delivery_status', 'payment_status', 'invoice_details', 'order_notes')
    list_editable = ('delivery_status',)
    inlines = [PaymentReceiptInline, OrderExpenseInline]


admin.site.register(Order, OrderAdmin)


admin.site.register(PaymentMode)
admin.site.register(PaymentReceipt)


class EmployeeNameAdmin(admin.ModelAdmin):
    list_display = ('employee_name', 'designation')
    list_display_links = ('employee_name', 'designation')
    list_filter = ('designation',)


admin.site.register(EmployeeName, EmployeeNameAdmin)
admin.site.register(OrderExpenseCategory)
admin.site.register(OrderExpenseMode)
admin.site.register(VendorCity)


class VendorAdmin(admin.ModelAdmin):
    list_display = ('vendor_id', 'vendor', 'vendor_city')
    list_display_links = ('vendor_id', 'vendor', 'vendor_city')
    list_filter = ('vendor_city',)
    search_fields = ('vendor_id', 'vendor', 'vendor_city', 'vendor_address',
                     'contact_person', 'email', 'phone', 'products_or_services', 'notes_or_remarks')


admin.site.register(Vendor, VendorAdmin)


class OrderExpenseAdmin(admin.ModelAdmin):
    list_display = ('expense_date', 'order_ref', 'expense_amount',
                    'expense_made_by', 'expense_mode', 'expense_category', 'vendor')
    list_display_links = ('expense_date', 'order_ref', 'expense_amount',
                          'expense_made_by', 'expense_mode', 'expense_category', 'vendor')
    list_filter = ('expense_made_by', 'expense_mode', 'expense_category')
    search_fields = ('expense_date', 'order_ref', 'expense_amount',
                     'expense_made_by', 'expense_mode', 'expense_category', 'vendor')


admin.site.register(OrderExpense, OrderExpenseAdmin)


admin.site.register(GeneralExpenseCategory)
admin.site.register(GeneralExpenseMode)


class GeneralExpenseAdmin(admin.ModelAdmin):
    list_display = ('expense_date', 'expense_amount',
                    'expense_made_by', 'expense_mode', 'expense_category')
    list_display_links = ('expense_date',  'expense_amount',
                          'expense_made_by', 'expense_mode', 'expense_category')
    list_filter = ('expense_made_by', 'expense_mode', 'expense_category')
    search_fields = ('expense_date',  'expense_amount',
                     'expense_made_by', 'expense_mode', 'expense_category')


admin.site.register(GeneralExpense, GeneralExpenseAdmin)
