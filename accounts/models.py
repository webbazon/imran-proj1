from django.db import models
from django.db.models.fields import CharField, related
from django.db.models.fields.related import ForeignKey

# Create your models here.
class CustomerCity(models.Model):
    customer_city = models.CharField(max_length=30, unique=True)

    class Meta:
        verbose_name_plural = 'Customer Cities'
        ordering = ('customer_city',)
    
    def __str__(self):
        return str(self.customer_city)



class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    customer = models.CharField(max_length=60)
    customer_address = models.CharField(max_length=255, default='No Record')
    customer_city = models.ForeignKey(CustomerCity, null=True, on_delete=models.SET_NULL, related_name='customers')
    contact_person = models.CharField(max_length=30, default='No Record')
    designation = models.CharField(max_length=30, default='No Record')
    email = models.CharField(max_length=40, default='No Record')
    phone = models.CharField(max_length=20, default='No Record')

    class Meta:
        ordering = ('customer',)
    
    def __str__(self):
        return str(self.customer)




class DeliveryStatus(models.Model):
    delivery_status = models.CharField(max_length=25)

    class Meta:
        verbose_name_plural = 'Status of Deliveries'
        ordering = ('delivery_status',)
    
    def __str__(self):
        return str(self.delivery_status)




class PaymentTerm(models.Model):
    payment_terms = models.CharField(max_length=20)

    class Meta:
        verbose_name_plural = 'Terms of Payment'
        ordering = ('payment_terms',)
    
    def __str__(self):
        return str(self.payment_terms)




class PaymentStatus(models.Model):
    payment_status = models.CharField(max_length=25)

    class Meta:
        verbose_name_plural = 'Status of Payments'
        ordering = ('payment_status',)
    
    def __str__(self):
        return str(self.payment_status)




class Order(models.Model):
    order_ref = models.AutoField(primary_key=True)
    order_date = models.DateField()
    value = models.FloatField(default=0.00)
    description = models.CharField(max_length=255)
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL, related_name='orders')
    customer_city = models.ForeignKey(CustomerCity, null=True, on_delete=models.SET_NULL, related_name='orders_city')
    due_date = models.DateField(blank=True, null=True)
    delivery_status = ForeignKey(DeliveryStatus, null=True, on_delete=models.SET_NULL, related_name='orders_delivery_status')
    invoice_details = models.CharField(max_length=255, blank=True, null=True)
    payment_terms = ForeignKey(PaymentTerm, null=True, on_delete=models.SET_NULL, related_name='orders_payment_terms')
    payment_status = ForeignKey(PaymentStatus, null=True, on_delete=models.SET_NULL, related_name='orders_payment_status')
    order_notes = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ('-order_ref',)
    
    def __str__(self):
        return str(self.order_ref)




class PaymentMode(models.Model):
    payment_mode = models.CharField(max_length=20)

    class Meta:
        verbose_name_plural = 'Received Payment Modes'
        ordering = ('payment_mode',)
    
    def __str__(self):
        return str(self.payment_mode)




class PaymentReceipt(models.Model):
    payment_received_date = models.DateField()
    received_amount = models.FloatField(default=0.00)
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL, related_name='paid_by')
    order_ref = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL, related_name='payments')
    invoice_ref = models.CharField(max_length=15, blank=True, null=True)
    payment_mode = models.ForeignKey(PaymentMode, null=True, on_delete=models.SET_NULL, related_name='payment_receive_mode')
    notes_or_remarks = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Received Payments'
        ordering = ('-payment_received_date',)
    
    def __str__(self):
        return str(self.payment_received_date)




class EmployeeName(models.Model):
    employee_name = models.CharField(max_length=60)
    designation = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = 'Employee Names'
        ordering = ('employee_name',)

    def __str__(self):
        return str(self.employee_name)




class OrderExpenseCategory(models.Model):
    order_expense_category = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = 'Expense Categories - Orders'
        ordering = ('order_expense_category',)

    def __str__(self):
        return str(self.order_expense_category)




class OrderExpenseMode(models.Model):
    order_expense_mode = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = 'Expense Modes - Orders'
        ordering = ('order_expense_mode',)

    def __str__(self):
        return str(self.order_expense_mode)




class VendorCity(models.Model):
    vendor_city = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = 'Vendor Cities'
        ordering = ('vendor_city',)

    def __str__(self):
        return str(self.vendor_city)




class Vendor(models.Model):
    vendor_id = models.AutoField(primary_key=True)
    vendor = models.CharField(max_length=60)
    vendor_address = models.CharField(max_length=255, blank=True, null=True)
    vendor_city = models.ForeignKey(VendorCity, null=True, on_delete=models.SET_NULL, related_name='vendors')
    contact_person = models.CharField(max_length=60, default='No Record')
    designation = models.CharField(max_length=30, default='No Record')
    email = models.CharField(max_length=30, default='No Record')
    phone = models.CharField(max_length=15, default='No Record')
    products_or_services = models.CharField(max_length=255, blank=True, null=True)
    notes_or_remarks = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ('vendor',)
    
    def __str__(self):
        return str(self.vendor)






class OrderExpense(models.Model):
    expense_date = models.DateField()
    expense_amount = models.FloatField(default = 0.00)
    expense_made_by = models.ForeignKey(EmployeeName, null=True, on_delete = models.SET_NULL, related_name = 'expense_by')
    expense_mode = models.ForeignKey(OrderExpenseMode, null=True, on_delete = models.SET_NULL, related_name='orders_expense_mode')
    order_ref = models.ForeignKey(Order, null=True, on_delete = models.SET_NULL, related_name = 'expenses')
    expense_category = models.ForeignKey(OrderExpenseCategory, null=True, on_delete = models.SET_NULL, related_name='orders_expense_category')
    description = models.CharField(max_length = 255, blank = True, null = True)
    vendor = models.ForeignKey(Vendor, null=True, on_delete = models.SET_NULL, related_name = 'paid_to')
    notes_or_remarks = models.CharField(max_length = 255, blank = True, null = True)

    class Meta:
        verbose_name_plural = 'Expenses - Orders'
        ordering = ('-expense_date',)
    
    def __str__(self):
        return str(self.expense_date)




class GeneralExpenseCategory(models.Model):
    general_expense_category = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = 'Expense Categories - General'
        ordering = ('general_expense_category',)

    def __str__(self):
        return str(self.general_expense_category)




class GeneralExpenseMode(models.Model):
    expense_mode = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = 'Expense Modes - General'
        ordering = ('expense_mode',)

    def __str__(self):
        return str(self.expense_mode)




class GeneralExpense(models.Model):
    expense_date = models.DateField()
    expense_amount = models.FloatField(default = 0.00)
    expense_made_by = models.ForeignKey(EmployeeName, null=True, on_delete=models.SET_NULL, related_name='spent_by')
    expense_mode = models.ForeignKey(GeneralExpenseMode, null=True, on_delete=models.SET_NULL, related_name='general_expense_mode')
    expense_category = models.ForeignKey(GeneralExpenseCategory, null=True, on_delete=models.SET_NULL, related_name='gen_expense_category')
    description = models.CharField(max_length = 255, blank = True, null = True)
    notes_or_remarks = models.CharField(max_length = 255, blank = True, null = True)

    class Meta:
        verbose_name_plural = 'Expenses - General'
        ordering = ('-expense_date',)
    
    def __str__(self):
        return str(self.expense_date)

