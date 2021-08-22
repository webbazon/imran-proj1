from django.contrib import auth
from django.http.response import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import *
from django.db.models import Sum, Count, Min, Max
from .forms import *
from .filters import *
import datetime
from datetime import timedelta
from django.contrib.auth.decorators import login_required


# Create your views here.

def error_404_view(request, exception):
    return render(request, 'accounts/error-404.html')



def login_page(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.info(request, 'Incorret username or password. Please try again.')
                return render(request, 'accounts/login.html')

        return render(request, 'accounts/login.html')





def logout_user(request):
    logout(request)
    return redirect('login')



@login_required(login_url='login')
def index_bkp(request):
    customers_count = Customer.objects.all().count()
    orders_count = Order.objects.all().count()
    orders_sum = Order.objects.all().aggregate(Sum('value'))['value__sum']
    average_order_value = orders_sum / orders_count
    
    orders_expenses = OrderExpense.objects.all().aggregate(Sum('expense_amount'))['expense_amount__sum']
    gross_profit = orders_sum - orders_expenses
    gross_profit_percentage = (gross_profit / orders_sum) * 100
    other_expenses = GeneralExpense.objects.all().aggregate(Sum('expense_amount'))['expense_amount__sum']
    net_profit = gross_profit - other_expenses
    net_profit_percentage = (net_profit / orders_sum) * 100
    

    customers_ninety = Customer.objects.filter(orders__order_date__gte=datetime.datetime.now()-timedelta(days=90)).annotate(orders_count=Count('orders'), orders_sum=Sum('orders__value')).order_by('-orders_sum')[:5]
    customers_top_five = Customer.objects.annotate(orders_count=Count('orders'), orders_sum=Sum('orders__value')).order_by('-orders_sum')[:5]
    customer_labels = []
    customer_data = []
    for customer in customers_ninety:
        customer_labels.append(customer.customer)
        if customer.orders_sum is not None:
            customer_data.append(customer.orders_sum)
        else:
            customer_data.append(0.00)
    
    cities_top_five = CustomerCity.objects.annotate(ord_count=Count('orders_city'), ord_sum=Sum('orders_city__value')).order_by('-ord_sum')[:5]
    city_labels = []
    city_data = []
    for city in cities_top_five:
        city_labels.append(city.customer_city)
        if city.ord_sum is not None:
            city_data.append(city.ord_sum)
        else:
            city_data.append(0.00)
    
    deliveries_status = DeliveryStatus.objects.annotate(del_stat_count=Count('orders_delivery_status'), del_stat_sum=Sum('orders_delivery_status__value')).order_by('-del_stat_count')
    delivery_labels = []
    delivery_data = []
    for status in deliveries_status:
        delivery_labels.append(status.delivery_status)
        if status.del_stat_sum is not None:
            delivery_data.append(status.del_stat_sum)
        else:
            delivery_data.append(0.00)
    
    payments_status = PaymentStatus.objects.annotate(pay_stat_count=Count('orders_payment_status'), pay_stat_sum=Sum('orders_payment_status__value')).order_by('-pay_stat_count')
    payment_labels = []
    payment_data = []
    for status in payments_status:
        payment_labels.append(status.payment_status)
        if status.pay_stat_sum is not None:
            payment_data.append(status.pay_stat_sum)
        else:
            payment_data.append(0.00)

    context = {
        'customers_count': customers_count,
        'orders_count': orders_count,
        'orders_sum': orders_sum,
        'average_order_value': average_order_value,
        'orders_expenses': orders_expenses,
        'gross_profit': gross_profit,
        'gross_profit_percentage': gross_profit_percentage, 
        'other_expenses': other_expenses,
        'net_profit': net_profit,
        'net_profit_percentage': net_profit_percentage,
        'customers_ninety': customers_ninety,
        'customers_top_five': customers_top_five,
        'customer_labels': customer_labels,
        'customer_data': customer_data,
        'cities_top_five': cities_top_five,
        'city_labels': city_labels,
        'city_data': city_data,
        'deliveries_status': deliveries_status,
        'delivery_labels': delivery_labels,
        'delivery_data': delivery_data,
        'payments_status': payments_status,
        'payment_labels': payment_labels,
        'payment_data': payment_data,
    }
    return render(request, 'accounts/index-bkp.html', context)



@login_required(login_url='login')
def index(request):
    
    range = 'All Time'
    customers_count = Customer.objects.all().count()
    orders_count = Order.objects.all().count()
    orders_sum = Order.objects.all().aggregate(Sum('value'))['value__sum']
    if orders_count is not None and orders_sum is not None:
        average_order_value = orders_sum / orders_count
    else:
        average_order_value = 0.00
    
    orders_expenses = OrderExpense.objects.all().aggregate(Sum('expense_amount'))['expense_amount__sum']
    if orders_sum is None:
        orders_sum = 0.00
    if orders_expenses is None:
        orders_expenses = 0.00

    gross_profit = orders_sum - orders_expenses
    if orders_sum == 0.00:
        gross_profit_percentage = 0.00
    else:
        gross_profit_percentage = (gross_profit / orders_sum) * 100
    
    other_expenses = GeneralExpense.objects.all().aggregate(Sum('expense_amount'))['expense_amount__sum']
    if other_expenses is None:
        other_expenses = 0.00
    net_profit = gross_profit - other_expenses

    if orders_sum == 0.00:
        net_profit_percentage = 0.00
    else:
        net_profit_percentage = (net_profit / orders_sum) * 100
    
    # customers_top_five = Customer.objects.annotate(orders_count=Count('orders'), orders_sum=Sum('orders__value')).order_by('-orders_sum')[:5]
    # customer_labels = []
    # customer_data = []
    # for customer in customers_top_five:
        # customer_labels.append(customer.customer)
        # if customer.orders_sum is not None:
            # customer_data.append(customer.orders_sum)
        # else:
            # customer_data.append(0.00)
    

    customers_top_five = Customer.objects.annotate(orders_count=Count('orders'), orders_sum=Sum('orders__value')).order_by('-orders_sum')[:5]
    customer_labels = []
    customer_data = []
    for customer in customers_top_five:
        customer_labels.append(customer.customer)
        if customer.orders_sum is not None:
            customer_data.append(customer.orders_sum)
        else:
            customer_data.append(0.00)


    cities_top_five = CustomerCity.objects.annotate(ord_count=Count('orders_city'), ord_sum=Sum('orders_city__value')).order_by('-ord_sum')[:5]
    city_labels = []
    city_data = []
    for city in cities_top_five:
        city_labels.append(city.customer_city)
        if city.ord_sum is not None:
            city_data.append(city.ord_sum)
        else:
            city_data.append(0.00)
    
    deliveries_status = DeliveryStatus.objects.annotate(del_stat_count=Count('orders_delivery_status'), del_stat_sum=Sum('orders_delivery_status__value')).order_by('-del_stat_count')
    delivery_labels = []
    delivery_data = []
    for status in deliveries_status:
        delivery_labels.append(status.delivery_status)
        if status.del_stat_sum is not None:
            delivery_data.append(status.del_stat_sum)
        else:
            delivery_data.append(0.00)
    
    payments_status = PaymentStatus.objects.annotate(pay_stat_count=Count('orders_payment_status'), pay_stat_sum=Sum('orders_payment_status__value')).order_by('-pay_stat_count')
    
    payment_labels = []
    payment_data = []
    for status in payments_status:
        payment_labels.append(status.payment_status)
        if status.pay_stat_sum is not None:
            payment_data.append(status.pay_stat_sum)
        else:
            payment_data.append(0.00)
    

    if request.method == 'POST':
        dataperiod = request.POST.get('dataperiod')

        # ------------------- TODAY'S DATA -----------------------------------

        if dataperiod == 'today':
            range = "Today's"
            range_orders = Order.objects.filter(order_date__gte=datetime.datetime.now()-timedelta(days=0))
            customers_count = range_orders.values('customer').distinct().count()
            orders_count = range_orders.count()
            if orders_count is None:
                orders_count = 0
            orders_sum = range_orders.aggregate(Sum('value'))['value__sum']
            if orders_sum is None:
                orders_sum = 0.00
            if orders_count == 0:
                average_order_value = 0.00
            else:
                average_order_value = orders_sum / orders_count
            
            # orders = Order.objects.filter(order_date__gte=datetime.datetime.now()-timedelta(days=0))
            orders_expenses = 0.00
            for order in range_orders:
                order_expense = OrderExpense.objects.filter(order_ref=order).aggregate(Sum('expense_amount'))['expense_amount__sum']
                if order_expense is not None:
                    orders_expenses += order_expense
                else:
                    orders_expenses = orders_expenses + 0.00
            
            if orders_expenses is None:
                orders_expenses = 0.00
            gross_profit = orders_sum - orders_expenses
            if orders_sum == 0.00:
                gross_profit_percentage = 0.00
            else:
                gross_profit_percentage = (gross_profit / orders_sum) * 100    
            
            other_expenses = GeneralExpense.objects.filter(expense_date__gte=datetime.datetime.now()-timedelta(days=0)).aggregate(Sum('expense_amount'))['expense_amount__sum']
            if other_expenses is None:
                other_expenses = 0.00
            net_profit = gross_profit - other_expenses
            if orders_sum == 0.00:
                net_profit_percentage = 0.00
            else:
                net_profit_percentage = (net_profit / orders_sum) * 100

            # customers_count = Order.objects.filter(order_date__gte=datetime.datetime.now()-timedelta(days=0)).values('customer').distinct().count()

            # range_customers = range_orders.values('customer').distinct()[:5]
            # range_customers_info = range_customers.annotate(orders_count=Count('customer'), orders_sum=Sum('value')).order_by('orders_sum',)
            # range_customers_info = range_orders.values('customer').distinct().annotate(orders_count=Count('customer'), orders_sum=Sum('value')).order_by('orders_sum',)[:5]

            # customers_top_five = Customer.objects.annotate(orders_count=Count('orders'), orders_sum=Sum('orders__value')).order_by('-orders_sum')[:5]
            customers_top_five = Customer.objects.filter(orders__order_date__gte=datetime.datetime.now()-timedelta(days=0)).annotate(orders_count=Count('orders'), orders_sum=Sum('orders__value')).order_by('-orders_sum')[:5]
            customer_labels = []
            customer_data = []
            for customer in customers_top_five:
                customer_labels.append(customer.customer)
                if customer.orders_sum is not None:
                    customer_data.append(customer.orders_sum)
                else:
                    customer_data.append(0.00)
            
            cities_top_five = CustomerCity.objects.filter(orders_city__order_date__gte=datetime.datetime.now()-timedelta(days=0)).annotate(ord_count=Count('orders_city'), ord_sum=Sum('orders_city__value')).order_by('-ord_sum')[:5]
            city_labels = []
            city_data = []
            for city in cities_top_five:
                city_labels.append(city.customer_city)
                if city.ord_sum is not None:
                    city_data.append(city.ord_sum)
                else:
                    city_data.append(0.00)


            # customers_count = Order.objects.filter(order_date__gte=datetime.datetime.now()-timedelta(days=0)).values('customer').distinct().count()
            
            #deliveries_status = range_orders.values('deliver_status')
            deliveries_status = DeliveryStatus.objects.filter(orders_delivery_status__order_date__gte=datetime.datetime.now()-timedelta(days=0)).annotate(del_stat_count=Count('orders_delivery_status'), del_stat_sum=Sum('orders_delivery_status__value')).order_by('-del_stat_count')
            delivery_labels = []
            delivery_data = []
            for status in deliveries_status:
                delivery_labels.append(status.delivery_status)
                if status.del_stat_sum is not None:
                    delivery_data.append(status.del_stat_sum)
                else:
                    delivery_data.append(0.00)
            
            payments_status = PaymentStatus.objects.filter(orders_payment_status__order_date__gte=datetime.datetime.now()-timedelta(days=0)).annotate(pay_stat_count=Count('orders_payment_status'), pay_stat_sum=Sum('orders_payment_status__value')).order_by('-pay_stat_count')
            payment_labels = []
            payment_data = []
            for status in payments_status:
                payment_labels.append(status.payment_status)
                if status.pay_stat_sum is not None:
                    payment_data.append(status.pay_stat_sum)
                else:
                    payment_data.append(0.00)


        # ------------------- LAST 7 DAYS DATA -----------------------------------

        elif dataperiod == 'last_7_days':
            range = 'Last 7 Days'
            range_orders = Order.objects.filter(order_date__gte=datetime.datetime.now()-timedelta(days=7))
            customers_count = range_orders.values('customer').distinct().count()
            orders_count = range_orders.count()
            if orders_count is None:
                orders_count = 0
            orders_sum = range_orders.aggregate(Sum('value'))['value__sum']
            if orders_sum is None:
                orders_sum = 0.00
            if orders_count == 0:
                average_order_value = 0.00
            else:
                average_order_value = orders_sum / orders_count
            
            # orders = Order.objects.filter(order_date__gte=datetime.datetime.now()-timedelta(days=7))
            orders_expenses = 0.00
            for order in range_orders:
                order_expense = OrderExpense.objects.filter(order_ref=order).aggregate(Sum('expense_amount'))['expense_amount__sum']
                if order_expense is not None:
                    orders_expenses += order_expense
                else:
                    orders_expenses = orders_expenses + 0.00

            if orders_expenses is None:
                orders_expenses = 0.00
            gross_profit = orders_sum - orders_expenses
            if orders_sum == 0.00:
                gross_profit_percentage = 0.00
            else:
                gross_profit_percentage = (gross_profit / orders_sum) * 100    
            other_expenses = GeneralExpense.objects.filter(expense_date__gte=datetime.datetime.now()-timedelta(days=7)).aggregate(Sum('expense_amount'))['expense_amount__sum']
            if other_expenses is None:
                other_expenses = 0.00
            net_profit = gross_profit - other_expenses
            if orders_sum == 0.00:
                net_profit_percentage = 0.00
            else:
                net_profit_percentage = (net_profit / orders_sum) * 100
            

            # range_customers = range_orders.values('customer').distinct()[:5]
            # range_customers_info = range_customers.annotate(orders_count=Count('customer'), orders_sum=Sum('value')).order_by('orders_sum',)
            # range_customers_info = range_orders.values('customer').distinct().annotate(orders_count=Count('customer'), orders_sum=Sum('value')).order_by('orders_sum',)[:5]

            customers_top_five = Customer.objects.filter(orders__order_date__gte=datetime.datetime.now()-timedelta(days=7)).annotate(orders_count=Count('orders'), orders_sum=Sum('orders__value')).order_by('-orders_sum')[:5]
            customer_labels = []
            customer_data = []
            for customer in customers_top_five:
                customer_labels.append(customer.customer)
                if customer.orders_sum is not None:
                    customer_data.append(customer.orders_sum)
                else:
                    customer_data.append(0.00)
            
            cities_top_five = CustomerCity.objects.filter(orders_city__order_date__gte=datetime.datetime.now()-timedelta(days=7)).annotate(ord_count=Count('orders_city'), ord_sum=Sum('orders_city__value')).order_by('-ord_sum')[:5]
            city_labels = []
            city_data = []
            for city in cities_top_five:
                city_labels.append(city.customer_city)
                if city.ord_sum is not None:
                    city_data.append(city.ord_sum)
                else:
                    city_data.append(0.00)
            
            deliveries_status = DeliveryStatus.objects.filter(orders_delivery_status__order_date__gte=datetime.datetime.now()-timedelta(days=7)).annotate(del_stat_count=Count('orders_delivery_status'), del_stat_sum=Sum('orders_delivery_status__value')).order_by('-del_stat_count')
            delivery_labels = []
            delivery_data = []
            for status in deliveries_status:
                delivery_labels.append(status.delivery_status)
                if status.del_stat_sum is not None:
                    delivery_data.append(status.del_stat_sum)
                else:
                    delivery_data.append(0.00)
            
            payments_status = PaymentStatus.objects.filter(orders_payment_status__order_date__gte=datetime.datetime.now()-timedelta(days=7)).annotate(pay_stat_count=Count('orders_payment_status'), pay_stat_sum=Sum('orders_payment_status__value')).order_by('-pay_stat_count')
            payment_labels = []
            payment_data = []
            for status in payments_status:
                payment_labels.append(status.payment_status)
                if status.pay_stat_sum is not None:
                    payment_data.append(status.pay_stat_sum)
                else:
                    payment_data.append(0.00)


        # ------------------- LAST 30 DAYS DATA -----------------------------------

        elif dataperiod == 'last_30_days':
            range = 'Last 30 Days'
            range_orders = Order.objects.filter(order_date__gte=datetime.datetime.now()-timedelta(days=30))
            customers_count = range_orders.values('customer').distinct().count()
            orders_count = range_orders.count()
            if orders_count is None:
                orders_count = 0
            orders_sum = range_orders.aggregate(Sum('value'))['value__sum']
            if orders_sum is None:
                orders_sum = 0.00
            if orders_count == 0:
                average_order_value = 0.00
            else:
                average_order_value = orders_sum / orders_count

            # orders = Order.objects.filter(order_date__gte=datetime.datetime.now()-timedelta(days=30))
            orders_expenses = 0.00
            for order in range_orders:
                order_expense = OrderExpense.objects.filter(order_ref=order).aggregate(Sum('expense_amount'))['expense_amount__sum']
                if order_expense is not None:
                    orders_expenses += order_expense
                else:
                    orders_expenses = orders_expenses + 0.00
            
            if orders_expenses is None:
                orders_expenses = 0.00
            gross_profit = orders_sum - orders_expenses
            if orders_sum == 0.00:
                gross_profit_percentage = 0.00
            else:
                gross_profit_percentage = (gross_profit / orders_sum) * 100    
            other_expenses = GeneralExpense.objects.filter(expense_date__gte=datetime.datetime.now()-timedelta(days=30)).aggregate(Sum('expense_amount'))['expense_amount__sum']
            if other_expenses is None:
                other_expenses = 0.00
            net_profit = gross_profit - other_expenses
            if orders_sum == 0.00:
                net_profit_percentage = 0.00
            else:
                net_profit_percentage = (net_profit / orders_sum) * 100
            
            # range_customers = range_orders.values('customer').distinct()[:5]
            # range_customers_info = range_customers.annotate(orders_count=Count('customer'), orders_sum=Sum('value')).order_by('orders_sum',)
            # range_customers_info = range_orders.values('customer').distinct().annotate(orders_count=Count('customer'), orders_sum=Sum('value')).order_by('orders_sum',)[:5]

            customers_top_five = Customer.objects.filter(orders__order_date__gte=datetime.datetime.now()-timedelta(days=30)).annotate(orders_count=Count('orders'), orders_sum=Sum('orders__value')).order_by('-orders_sum')[:5]
            customer_labels = []
            customer_data = []
            for customer in customers_top_five:
                customer_labels.append(customer.customer)
                if customer.orders_sum is not None:
                    customer_data.append(customer.orders_sum)
                else:
                    customer_data.append(0.00)
            
            cities_top_five = CustomerCity.objects.filter(orders_city__order_date__gte=datetime.datetime.now()-timedelta(days=30)).annotate(ord_count=Count('orders_city'), ord_sum=Sum('orders_city__value')).order_by('-ord_sum')[:5]
            city_labels = []
            city_data = []
            for city in cities_top_five:
                city_labels.append(city.customer_city)
                if city.ord_sum is not None:
                    city_data.append(city.ord_sum)
                else:
                    city_data.append(0.00)
            
            deliveries_status = DeliveryStatus.objects.filter(orders_delivery_status__order_date__gte=datetime.datetime.now()-timedelta(days=30)).annotate(del_stat_count=Count('orders_delivery_status'), del_stat_sum=Sum('orders_delivery_status__value')).order_by('-del_stat_count')
            delivery_labels = []
            delivery_data = []
            for status in deliveries_status:
                delivery_labels.append(status.delivery_status)
                if status.del_stat_sum is not None:
                    delivery_data.append(status.del_stat_sum)
                else:
                    delivery_data.append(0.00)
            
            payments_status = PaymentStatus.objects.filter(orders_payment_status__order_date__gte=datetime.datetime.now()-timedelta(days=30)).annotate(pay_stat_count=Count('orders_payment_status'), pay_stat_sum=Sum('orders_payment_status__value')).order_by('-pay_stat_count')
            payment_labels = []
            payment_data = []
            for status in payments_status:
                payment_labels.append(status.payment_status)
                if status.pay_stat_sum is not None:
                    payment_data.append(status.pay_stat_sum)
                else:
                    payment_data.append(0.00)


        # ------------------- LAST 60 DAYS DATA -----------------------------------
        elif dataperiod == 'last_60_days':
            range = 'Last 60 Days'
            range_orders = Order.objects.filter(order_date__gte=datetime.datetime.now()-timedelta(days=60))
            customers_count = range_orders.values('customer').distinct().count()
            orders_count = range_orders.count()
            if orders_count is None:
                orders_count = 0
            orders_sum = range_orders.aggregate(Sum('value'))['value__sum']
            if orders_sum is None:
                orders_sum = 0.00
            if orders_count == 0:
                average_order_value = 0.00
            else:
                average_order_value = orders_sum / orders_count
            
            # orders = Order.objects.filter(order_date__gte=datetime.datetime.now()-timedelta(days=60))
            orders_expenses = 0.00
            for order in range_orders:
                order_expense = OrderExpense.objects.filter(order_ref=order).aggregate(Sum('expense_amount'))['expense_amount__sum']
                if order_expense is not None:
                    orders_expenses += order_expense
                else:
                    orders_expenses = orders_expenses + 0.00

            if orders_expenses is None:
                orders_expenses = 0.00
            gross_profit = orders_sum - orders_expenses
            if orders_sum == 0.00:
                gross_profit_percentage = 0.00
            else:
                gross_profit_percentage = (gross_profit / orders_sum) * 100    
            other_expenses = GeneralExpense.objects.filter(expense_date__gte=datetime.datetime.now()-timedelta(days=60)).aggregate(Sum('expense_amount'))['expense_amount__sum']
            if other_expenses is None:
                other_expenses = 0.00
            net_profit = gross_profit - other_expenses
            if orders_sum == 0.00:
                net_profit_percentage = 0.00
            else:
                net_profit_percentage = (net_profit / orders_sum) * 100

            # range_customers = range_orders.values('customer').distinct()[:5]
            # range_customers_info = range_customers.annotate(orders_count=Count('customer'), orders_sum=Sum('value')).order_by('orders_sum',)
            # range_customers_info = range_orders.values('customer').distinct().annotate(orders_count=Count('customer'), orders_sum=Sum('value')).order_by('orders_sum',)[:5]

            customers_top_five = Customer.objects.filter(orders__order_date__gte=datetime.datetime.now()-timedelta(days=60)).annotate(orders_count=Count('orders'), orders_sum=Sum('orders__value')).order_by('-orders_sum')[:5]
            customer_labels = []
            customer_data = []
            for customer in customers_top_five:
                customer_labels.append(customer.customer)
                if customer.orders_sum is not None:
                    customer_data.append(customer.orders_sum)
                else:
                    customer_data.append(0.00)
            
            cities_top_five = CustomerCity.objects.filter(orders_city__order_date__gte=datetime.datetime.now()-timedelta(days=60)).annotate(ord_count=Count('orders_city'), ord_sum=Sum('orders_city__value')).order_by('-ord_sum')[:5]
            city_labels = []
            city_data = []
            for city in cities_top_five:
                city_labels.append(city.customer_city)
                if city.ord_sum is not None:
                    city_data.append(city.ord_sum)
                else:
                    city_data.append(0.00)
            
            deliveries_status = DeliveryStatus.objects.filter(orders_delivery_status__order_date__gte=datetime.datetime.now()-timedelta(days=60)).annotate(del_stat_count=Count('orders_delivery_status'), del_stat_sum=Sum('orders_delivery_status__value')).order_by('-del_stat_count')
            delivery_labels = []
            delivery_data = []
            for status in deliveries_status:
                delivery_labels.append(status.delivery_status)
                if status.del_stat_sum is not None:
                    delivery_data.append(status.del_stat_sum)
                else:
                    delivery_data.append(0.00)
            
            payments_status = PaymentStatus.objects.filter(orders_payment_status__order_date__gte=datetime.datetime.now()-timedelta(days=60)).annotate(pay_stat_count=Count('orders_payment_status'), pay_stat_sum=Sum('orders_payment_status__value')).order_by('-pay_stat_count')
            payment_labels = []
            payment_data = []
            for status in payments_status:
                payment_labels.append(status.payment_status)
                if status.pay_stat_sum is not None:
                    payment_data.append(status.pay_stat_sum)
                else:
                    payment_data.append(0.00)
        
        # ------------------- LAST 90 DAYS DATA -----------------------------------
        elif dataperiod == 'last_90_days':
            range = 'Last 90 Days'
            range_orders = Order.objects.filter(order_date__gte=datetime.datetime.now()-timedelta(days=90))
            customers_count = range_orders.values('customer').distinct().count()
            orders_count = range_orders.count()
            if orders_count is None:
                orders_count = 0
            orders_sum = range_orders.aggregate(Sum('value'))['value__sum']
            if orders_sum is None:
                orders_sum = 0.00
            if orders_count == 0:
                average_order_value = 0.00
            else:
                average_order_value = orders_sum / orders_count
            
            # orders = Order.objects.filter(order_date__gte=datetime.datetime.now()-timedelta(days=90))
            orders_expenses = 0.00
            for order in range_orders:
                order_expense = OrderExpense.objects.filter(order_ref=order).aggregate(Sum('expense_amount'))['expense_amount__sum']
                if order_expense is not None:
                    orders_expenses += order_expense
                else:
                    orders_expenses = orders_expenses + 0.00

            if orders_expenses is None:
                orders_expenses = 0.00
            gross_profit = orders_sum - orders_expenses
            if orders_sum == 0.00:
                gross_profit_percentage = 0.00
            else:
                gross_profit_percentage = (gross_profit / orders_sum) * 100    
            other_expenses = GeneralExpense.objects.filter(expense_date__gte=datetime.datetime.now()-timedelta(days=90)).aggregate(Sum('expense_amount'))['expense_amount__sum']
            if other_expenses is None:
                other_expenses = 0.00
            net_profit = gross_profit - other_expenses
            if orders_sum == 0.00:
                net_profit_percentage = 0.00
            else:
                net_profit_percentage = (net_profit / orders_sum) * 100

            # range_customers = range_orders.values('customer').distinct()[:5]
            # range_customers_info = range_customers.annotate(orders_count=Count('customer'), orders_sum=Sum('value')).order_by('orders_sum',)
            # range_customers_info = range_orders.values('customer').distinct().annotate(orders_count=Count('customer'), orders_sum=Sum('value')).order_by('orders_sum',)[:5]

            customers_top_five = Customer.objects.filter(orders__order_date__gte=datetime.datetime.now()-timedelta(days=90)).annotate(orders_count=Count('orders'), orders_sum=Sum('orders__value')).order_by('-orders_sum')[:5]
            customer_labels = []
            customer_data = []
            for customer in customers_top_five:
                customer_labels.append(customer.customer)
                if customer.orders_sum is not None:
                    customer_data.append(customer.orders_sum)
                else:
                    customer_data.append(0.00)
            
            cities_top_five = CustomerCity.objects.filter(orders_city__order_date__gte=datetime.datetime.now()-timedelta(days=90)).annotate(ord_count=Count('orders_city'), ord_sum=Sum('orders_city__value')).order_by('-ord_sum')[:5]
            city_labels = []
            city_data = []
            for city in cities_top_five:
                city_labels.append(city.customer_city)
                if city.ord_sum is not None:
                    city_data.append(city.ord_sum)
                else:
                    city_data.append(0.00)
            
            deliveries_status = DeliveryStatus.objects.filter(orders_delivery_status__order_date__gte=datetime.datetime.now()-timedelta(days=90)).annotate(del_stat_count=Count('orders_delivery_status'), del_stat_sum=Sum('orders_delivery_status__value')).order_by('-del_stat_count')
            delivery_labels = []
            delivery_data = []
            for status in deliveries_status:
                delivery_labels.append(status.delivery_status)
                if status.del_stat_sum is not None:
                    delivery_data.append(status.del_stat_sum)
                else:
                    delivery_data.append(0.00)
            
            payments_status = PaymentStatus.objects.filter(orders_payment_status__order_date__gte=datetime.datetime.now()-timedelta(days=90)).annotate(pay_stat_count=Count('orders_payment_status'), pay_stat_sum=Sum('orders_payment_status__value')).order_by('-pay_stat_count')
            payment_labels = []
            payment_data = []
            for status in payments_status:
                payment_labels.append(status.payment_status)
                if status.pay_stat_sum is not None:
                    payment_data.append(status.pay_stat_sum)
                else:
                    payment_data.append(0.00)
        
        # ------------------- CURRENT MONTH DATA -----------------------------------        
        elif dataperiod == 'current_month':
            range = "Current Month's"
            today = datetime.date.today()
            range_orders = Order.objects.filter(order_date__year=today.year, order_date__month=today.month)
            customers_count = range_orders.values('customer').distinct().count()
            orders_count = range_orders.count()
            if orders_count is None:
                orders_count = 0
            orders_sum = range_orders.aggregate(Sum('value'))['value__sum']
            if orders_sum is None:
                orders_sum = 0.00
            if orders_count == 0:
                average_order_value = 0.00
            else:
                average_order_value = orders_sum / orders_count
            
            # orders = Order.objects.filter(order_date__year=today.year, order_date__month=today.month)
            orders_expenses = 0.00
            for order in range_orders:
                order_expense = OrderExpense.objects.filter(order_ref=order).aggregate(Sum('expense_amount'))['expense_amount__sum']
                if order_expense is not None:
                    orders_expenses += order_expense
                else:
                    orders_expenses = orders_expenses + 0.00

            if orders_expenses is None:
                orders_expenses = 0.00
            gross_profit = orders_sum - orders_expenses
            if orders_sum == 0.00:
                gross_profit_percentage = 0.00
            else:
                gross_profit_percentage = (gross_profit / orders_sum) * 100    
            other_expenses = GeneralExpense.objects.filter(expense_date__year=today.year, expense_date__month=today.month).aggregate(Sum('expense_amount'))['expense_amount__sum']
            if other_expenses is None:
                other_expenses = 0.00
            net_profit = gross_profit - other_expenses
            if orders_sum == 0.00:
                net_profit_percentage = 0.00
            else:
                net_profit_percentage = (net_profit / orders_sum) * 100

            # range_customers = range_orders.values('customer').distinct()[:5]
            # range_customers_info = range_customers.annotate(orders_count=Count('customer'), orders_sum=Sum('value')).order_by('orders_sum',)
            # range_customers_info = range_orders.values('customer').distinct().annotate(orders_count=Count('customer'), orders_sum=Sum('value')).order_by('orders_sum',)[:5]

            customers_top_five = Customer.objects.filter(orders__order_date__year=today.year, orders__order_date__month=today.month).annotate(orders_count=Count('orders'), orders_sum=Sum('orders__value')).order_by('-orders_sum')[:5]
            customer_labels = []
            customer_data = []
            for customer in customers_top_five:
                customer_labels.append(customer.customer)
                if customer.orders_sum is not None:
                    customer_data.append(customer.orders_sum)
                else:
                    customer_data.append(0.00)
            
            cities_top_five = CustomerCity.objects.filter(orders_city__order_date__year=today.year, orders_city__order_date__month=today.month).annotate(ord_count=Count('orders_city'), ord_sum=Sum('orders_city__value')).order_by('-ord_sum')[:5]
            city_labels = []
            city_data = []
            for city in cities_top_five:
                city_labels.append(city.customer_city)
                if city.ord_sum is not None:
                    city_data.append(city.ord_sum)
                else:
                    city_data.append(0.00)
            
            deliveries_status = DeliveryStatus.objects.filter(orders_delivery_status__order_date__year=today.year, orders_delivery_status__order_date__month=today.month).annotate(del_stat_count=Count('orders_delivery_status'), del_stat_sum=Sum('orders_delivery_status__value')).order_by('-del_stat_count')
            delivery_labels = []
            delivery_data = []
            for status in deliveries_status:
                delivery_labels.append(status.delivery_status)
                if status.del_stat_sum is not None:
                    delivery_data.append(status.del_stat_sum)
                else:
                    delivery_data.append(0.00)
            
            payments_status = PaymentStatus.objects.filter(orders_payment_status__order_date__year=today.year, orders_payment_status__order_date__month=today.month).annotate(pay_stat_count=Count('orders_payment_status'), pay_stat_sum=Sum('orders_payment_status__value')).order_by('-pay_stat_count')
            payment_labels = []
            payment_data = []
            for status in payments_status:
                payment_labels.append(status.payment_status)
                if status.pay_stat_sum is not None:
                    payment_data.append(status.pay_stat_sum)
                else:
                    payment_data.append(0.00)
        
        
        # ------------------- CURRENT YEAR DATA -----------------------------------        
        elif dataperiod == 'current_year':
            range = "Current Year's"
            today = datetime.date.today()
            range_orders = Order.objects.filter(order_date__year=today.year)
            customers_count = range_orders.values('customer').distinct().count()
            orders_count = range_orders.count()
            if orders_count is None:
                orders_count = 0
            orders_sum = range_orders.aggregate(Sum('value'))['value__sum']
            if orders_sum is None:
                orders_sum = 0.00
            if orders_count == 0:
                average_order_value = 0.00
            else:
                average_order_value = orders_sum / orders_count
            
            # orders = Order.objects.filter(order_date__year=today.year)
            orders_expenses = 0.00
            for order in range_orders:
                order_expense = OrderExpense.objects.filter(order_ref=order).aggregate(Sum('expense_amount'))['expense_amount__sum']
                if order_expense is not None:
                    orders_expenses += order_expense
                else:
                    orders_expenses = orders_expenses + 0.00

            if orders_expenses is None:
                orders_expenses = 0.00
            gross_profit = orders_sum - orders_expenses
            if orders_sum == 0.00:
                gross_profit_percentage = 0.00
            else:
                gross_profit_percentage = (gross_profit / orders_sum) * 100    
            other_expenses = GeneralExpense.objects.filter(expense_date__year=today.year).aggregate(Sum('expense_amount'))['expense_amount__sum']
            if other_expenses is None:
                other_expenses = 0.00
            net_profit = gross_profit - other_expenses
            if orders_sum == 0.00:
                net_profit_percentage = 0.00
            else:
                net_profit_percentage = (net_profit / orders_sum) * 100
            
            # range_customers = range_orders.values('customer').distinct()[:5]
            # range_cust = range_orders.
            # range_customers_info = range_customers.annotate(orders_count=Count('customer'), orders_sum=Sum('value')).order_by('orders_sum',)
            # range_customers_info = range_orders.values('customer').annotate(orders_count=Count('order_ref'), orders_sum=Sum('value')).order_by('orders_sum',).values('customer', 'orders_count', 'orders_sum')[:5]
            
            customers_top_five = Customer.objects.filter(orders__order_date__year=today.year).annotate(orders_count=Count('orders'), orders_sum=Sum('orders__value')).order_by('-orders_sum')[:5]
            customer_labels = []
            customer_data = []
            for customer in customers_top_five:
                customer_labels.append(customer.customer)
                if customer.orders_sum is not None:
                    customer_data.append(customer.orders_sum)
                else:
                    customer_data.append(0.00)
            
            cities_top_five = CustomerCity.objects.filter(orders_city__order_date__year=today.year).annotate(ord_count=Count('orders_city'), ord_sum=Sum('orders_city__value')).order_by('-ord_sum')[:5]
            city_labels = []
            city_data = []
            for city in cities_top_five:
                city_labels.append(city.customer_city)
                if city.ord_sum is not None:
                    city_data.append(city.ord_sum)
                else:
                    city_data.append(0.00)
            
            deliveries_status = DeliveryStatus.objects.filter(orders_delivery_status__order_date__year=today.year).annotate(del_stat_count=Count('orders_delivery_status'), del_stat_sum=Sum('orders_delivery_status__value')).order_by('-del_stat_count')
            delivery_labels = []
            delivery_data = []
            for status in deliveries_status:
                delivery_labels.append(status.delivery_status)
                if status.del_stat_sum is not None:
                    delivery_data.append(status.del_stat_sum)
                else:
                    delivery_data.append(0.00)
            
            payments_status = PaymentStatus.objects.filter(orders_payment_status__order_date__year=today.year).annotate(pay_stat_count=Count('orders_payment_status'), pay_stat_sum=Sum('orders_payment_status__value')).order_by('-pay_stat_count')
            payment_labels = []
            payment_data = []
            for status in payments_status:
                payment_labels.append(status.payment_status)
                if status.pay_stat_sum is not None:
                    payment_data.append(status.pay_stat_sum)
                else:
                    payment_data.append(0.00)
        
        # ------------------- CUSTOM PERIOD DATA -----------------------------------        
        elif dataperiod == 'custom_period':
            pass


    context = {
        'range': range,
        # 'range_customers_info': range_customers_info,
        'customers_count': customers_count,
        'orders_count': orders_count,
        'orders_sum': orders_sum,
        'average_order_value': average_order_value,
        'orders_expenses': orders_expenses,
        'gross_profit': gross_profit,
        'gross_profit_percentage': gross_profit_percentage, 
        'other_expenses': other_expenses,
        'net_profit': net_profit,
        'net_profit_percentage': net_profit_percentage,
        'customers_top_five': customers_top_five,
        'customer_labels': customer_labels,
        'customer_data': customer_data,
        'cities_top_five': cities_top_five,
        'city_labels': city_labels,
        'city_data': city_data,
        'deliveries_status': deliveries_status,
        'delivery_labels': delivery_labels,
        'delivery_data': delivery_data,
        'payments_status': payments_status,
        'payment_labels': payment_labels,
        'payment_data': payment_data,
    }
    return render(request, 'accounts/index.html', context)








@login_required(login_url='login')
def customer_cities(request):

    range = "All Time"
    cities_count = CustomerCity.objects.all().count()
    orders_count = Order.objects.all().count()
    orders_sum = Order.objects.all().aggregate(Sum('value'))['value__sum']

    if cities_count is not None and orders_sum is not None:
        aov_city = orders_sum / cities_count
    else:
        aov_city = 0.00
    
    cities = CustomerCity.objects.annotate(ord_count=Count('orders_city'), ord_sum=Sum('orders_city__value'), aov=Sum('orders_city__value')/Count('orders_city'))

    cities_top_five = CustomerCity.objects.annotate(ord_count=Count('orders_city'), ord_sum=Sum('orders_city__value')).order_by('-ord_sum')[:5]
    city_labels = []
    city_data = []
    for city in cities_top_five:
        city_labels.append(city.customer_city)
        if city.ord_sum is not None:
            city_data.append(city.ord_sum)
        else:
            city_data.append(0.00)

    
    if request.method == 'POST':
        dataperiod = request.POST.get('dataperiod')

        # ------------------- TODAY'S DATA -----------------------------------

        if dataperiod == 'today':
            range = "Today's"
            range_orders = Order.objects.filter(order_date__gte=datetime.datetime.now()-timedelta(days=0))

            orders_count = range_orders.count()

            cities_count = range_orders.values('customer_city').distinct().count()

            orders_sum = range_orders.aggregate(Sum('value'))['value__sum']
            if orders_sum is None:
                orders_sum = 0.00

            if cities_count == 0:
                aov_city = 0.00
            else:
                aov_city = orders_sum / cities_count
            
            cities = CustomerCity.objects.filter(orders_city__order_date__gte=datetime.datetime.now()-timedelta(days=0)).annotate(ord_count=Count('orders_city'), ord_sum=Sum('orders_city__value'), aov=Sum('orders_city__value')/Count('orders_city'))

            cities_top_five = CustomerCity.objects.filter(orders_city__order_date__gte=datetime.datetime.now()-timedelta(days=0)).annotate(ord_count=Count('orders_city'), ord_sum=Sum('orders_city__value'), aov=Sum('orders_city__value')/Count('orders_city')).order_by('-ord_sum')[:5]

            city_labels = []
            city_data = []
            for city in cities_top_five:
                city_labels.append(city.customer_city)
                if city.ord_sum is not None:
                    city_data.append(city.ord_sum)
                else:
                    city_data.append(0.00)



        # ------------------- LAST 7 DAYS DATA -----------------------------------

        if dataperiod == 'last_7_days':
            range = "Last 7 Days"
            range_orders = Order.objects.filter(order_date__gte=datetime.datetime.now()-timedelta(days=7))

            orders_count = range_orders.count()

            cities_count = range_orders.values('customer_city').distinct().count()

            orders_sum = range_orders.aggregate(Sum('value'))['value__sum']
            if orders_sum is None:
                orders_sum = 0.00

            if cities_count == 0:
                aov_city = 0.00
            else:
                aov_city = orders_sum / cities_count
            
            cities = CustomerCity.objects.filter(orders_city__order_date__gte=datetime.datetime.now()-timedelta(days=7)).annotate(ord_count=Count('orders_city'), ord_sum=Sum('orders_city__value'), aov=Sum('orders_city__value')/Count('orders_city'))

            cities_top_five = CustomerCity.objects.filter(orders_city__order_date__gte=datetime.datetime.now()-timedelta(days=7)).annotate(ord_count=Count('orders_city'), ord_sum=Sum('orders_city__value'), aov=Sum('orders_city__value')/Count('orders_city')).order_by('-ord_sum')[:5]
            
            city_labels = []
            city_data = []
            for city in cities_top_five:
                city_labels.append(city.customer_city)
                if city.ord_sum is not None:
                    city_data.append(city.ord_sum)
                else:
                    city_data.append(0.00)



        # ------------------- LAST 30 DAYS DATA -----------------------------------

        if dataperiod == 'last_30_days':
            range = "Last 30 Days"
            range_orders = Order.objects.filter(order_date__gte=datetime.datetime.now()-timedelta(days=30))

            orders_count = range_orders.count()

            cities_count = range_orders.values('customer_city').distinct().count()

            orders_sum = range_orders.aggregate(Sum('value'))['value__sum']
            if orders_sum is None:
                orders_sum = 0.00

            if cities_count == 0:
                aov_city = 0.00
            else:
                aov_city = orders_sum / cities_count
            
            cities = CustomerCity.objects.filter(orders_city__order_date__gte=datetime.datetime.now()-timedelta(days=30)).annotate(ord_count=Count('orders_city'), ord_sum=Sum('orders_city__value'), aov=Sum('orders_city__value')/Count('orders_city'))

            cities_top_five = CustomerCity.objects.filter(orders_city__order_date__gte=datetime.datetime.now()-timedelta(days=30)).annotate(ord_count=Count('orders_city'), ord_sum=Sum('orders_city__value'), aov=Sum('orders_city__value')/Count('orders_city')).order_by('-ord_sum')[:5]
            
            city_labels = []
            city_data = []
            for city in cities_top_five:
                city_labels.append(city.customer_city)
                if city.ord_sum is not None:
                    city_data.append(city.ord_sum)
                else:
                    city_data.append(0.00)



        # ------------------- LAST 60 DAYS DATA -----------------------------------

        if dataperiod == 'last_60_days':
            range = "Last 60 Days"
            range_orders = Order.objects.filter(order_date__gte=datetime.datetime.now()-timedelta(days=60))

            orders_count = range_orders.count()

            cities_count = range_orders.values('customer_city').distinct().count()

            orders_sum = range_orders.aggregate(Sum('value'))['value__sum']
            if orders_sum is None:
                orders_sum = 0.00

            if cities_count == 0:
                aov_city = 0.00
            else:
                aov_city = orders_sum / cities_count
            
            cities = CustomerCity.objects.filter(orders_city__order_date__gte=datetime.datetime.now()-timedelta(days=60)).annotate(ord_count=Count('orders_city'), ord_sum=Sum('orders_city__value'), aov=Sum('orders_city__value')/Count('orders_city'))

            cities_top_five = CustomerCity.objects.filter(orders_city__order_date__gte=datetime.datetime.now()-timedelta(days=60)).annotate(ord_count=Count('orders_city'), ord_sum=Sum('orders_city__value'), aov=Sum('orders_city__value')/Count('orders_city')).order_by('-ord_sum')[:5]
            
            city_labels = []
            city_data = []
            for city in cities_top_five:
                city_labels.append(city.customer_city)
                if city.ord_sum is not None:
                    city_data.append(city.ord_sum)
                else:
                    city_data.append(0.00)



        # ------------------- LAST 90 DAYS DATA -----------------------------------

        if dataperiod == 'last_90_days':
            range = "Last 90 Days"
            range_orders = Order.objects.filter(order_date__gte=datetime.datetime.now()-timedelta(days=90))

            orders_count = range_orders.count()

            cities_count = range_orders.values('customer_city').distinct().count()

            orders_sum = range_orders.aggregate(Sum('value'))['value__sum']
            if orders_sum is None:
                orders_sum = 0.00

            if cities_count == 0:
                aov_city = 0.00
            else:
                aov_city = orders_sum / cities_count
            
            cities = CustomerCity.objects.filter(orders_city__order_date__gte=datetime.datetime.now()-timedelta(days=90)).annotate(ord_count=Count('orders_city'), ord_sum=Sum('orders_city__value'), aov=Sum('orders_city__value')/Count('orders_city'))

            cities_top_five = CustomerCity.objects.filter(orders_city__order_date__gte=datetime.datetime.now()-timedelta(days=90)).annotate(ord_count=Count('orders_city'), ord_sum=Sum('orders_city__value'), aov=Sum('orders_city__value')/Count('orders_city')).order_by('-ord_sum')[:5]
            
            city_labels = []
            city_data = []
            for city in cities_top_five:
                city_labels.append(city.customer_city)
                if city.ord_sum is not None:
                    city_data.append(city.ord_sum)
                else:
                    city_data.append(0.00)



        # ------------------- CURRENT MONTH DATA -----------------------------------

        if dataperiod == 'current_month':
            range = "Current Month's"
            today = datetime.date.today()
            range_orders = Order.objects.filter(order_date__year=today.year, order_date__month=today.month)

            orders_count = range_orders.count()

            cities_count = range_orders.values('customer_city').distinct().count()

            orders_sum = range_orders.aggregate(Sum('value'))['value__sum']
            if orders_sum is None:
                orders_sum = 0.00

            if cities_count == 0:
                aov_city = 0.00
            else:
                aov_city = orders_sum / cities_count
            
            cities = CustomerCity.objects.filter(orders_city__order_date__year=today.year, orders_city__order_date__month=today.month).annotate(ord_count=Count('orders_city'), ord_sum=Sum('orders_city__value'), aov=Sum('orders_city__value')/Count('orders_city'))

            cities_top_five = CustomerCity.objects.filter(orders_city__order_date__year=today.year, orders_city__order_date__month=today.month).annotate(ord_count=Count('orders_city'), ord_sum=Sum('orders_city__value'), aov=Sum('orders_city__value')/Count('orders_city')).order_by('-ord_sum')[:5]
            
            city_labels = []
            city_data = []
            for city in cities_top_five:
                city_labels.append(city.customer_city)
                if city.ord_sum is not None:
                    city_data.append(city.ord_sum)
                else:
                    city_data.append(0.00)



        # ------------------- CURRENT YEAR DATA -----------------------------------

        if dataperiod == 'current_year':
            range = "Current Year's"
            today = datetime.date.today()
            range_orders = Order.objects.filter(order_date__year=today.year)

            orders_count = range_orders.count()

            cities_count = range_orders.values('customer_city').distinct().count()

            orders_sum = range_orders.aggregate(Sum('value'))['value__sum']
            if orders_sum is None:
                orders_sum = 0.00

            if cities_count == 0:
                aov_city = 0.00
            else:
                aov_city = orders_sum / cities_count
            
            cities = CustomerCity.objects.filter(orders_city__order_date__year=today.year).annotate(ord_count=Count('orders_city'), ord_sum=Sum('orders_city__value'), aov=Sum('orders_city__value')/Count('orders_city'))

            cities_top_five = CustomerCity.objects.filter(orders_city__order_date__year=today.year).annotate(ord_count=Count('orders_city'), ord_sum=Sum('orders_city__value'), aov=Sum('orders_city__value')/Count('orders_city')).order_by('-ord_sum')[:5]
            
            city_labels = []
            city_data = []
            for city in cities_top_five:
                city_labels.append(city.customer_city)
                if city.ord_sum is not None:
                    city_data.append(city.ord_sum)
                else:
                    city_data.append(0.00)


    context = {
        'range': range,
        'cities_count': cities_count,
        'orders_count': orders_count,
        'orders_sum': orders_sum,
        'cities': cities,
        'aov_city': aov_city,
        'cities_top_five': cities_top_five,
        'city_labels': city_labels,
        'city_data': city_data,
    }
    return render(request, 'accounts/customer-cities/customer-cities.html', context)



@login_required(login_url='login')
def customer_cities_add(request):
    form = CustomerCityForm
    if request.method == 'POST':
        form = CustomerCityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/customer-cities/')
    context = {
        'form': form,
    }
    return render(request, 'accounts/customer-cities/customer-cities-add.html', context)



@login_required(login_url='login')
def customer_cities_delete(request, pk):
    city = CustomerCity.objects.get(id=pk)
    city_name = city.customer_city
    if request.method == 'POST':
        city.delete()
        return redirect('/customer-cities/')
    context = {
        'city': city,
        'city_name': city_name,
    }
    return render(request, 'accounts/customer-cities/customer-cities-delete.html', context)



@login_required(login_url='login')
def customer_cities_edit(request, pk):
    city = CustomerCity.objects.get(id=pk)
    city_name = city.customer_city
    form = CustomerCityForm(instance=city)
    if request.method == 'POST':
        form = CustomerCityForm(request.POST, instance=city)
        if form.is_valid():
            form.save()
            return redirect('/customer-cities/')
    context = {
        'city_name': city_name,
        'form': form,
    }
    return render(request, 'accounts/customer-cities/customer-cities-edit.html', context)



@login_required(login_url='login')
def customer(request, pk):
    customer = Customer.objects.get(customer_id=pk)
    orders = customer.orders.all()
    orders_count = orders.count()
    orders_sum = orders.aggregate(Sum('value'))['value__sum']
    average_order_value = orders_sum / orders_count
    customer_first_order = customer.orders.aggregate(first_order_date=Min('order_date'))
    customer_last_order = customer.orders.aggregate(last_order_date=Max('order_date'))
    total_order_value = Order.objects.aggregate(Sum('value'))['value__sum']
    percentage_share = ((orders_sum) / (total_order_value)) * 100
    # del_stat = customer.orders.annotate(del_stat_count=Count('delivery_status')).distinct()
    context = {
        'customer': customer,
        'orders': orders,
        'orders_count': orders_count,
        'orders_sum': orders_sum,
        'average_order_value': average_order_value,
        'customer_first_order': customer_first_order,
        'customer_last_order': customer_last_order,
        'percentage_share': percentage_share,
        # 'del_stat': del_stat,
    }
    return render(request,'accounts/customers/customer.html', context)



@login_required(login_url='login')
def customers_add(request):
    form = CustomerForm
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/customers/')
    context = {
        'form': form,
    }
    return render(request,'accounts/customers/customers-add.html', context)



@login_required(login_url='login')
def customers_delete(request, pk):
    customer = Customer.objects.get(customer_id=pk)
    customer_name = customer.customer
    if request.method == 'POST':
        customer.delete()
        return redirect('/customers/')
    context = {
        'customer': customer,
        'customer_name': customer_name,
    }
    return render(request,'accounts/customers/customers-delete.html', context)



@login_required(login_url='login')
def customers_edit(request, pk):
    customer = Customer.objects.get(customer_id=pk)
    customer_name = customer.customer
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('/customers/')
    context = {
        'customer_name': customer_name,
        'form': form,
    }
    return render(request,'accounts/customers/customers-edit.html', context)



@login_required(login_url='login')
def customers(request):
    range = "All Time"
    customers_count = Customer.objects.all().count()
    orders_count = Order.objects.all().count()
    orders_sum = Order.objects.all().aggregate(Sum('value'))['value__sum']
    customers_info = Customer.objects.annotate(orders_count=Count('orders'), orders_sum=Sum('orders__value'), aov=Sum('orders__value')/Count('orders')).order_by('customer_id')
    if orders_count is not None and orders_sum is not None:
        aov_customer = orders_sum / customers_count
    else:
        aov_customer = 0.00
    # aov_customer = orders_sum / customers_count
    
    customers_top_five = Customer.objects.annotate(orders_count=Count('orders'), orders_sum=Sum('orders__value')).order_by('-orders_sum')[:5]
    customer_labels = []
    customer_data = []
    for customer in customers_top_five:
        customer_labels.append(customer.customer)
        if customer.orders_sum is not None:
            customer_data.append(customer.orders_sum)
        else:
            customer_data.appen(0.00)

    cities_top_five = CustomerCity.objects.annotate(ord_count=Count('orders_city'), ord_sum=Sum('orders_city__value')).order_by('-ord_sum')[:5]
    city_labels = []
    city_data = []
    for city in cities_top_five:
        city_labels.append(city.customer_city)
        if city.ord_sum is not None:
            city_data.append(city.ord_sum)
        else:
            city_data.append(0.00)
    

    if request.method == 'POST':
        dataperiod = request.POST.get('dataperiod')

        # ------------------- TODAY'S DATA -----------------------------------

        if dataperiod == 'today':
            range = "Today's"
            range_orders = Order.objects.filter(order_date__gte=datetime.datetime.now()-timedelta(days=0))

            customers_count = range_orders.values('customer').distinct().count()
            orders_count = range_orders.count()
            orders_sum = range_orders.aggregate(Sum('value'))['value__sum']
            if orders_sum is None:
                orders_sum = 0.00
            if customers_count == 0:
                aov_customer = 0.00
            else:
                aov_customer = orders_sum / customers_count

            customers_info = Customer.objects.filter(orders__order_date__gte=datetime.datetime.now()-timedelta(days=0)).annotate(orders_count=Count('orders'), orders_sum=Sum('orders__value'), aov=Sum('orders__value')/Count('orders')).order_by('customer_id')
            # if orders_count is None:
                # aov_customer = 0.00
            # else:
                # aov_customer = orders_sum / customers_count
            
            customers_top_five = Customer.objects.filter(orders__order_date__gte=datetime.datetime.now()-timedelta(days=0)).annotate(orders_count=Count('orders'), orders_sum=Sum('orders__value')).order_by('-orders_sum')[:5]
            customer_labels = []
            customer_data = []
            for customer in customers_top_five:
                customer_labels.append(customer.customer)
                if customer.orders_sum is not None:
                    customer_data.append(customer.orders_sum)
                else:
                    customer_data.append(0.00)

            cities_top_five = CustomerCity.objects.filter(orders_city__order_date__gte=datetime.datetime.now()-timedelta(days=0)).annotate(ord_count=Count('orders_city'), ord_sum=Sum('orders_city__value')).order_by('-ord_sum')[:5]
            city_labels = []
            city_data = []
            for city in cities_top_five:
                city_labels.append(city.customer_city)
                if city.ord_sum is not None:
                    city_data.append(city.ord_sum)
                else:
                    city_data.append(0.00)


        # ------------------- LAST 7 DAYS DATA -----------------------------------

        elif dataperiod == 'last_7_days':
            range = "Last 7 Days"
            range_orders = Order.objects.filter(order_date__gte=datetime.datetime.now()-timedelta(days=7))

            customers_count = range_orders.values('customer').distinct().count()
            orders_count = range_orders.count()
            orders_sum = range_orders.aggregate(Sum('value'))['value__sum']
            if orders_sum is None:
                orders_sum = 0.00
            if customers_count == 0:
                aov_customer = 0.00
            else:
                aov_customer = orders_sum / customers_count

            customers_info = Customer.objects.filter(orders__order_date__gte=datetime.datetime.now()-timedelta(days=7)).annotate(orders_count=Count('orders'), orders_sum=Sum('orders__value'), aov=Sum('orders__value')/Count('orders')).order_by('customer_id')
            # if orders_count is None:
                # aov_customer = 0.00
            # else:
                # aov_customer = orders_sum / customers_count
            
            customers_top_five = Customer.objects.filter(orders__order_date__gte=datetime.datetime.now()-timedelta(days=7)).annotate(orders_count=Count('orders'), orders_sum=Sum('orders__value')).order_by('-orders_sum')[:5]
            customer_labels = []
            customer_data = []
            for customer in customers_top_five:
                customer_labels.append(customer.customer)
                if customer.orders_sum is not None:
                    customer_data.append(customer.orders_sum)
                else:
                    customer_data.append(0.00)

            cities_top_five = CustomerCity.objects.filter(orders_city__order_date__gte=datetime.datetime.now()-timedelta(days=7)).annotate(ord_count=Count('orders_city'), ord_sum=Sum('orders_city__value')).order_by('-ord_sum')[:5]
            city_labels = []
            city_data = []
            for city in cities_top_five:
                city_labels.append(city.customer_city)
                if city.ord_sum is not None:
                    city_data.append(city.ord_sum)
                else:
                    city_data.append(0.00)


        # ------------------- LAST 30 DAYS DATA -----------------------------------

        elif dataperiod == 'last_30_days':
            range = "Last 30 Days"
            range_orders = Order.objects.filter(order_date__gte=datetime.datetime.now()-timedelta(days=30))

            customers_count = range_orders.values('customer').distinct().count()
            orders_count = range_orders.count()
            orders_sum = range_orders.aggregate(Sum('value'))['value__sum']
            if orders_sum is None:
                orders_sum = 0.00
            if customers_count == 0:
                aov_customer = 0.00
            else:
                aov_customer = orders_sum / customers_count

            customers_info = Customer.objects.filter(orders__order_date__gte=datetime.datetime.now()-timedelta(days=30)).annotate(orders_count=Count('orders'), orders_sum=Sum('orders__value'), aov=Sum('orders__value')/Count('orders')).order_by('customer_id')
            # if orders_count is None:
                # aov_customer = 0.00
            # else:
                # aov_customer = orders_sum / customers_count
            
            customers_top_five = Customer.objects.filter(orders__order_date__gte=datetime.datetime.now()-timedelta(days=30)).annotate(orders_count=Count('orders'), orders_sum=Sum('orders__value')).order_by('-orders_sum')[:5]
            customer_labels = []
            customer_data = []
            for customer in customers_top_five:
                customer_labels.append(customer.customer)
                if customer.orders_sum is not None:
                    customer_data.append(customer.orders_sum)
                else:
                    customer_data.append(0.00)

            cities_top_five = CustomerCity.objects.filter(orders_city__order_date__gte=datetime.datetime.now()-timedelta(days=30)).annotate(ord_count=Count('orders_city'), ord_sum=Sum('orders_city__value')).order_by('-ord_sum')[:5]
            city_labels = []
            city_data = []
            for city in cities_top_five:
                city_labels.append(city.customer_city)
                if city.ord_sum is not None:
                    city_data.append(city.ord_sum)
                else:
                    city_data.append(0.00)

        # ------------------- LAST 60 DAYS DATA -----------------------------------

        elif dataperiod == 'last_60_days':
            range = "Last 60 Days"
            range_orders = Order.objects.filter(order_date__gte=datetime.datetime.now()-timedelta(days=60))

            customers_count = range_orders.values('customer').distinct().count()
            orders_count = range_orders.count()
            orders_sum = range_orders.aggregate(Sum('value'))['value__sum']
            if orders_sum is None:
                orders_sum = 0.00
            if customers_count == 0:
                aov_customer = 0.00
            else:
                aov_customer = orders_sum / customers_count

            customers_info = Customer.objects.filter(orders__order_date__gte=datetime.datetime.now()-timedelta(days=60)).annotate(orders_count=Count('orders'), orders_sum=Sum('orders__value'), aov=Sum('orders__value')/Count('orders')).order_by('customer_id')
            # if orders_count is None:
                # aov_customer = 0.00
            # else:
                # aov_customer = orders_sum / customers_count
            
            customers_top_five = Customer.objects.filter(orders__order_date__gte=datetime.datetime.now()-timedelta(days=60)).annotate(orders_count=Count('orders'), orders_sum=Sum('orders__value')).order_by('-orders_sum')[:5]
            customer_labels = []
            customer_data = []
            for customer in customers_top_five:
                customer_labels.append(customer.customer)
                if customer.orders_sum is not None:
                    customer_data.append(customer.orders_sum)
                else:
                    customer_data.append(0.00)

            cities_top_five = CustomerCity.objects.filter(orders_city__order_date__gte=datetime.datetime.now()-timedelta(days=60)).annotate(ord_count=Count('orders_city'), ord_sum=Sum('orders_city__value')).order_by('-ord_sum')[:5]
            city_labels = []
            city_data = []
            for city in cities_top_five:
                city_labels.append(city.customer_city)
                if city.ord_sum is not None:
                    city_data.append(city.ord_sum)
                else:
                    city_data.append(0.00)


        # ------------------- LAST 90 DAYS DATA -----------------------------------

        elif dataperiod == 'last_90_days':
            range = "Last 90 Days"
            range_orders = Order.objects.filter(order_date__gte=datetime.datetime.now()-timedelta(days=90))

            customers_count = range_orders.values('customer').distinct().count()
            orders_count = range_orders.count()
            orders_sum = range_orders.aggregate(Sum('value'))['value__sum']
            if orders_sum is None:
                orders_sum = 0.00
            if customers_count == 0:
                aov_customer = 0.00
            else:
                aov_customer = orders_sum / customers_count

            customers_info = Customer.objects.filter(orders__order_date__gte=datetime.datetime.now()-timedelta(days=90)).annotate(orders_count=Count('orders'), orders_sum=Sum('orders__value'), aov=Sum('orders__value')/Count('orders')).order_by('customer_id')
            # if orders_count is None:
                # aov_customer = 0.00
            # else:
                # aov_customer = orders_sum / customers_count
            
            customers_top_five = Customer.objects.filter(orders__order_date__gte=datetime.datetime.now()-timedelta(days=90)).annotate(orders_count=Count('orders'), orders_sum=Sum('orders__value')).order_by('-orders_sum')[:5]
            customer_labels = []
            customer_data = []
            for customer in customers_top_five:
                customer_labels.append(customer.customer)
                if customer.orders_sum is not None:
                    customer_data.append(customer.orders_sum)
                else:
                    customer_data.append(0.00)

            cities_top_five = CustomerCity.objects.filter(orders_city__order_date__gte=datetime.datetime.now()-timedelta(days=90)).annotate(ord_count=Count('orders_city'), ord_sum=Sum('orders_city__value')).order_by('-ord_sum')[:5]
            city_labels = []
            city_data = []
            for city in cities_top_five:
                city_labels.append(city.customer_city)
                if city.ord_sum is not None:
                    city_data.append(city.ord_sum)
                else:
                    city_data.append(0.00)

        # ------------------- CURRENT MONTH DATA-----------

        elif dataperiod == 'current_month':
            range = "Current Month's"
            today = datetime.date.today()
            range_orders = Order.objects.filter(order_date__year=today.year, order_date__month=today.month)

            customers_count = range_orders.values('customer').distinct().count()
            orders_count = range_orders.count()
            orders_sum = range_orders.aggregate(Sum('value'))['value__sum']
            if orders_sum is None:
                orders_sum = 0.00
            if customers_count == 0:
                aov_customer = 0.00
            else:
                aov_customer = orders_sum / customers_count

            customers_info = Customer.objects.filter(orders__order_date__year=today.year, orders__order_date__month=today.month).annotate(orders_count=Count('orders'), orders_sum=Sum('orders__value'), aov=Sum('orders__value')/Count('orders')).order_by('customer_id')
            # if orders_count is None:
                # aov_customer = 0.00
            # else:
                # aov_customer = orders_sum / customers_count
            
            customers_top_five = Customer.objects.filter(orders__order_date__year=today.year, orders__order_date__month=today.month).annotate(orders_count=Count('orders'), orders_sum=Sum('orders__value')).order_by('-orders_sum')[:5]
            customer_labels = []
            customer_data = []
            for customer in customers_top_five:
                customer_labels.append(customer.customer)
                if customer.orders_sum is not None:
                    customer_data.append(customer.orders_sum)
                else:
                    customer_data.append(0.00)

            cities_top_five = CustomerCity.objects.filter(orders_city__order_date__year=today.year, orders_city__order_date__month=today.month).annotate(ord_count=Count('orders_city'), ord_sum=Sum('orders_city__value')).order_by('-ord_sum')[:5]
            city_labels = []
            city_data = []
            for city in cities_top_five:
                city_labels.append(city.customer_city)
                if city.ord_sum is not None:
                    city_data.append(city.ord_sum)
                else:
                    city_data.append(0.00)



        # ------------------- CURRENT YEAR DATA-----------

        elif dataperiod == 'current_month':
            range = "Current Month's"
            today = datetime.date.today()
            range_orders = Order.objects.filter(order_date__year=today.year)

            customers_count = range_orders.values('customer').distinct().count()
            orders_count = range_orders.count()
            orders_sum = range_orders.aggregate(Sum('value'))['value__sum']
            if orders_sum is None:
                orders_sum = 0.00
            if customers_count == 0:
                aov_customer = 0.00
            else:
                aov_customer = orders_sum / customers_count

            customers_info = Customer.objects.filter(orders__order_date__year=today.year).annotate(orders_count=Count('orders'), orders_sum=Sum('orders__value'), aov=Sum('orders__value')/Count('orders')).order_by('customer_id')
            # if orders_count is None:
                # aov_customer = 0.00
            # else:
                # aov_customer = orders_sum / customers_count
            
            customers_top_five = Customer.objects.filter(orders__order_date__year=today.year).annotate(orders_count=Count('orders'), orders_sum=Sum('orders__value')).order_by('-orders_sum')[:5]
            customer_labels = []
            customer_data = []
            for customer in customers_top_five:
                customer_labels.append(customer.customer)
                if customer.orders_sum is not None:
                    customer_data.append(customer.orders_sum)
                else:
                    customer_data.append(0.00)

            cities_top_five = CustomerCity.objects.filter(orders_city__order_date__year=today.year).annotate(ord_count=Count('orders_city'), ord_sum=Sum('orders_city__value')).order_by('-ord_sum')[:5]
            city_labels = []
            city_data = []
            for city in cities_top_five:
                city_labels.append(city.customer_city)
                if city.ord_sum is not None:
                    city_data.append(city.ord_sum)
                else:
                    city_data.append(0.00)


    myFilter = CustomerFilter(request.GET, queryset=customers_info)
    customers_info = myFilter.qs

    context = {
        'range': range,
        'customers_count': customers_count,
        'orders_count': orders_count,
        'orders_sum': orders_sum,
        'aov_customer': aov_customer,
        'customers_info': customers_info,
        'customers_top_five': customers_top_five,
        'customer_labels': customer_labels,
        'customer_data': customer_data,
        'cities_top_five': cities_top_five,
        'city_labels': city_labels,
        'city_data': city_data,
        'myFilter': myFilter,
    }
    return render(request,'accounts/customers/customers.html', context)



@login_required(login_url='login')
def expenses_general(request):

    range = "All Time"
    customers_count = Customer.objects.all().count()
    orders_count = Order.objects.all().count()
    orders_sum = Order.objects.all().aggregate(Sum('value'))['value__sum']
    if orders_count is not None and orders_sum is not None:
        average_order_value = orders_sum / orders_count
    else:
        average_order_value = 0.00
    
    orders_expenses = OrderExpense.objects.all().aggregate(Sum('expense_amount'))['expense_amount__sum']
    
    if orders_sum is None:
        orders_sum = 0.00
    if orders_expenses is None:
        orders_expenses = 0.00
    gross_profit = orders_sum - orders_expenses

    if orders_sum == 0.00:
        gross_profit_percentage = 0.00
    else:
        gross_profit_percentage = (gross_profit / orders_sum) * 100
    
    other_expenses = GeneralExpense.objects.all().aggregate(Sum('expense_amount'))['expense_amount__sum']

    if other_expenses is None:
        other_expenses = 0.00
    net_profit = gross_profit - other_expenses

    if orders_sum == 0.00:
        net_profit_percentage = 0.00
    else:
        net_profit_percentage = (net_profit / orders_sum) * 100
    
    expenses_category = GeneralExpenseCategory.objects.annotate(cat_count=Count('gen_expense_category'), cat_sum=Sum('gen_expense_category__expense_amount')).order_by('-cat_count')
    category_labels = []
    category_data = []
    for category in expenses_category:
        category_labels.append(category.general_expense_category)
        if category.cat_sum is not None:
            category_data.append(category.cat_sum)
        else:
            category_data.append(0.00)
    
    expenses_mode = GeneralExpenseMode.objects.annotate(mode_count=Count('general_expense_mode'), mode_sum=Sum('general_expense_mode__expense_amount')).order_by('-mode_count')
    mode_labels = []
    mode_data = []
    for mode in expenses_mode:
        mode_labels.append(mode.expense_mode)
        if mode.mode_sum is not None:
            mode_data.append(mode.mode_sum)
        else:
            mode_data.append(0.00)

    general_expenses = GeneralExpense.objects.all()

    if request.method == 'POST':
        dataperiod = request.POST.get('dataperiod')
    
        # ------------------- TODAY'S DATA -----------------------------------

        if dataperiod == 'today':
            range = "Today's"
            range_orders = Order.objects.filter(order_date__gte=datetime.datetime.now()-timedelta(days=0))
    
            customers_count = range_orders.values('customer').distinct().count()
            orders_count = range_orders.count()
            if orders_count is None:
                orders_count = 0
            orders_sum = range_orders.aggregate(Sum('value'))['value__sum']
            if orders_sum is None:
                orders_sum = 0.00
            if orders_count == 0:
                average_order_value = 0.00
            else:
                average_order_value = orders_sum / orders_count
            
            orders_expenses = 0.00
            for order in range_orders:
                order_expense = OrderExpense.objects.filter(order_ref=order).aggregate(Sum('expense_amount'))['expense_amount__sum']
                if order_expense is not None:
                    orders_expenses += order_expense
                else:
                    orders_expenses = orders_expenses + 0.00
            
            if orders_expenses is None:
                orders_expenses = 0.00
            gross_profit = orders_sum - orders_expenses
            if orders_sum == 0.00:
                gross_profit_percentage = 0.00
            else:
                gross_profit_percentage = (gross_profit / orders_sum) * 100    
            
            other_expenses = GeneralExpense.objects.filter(expense_date__gte=datetime.datetime.now()-timedelta(days=0)).aggregate(Sum('expense_amount'))['expense_amount__sum']
            if other_expenses is None:
                other_expenses = 0.00
            net_profit = gross_profit - other_expenses
            if orders_sum == 0.00:
                net_profit_percentage = 0.00
            else:
                net_profit_percentage = (net_profit / orders_sum) * 100
            
            expenses_category = GeneralExpenseCategory.objects.filter(gen_expense_category__expense_date__gte=datetime.datetime.now()-timedelta(days=0)).annotate(cat_count=Count('gen_expense_category'), cat_sum=Sum('gen_expense_category__expense_amount')).order_by('-cat_count')
            category_labels = []
            category_data = []
            for category in expenses_category:
                category_labels.append(category.general_expense_category)
                if category.cat_sum is not None:
                    category_data.append(category.cat_sum)
                else:
                    category_data.append(0.00)
            
            expenses_mode = GeneralExpenseMode.objects.filter(general_expense_mode__expense_date__gte=datetime.datetime.now()-timedelta(days=0)).annotate(mode_count=Count('general_expense_mode'), mode_sum=Sum('general_expense_mode__expense_amount')).order_by('-mode_count')
            mode_labels = []
            mode_data = []
            for mode in expenses_mode:
                mode_labels.append(mode.expense_mode)
                if mode.mode_sum is not None:
                    mode_data.append(mode.mode_sum)
                else:
                    mode_data.append(0.00)

            general_expenses = GeneralExpense.objects.filter(expense_date__gte=datetime.datetime.now()-timedelta(days=0))



        # ------------------- LAST 7 DAYS DATA -----------------------------------

        elif dataperiod == 'last_7_days':
            range = "Last 7 Days"
            range_orders = Order.objects.filter(order_date__gte=datetime.datetime.now()-timedelta(days=7))
    
            customers_count = range_orders.values('customer').distinct().count()
            orders_count = range_orders.count()
            if orders_count is None:
                orders_count = 0
            orders_sum = range_orders.aggregate(Sum('value'))['value__sum']
            if orders_sum is None:
                orders_sum = 0.00
            if orders_count == 0:
                average_order_value = 0.00
            else:
                average_order_value = orders_sum / orders_count
            
            orders_expenses = 0.00
            for order in range_orders:
                order_expense = OrderExpense.objects.filter(order_ref=order).aggregate(Sum('expense_amount'))['expense_amount__sum']
                if order_expense is not None:
                    orders_expenses += order_expense
                else:
                    orders_expenses = orders_expenses + 0.00
            
            if orders_expenses is None:
                orders_expenses = 0.00
            gross_profit = orders_sum - orders_expenses
            if orders_sum == 0.00:
                gross_profit_percentage = 0.00
            else:
                gross_profit_percentage = (gross_profit / orders_sum) * 100    
            
            other_expenses = GeneralExpense.objects.filter(expense_date__gte=datetime.datetime.now()-timedelta(days=7)).aggregate(Sum('expense_amount'))['expense_amount__sum']
            if other_expenses is None:
                other_expenses = 0.00
            net_profit = gross_profit - other_expenses
            if orders_sum == 0.00:
                net_profit_percentage = 0.00
            else:
                net_profit_percentage = (net_profit / orders_sum) * 100
            
            expenses_category = GeneralExpenseCategory.objects.filter(gen_expense_category__expense_date__gte=datetime.datetime.now()-timedelta(days=7)).annotate(cat_count=Count('gen_expense_category'), cat_sum=Sum('gen_expense_category__expense_amount')).order_by('-cat_count')
            category_labels = []
            category_data = []
            for category in expenses_category:
                category_labels.append(category.general_expense_category)
                if category.cat_sum is not None:
                    category_data.append(category.cat_sum)
                else:
                    category_data.append(0.00)
            
            expenses_mode = GeneralExpenseMode.objects.filter(general_expense_mode__expense_date__gte=datetime.datetime.now()-timedelta(days=7)).annotate(mode_count=Count('general_expense_mode'), mode_sum=Sum('general_expense_mode__expense_amount')).order_by('-mode_count')
            mode_labels = []
            mode_data = []
            for mode in expenses_mode:
                mode_labels.append(mode.expense_mode)
                if mode.mode_sum is not None:
                    mode_data.append(mode.mode_sum)
                else:
                    mode_data.append(0.00)

            general_expenses = GeneralExpense.objects.filter(expense_date__gte=datetime.datetime.now()-timedelta(days=7))



        # ------------------- LAST 30 DAYS DATA -----------------------------------

        elif dataperiod == 'last_30_days':
            range = "Last 30 Days"
            range_orders = Order.objects.filter(order_date__gte=datetime.datetime.now()-timedelta(days=30))
    
            customers_count = range_orders.values('customer').distinct().count()
            orders_count = range_orders.count()
            if orders_count is None:
                orders_count = 0
            orders_sum = range_orders.aggregate(Sum('value'))['value__sum']
            if orders_sum is None:
                orders_sum = 0.00
            if orders_count == 0:
                average_order_value = 0.00
            else:
                average_order_value = orders_sum / orders_count
            
            orders_expenses = 0.00
            for order in range_orders:
                order_expense = OrderExpense.objects.filter(order_ref=order).aggregate(Sum('expense_amount'))['expense_amount__sum']
                if order_expense is not None:
                    orders_expenses += order_expense
                else:
                    orders_expenses = orders_expenses + 0.00
            
            if orders_expenses is None:
                orders_expenses = 0.00
            gross_profit = orders_sum - orders_expenses
            if orders_sum == 0.00:
                gross_profit_percentage = 0.00
            else:
                gross_profit_percentage = (gross_profit / orders_sum) * 100    
            
            other_expenses = GeneralExpense.objects.filter(expense_date__gte=datetime.datetime.now()-timedelta(days=30)).aggregate(Sum('expense_amount'))['expense_amount__sum']
            if other_expenses is None:
                other_expenses = 0.00
            net_profit = gross_profit - other_expenses
            if orders_sum == 0.00:
                net_profit_percentage = 0.00
            else:
                net_profit_percentage = (net_profit / orders_sum) * 100
            
            expenses_category = GeneralExpenseCategory.objects.filter(gen_expense_category__expense_date__gte=datetime.datetime.now()-timedelta(days=30)).annotate(cat_count=Count('gen_expense_category'), cat_sum=Sum('gen_expense_category__expense_amount')).order_by('-cat_count')
            category_labels = []
            category_data = []
            for category in expenses_category:
                category_labels.append(category.general_expense_category)
                if category.cat_sum is not None:
                    category_data.append(category.cat_sum)
                else:
                    category_data.append(0.00)
            
            expenses_mode = GeneralExpenseMode.objects.filter(general_expense_mode__expense_date__gte=datetime.datetime.now()-timedelta(days=30)).annotate(mode_count=Count('general_expense_mode'), mode_sum=Sum('general_expense_mode__expense_amount')).order_by('-mode_count')
            mode_labels = []
            mode_data = []
            for mode in expenses_mode:
                mode_labels.append(mode.expense_mode)
                if mode.mode_sum is not None:
                    mode_data.append(mode.mode_sum)
                else:
                    mode_data.append(0.00)

            general_expenses = GeneralExpense.objects.filter(expense_date__gte=datetime.datetime.now()-timedelta(days=30))




        # ------------------- LAST 60 DAYS DATA -----------------------------------

        elif dataperiod == 'last_60_days':
            range = "Last 60 Days"
            range_orders = Order.objects.filter(order_date__gte=datetime.datetime.now()-timedelta(days=60))
    
            customers_count = range_orders.values('customer').distinct().count()
            orders_count = range_orders.count()
            if orders_count is None:
                orders_count = 0
            orders_sum = range_orders.aggregate(Sum('value'))['value__sum']
            if orders_sum is None:
                orders_sum = 0.00
            if orders_count == 0:
                average_order_value = 0.00
            else:
                average_order_value = orders_sum / orders_count
            
            orders_expenses = 0.00
            for order in range_orders:
                order_expense = OrderExpense.objects.filter(order_ref=order).aggregate(Sum('expense_amount'))['expense_amount__sum']
                if order_expense is not None:
                    orders_expenses += order_expense
                else:
                    orders_expenses = orders_expenses + 0.00
            
            if orders_expenses is None:
                orders_expenses = 0.00
            gross_profit = orders_sum - orders_expenses
            if orders_sum == 0.00:
                gross_profit_percentage = 0.00
            else:
                gross_profit_percentage = (gross_profit / orders_sum) * 100    
            
            other_expenses = GeneralExpense.objects.filter(expense_date__gte=datetime.datetime.now()-timedelta(days=60)).aggregate(Sum('expense_amount'))['expense_amount__sum']
            if other_expenses is None:
                other_expenses = 0.00
            net_profit = gross_profit - other_expenses
            if orders_sum == 0.00:
                net_profit_percentage = 0.00
            else:
                net_profit_percentage = (net_profit / orders_sum) * 100
            
            expenses_category = GeneralExpenseCategory.objects.filter(gen_expense_category__expense_date__gte=datetime.datetime.now()-timedelta(days=60)).annotate(cat_count=Count('gen_expense_category'), cat_sum=Sum('gen_expense_category__expense_amount')).order_by('-cat_count')
            category_labels = []
            category_data = []
            for category in expenses_category:
                category_labels.append(category.general_expense_category)
                if category.cat_sum is not None:
                    category_data.append(category.cat_sum)
                else:
                    category_data.append(0.00)
            
            expenses_mode = GeneralExpenseMode.objects.filter(general_expense_mode__expense_date__gte=datetime.datetime.now()-timedelta(days=60)).annotate(mode_count=Count('general_expense_mode'), mode_sum=Sum('general_expense_mode__expense_amount')).order_by('-mode_count')
            mode_labels = []
            mode_data = []
            for mode in expenses_mode:
                mode_labels.append(mode.expense_mode)
                if mode.mode_sum is not None:
                    mode_data.append(mode.mode_sum)
                else:
                    mode_data.append(0.00)

            general_expenses = GeneralExpense.objects.filter(expense_date__gte=datetime.datetime.now()-timedelta(days=60))




        # ------------------- LAST 90 DAYS DATA -----------------------------------

        elif dataperiod == 'last_90_days':
            range = "Last 90 Days"
            range_orders = Order.objects.filter(order_date__gte=datetime.datetime.now()-timedelta(days=90))
    
            customers_count = range_orders.values('customer').distinct().count()
            orders_count = range_orders.count()
            if orders_count is None:
                orders_count = 0
            orders_sum = range_orders.aggregate(Sum('value'))['value__sum']
            if orders_sum is None:
                orders_sum = 0.00
            if orders_count == 0:
                average_order_value = 0.00
            else:
                average_order_value = orders_sum / orders_count
            
            orders_expenses = 0.00
            for order in range_orders:
                order_expense = OrderExpense.objects.filter(order_ref=order).aggregate(Sum('expense_amount'))['expense_amount__sum']
                if order_expense is not None:
                    orders_expenses += order_expense
                else:
                    orders_expenses = orders_expenses + 0.00
            
            if orders_expenses is None:
                orders_expenses = 0.00
            gross_profit = orders_sum - orders_expenses
            if orders_sum == 0.00:
                gross_profit_percentage = 0.00
            else:
                gross_profit_percentage = (gross_profit / orders_sum) * 100    
            
            other_expenses = GeneralExpense.objects.filter(expense_date__gte=datetime.datetime.now()-timedelta(days=90)).aggregate(Sum('expense_amount'))['expense_amount__sum']
            if other_expenses is None:
                other_expenses = 0.00
            net_profit = gross_profit - other_expenses
            if orders_sum == 0.00:
                net_profit_percentage = 0.00
            else:
                net_profit_percentage = (net_profit / orders_sum) * 100
            
            expenses_category = GeneralExpenseCategory.objects.filter(gen_expense_category__expense_date__gte=datetime.datetime.now()-timedelta(days=90)).annotate(cat_count=Count('gen_expense_category'), cat_sum=Sum('gen_expense_category__expense_amount')).order_by('-cat_count')
            category_labels = []
            category_data = []
            for category in expenses_category:
                category_labels.append(category.general_expense_category)
                if category.cat_sum is not None:
                    category_data.append(category.cat_sum)
                else:
                    category_data.append(0.00)
            
            expenses_mode = GeneralExpenseMode.objects.filter(general_expense_mode__expense_date__gte=datetime.datetime.now()-timedelta(days=90)).annotate(mode_count=Count('general_expense_mode'), mode_sum=Sum('general_expense_mode__expense_amount')).order_by('-mode_count')
            mode_labels = []
            mode_data = []
            for mode in expenses_mode:
                mode_labels.append(mode.expense_mode)
                if mode.mode_sum is not None:
                    mode_data.append(mode.mode_sum)
                else:
                    mode_data.append(0.00)

            general_expenses = GeneralExpense.objects.filter(expense_date__gte=datetime.datetime.now()-timedelta(days=90))



        # ------------------- CURRENT MONTH -----------------------------------

        elif dataperiod == 'current_month':
            range = "Current Month's"
            today = datetime.date.today()
            range_orders = Order.objects.filter(order_date__year=today.year, order_date__month=today.month)
    
            customers_count = range_orders.values('customer').distinct().count()
            orders_count = range_orders.count()
            if orders_count is None:
                orders_count = 0
            orders_sum = range_orders.aggregate(Sum('value'))['value__sum']
            if orders_sum is None:
                orders_sum = 0.00
            if orders_count == 0:
                average_order_value = 0.00
            else:
                average_order_value = orders_sum / orders_count
            
            orders_expenses = 0.00
            for order in range_orders:
                order_expense = OrderExpense.objects.filter(order_ref=order).aggregate(Sum('expense_amount'))['expense_amount__sum']
                if order_expense is not None:
                    orders_expenses += order_expense
                else:
                    orders_expenses = orders_expenses + 0.00
            
            if orders_expenses is None:
                orders_expenses = 0.00
            gross_profit = orders_sum - orders_expenses
            if orders_sum == 0.00:
                gross_profit_percentage = 0.00
            else:
                gross_profit_percentage = (gross_profit / orders_sum) * 100    
            
            other_expenses = GeneralExpense.objects.filter(expense_date__year=today.year, expense_date__month=today.month).aggregate(Sum('expense_amount'))['expense_amount__sum']
            if other_expenses is None:
                other_expenses = 0.00
            net_profit = gross_profit - other_expenses
            if orders_sum == 0.00:
                net_profit_percentage = 0.00
            else:
                net_profit_percentage = (net_profit / orders_sum) * 100
            
            expenses_category = GeneralExpenseCategory.objects.filter(gen_expense_category__expense_date__year=today.year, gen_expense_category__expense_date__month=today.month).annotate(cat_count=Count('gen_expense_category'), cat_sum=Sum('gen_expense_category__expense_amount')).order_by('-cat_count')
            category_labels = []
            category_data = []
            for category in expenses_category:
                category_labels.append(category.general_expense_category)
                if category.cat_sum is not None:
                    category_data.append(category.cat_sum)
                else:
                    category_data.append(0.00)
            
            expenses_mode = GeneralExpenseMode.objects.filter(general_expense_mode__expense_date__year=today.year, general_expense_mode__expense_date__month=today.month).annotate(mode_count=Count('general_expense_mode'), mode_sum=Sum('general_expense_mode__expense_amount')).order_by('-mode_count')
            mode_labels = []
            mode_data = []
            for mode in expenses_mode:
                mode_labels.append(mode.expense_mode)
                if mode.mode_sum is not None:
                    mode_data.append(mode.mode_sum)
                else:
                    mode_data.append(0.00)

            general_expenses = GeneralExpense.objects.filter(expense_date__year=today.year, expense_date__month=today.month)



        # ------------------- CURRENT YEAR -----------------------------------

        elif dataperiod == 'current_year':
            range = "Current Year's"
            today = datetime.date.today()
            range_orders = Order.objects.filter(order_date__year=today.year)
    
            customers_count = range_orders.values('customer').distinct().count()
            orders_count = range_orders.count()
            if orders_count is None:
                orders_count = 0
            orders_sum = range_orders.aggregate(Sum('value'))['value__sum']
            if orders_sum is None:
                orders_sum = 0.00
            if orders_count == 0:
                average_order_value = 0.00
            else:
                average_order_value = orders_sum / orders_count
            
            orders_expenses = 0.00
            for order in range_orders:
                order_expense = OrderExpense.objects.filter(order_ref=order).aggregate(Sum('expense_amount'))['expense_amount__sum']
                if order_expense is not None:
                    orders_expenses += order_expense
                else:
                    orders_expenses = orders_expenses + 0.00
            
            if orders_expenses is None:
                orders_expenses = 0.00
            gross_profit = orders_sum - orders_expenses
            if orders_sum == 0.00:
                gross_profit_percentage = 0.00
            else:
                gross_profit_percentage = (gross_profit / orders_sum) * 100    
            
            other_expenses = GeneralExpense.objects.filter(expense_date__year=today.year).aggregate(Sum('expense_amount'))['expense_amount__sum']
            if other_expenses is None:
                other_expenses = 0.00
            net_profit = gross_profit - other_expenses
            if orders_sum == 0.00:
                net_profit_percentage = 0.00
            else:
                net_profit_percentage = (net_profit / orders_sum) * 100
            
            expenses_category = GeneralExpenseCategory.objects.filter(gen_expense_category__expense_date__year=today.year).annotate(cat_count=Count('gen_expense_category'), cat_sum=Sum('gen_expense_category__expense_amount')).order_by('-cat_count')
            category_labels = []
            category_data = []
            for category in expenses_category:
                category_labels.append(category.general_expense_category)
                if category.cat_sum is not None:
                    category_data.append(category.cat_sum)
                else:
                    category_data.append(0.00)
            
            expenses_mode = GeneralExpenseMode.objects.filter(general_expense_mode__expense_date__year=today.year).annotate(mode_count=Count('general_expense_mode'), mode_sum=Sum('general_expense_mode__expense_amount')).order_by('-mode_count')
            mode_labels = []
            mode_data = []
            for mode in expenses_mode:
                mode_labels.append(mode.expense_mode)
                if mode.mode_sum is not None:
                    mode_data.append(mode.mode_sum)
                else:
                    mode_data.append(0.00)

            general_expenses = GeneralExpense.objects.filter(expense_date__year=today.year)    


    myFilter = GeneralExpenseFilter(request.GET, queryset=general_expenses)
    general_expenses = myFilter.qs

    context = {
        'range': range,
        'customers_count': customers_count,
        'orders_count': orders_count,
        'orders_sum': orders_sum,
        'average_order_value': average_order_value,
        'orders_expenses': orders_expenses,
        'gross_profit': gross_profit,
        'gross_profit_percentage': gross_profit_percentage,
        'other_expenses': other_expenses,
        'net_profit': net_profit,
        'net_profit_percentage': net_profit_percentage,
        'expenses_category': expenses_category,
        'category_labels': category_labels,
        'category_data': category_data,
        'expenses_mode': expenses_mode,
        'mode_labels': mode_labels,
        'mode_data': mode_data,
        'general_expenses': general_expenses,
        'myFilter': myFilter,
    }
    return render(request,'accounts/expenses-general/expenses-general.html', context)



@login_required(login_url='login')
def expenses_general_add(request):
    form = GeneralExpenseForm
    if request.method == 'POST':
        form = GeneralExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/expenses-general/')
    context = {
        'form': form,
    }
    return render(request,'accounts/expenses-general/expenses-general-add.html', context)




@login_required(login_url='login')
def expenses_general_delete(request, pk):
    expense = GeneralExpense.objects.get(id=pk)
    if request.method == 'POST':
        expense.delete()
        return redirect('/expenses-general/')
    context= {
        'expense': expense,
    }
    return render(request,'accounts/expenses-general/expenses-general-delete.html', context)




@login_required(login_url='login')
def expenses_general_edit(request, pk):
    expense = GeneralExpense.objects.get(id=pk)
    form = GeneralExpenseForm(instance=expense)
    if request.method == 'POST':
        form = GeneralExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('/expenses-general/')
    context = {
        'form': form,
    }
    return render(request,'accounts/expenses-general/expenses-general-edit.html', context)




@login_required(login_url='login')
def expense_categories_general(request):

    range = "All Time"
    expenses_category = GeneralExpenseCategory.objects.annotate(cat_count=Count('gen_expense_category'), cat_sum=Sum('gen_expense_category__expense_amount')).order_by('-cat_count')
    
    category_labels = []
    category_data = []
    for category in expenses_category:
        category_labels.append(category.general_expense_category)
        if category.cat_sum is not None:
            category_data.append(category.cat_sum)
        else:
            category_data.append(0.00)
    
    if request.method == 'POST':
        dataperiod = request.POST.get('dataperiod')

        # ------------------- TODAY'S DATA -----------------------------------

        if dataperiod == 'today':
            range = "Today's"
            expenses_category = GeneralExpenseCategory.objects.filter(gen_expense_category__expense_date__gte=datetime.datetime.now()-timedelta(days=0)).annotate(cat_count=Count('gen_expense_category'), cat_sum=Sum('gen_expense_category__expense_amount')).order_by('-cat_count')

            category_labels = []
            category_data = []
            for category in expenses_category:
                category_labels.append(category.general_expense_category)
                if category.cat_sum is not None:
                    category_data.append(category.cat_sum)
                else:
                    category_data.append(0.00)



        # ------------------- LAST 7 DAYS DATA -----------------------------------

        elif dataperiod == 'last_7_days':
            range = "Last 7 Days"
            expenses_category = GeneralExpenseCategory.objects.filter(gen_expense_category__expense_date__gte=datetime.datetime.now()-timedelta(days=7)).annotate(cat_count=Count('gen_expense_category'), cat_sum=Sum('gen_expense_category__expense_amount')).order_by('-cat_count')

            category_labels = []
            category_data = []
            for category in expenses_category:
                category_labels.append(category.general_expense_category)
                if category.cat_sum is not None:
                    category_data.append(category.cat_sum)
                else:
                    category_data.append(0.00)



        # ------------------- LAST 30 DAYS DATA -----------------------------------

        elif dataperiod == 'last_30_days':
            range = "Last 30 Days"
            expenses_category = GeneralExpenseCategory.objects.filter(gen_expense_category__expense_date__gte=datetime.datetime.now()-timedelta(days=30)).annotate(cat_count=Count('gen_expense_category'), cat_sum=Sum('gen_expense_category__expense_amount')).order_by('-cat_count')

            category_labels = []
            category_data = []
            for category in expenses_category:
                category_labels.append(category.general_expense_category)
                if category.cat_sum is not None:
                    category_data.append(category.cat_sum)
                else:
                    category_data.append(0.00)



        # ------------------- LAST 60 DAYS DATA -----------------------------------

        elif dataperiod == 'last_60_days':
            range = "Last 60 Days"
            expenses_category = GeneralExpenseCategory.objects.filter(gen_expense_category__expense_date__gte=datetime.datetime.now()-timedelta(days=60)).annotate(cat_count=Count('gen_expense_category'), cat_sum=Sum('gen_expense_category__expense_amount')).order_by('-cat_count')

            category_labels = []
            category_data = []
            for category in expenses_category:
                category_labels.append(category.general_expense_category)
                if category.cat_sum is not None:
                    category_data.append(category.cat_sum)
                else:
                    category_data.append(0.00)



        # ------------------- LAST 90 DAYS DATA -----------------------------------

        elif dataperiod == 'last_90_days':
            range = "Last 90 Days"
            expenses_category = GeneralExpenseCategory.objects.filter(gen_expense_category__expense_date__gte=datetime.datetime.now()-timedelta(days=90)).annotate(cat_count=Count('gen_expense_category'), cat_sum=Sum('gen_expense_category__expense_amount')).order_by('-cat_count')

            category_labels = []
            category_data = []
            for category in expenses_category:
                category_labels.append(category.general_expense_category)
                if category.cat_sum is not None:
                    category_data.append(category.cat_sum)
                else:
                    category_data.append(0.00)



        # ------------------- CURRENT MONTH DATA -----------------------------------

        elif dataperiod == 'current_month':
            range = "Current Month's"
            today = datetime.date.today()
            expenses_category = GeneralExpenseCategory.objects.filter(gen_expense_category__expense_date__year=today.year, gen_expense_category__expense_date__month=today.month).annotate(cat_count=Count('gen_expense_category'), cat_sum=Sum('gen_expense_category__expense_amount')).order_by('-cat_count')

            category_labels = []
            category_data = []
            for category in expenses_category:
                category_labels.append(category.general_expense_category)
                if category.cat_sum is not None:
                    category_data.append(category.cat_sum)
                else:
                    category_data.append(0.00)



        # ------------------- CURRENT YEAR DATA -----------------------------------

        elif dataperiod == 'current_year':
            range = "Current Year's"
            today = datetime.date.today()
            expenses_category = GeneralExpenseCategory.objects.filter(gen_expense_category__expense_date__year=today.year).annotate(cat_count=Count('gen_expense_category'), cat_sum=Sum('gen_expense_category__expense_amount')).order_by('-cat_count')

            category_labels = []
            category_data = []
            for category in expenses_category:
                category_labels.append(category.general_expense_category)
                if category.cat_sum is not None:
                    category_data.append(category.cat_sum)
                else:
                    category_data.append(0.00)


    context = {
        'range': range,
        'expenses_category': expenses_category,
        'category_labels': category_labels,
        'category_data': category_data,
    }
    return render(request,'accounts/expense-categories-general/expense-categories-general.html', context)




@login_required(login_url='login')
def expense_categories_general_add(request):
    form = GeneralExpenseCategoryForm
    if request.method == 'POST':
        form = GeneralExpenseCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/expense-categories-general/')
    context = {
        'form': form,
    }
    return render(request,'accounts/expense-categories-general/expense-categories-general-add.html', context)




@login_required(login_url='login')
def expense_categories_general_delete(request, pk):
    category = GeneralExpenseCategory.objects.get(id=pk)
    category_name = category.general_expense_category
    if request.method == 'POST':
        category.delete()
        return redirect('/expense-categories-general/')
    context = {
        'category': category,
        'category_name': category_name,
    }
    return render(request,'accounts/expense-categories-general/expense-categories-general-delete.html', context)




@login_required(login_url='login')
def expense_categories_general_edit(request, pk):
    category = GeneralExpenseCategory.objects.get(id=pk)
    category_name = category.general_expense_category
    form = GeneralExpenseCategoryForm(instance=category)
    if request.method == 'POST':
        form = GeneralExpenseCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('/expense-categories-general/')
    context = {
        'category_name': category_name,
        'form': form,
    }
    return render(request,'accounts/expense-categories-general/expense-categories-general-edit.html', context)






@login_required(login_url='login')
def expense_modes_general(request):
    range = "All Time"
    expense_mode = GeneralExpenseMode.objects.annotate(mode_count=Count('general_expense_mode'), mode_sum=Sum('general_expense_mode__expense_amount')).order_by('-mode_count')
    mode_labels = []
    mode_data = []
    for mode in expense_mode:
        mode_labels.append(mode.expense_mode)
        if mode.mode_sum is not None:
            mode_data.append(mode.mode_sum)
        else:
            mode_data.append(0.00)

    if request.method == 'POST':
        dataperiod = request.POST.get('dataperiod')

        # ------------------- TODAY'S DATA -----------------------------------

        if dataperiod == 'today':
            range = "Today's"
            expense_mode = GeneralExpenseMode.objects.filter(general_expense_mode__expense_date__gte=datetime.datetime.now()-timedelta(days=0)).annotate(mode_count=Count('general_expense_mode'), mode_sum=Sum('general_expense_mode__expense_amount')).order_by('-mode_count')
            mode_labels = []
            mode_data = []
            for mode in expense_mode:
                mode_labels.append(mode.expense_mode)
                if mode.mode_sum is not None:
                    mode_data.append(mode.mode_sum)
                else:
                    mode_data.append(0.00)



        # ------------------- LAST 7 DAYS DATA -----------------------------------

        elif dataperiod == 'last_7_days':
            range = "Last 7 Days"
            expense_mode = GeneralExpenseMode.objects.filter(general_expense_mode__expense_date__gte=datetime.datetime.now()-timedelta(days=7)).annotate(mode_count=Count('general_expense_mode'), mode_sum=Sum('general_expense_mode__expense_amount')).order_by('-mode_count')
            mode_labels = []
            mode_data = []
            for mode in expense_mode:
                mode_labels.append(mode.expense_mode)
                if mode.mode_sum is not None:
                    mode_data.append(mode.mode_sum)
                else:
                    mode_data.append(0.00)



        # ------------------- LAST 30 DAYS DATA -----------------------------------

        elif dataperiod == 'last_30_days':
            range = "Last 30 Days"
            expense_mode = GeneralExpenseMode.objects.filter(general_expense_mode__expense_date__gte=datetime.datetime.now()-timedelta(days=30)).annotate(mode_count=Count('general_expense_mode'), mode_sum=Sum('general_expense_mode__expense_amount')).order_by('-mode_count')
            mode_labels = []
            mode_data = []
            for mode in expense_mode:
                mode_labels.append(mode.expense_mode)
                if mode.mode_sum is not None:
                    mode_data.append(mode.mode_sum)
                else:
                    mode_data.append(0.00)



        # ------------------- LAST 60 DAYS DATA -----------------------------------

        elif dataperiod == 'last_60_days':
            range = "Last 60 Days"
            expense_mode = GeneralExpenseMode.objects.filter(general_expense_mode__expense_date__gte=datetime.datetime.now()-timedelta(days=60)).annotate(mode_count=Count('general_expense_mode'), mode_sum=Sum('general_expense_mode__expense_amount')).order_by('-mode_count')
            mode_labels = []
            mode_data = []
            for mode in expense_mode:
                mode_labels.append(mode.expense_mode)
                if mode.mode_sum is not None:
                    mode_data.append(mode.mode_sum)
                else:
                    mode_data.append(0.00)




        # ------------------- LAST 90 DAYS DATA -----------------------------------

        elif dataperiod == 'last_90_days':
            range = "Last 90 Days"
            expense_mode = GeneralExpenseMode.objects.filter(general_expense_mode__expense_date__gte=datetime.datetime.now()-timedelta(days=90)).annotate(mode_count=Count('general_expense_mode'), mode_sum=Sum('general_expense_mode__expense_amount')).order_by('-mode_count')
            mode_labels = []
            mode_data = []
            for mode in expense_mode:
                mode_labels.append(mode.expense_mode)
                if mode.mode_sum is not None:
                    mode_data.append(mode.mode_sum)
                else:
                    mode_data.append(0.00)



        # ------------------- CURRENT MONTH DATA -----------------------------------

        elif dataperiod == 'current_month':
            range = "Current Month's"
            today = datetime.date.today()
            expense_mode = GeneralExpenseMode.objects.filter(general_expense_mode__expense_date__year=today.year, general_expense_mode__expense_date__month=today.month).annotate(mode_count=Count('general_expense_mode'), mode_sum=Sum('general_expense_mode__expense_amount')).order_by('-mode_count')
            mode_labels = []
            mode_data = []
            for mode in expense_mode:
                mode_labels.append(mode.expense_mode)
                if mode.mode_sum is not None:
                    mode_data.append(mode.mode_sum)
                else:
                    mode_data.append(0.00)



        # ------------------- CURRENT YEAR DATA -----------------------------------

        elif dataperiod == 'current_year':
            range = "Current Year"
            today = datetime.date.today()
            expense_mode = GeneralExpenseMode.objects.filter(general_expense_mode__expense_date__year=today.year).annotate(mode_count=Count('general_expense_mode'), mode_sum=Sum('general_expense_mode__expense_amount')).order_by('-mode_count')
            mode_labels = []
            mode_data = []
            for mode in expense_mode:
                mode_labels.append(mode.expense_mode)
                if mode.mode_sum is not None:
                    mode_data.append(mode.mode_sum)
                else:
                    mode_data.append(0.00)


    context = {
        'range': range,
        'expense_mode': expense_mode,
        'mode_labels': mode_labels,
        'mode_data': mode_data,
    }
    return render(request,'accounts/expense-modes-general/expense-modes-general.html', context)





@login_required(login_url='login')
def expense_modes_general_add(request):
    form = GeneralExpenseModeForm
    if request.method == 'POST':
        form = GeneralExpenseModeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/expense-modes-general/')
    context = {
        'form': form,
    }
    return render(request,'accounts/expense-modes-general/expense-modes-general-add.html', context)




@login_required(login_url='login')
def expense_modes_general_delete(request, pk):
    mode = GeneralExpenseMode.objects.get(id=pk)
    expense_mode = mode.expense_mode
    if request.method == 'POST':
        mode.delete()
        return redirect('/expense-modes-general/')
    context = {
        'mode': mode,
        'expense_mode': expense_mode,
    }
    return render(request,'accounts/expense-modes-general/expense-modes-general-delete.html', context)




@login_required(login_url='login')
def expense_modes_general_edit(request, pk):
    mode = GeneralExpenseMode.objects.get(id=pk)
    expense_mode = mode.expense_mode
    form = GeneralExpenseModeForm(instance=mode)
    if request.method == 'POST':
        form = GeneralExpenseModeForm(request.POST, instance=mode)
        if form.is_valid():
            form.save()
            return redirect('/expense-modes-general/')
    context = {
        'expense_mode': expense_mode,
        'form': form,
    }
    return render(request,'accounts/expense-modes-general/expense-modes-general-edit.html', context)





@login_required(login_url='login')
def expenses_orders(request):

    range = "All Time"
    customers_count = Customer.objects.all().count()
    orders_count = Order.objects.all().count()
    orders_sum = Order.objects.all().aggregate(Sum('value'))['value__sum']
    if orders_count is not None and orders_sum is not None:
        average_order_value = orders_sum / orders_count
    else:
        average_order_value = 0.00
    
    orders_expenses = OrderExpense.objects.all().aggregate(Sum('expense_amount'))['expense_amount__sum']

    if orders_sum is None:
        orders_sum = 0.00
    if orders_expenses is None:
        orders_expenses = 0.00
    gross_profit = orders_sum - orders_expenses

    if orders_sum == 0.00:
        gross_profit_percentage = 0.00
    else:
        gross_profit_percentage = (gross_profit / orders_sum) * 100

    other_expenses = GeneralExpense.objects.all().aggregate(Sum('expense_amount'))['expense_amount__sum']

    if other_expenses is None:
        other_expenses = 0.00
    
    net_profit = gross_profit - other_expenses

    if other_expenses == 0.00:
        net_profit_percentage = 0.00
    else:
        net_profit_percentage = (net_profit / orders_sum) * 100
    
    
    
    
    expenses_category = OrderExpenseCategory.objects.annotate(cat_count=Count('orders_expense_category'), cat_sum=Sum('orders_expense_category__expense_amount')).order_by('-cat_count')
    category_labels = []
    category_data = []
    for category in expenses_category:
        category_labels.append(category.order_expense_category)
        if category.cat_sum is not None:
            category_data.append(category.cat_sum)
        else:
            category_data.append(0.00)
    
    expenses_mode = OrderExpenseMode.objects.annotate(mode_count=Count('orders_expense_mode'), mode_sum=Sum('orders_expense_mode__expense_amount')).order_by('-mode_count')
    mode_labels = []
    mode_data = []
    for mode in expenses_mode:
        mode_labels.append(mode.order_expense_mode)
        if mode.mode_sum is not None:
            mode_data.append(mode.mode_sum)
        else:
            mode_data.append(0.00)
    
    order_expenses = OrderExpense.objects.all()
    
    if request.method == 'POST':
        dataperiod = request.POST.get('dataperiod')

        # ------------------- TODAY'S DATA -----------------------------------

        if dataperiod == 'today':
            range = "Today's"
            range_orders = Order.objects.filter(order_date__gte=datetime.datetime.now()-timedelta(days=0))
    
            customers_count = range_orders.values('customer').distinct().count()
            orders_count = range_orders.count()
            if orders_count is None:
                orders_count = 0
            orders_sum = range_orders.aggregate(Sum('value'))['value__sum']
            if orders_sum is None:
                orders_sum = 0.00
            if orders_count == 0:
                average_order_value = 0.00
            else:
                average_order_value = orders_sum / orders_count

            orders_expenses = 0.00
            for order in range_orders:
                order_expense = OrderExpense.objects.filter(order_ref=order).aggregate(Sum('expense_amount'))['expense_amount__sum']
                if order_expense is not None:
                    orders_expenses += order_expense
                else:
                    orders_expenses = orders_expenses + 0.00
            
            if orders_expenses is None:
                orders_expenses = 0.00
            gross_profit = orders_sum - orders_expenses
            if orders_sum == 0.00:
                gross_profit_percentage = 0.00
            else:
                gross_profit_percentage = (gross_profit / orders_sum) * 100    
            
            other_expenses = GeneralExpense.objects.filter(expense_date__gte=datetime.datetime.now()-timedelta(days=0)).aggregate(Sum('expense_amount'))['expense_amount__sum']
            if other_expenses is None:
                other_expenses = 0.00
            net_profit = gross_profit - other_expenses
            if orders_sum == 0.00:
                net_profit_percentage = 0.00
            else:
                net_profit_percentage = (net_profit / orders_sum) * 100
            
            expenses_category = OrderExpenseCategory.objects.filter(orders_expense_category__expense_date__gte=datetime.datetime.now()-timedelta(days=0)).annotate(cat_count=Count('orders_expense_category'), cat_sum=Sum('orders_expense_category__expense_amount')).order_by('-cat_count')
            category_labels = []
            category_data = []
            for category in expenses_category:
                category_labels.append(category.order_expense_category)
                if category.cat_sum is not None:
                    category_data.append(category.cat_sum)
                else:
                    category_data.append(0.00)
            
            expenses_mode = OrderExpenseMode.objects.filter(orders_expense_mode__expense_date__gte=datetime.datetime.now()-timedelta(days=0)).annotate(mode_count=Count('orders_expense_mode'), mode_sum=Sum('orders_expense_mode__expense_amount')).order_by('-mode_count')
            mode_labels = []
            mode_data = []
            for mode in expenses_mode:
                mode_labels.append(mode.order_expense_mode)
                if mode.mode_sum is not None:
                    mode_data.append(mode.mode_sum)
                else:
                    mode_data.append(0.00)
            
            order_expenses = OrderExpense.objects.filter(expense_date__gte=datetime.datetime.now()-timedelta(days=0))



        # ------------------- LAST 7 DAYS DATA -----------------------------------

        elif dataperiod == 'last_7_days':
            range = "Last 7 Days"
            range_orders = Order.objects.filter(order_date__gte=datetime.datetime.now()-timedelta(days=7))
    
            customers_count = range_orders.values('customer').distinct().count()
            orders_count = range_orders.count()
            if orders_count is None:
                orders_count = 0
            orders_sum = range_orders.aggregate(Sum('value'))['value__sum']
            if orders_sum is None:
                orders_sum = 0.00
            if orders_count == 0:
                average_order_value = 0.00
            else:
                average_order_value = orders_sum / orders_count
            

            orders_expenses = 0.00
            for order in range_orders:
                order_expense = OrderExpense.objects.filter(order_ref=order).aggregate(Sum('expense_amount'))['expense_amount__sum']
                if order_expense is not None:
                    orders_expenses += order_expense
                else:
                    orders_expenses = orders_expenses + 0.00
            
            if orders_expenses is None:
                orders_expenses = 0.00
            gross_profit = orders_sum - orders_expenses
            if orders_sum == 0.00:
                gross_profit_percentage = 0.00
            else:
                gross_profit_percentage = (gross_profit / orders_sum) * 100    
            
            other_expenses = GeneralExpense.objects.filter(expense_date__gte=datetime.datetime.now()-timedelta(days=7)).aggregate(Sum('expense_amount'))['expense_amount__sum']
            if other_expenses is None:
                other_expenses = 0.00
            net_profit = gross_profit - other_expenses
            if orders_sum == 0.00:
                net_profit_percentage = 0.00
            else:
                net_profit_percentage = (net_profit / orders_sum) * 100
            
            expenses_category = OrderExpenseCategory.objects.filter(orders_expense_category__expense_date__gte=datetime.datetime.now()-timedelta(days=7)).annotate(cat_count=Count('orders_expense_category'), cat_sum=Sum('orders_expense_category__expense_amount')).order_by('-cat_count')
            category_labels = []
            category_data = []
            for category in expenses_category:
                category_labels.append(category.order_expense_category)
                if category.cat_sum is not None:
                    category_data.append(category.cat_sum)
                else:
                    category_data.append(0.00)
            
            expenses_mode = OrderExpenseMode.objects.filter(orders_expense_mode__expense_date__gte=datetime.datetime.now()-timedelta(days=7)).annotate(mode_count=Count('orders_expense_mode'), mode_sum=Sum('orders_expense_mode__expense_amount')).order_by('-mode_count')
            mode_labels = []
            mode_data = []
            for mode in expenses_mode:
                mode_labels.append(mode.order_expense_mode)
                if mode.mode_sum is not None:
                    mode_data.append(mode.mode_sum)
                else:
                    mode_data.append(0.00)
            
            order_expenses = OrderExpense.objects.filter(expense_date__gte=datetime.datetime.now()-timedelta(days=7))



        # ------------------- LAST 30 DAYS DATA -----------------------------------

        elif dataperiod == 'last_30_days':
            range = "Last 30 Days"
            range_orders = Order.objects.filter(order_date__gte=datetime.datetime.now()-timedelta(days=30))
    
            customers_count = range_orders.values('customer').distinct().count()
            orders_count = range_orders.count()
            if orders_count is None:
                orders_count = 0
            orders_sum = range_orders.aggregate(Sum('value'))['value__sum']
            if orders_sum is None:
                orders_sum = 0.00
            if orders_count == 0:
                average_order_value = 0.00
            else:
                average_order_value = orders_sum / orders_count
            

            orders_expenses = 0.00
            for order in range_orders:
                order_expense = OrderExpense.objects.filter(order_ref=order).aggregate(Sum('expense_amount'))['expense_amount__sum']
                if order_expense is not None:
                    orders_expenses += order_expense
                else:
                    orders_expenses = orders_expenses + 0.00
            
            if orders_expenses is None:
                orders_expenses = 0.00
            gross_profit = orders_sum - orders_expenses
            if orders_sum == 0.00:
                gross_profit_percentage = 0.00
            else:
                gross_profit_percentage = (gross_profit / orders_sum) * 100    
            
            other_expenses = GeneralExpense.objects.filter(expense_date__gte=datetime.datetime.now()-timedelta(days=30)).aggregate(Sum('expense_amount'))['expense_amount__sum']
            if other_expenses is None:
                other_expenses = 0.00
            net_profit = gross_profit - other_expenses
            if orders_sum == 0.00:
                net_profit_percentage = 0.00
            else:
                net_profit_percentage = (net_profit / orders_sum) * 100
            
            expenses_category = OrderExpenseCategory.objects.filter(orders_expense_category__expense_date__gte=datetime.datetime.now()-timedelta(days=30)).annotate(cat_count=Count('orders_expense_category'), cat_sum=Sum('orders_expense_category__expense_amount')).order_by('-cat_count')
            category_labels = []
            category_data = []
            for category in expenses_category:
                category_labels.append(category.order_expense_category)
                if category.cat_sum is not None:
                    category_data.append(category.cat_sum)
                else:
                    category_data.append(0.00)
            
            expenses_mode = OrderExpenseMode.objects.filter(orders_expense_mode__expense_date__gte=datetime.datetime.now()-timedelta(days=30)).annotate(mode_count=Count('orders_expense_mode'), mode_sum=Sum('orders_expense_mode__expense_amount')).order_by('-mode_count')
            mode_labels = []
            mode_data = []
            for mode in expenses_mode:
                mode_labels.append(mode.order_expense_mode)
                if mode.mode_sum is not None:
                    mode_data.append(mode.mode_sum)
                else:
                    mode_data.append(0.00)
            
            order_expenses = OrderExpense.objects.filter(expense_date__gte=datetime.datetime.now()-timedelta(days=30))



        # ------------------- LAST 60 DAYS DATA -----------------------------------

        elif dataperiod == 'last_60_days':
            range = "Last 60 Days"
            range_orders = Order.objects.filter(order_date__gte=datetime.datetime.now()-timedelta(days=60))
    
            customers_count = range_orders.values('customer').distinct().count()
            orders_count = range_orders.count()
            if orders_count is None:
                orders_count = 0
            orders_sum = range_orders.aggregate(Sum('value'))['value__sum']
            if orders_sum is None:
                orders_sum = 0.00
            if orders_count == 0:
                average_order_value = 0.00
            else:
                average_order_value = orders_sum / orders_count
            

            orders_expenses = 0.00
            for order in range_orders:
                order_expense = OrderExpense.objects.filter(order_ref=order).aggregate(Sum('expense_amount'))['expense_amount__sum']
                if order_expense is not None:
                    orders_expenses += order_expense
                else:
                    orders_expenses = orders_expenses + 0.00
            
            if orders_expenses is None:
                orders_expenses = 0.00
            gross_profit = orders_sum - orders_expenses
            if orders_sum == 0.00:
                gross_profit_percentage = 0.00
            else:
                gross_profit_percentage = (gross_profit / orders_sum) * 100    
            
            other_expenses = GeneralExpense.objects.filter(expense_date__gte=datetime.datetime.now()-timedelta(days=60)).aggregate(Sum('expense_amount'))['expense_amount__sum']
            if other_expenses is None:
                other_expenses = 0.00
            net_profit = gross_profit - other_expenses
            if orders_sum == 0.00:
                net_profit_percentage = 0.00
            else:
                net_profit_percentage = (net_profit / orders_sum) * 100
            
            expenses_category = OrderExpenseCategory.objects.filter(orders_expense_category__expense_date__gte=datetime.datetime.now()-timedelta(days=60)).annotate(cat_count=Count('orders_expense_category'), cat_sum=Sum('orders_expense_category__expense_amount')).order_by('-cat_count')
            category_labels = []
            category_data = []
            for category in expenses_category:
                category_labels.append(category.order_expense_category)
                if category.cat_sum is not None:
                    category_data.append(category.cat_sum)
                else:
                    category_data.append(0.00)
            
            expenses_mode = OrderExpenseMode.objects.filter(orders_expense_mode__expense_date__gte=datetime.datetime.now()-timedelta(days=60)).annotate(mode_count=Count('orders_expense_mode'), mode_sum=Sum('orders_expense_mode__expense_amount')).order_by('-mode_count')
            mode_labels = []
            mode_data = []
            for mode in expenses_mode:
                mode_labels.append(mode.order_expense_mode)
                if mode.mode_sum is not None:
                    mode_data.append(mode.mode_sum)
                else:
                    mode_data.append(0.00)
            
            order_expenses = OrderExpense.objects.filter(expense_date__gte=datetime.datetime.now()-timedelta(days=60))




        # ------------------- LAST 90 DAYS DATA -----------------------------------

        elif dataperiod == 'last_90_days':
            range = "Last 90 Days"
            range_orders = Order.objects.filter(order_date__gte=datetime.datetime.now()-timedelta(days=90))
    
            customers_count = range_orders.values('customer').distinct().count()
            orders_count = range_orders.count()
            if orders_count is None:
                orders_count = 0
            orders_sum = range_orders.aggregate(Sum('value'))['value__sum']
            if orders_sum is None:
                orders_sum = 0.00
            if orders_count == 0:
                average_order_value = 0.00
            else:
                average_order_value = orders_sum / orders_count
            

            orders_expenses = 0.00
            for order in range_orders:
                order_expense = OrderExpense.objects.filter(order_ref=order).aggregate(Sum('expense_amount'))['expense_amount__sum']
                if order_expense is not None:
                    orders_expenses += order_expense
                else:
                    orders_expenses = orders_expenses + 0.00
            
            if orders_expenses is None:
                orders_expenses = 0.00
            gross_profit = orders_sum - orders_expenses
            if orders_sum == 0.00:
                gross_profit_percentage = 0.00
            else:
                gross_profit_percentage = (gross_profit / orders_sum) * 100    
            
            other_expenses = GeneralExpense.objects.filter(expense_date__gte=datetime.datetime.now()-timedelta(days=90)).aggregate(Sum('expense_amount'))['expense_amount__sum']
            if other_expenses is None:
                other_expenses = 0.00
            net_profit = gross_profit - other_expenses
            if orders_sum == 0.00:
                net_profit_percentage = 0.00
            else:
                net_profit_percentage = (net_profit / orders_sum) * 100
            
            expenses_category = OrderExpenseCategory.objects.filter(orders_expense_category__expense_date__gte=datetime.datetime.now()-timedelta(days=90)).annotate(cat_count=Count('orders_expense_category'), cat_sum=Sum('orders_expense_category__expense_amount')).order_by('-cat_count')
            category_labels = []
            category_data = []
            for category in expenses_category:
                category_labels.append(category.order_expense_category)
                if category.cat_sum is not None:
                    category_data.append(category.cat_sum)
                else:
                    category_data.append(0.00)
            
            expenses_mode = OrderExpenseMode.objects.filter(orders_expense_mode__expense_date__gte=datetime.datetime.now()-timedelta(days=90)).annotate(mode_count=Count('orders_expense_mode'), mode_sum=Sum('orders_expense_mode__expense_amount')).order_by('-mode_count')
            mode_labels = []
            mode_data = []
            for mode in expenses_mode:
                mode_labels.append(mode.order_expense_mode)
                if mode.mode_sum is not None:
                    mode_data.append(mode.mode_sum)
                else:
                    mode_data.append(0.00)
            
            order_expenses = OrderExpense.objects.filter(expense_date__gte=datetime.datetime.now()-timedelta(days=90))




        # ------------------- CURRENT MONTH DATA -----------------------------------

        elif dataperiod == 'current_month':
            range = "Current Month's"
            today = datetime.date.today()
            range_orders = Order.objects.filter(order_date__year=today.year, order_date__month=today.month)
    
            customers_count = range_orders.values('customer').distinct().count()
            orders_count = range_orders.count()
            if orders_count is None:
                orders_count = 0
            orders_sum = range_orders.aggregate(Sum('value'))['value__sum']
            if orders_sum is None:
                orders_sum = 0.00
            if orders_count == 0:
                average_order_value = 0.00
            else:
                average_order_value = orders_sum / orders_count
            

            orders_expenses = 0.00
            for order in range_orders:
                order_expense = OrderExpense.objects.filter(order_ref=order).aggregate(Sum('expense_amount'))['expense_amount__sum']
                if order_expense is not None:
                    orders_expenses += order_expense
                else:
                    orders_expenses = orders_expenses + 0.00
            
            if orders_expenses is None:
                orders_expenses = 0.00
            gross_profit = orders_sum - orders_expenses
            if orders_sum == 0.00:
                gross_profit_percentage = 0.00
            else:
                gross_profit_percentage = (gross_profit / orders_sum) * 100    
            
            other_expenses = GeneralExpense.objects.filter(expense_date__year=today.year, expense_date__month=today.month).aggregate(Sum('expense_amount'))['expense_amount__sum']
            if other_expenses is None:
                other_expenses = 0.00
            net_profit = gross_profit - other_expenses
            if orders_sum == 0.00:
                net_profit_percentage = 0.00
            else:
                net_profit_percentage = (net_profit / orders_sum) * 100
            
            expenses_category = OrderExpenseCategory.objects.filter(orders_expense_category__expense_date__year=today.year, orders_expense_category__expense_date__month=today.month).annotate(cat_count=Count('orders_expense_category'), cat_sum=Sum('orders_expense_category__expense_amount')).order_by('-cat_count')
            category_labels = []
            category_data = []
            for category in expenses_category:
                category_labels.append(category.order_expense_category)
                if category.cat_sum is not None:
                    category_data.append(category.cat_sum)
                else:
                    category_data.append(0.00)
            
            expenses_mode = OrderExpenseMode.objects.filter(orders_expense_mode__expense_date__year=today.year, orders_expense_mode__expense_date__month=today.month).annotate(mode_count=Count('orders_expense_mode'), mode_sum=Sum('orders_expense_mode__expense_amount')).order_by('-mode_count')
            mode_labels = []
            mode_data = []
            for mode in expenses_mode:
                mode_labels.append(mode.order_expense_mode)
                if mode.mode_sum is not None:
                    mode_data.append(mode.mode_sum)
                else:
                    mode_data.append(0.00)
            
            order_expenses = OrderExpense.objects.filter(expense_date__year=today.year, expense_date__month=today.month)



        # ------------------- CURRENT YEAR DATA -----------------------------------

        elif dataperiod == 'current_year':
            range = "Current Year's"
            today = datetime.date.today()
            range_orders = Order.objects.filter(order_date__year=today.year)
    
            customers_count = range_orders.values('customer').distinct().count()
            orders_count = range_orders.count()
            if orders_count is None:
                orders_count = 0
            orders_sum = range_orders.aggregate(Sum('value'))['value__sum']
            if orders_sum is None:
                orders_sum = 0.00
            if orders_count == 0:
                average_order_value = 0.00
            else:
                average_order_value = orders_sum / orders_count
            

            orders_expenses = 0.00
            for order in range_orders:
                order_expense = OrderExpense.objects.filter(order_ref=order).aggregate(Sum('expense_amount'))['expense_amount__sum']
                if order_expense is not None:
                    orders_expenses += order_expense
                else:
                    orders_expenses = orders_expenses + 0.00
            
            if orders_expenses is None:
                orders_expenses = 0.00
            gross_profit = orders_sum - orders_expenses
            if orders_sum == 0.00:
                gross_profit_percentage = 0.00
            else:
                gross_profit_percentage = (gross_profit / orders_sum) * 100    
            
            other_expenses = GeneralExpense.objects.filter(expense_date__year=today.year).aggregate(Sum('expense_amount'))['expense_amount__sum']
            if other_expenses is None:
                other_expenses = 0.00
            net_profit = gross_profit - other_expenses
            if orders_sum == 0.00:
                net_profit_percentage = 0.00
            else:
                net_profit_percentage = (net_profit / orders_sum) * 100
            
            expenses_category = OrderExpenseCategory.objects.filter(orders_expense_category__expense_date__year=today.year).annotate(cat_count=Count('orders_expense_category'), cat_sum=Sum('orders_expense_category__expense_amount')).order_by('-cat_count')
            category_labels = []
            category_data = []
            for category in expenses_category:
                category_labels.append(category.order_expense_category)
                if category.cat_sum is not None:
                    category_data.append(category.cat_sum)
                else:
                    category_data.append(0.00)
            
            expenses_mode = OrderExpenseMode.objects.filter(orders_expense_mode__expense_date__year=today.year).annotate(mode_count=Count('orders_expense_mode'), mode_sum=Sum('orders_expense_mode__expense_amount')).order_by('-mode_count')
            mode_labels = []
            mode_data = []
            for mode in expenses_mode:
                mode_labels.append(mode.order_expense_mode)
                if mode.mode_sum is not None:
                    mode_data.append(mode.mode_sum)
                else:
                    mode_data.append(0.00)
            
            order_expenses = OrderExpense.objects.filter(expense_date__year=today.year)



    myFilter = OrderExpenseFilter(request.GET, queryset=order_expenses)
    order_expenses = myFilter.qs
    
    context = {
        'range': range,
        'customers_count': customers_count,
        'orders_count': orders_count,
        'orders_sum': orders_sum,
        'average_order_value': average_order_value,
        'orders_expenses': orders_expenses,
        'gross_profit': gross_profit,
        'gross_profit_percentage': gross_profit_percentage,
        'other_expenses': other_expenses,
        'net_profit': net_profit,
        'net_profit_percentage': net_profit_percentage,
        'expenses_category': expenses_category,
        'category_labels': category_labels,
        'category_data': category_data,
        'expenses_mode': expenses_mode,
        'mode_labels': mode_labels,
        'mode_data': mode_data,
        'order_expenses': order_expenses,
        'myFilter': myFilter,
    }
    return render(request,'accounts/expenses-orders/expenses-orders.html', context)




@login_required(login_url='login')
def expenses_orders_add(request, pk):
    order = Order.objects.get(order_ref=pk)
    form = OrderExpenseForm(initial={'order_ref': order.order_ref})
    if request.method == 'POST':
        form = OrderExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/orders/')
    context = {
        'order': order,
        'form': form,
    }
    return render(request,'accounts/expenses-orders/expenses-orders-add.html', context)




@login_required(login_url='login')
def expenses_orders_delete(request, pk):
    expense = OrderExpense.objects.get(id=pk)
    order_ref = expense.order_ref
    if request.method == 'POST':
        expense.delete()
        return redirect('/expenses-orders/')
    context = {
        'expense': expense,
        'order_ref': order_ref,
    }
    return render(request,'accounts/expenses-orders/expenses-orders-delete.html', context)




@login_required(login_url='login')
def expenses_orders_edit(request, pk):
    expense = OrderExpense.objects.get(id=pk)
    order_ref = expense.order_ref
    form = OrderExpenseForm(instance=expense)
    if request.method == 'POST':
        form = OrderExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('/expenses-orders/')
    context = {
        'form': form,
        'order_ref': order_ref,
    }
    return render(request,'accounts/expenses-orders/expenses-orders-edit.html', context)




@login_required(login_url='login')
def expense_categories_orders(request):

    range = "All Time"
    expenses_category = OrderExpenseCategory.objects.annotate(cat_count=Count('orders_expense_category'), cat_sum=Sum('orders_expense_category__expense_amount')).order_by('-cat_count')

    category_labels = []
    category_data = []
    for category in expenses_category:
        category_labels.append(category.order_expense_category)
        if category.cat_sum is not None:
            category_data.append(category.cat_sum)
        else:
            category_data.append(0.00)
    
    if request.method == 'POST':
        dataperiod = request.POST.get('dataperiod')

        # ------------------- TODAY'S DATA -----------------------------------

        if dataperiod == 'today':
            range = "Today's"
            expenses_category = OrderExpenseCategory.objects.filter(orders_expense_category__expense_date__gte=datetime.datetime.now()-timedelta(days=0)).annotate(cat_count=Count('orders_expense_category'), cat_sum=Sum('orders_expense_category__expense_amount')).order_by('-cat_count')

            category_labels = []
            category_data = []
            for category in expenses_category:
                category_labels.append(category.order_expense_category)
                if category.cat_sum is not None:
                    category_data.append(category.cat_sum)
                else:
                    category_data.append(0.00)



        # ------------------- LAST 7 DAYS DATA -----------------------------------

        elif dataperiod == 'last_7_days':
            range = "Last 7 Days"
            expenses_category = OrderExpenseCategory.objects.filter(orders_expense_category__expense_date__gte=datetime.datetime.now()-timedelta(days=7)).annotate(cat_count=Count('orders_expense_category'), cat_sum=Sum('orders_expense_category__expense_amount')).order_by('-cat_count')

            category_labels = []
            category_data = []
            for category in expenses_category:
                category_labels.append(category.order_expense_category)
                if category.cat_sum is not None:
                    category_data.append(category.cat_sum)
                else:
                    category_data.append(0.00)



        # ------------------- LAST 30 DAYS DATA -----------------------------------

        elif dataperiod == 'last_30_days':
            range = "Last 30 Days"
            expenses_category = OrderExpenseCategory.objects.filter(orders_expense_category__expense_date__gte=datetime.datetime.now()-timedelta(days=30)).annotate(cat_count=Count('orders_expense_category'), cat_sum=Sum('orders_expense_category__expense_amount')).order_by('-cat_count')

            category_labels = []
            category_data = []
            for category in expenses_category:
                category_labels.append(category.order_expense_category)
                if category.cat_sum is not None:
                    category_data.append(category.cat_sum)
                else:
                    category_data.append(0.00)



        # ------------------- LAST 60 DAYS DATA -----------------------------------

        elif dataperiod == 'last_60_days':
            range = "Last 60 Days"
            expenses_category = OrderExpenseCategory.objects.filter(orders_expense_category__expense_date__gte=datetime.datetime.now()-timedelta(days=60)).annotate(cat_count=Count('orders_expense_category'), cat_sum=Sum('orders_expense_category__expense_amount')).order_by('-cat_count')

            category_labels = []
            category_data = []
            for category in expenses_category:
                category_labels.append(category.order_expense_category)
                if category.cat_sum is not None:
                    category_data.append(category.cat_sum)
                else:
                    category_data.append(0.00)




        # ------------------- LAST 90 DAYS DATA -----------------------------------

        elif dataperiod == 'last_90_days':
            range = "Last 90 Days"
            expenses_category = OrderExpenseCategory.objects.filter(orders_expense_category__expense_date__gte=datetime.datetime.now()-timedelta(days=90)).annotate(cat_count=Count('orders_expense_category'), cat_sum=Sum('orders_expense_category__expense_amount')).order_by('-cat_count')

            category_labels = []
            category_data = []
            for category in expenses_category:
                category_labels.append(category.order_expense_category)
                if category.cat_sum is not None:
                    category_data.append(category.cat_sum)
                else:
                    category_data.append(0.00)




        # ------------------- CURRENT MONTH DATA -----------------------------------

        elif dataperiod == 'current_month':
            range = "Current Month's"
            today = datetime.date.today()
            expenses_category = OrderExpenseCategory.objects.filter(orders_expense_category__expense_date__year=today.year,orders_expense_category__expense_date__month=today.month).annotate(cat_count=Count('orders_expense_category'), cat_sum=Sum('orders_expense_category__expense_amount')).order_by('-cat_count')

            category_labels = []
            category_data = []
            for category in expenses_category:
                category_labels.append(category.order_expense_category)
                if category.cat_sum is not None:
                    category_data.append(category.cat_sum)
                else:
                    category_data.append(0.00)



        # ------------------- CURRENT YEAR DATA -----------------------------------

        elif dataperiod == 'current_year':
            range = "Current Year's"
            today = datetime.date.today()
            expenses_category = OrderExpenseCategory.objects.filter(orders_expense_category__expense_date__year=today.year).annotate(cat_count=Count('orders_expense_category'), cat_sum=Sum('orders_expense_category__expense_amount')).order_by('-cat_count')

            category_labels = []
            category_data = []
            for category in expenses_category:
                category_labels.append(category.order_expense_category)
                if category.cat_sum is not None:
                    category_data.append(category.cat_sum)
                else:
                    category_data.append(0.00)


    context = {
        'range': range,
        'expenses_category': expenses_category,
        'category_labels': category_labels,
        'category_data': category_data,
    }
    return render(request,'accounts/expense-categories-orders/expense-categories-orders.html', context)





@login_required(login_url='login')
def expense_categories_orders_add(request):
    form = OrderExpenseCategoryForm
    if request.method == 'POST':
        form = OrderExpenseCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/expense-categories-orders/')
    context = {
        'form': form,
    }
    return render(request,'accounts/expense-categories-orders/expense-categories-orders-add.html', context)




@login_required(login_url='login')
def expense_categories_orders_delete(request, pk):
    category = OrderExpenseCategory.objects.get(id=pk)
    category_name = category.order_expense_category
    if request.method == 'POST':
        category.delete()
        return redirect('/expense-categories-orders/')
    context = {
        'category': category,
        'category_name': category_name,
    }
    return render(request,'accounts/expense-categories-orders/expense-categories-orders-delete.html', context)




@login_required(login_url='login')
def expense_categories_orders_edit(request, pk):
    category = OrderExpenseCategory.objects.get(id=pk)
    category_name = category.order_expense_category
    form = OrderExpenseCategoryForm(instance=category)
    if request.method == 'POST':
        form = OrderExpenseCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('/expense-categories-orders/')
    context = {
        'category_name': category_name,
        'form': form,
    }
    return render(request,'accounts/expense-categories-orders/expense-categories-orders-edit.html', context)






@login_required(login_url='login')
def expense_modes_orders(request):

    range = "All Time"
    expense_modes = OrderExpenseMode.objects.annotate(mode_count=Count('orders_expense_mode'), mode_sum=Sum('orders_expense_mode__expense_amount'))
    mode_labels = []
    mode_data = []
    for mode in expense_modes:
        mode_labels.append(mode.order_expense_mode)
        if mode.mode_sum is not None:
            mode_data.append(mode.mode_sum)
        else:
            mode_data.append(0.00)

    if request.method == 'POST':
        dataperiod = request.POST.get('dataperiod')
    
        # ------------------- TODAY'S DATA -----------------------------------

        if dataperiod == 'today':
            range = "Today's"
            expense_modes = OrderExpenseMode.objects.filter(orders_expense_mode__expense_date__gte=datetime.datetime.now()-timedelta(days=0)).annotate(mode_count=Count('orders_expense_mode'), mode_sum=Sum('orders_expense_mode__expense_amount'))
            mode_labels = []
            mode_data = []
            for mode in expense_modes:
                mode_labels.append(mode.order_expense_mode)
                if mode.mode_sum is not None:
                    mode_data.append(mode.mode_sum)
                else:
                    mode_data.append(0.00)            



        # ------------------- LAST 7 DAYS DATA -----------------------------------

        elif dataperiod == 'last_7_days':
            range = "Last 7 Days"
            expense_modes = OrderExpenseMode.objects.filter(orders_expense_mode__expense_date__gte=datetime.datetime.now()-timedelta(days=7)).annotate(mode_count=Count('orders_expense_mode'), mode_sum=Sum('orders_expense_mode__expense_amount'))
            mode_labels = []
            mode_data = []
            for mode in expense_modes:
                mode_labels.append(mode.order_expense_mode)
                if mode.mode_sum is not None:
                    mode_data.append(mode.mode_sum)
                else:
                    mode_data.append(0.00)



        # ------------------- LAST 30 DAYS DATA -----------------------------------

        elif dataperiod == 'last_30_days':
            range = "Last 30 Days"
            expense_modes = OrderExpenseMode.objects.filter(orders_expense_mode__expense_date__gte=datetime.datetime.now()-timedelta(days=30)).annotate(mode_count=Count('orders_expense_mode'), mode_sum=Sum('orders_expense_mode__expense_amount'))
            mode_labels = []
            mode_data = []
            for mode in expense_modes:
                mode_labels.append(mode.order_expense_mode)
                if mode.mode_sum is not None:
                    mode_data.append(mode.mode_sum)
                else:
                    mode_data.append(0.00)



        # ------------------- LAST 60 DAYS DATA -----------------------------------

        elif dataperiod == 'last_60_days':
            range = "Last 60 Days"
            expense_modes = OrderExpenseMode.objects.filter(orders_expense_mode__expense_date__gte=datetime.datetime.now()-timedelta(days=60)).annotate(mode_count=Count('orders_expense_mode'), mode_sum=Sum('orders_expense_mode__expense_amount'))
            mode_labels = []
            mode_data = []
            for mode in expense_modes:
                mode_labels.append(mode.order_expense_mode)
                if mode.mode_sum is not None:
                    mode_data.append(mode.mode_sum)
                else:
                    mode_data.append(0.00)




        # ------------------- LAST 90 DAYS DATA -----------------------------------

        elif dataperiod == 'last_90_days':
            range = "Last 90 Days"
            expense_modes = OrderExpenseMode.objects.filter(orders_expense_mode__expense_date__gte=datetime.datetime.now()-timedelta(days=90)).annotate(mode_count=Count('orders_expense_mode'), mode_sum=Sum('orders_expense_mode__expense_amount'))
            mode_labels = []
            mode_data = []
            for mode in expense_modes:
                mode_labels.append(mode.order_expense_mode)
                if mode.mode_sum is not None:
                    mode_data.append(mode.mode_sum)
                else:
                    mode_data.append(0.00)



        # ------------------- CURRENT MONTH DATA -----------------------------------

        elif dataperiod == 'current_month':
            range = "Current Month's"
            today = datetime.date.today()
            expense_modes = OrderExpenseMode.objects.filter(orders_expense_mode__expense_date__year=today.year, orders_expense_mode__expense_date__month=today.month).annotate(mode_count=Count('orders_expense_mode'), mode_sum=Sum('orders_expense_mode__expense_amount'))
            mode_labels = []
            mode_data = []
            for mode in expense_modes:
                mode_labels.append(mode.order_expense_mode)
                if mode.mode_sum is not None:
                    mode_data.append(mode.mode_sum)
                else:
                    mode_data.append(0.00)




        # ------------------- CURRENT YEAR DATA -----------------------------------

        elif dataperiod == 'current_year':
            range = "Current Year's"
            today = datetime.date.today()
            expense_modes = OrderExpenseMode.objects.filter(orders_expense_mode__expense_date__year=today.year).annotate(mode_count=Count('orders_expense_mode'), mode_sum=Sum('orders_expense_mode__expense_amount'))
            mode_labels = []
            mode_data = []
            for mode in expense_modes:
                mode_labels.append(mode.order_expense_mode)
                if mode.mode_sum is not None:
                    mode_data.append(mode.mode_sum)
                else:
                    mode_data.append(0.00)



    context = {
        'range': range,
        'expense_modes': expense_modes,
        'mode_labels': mode_labels,
        'mode_data': mode_data,
    }
    return render(request,'accounts/expense-modes-orders/expense-modes-orders.html', context)





@login_required(login_url='login')
def expense_modes_orders_add(request):
    form = OrderExpenseModeForm
    if request.method == 'POST':
        form = OrderExpenseModeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/expense-modes-orders/')
    context = {
        'form': form,
    }
    return render(request,'accounts/expense-modes-orders/expense-modes-orders-add.html', context)




@login_required(login_url='login')
def expense_modes_orders_delete(request, pk):
    mode = OrderExpenseMode.objects.get(id=pk)
    expense_mode = mode.order_expense_mode
    if request.method == 'POST':
        mode.delete()
        return redirect('/expense-modes-orders/')
    context = {
        'mode': mode,
        'expense_mode': expense_mode,
    }
    return render(request,'accounts/expense-modes-orders/expense-modes-orders-delete.html', context)




@login_required(login_url='login')
def expense_modes_orders_edit(request, pk):
    mode = OrderExpenseMode.objects.get(id=pk)
    expense_mode = mode.order_expense_mode
    form = OrderExpenseModeForm(instance=mode)
    if request.method == 'POST':
        form = OrderExpenseModeForm(request.POST, instance=mode)
        if form.is_valid():
            form.save()
            return redirect('/expense-modes-orders/')
    context = {
        'expense_mode': expense_mode,
        'form': form,
    }
    return render(request,'accounts/expense-modes-orders/expense-modes-orders-edit.html', context)






@login_required(login_url='login')
def order(request, pk):

    paydata = PaymentReceipt.objects.filter(order_ref=pk).order_by('-payment_received_date')

    expdata = OrderExpense.objects.filter(order_ref=pk).order_by('-expense_date')
    expense_labels = []
    expense_data = []
    for exp in expdata:
        expense_labels.append(exp.expense_category)
        if exp.expense_amount is not None:
            expense_data.append(exp.expense_amount)
        else:
            expense_data.append(0.00)

    order = Order.objects.get(order_ref=pk)
    order_expenses = order.expenses.all()
    total_expense = order.expenses.all().aggregate(Sum('expense_amount'))['expense_amount__sum']
    order_value = order.value

    if total_expense is not None:
        total_expenses = total_expense
    else:
        total_expenses = 0.00
    
    order_profit = order.value - total_expenses
    profit_percentage = (order_profit / order.value) * 100

    profit_labels = ['Order Expenses', 'Order Profit']
    profit_data = [total_expenses, order_profit]
    

    order_payments = order.payments.all().aggregate(Sum('received_amount'))['received_amount__sum']
    if order_payments is not None:
        received_amount = order_payments
    else:
        received_amount = 0.00
    
    pending_amount = order_value - received_amount

    context = {
        'order': order,
        'expdata': expdata,
        'order_expenses': order_expenses,
        'total_expenses': total_expenses,
        'order_profit': order_profit,
        'profit_percentage': profit_percentage,
        'profit_labels': profit_labels,
        'profit_data': profit_data,
        'expense_labels': expense_labels,
        'expense_data': expense_data,
        'received_amount': received_amount,
        'pending_amount': pending_amount,
        'paydata': paydata,
    }
    return render(request,'accounts/orders/order.html', context)





@login_required(login_url='login')
def orders_create(request):
    form = OrderForm
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Order created successfully!')
            return redirect('/orders-create/')
        else:
            messages.warning(request,'One or more fields have an error. Please try again.')
            return render(request, 'accounts/orders-create.html')

    context = {
        'form': form,
    }
    return render(request,'accounts/orders/orders-create.html', context)





@login_required(login_url='login')
def orders_delete(request, pk):
    order = Order.objects.get(order_ref=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/orders/')
    context = {
        'order': order,
    }
    return render(request, 'accounts/orders/orders-delete.html', context)



@login_required(login_url='login')
def orders_edit(request, pk):
    order = Order.objects.get(order_ref=pk)
    order_ref = order.order_ref
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/orders/')
    context = {
        'order_ref': order_ref,
        'form': form,
    }
    return render(request,'accounts/orders/orders-edit.html', context)





@login_required(login_url='login')
def orders(request):
    range = 'All Time'
    orders_count = Order.objects.all().count()
    orders_sum = Order.objects.all().aggregate(Sum('value'))['value__sum']
    if orders_count is not None and orders_sum is not None:
        average_order_value = orders_sum / orders_count
    else:
        average_order_value = 0.00

    orders_expenses = OrderExpense.objects.all().aggregate(Sum('expense_amount'))['expense_amount__sum']

    if orders_expenses is None:
        orders_expenses = 0.00
    
    if orders_sum is None:
        orders_sum = 0.00
    if orders_expenses is None:
        orders_expenses = 0.00
    gross_profit = orders_sum - orders_expenses
    
    if orders_sum == 0.00:
        gross_profit_percentage = 0.00
    else:
        gross_profit_percentage = (gross_profit / orders_sum) * 100  


    # deliveries_status = DeliveryStatus.objects.annotate(stat_count=Count('orders_delivery_status'), stat_total=Sum('orders_delivery_status__value')).order_by('-stat_total')
    
    deliveries_status = DeliveryStatus.objects.annotate(del_stat_count=Count('orders_delivery_status'), del_stat_sum=Sum('orders_delivery_status__value')).order_by('-del_stat_count')
    delivery_labels = []
    delivery_data = []
    for status in deliveries_status:
        delivery_labels.append(status.delivery_status)
        if status.del_stat_sum is not None:
            delivery_data.append(status.del_stat_sum)
        else:
            delivery_data.append(0.00)
    
    payments_status = PaymentStatus.objects.annotate(pay_stat_count=Count('orders_payment_status'), pay_stat_sum=Sum('orders_payment_status__value')).order_by('-pay_stat_count')
    payment_labels = []
    payment_data = []
    for status in payments_status:
        payment_labels.append(status.payment_status)
        if status.pay_stat_sum is not None:
            payment_data.append(status.pay_stat_sum)
        else:
            payment_data.append(0.00)
    
    # pay_terms = PaymentTerm.objects.annotate(pay_term_count=Count('orders_payment_terms'), pay_term_sum=Sum('orders_payment_terms__value')).order_by('-pay_term_count')

    orders_info = Order.objects.all().order_by('-order_ref')

    if request.method == 'POST':
        dataperiod = request.POST.get('dataperiod')

        # ------------------- TODAY'S DATA -----------------------------------
        if dataperiod == 'today':
            range = "Today's"
            range_orders = Order.objects.filter(order_date__gte=datetime.datetime.now()-timedelta(days=0))

            orders_count = range_orders.count()
            orders_sum = range_orders.aggregate(Sum('value'))['value__sum']
            if orders_sum is None:
                orders_sum = 0.00
            if orders_count == 0:
                average_order_value = 0.00
            else:
                average_order_value = orders_sum / orders_count

            orders_expenses = 0.00
            for order in range_orders:
                order_expense = OrderExpense.objects.filter(order_ref=order).aggregate(Sum('expense_amount'))['expense_amount__sum']
                if order_expense is not None:
                    orders_expenses += order_expense
                else:
                    orders_expenses = orders_expenses + 0.00

            if orders_expenses is None:
                orders_expenses = 0.00
            gross_profit = orders_sum - orders_expenses
            if orders_sum == 0.00:
                gross_profit_percentage = 0.00
            else:
                gross_profit_percentage = (gross_profit / orders_sum) * 100

            
            deliveries_status = DeliveryStatus.objects.filter(orders_delivery_status__order_date__gte=datetime.datetime.now()-timedelta(days=0)).annotate(del_stat_count=Count('orders_delivery_status'), del_stat_sum=Sum('orders_delivery_status__value')).order_by('-del_stat_count')
            delivery_labels = []
            delivery_data = []
            for status in deliveries_status:
                delivery_labels.append(status.delivery_status)
                if status.del_stat_sum is not None:
                    delivery_data.append(status.del_stat_sum)
                else:
                    delivery_data.append(0.00)
            
            payments_status = PaymentStatus.objects.filter(orders_payment_status__order_date__gte=datetime.datetime.now()-timedelta(days=0)).annotate(pay_stat_count=Count('orders_payment_status'), pay_stat_sum=Sum('orders_payment_status__value')).order_by('-pay_stat_count')
            payment_labels = []
            payment_data = []
            for status in payments_status:
                payment_labels.append(status.payment_status)
                if status.pay_stat_sum is not None:
                    payment_data.append(status.pay_stat_sum)
                else:
                    payment_data.append(0.00)
        
            orders_info = Order.objects.filter(order_date__gte=datetime.datetime.now()-timedelta(days=0)).order_by('-order_ref')


        # ------------------- LAST 7 DAYS DATA -----------------------------------
        elif dataperiod == 'last_7_days':
            range = "Last 7 Days"
            range_orders = Order.objects.filter(order_date__gte=datetime.datetime.now()-timedelta(days=7))

            orders_count = range_orders.count()
            orders_sum = range_orders.aggregate(Sum('value'))['value__sum']
            if orders_sum is None:
                orders_sum = 0.00
            if orders_count == 0:
                average_order_value = 0.00
            else:
                average_order_value = orders_sum / orders_count

            orders_expenses = 0.00
            for order in range_orders:
                order_expense = OrderExpense.objects.filter(order_ref=order).aggregate(Sum('expense_amount'))['expense_amount__sum']
                if order_expense is not None:
                    orders_expenses += order_expense
                else:
                    orders_expenses = orders_expenses + 0.00

            if orders_expenses is None:
                orders_expenses = 0.00
            gross_profit = orders_sum - orders_expenses
            if orders_sum == 0.00:
                gross_profit_percentage = 0.00
            else:
                gross_profit_percentage = (gross_profit / orders_sum) * 100

            
            deliveries_status = DeliveryStatus.objects.filter(orders_delivery_status__order_date__gte=datetime.datetime.now()-timedelta(days=7)).annotate(del_stat_count=Count('orders_delivery_status'), del_stat_sum=Sum('orders_delivery_status__value')).order_by('-del_stat_count')
            delivery_labels = []
            delivery_data = []
            for status in deliveries_status:
                delivery_labels.append(status.delivery_status)
                if status.del_stat_sum is not None:
                    delivery_data.append(status.del_stat_sum)
                else:
                    delivery_data.append(0.00)
            
            payments_status = PaymentStatus.objects.filter(orders_payment_status__order_date__gte=datetime.datetime.now()-timedelta(days=7)).annotate(pay_stat_count=Count('orders_payment_status'), pay_stat_sum=Sum('orders_payment_status__value')).order_by('-pay_stat_count')
            payment_labels = []
            payment_data = []
            for status in payments_status:
                payment_labels.append(status.payment_status)
                if status.pay_stat_sum is not None:
                    payment_data.append(status.pay_stat_sum)
                else:
                    payment_data.append(0.00)

            orders_info = Order.objects.filter(order_date__gte=datetime.datetime.now()-timedelta(days=7)).order_by('-order_ref')
        

        # ------------------- LAST 30 DAYS DATA -----------------------------------
        elif dataperiod == 'last_30_days':
            range = "Last 30 Days"
            range_orders = Order.objects.filter(order_date__gte=datetime.datetime.now()-timedelta(days=30))

            orders_count = range_orders.count()
            orders_sum = range_orders.aggregate(Sum('value'))['value__sum']
            if orders_sum is None:
                orders_sum = 0.00
            if orders_count == 0:
                average_order_value = 0.00
            else:
                average_order_value = orders_sum / orders_count

            orders_expenses = 0.00
            for order in range_orders:
                order_expense = OrderExpense.objects.filter(order_ref=order).aggregate(Sum('expense_amount'))['expense_amount__sum']
                if order_expense is not None:
                    orders_expenses += order_expense
                else:
                    orders_expenses = orders_expenses + 0.00

            if orders_expenses is None:
                orders_expenses = 0.00
            gross_profit = orders_sum - orders_expenses
            if orders_sum == 0.00:
                gross_profit_percentage = 0.00
            else:
                gross_profit_percentage = (gross_profit / orders_sum) * 100

            
            deliveries_status = DeliveryStatus.objects.filter(orders_delivery_status__order_date__gte=datetime.datetime.now()-timedelta(days=30)).annotate(del_stat_count=Count('orders_delivery_status'), del_stat_sum=Sum('orders_delivery_status__value')).order_by('-del_stat_count')
            delivery_labels = []
            delivery_data = []
            for status in deliveries_status:
                delivery_labels.append(status.delivery_status)
                if status.del_stat_sum is not None:
                    delivery_data.append(status.del_stat_sum)
                else:
                    delivery_data.append(0.00)
            
            payments_status = PaymentStatus.objects.filter(orders_payment_status__order_date__gte=datetime.datetime.now()-timedelta(days=30)).annotate(pay_stat_count=Count('orders_payment_status'), pay_stat_sum=Sum('orders_payment_status__value')).order_by('-pay_stat_count')
            payment_labels = []
            payment_data = []
            for status in payments_status:
                payment_labels.append(status.payment_status)
                if status.pay_stat_sum is not None:
                    payment_data.append(status.pay_stat_sum)
                else:
                    payment_data.append(0.00)

            orders_info = Order.objects.filter(order_date__gte=datetime.datetime.now()-timedelta(days=30)).order_by('-order_ref')


        # ------------------- LAST 60 DAYS DATA -----------------------------------
        elif dataperiod == 'last_60_days':
            range = "Last 60 Days"
            range_orders = Order.objects.filter(order_date__gte=datetime.datetime.now()-timedelta(days=60))

            orders_count = range_orders.count()
            orders_sum = range_orders.aggregate(Sum('value'))['value__sum']
            if orders_sum is None:
                orders_sum = 0.00
            if orders_count == 0:
                average_order_value = 0.00
            else:
                average_order_value = orders_sum / orders_count

            orders_expenses = 0.00
            for order in range_orders:
                order_expense = OrderExpense.objects.filter(order_ref=order).aggregate(Sum('expense_amount'))['expense_amount__sum']
                if order_expense is not None:
                    orders_expenses += order_expense
                else:
                    orders_expenses = orders_expenses + 0.00

            if orders_expenses is None:
                orders_expenses = 0.00
            gross_profit = orders_sum - orders_expenses
            if orders_sum == 0.00:
                gross_profit_percentage = 0.00
            else:
                gross_profit_percentage = (gross_profit / orders_sum) * 100

            
            deliveries_status = DeliveryStatus.objects.filter(orders_delivery_status__order_date__gte=datetime.datetime.now()-timedelta(days=60)).annotate(del_stat_count=Count('orders_delivery_status'), del_stat_sum=Sum('orders_delivery_status__value')).order_by('-del_stat_count')
            delivery_labels = []
            delivery_data = []
            for status in deliveries_status:
                delivery_labels.append(status.delivery_status)
                if status.del_stat_sum is not None:
                    delivery_data.append(status.del_stat_sum)
                else:
                    delivery_data.append(0.00)
            
            payments_status = PaymentStatus.objects.filter(orders_payment_status__order_date__gte=datetime.datetime.now()-timedelta(days=60)).annotate(pay_stat_count=Count('orders_payment_status'), pay_stat_sum=Sum('orders_payment_status__value')).order_by('-pay_stat_count')
            payment_labels = []
            payment_data = []
            for status in payments_status:
                payment_labels.append(status.payment_status)
                if status.pay_stat_sum is not None:
                    payment_data.append(status.pay_stat_sum)
                else:
                    payment_data.append(0.00)

            orders_info = Order.objects.filter(order_date__gte=datetime.datetime.now()-timedelta(days=60)).order_by('-order_ref')
        

        # ------------------- LAST 90 DAYS DATA -----------------------------------
        elif dataperiod == 'last_90_days':
            range = "Last 90 Days"
            range_orders = Order.objects.filter(order_date__gte=datetime.datetime.now()-timedelta(days=90))

            orders_count = range_orders.count()
            orders_sum = range_orders.aggregate(Sum('value'))['value__sum']
            if orders_sum is None:
                orders_sum = 0.00
            if orders_count == 0:
                average_order_value = 0.00
            else:
                average_order_value = orders_sum / orders_count

            orders_expenses = 0.00
            for order in range_orders:
                order_expense = OrderExpense.objects.filter(order_ref=order).aggregate(Sum('expense_amount'))['expense_amount__sum']
                if order_expense is not None:
                    orders_expenses += order_expense
                else:
                    orders_expenses = orders_expenses + 0.00

            if orders_expenses is None:
                orders_expenses = 0.00
            gross_profit = orders_sum - orders_expenses
            if orders_sum == 0.00:
                gross_profit_percentage = 0.00
            else:
                gross_profit_percentage = (gross_profit / orders_sum) * 100

            
            deliveries_status = DeliveryStatus.objects.filter(orders_delivery_status__order_date__gte=datetime.datetime.now()-timedelta(days=90)).annotate(del_stat_count=Count('orders_delivery_status'), del_stat_sum=Sum('orders_delivery_status__value')).order_by('-del_stat_count')
            delivery_labels = []
            delivery_data = []
            for status in deliveries_status:
                delivery_labels.append(status.delivery_status)
                if status.del_stat_sum is not None:
                    delivery_data.append(status.del_stat_sum)
                else:
                    delivery_data.append(0.00)
            
            payments_status = PaymentStatus.objects.filter(orders_payment_status__order_date__gte=datetime.datetime.now()-timedelta(days=90)).annotate(pay_stat_count=Count('orders_payment_status'), pay_stat_sum=Sum('orders_payment_status__value')).order_by('-pay_stat_count')
            payment_labels = []
            payment_data = []
            for status in payments_status:
                payment_labels.append(status.payment_status)
                if status.pay_stat_sum is not None:
                    payment_data.append(status.pay_stat_sum)
                else:
                    payment_data.append(0.00)

            orders_info = Order.objects.filter(order_date__gte=datetime.datetime.now()-timedelta(days=90)).order_by('-order_ref')
        

        # ------------------- CURRENT MONTH DATA -----------------------------------
        elif dataperiod == 'current_month':
            range = "Current Month's"
            today = datetime.date.today()
            range_orders = Order.objects.filter(order_date__year=today.year, order_date__month=today.month)

            orders_count = range_orders.count()
            orders_sum = range_orders.aggregate(Sum('value'))['value__sum']
            if orders_sum is None:
                orders_sum = 0.00
            if orders_count == 0:
                average_order_value = 0.00
            else:
                average_order_value = orders_sum / orders_count

            orders_expenses = 0.00
            for order in range_orders:
                order_expense = OrderExpense.objects.filter(order_ref=order).aggregate(Sum('expense_amount'))['expense_amount__sum']
                if order_expense is not None:
                    orders_expenses += order_expense
                else:
                    orders_expenses = orders_expenses + 0.00

            if orders_expenses is None:
                orders_expenses = 0.00
            gross_profit = orders_sum - orders_expenses
            if orders_sum == 0.00:
                gross_profit_percentage = 0.00
            else:
                gross_profit_percentage = (gross_profit / orders_sum) * 100

            
            deliveries_status = DeliveryStatus.objects.filter(orders_delivery_status__order_date__year=today.year, orders_delivery_status__order_date__month=today.month).annotate(del_stat_count=Count('orders_delivery_status'), del_stat_sum=Sum('orders_delivery_status__value')).order_by('-del_stat_count')
            delivery_labels = []
            delivery_data = []
            for status in deliveries_status:
                delivery_labels.append(status.delivery_status)
                if status.del_stat_sum is not None:
                    delivery_data.append(status.del_stat_sum)
                else:
                    delivery_data.append(0.00)
            
            payments_status = PaymentStatus.objects.filter(orders_payment_status__order_date__year=today.year, orders_payment_status__order_date__month=today.month).annotate(pay_stat_count=Count('orders_payment_status'), pay_stat_sum=Sum('orders_payment_status__value')).order_by('-pay_stat_count')
            payment_labels = []
            payment_data = []
            for status in payments_status:
                payment_labels.append(status.payment_status)
                if status.pay_stat_sum is not None:
                    payment_data.append(status.pay_stat_sum)
                else:
                    payment_data.append(0.00)         

            orders_info = Order.objects.filter(order_date__year=today.year, order_date__month=today.month).order_by('-order_ref')
            
        

        # ------------------- CURRENT YEAR DATA -----------------------------------
        elif dataperiod == 'current_year':
            range = "Current Year's"
            today = datetime.date.today()
            range_orders = Order.objects.filter(order_date__year=today.year)

            orders_count = range_orders.count()
            orders_sum = range_orders.aggregate(Sum('value'))['value__sum']
            if orders_sum is None:
                orders_sum = 0.00
            if orders_count == 0:
                average_order_value = 0.00
            else:
                average_order_value = orders_sum / orders_count

            orders_expenses = 0.00
            for order in range_orders:
                order_expense = OrderExpense.objects.filter(order_ref=order).aggregate(Sum('expense_amount'))['expense_amount__sum']
                if order_expense is not None:
                    orders_expenses += order_expense
                else:
                    orders_expenses = orders_expenses + 0.00

            if orders_expenses is None:
                orders_expenses = 0.00
            gross_profit = orders_sum - orders_expenses
            if orders_sum == 0.00:
                gross_profit_percentage = 0.00
            else:
                gross_profit_percentage = (gross_profit / orders_sum) * 100

            
            deliveries_status = DeliveryStatus.objects.filter(orders_delivery_status__order_date__year=today.year).annotate(del_stat_count=Count('orders_delivery_status'), del_stat_sum=Sum('orders_delivery_status__value')).order_by('-del_stat_count')
            delivery_labels = []
            delivery_data = []
            for status in deliveries_status:
                delivery_labels.append(status.delivery_status)
                if status.del_stat_sum is not None:
                    delivery_data.append(status.del_stat_sum)
                else:
                    delivery_data.append(0.00)
            
            payments_status = PaymentStatus.objects.filter(orders_payment_status__order_date__year=today.year).annotate(pay_stat_count=Count('orders_payment_status'), pay_stat_sum=Sum('orders_payment_status__value')).order_by('-pay_stat_count')
            payment_labels = []
            payment_data = []
            for status in payments_status:
                payment_labels.append(status.payment_status)
                if status.pay_stat_sum is not None:
                    payment_data.append(status.pay_stat_sum)
                else:
                    payment_data.append(0.00)

            orders_info = Order.objects.filter(order_date__year=today.year).order_by('-order_ref')

    myFilter = OrderFilter(request.GET, queryset=orders_info)
    orders_info = myFilter.qs

    context = {
        'range': range,
        'orders_count': orders_count,
        'orders_sum': orders_sum,
        'average_order_value': average_order_value,
        'order_expenses': orders_expenses,
        'gross_profit': gross_profit,
        'gross_profit_percentage': gross_profit_percentage,
        'deliveries_status': deliveries_status,
        'delivery_labels': delivery_labels,
        'delivery_data': delivery_data,
        'payments_status': payments_status,
        'payment_labels': payment_labels,
        'payment_data': payment_data,
        # 'pay_terms': pay_terms,
        'orders_info': orders_info,
        'myFilter': myFilter,
    }
    return render(request,'accounts/orders/orders.html', context)



@login_required(login_url='login')
def payment_receipts(request):
    range = "All Time"
    payments_status = PaymentStatus.objects.annotate(pay_stat_count=Count('orders_payment_status'), pay_stat_sum=Sum('orders_payment_status__value')).order_by('-pay_stat_count')
    payment_labels = []
    payment_data = []
    for status in payments_status:
        payment_labels.append(status.payment_status)
        if status.pay_stat_sum is not None:
            payment_data.append(status.pay_stat_sum)
        else:
            payment_data.append(0.00)

    pay_terms = PaymentTerm.objects.annotate(pay_term_count=Count('orders_payment_terms'), pay_term_sum=Sum('orders_payment_terms__value')).order_by('-pay_term_count')
    term_labels = []
    term_data = []
    for term in pay_terms:
        term_labels.append(term.payment_terms)
        if term.pay_term_sum is not None:
            term_data.append(term.pay_term_sum)
        else:
            term_data.append(0.00)
    
    received_payments = PaymentReceipt.objects.all()
    
    if request.method == 'POST':
        dataperiod = request.POST.get('dataperiod')

        # ------------------- TODAY'S DATA -----------------------------------
        if dataperiod == 'today':
            range = "Today's"    
            payments_status = PaymentStatus.objects.filter(orders_payment_status__order_date__gte=datetime.datetime.now()-timedelta(days=0)).annotate(pay_stat_count=Count('orders_payment_status'), pay_stat_sum=Sum('orders_payment_status__value')).order_by('-pay_stat_count')
            
            payment_labels = []
            payment_data = []
            for status in payments_status:
                payment_labels.append(status.payment_status)
                if status.pay_stat_sum is not None:
                    payment_data.append(status.pay_stat_sum)
                else:
                    payment_data.append(0.00)

            pay_terms = PaymentTerm.objects.filter(orders_payment_terms__order_date__gte=datetime.datetime.now()-timedelta(days=0)).annotate(pay_term_count=Count('orders_payment_terms'), pay_term_sum=Sum('orders_payment_terms__value')).order_by('-pay_term_count')
            term_labels = []
            term_data = []
            for term in pay_terms:
                term_labels.append(term.payment_terms)
                if term.pay_term_sum is not None:
                    term_data.append(term.pay_term_sum)
                else:
                    term_data.append(0.00)
            
            received_payments = PaymentReceipt.objects.filter(payment_received_date__gte=datetime.datetime.now()-timedelta(days=0))
    
    
    
        # ------------------- LAST 7 DAYS DATA -----------------------------------
        elif dataperiod == 'last_7_days':
            range = "Last 7 Days"    
            payments_status = PaymentStatus.objects.filter(orders_payment_status__order_date__gte=datetime.datetime.now()-timedelta(days=7)).annotate(pay_stat_count=Count('orders_payment_status'), pay_stat_sum=Sum('orders_payment_status__value')).order_by('-pay_stat_count')
            
            payment_labels = []
            payment_data = []
            for status in payments_status:
                payment_labels.append(status.payment_status)
                if status.pay_stat_sum is not None:
                    payment_data.append(status.pay_stat_sum)
                else:
                    payment_data.append(0.00)

            pay_terms = PaymentTerm.objects.filter(orders_payment_terms__order_date__gte=datetime.datetime.now()-timedelta(days=7)).annotate(pay_term_count=Count('orders_payment_terms'), pay_term_sum=Sum('orders_payment_terms__value')).order_by('-pay_term_count')
            term_labels = []
            term_data = []
            for term in pay_terms:
                term_labels.append(term.payment_terms)
                if term.pay_term_sum is not None:
                    term_data.append(term.pay_term_sum)
                else:
                    term_data.append(0.00)
            
            received_payments = PaymentReceipt.objects.filter(payment_received_date__gte=datetime.datetime.now()-timedelta(days=7))    
    
    
    
        # ------------------- LAST 30 DAYS DATA -----------------------------------
        elif dataperiod == 'last_30_days':
            range = "Last 30 Days"    
            payments_status = PaymentStatus.objects.filter(orders_payment_status__order_date__gte=datetime.datetime.now()-timedelta(days=30)).annotate(pay_stat_count=Count('orders_payment_status'), pay_stat_sum=Sum('orders_payment_status__value')).order_by('-pay_stat_count')
            
            payment_labels = []
            payment_data = []
            for status in payments_status:
                payment_labels.append(status.payment_status)
                if status.pay_stat_sum is not None:
                    payment_data.append(status.pay_stat_sum)
                else:
                    payment_data.append(0.00)

            pay_terms = PaymentTerm.objects.filter(orders_payment_terms__order_date__gte=datetime.datetime.now()-timedelta(days=30)).annotate(pay_term_count=Count('orders_payment_terms'), pay_term_sum=Sum('orders_payment_terms__value')).order_by('-pay_term_count')
            term_labels = []
            term_data = []
            for term in pay_terms:
                term_labels.append(term.payment_terms)
                if term.pay_term_sum is not None:
                    term_data.append(term.pay_term_sum)
                else:
                    term_data.append(0.00)
            
            received_payments = PaymentReceipt.objects.filter(payment_received_date__gte=datetime.datetime.now()-timedelta(days=30))    
    


        # ------------------- LAST 60 DAYS DATA -----------------------------------
        elif dataperiod == 'last_60_days':
            range = "Last 60 Days"    
            payments_status = PaymentStatus.objects.filter(orders_payment_status__order_date__gte=datetime.datetime.now()-timedelta(days=60)).annotate(pay_stat_count=Count('orders_payment_status'), pay_stat_sum=Sum('orders_payment_status__value')).order_by('-pay_stat_count')
            
            payment_labels = []
            payment_data = []
            for status in payments_status:
                payment_labels.append(status.payment_status)
                if status.pay_stat_sum is not None:
                    payment_data.append(status.pay_stat_sum)
                else:
                    payment_data.append(0.00)

            pay_terms = PaymentTerm.objects.filter(orders_payment_terms__order_date__gte=datetime.datetime.now()-timedelta(days=60)).annotate(pay_term_count=Count('orders_payment_terms'), pay_term_sum=Sum('orders_payment_terms__value')).order_by('-pay_term_count')
            term_labels = []
            term_data = []
            for term in pay_terms:
                term_labels.append(term.payment_terms)
                if term.pay_term_sum is not None:
                    term_data.append(term.pay_term_sum)
                else:
                    term_data.append(0.00)
            
            received_payments = PaymentReceipt.objects.filter(payment_received_date__gte=datetime.datetime.now()-timedelta(days=60))



        # ------------------- LAST 90 DAYS DATA -----------------------------------
        elif dataperiod == 'last_90_days':
            range = "Last 90 Days"    
            payments_status = PaymentStatus.objects.filter(orders_payment_status__order_date__gte=datetime.datetime.now()-timedelta(days=90)).annotate(pay_stat_count=Count('orders_payment_status'), pay_stat_sum=Sum('orders_payment_status__value')).order_by('-pay_stat_count')
            
            payment_labels = []
            payment_data = []
            for status in payments_status:
                payment_labels.append(status.payment_status)
                if status.pay_stat_sum is not None:
                    payment_data.append(status.pay_stat_sum)
                else:
                    payment_data.append(0.00)

            pay_terms = PaymentTerm.objects.filter(orders_payment_terms__order_date__gte=datetime.datetime.now()-timedelta(days=90)).annotate(pay_term_count=Count('orders_payment_terms'), pay_term_sum=Sum('orders_payment_terms__value')).order_by('-pay_term_count')
            term_labels = []
            term_data = []
            for term in pay_terms:
                term_labels.append(term.payment_terms)
                if term.pay_term_sum is not None:
                    term_data.append(term.pay_term_sum)
                else:
                    term_data.append(0.00)
            
            received_payments = PaymentReceipt.objects.filter(payment_received_date__gte=datetime.datetime.now()-timedelta(days=90))



        # ------------------- CURRENT MONTH DATA -----------------------------------
        elif dataperiod == 'current_month':
            range = "Current Month's"
            today = datetime.date.today()
            payments_status = PaymentStatus.objects.filter(orders_payment_status__order_date__year=today.year, orders_payment_status__order_date__month=today.month).annotate(pay_stat_count=Count('orders_payment_status'), pay_stat_sum=Sum('orders_payment_status__value')).order_by('-pay_stat_count')
            
            payment_labels = []
            payment_data = []
            for status in payments_status:
                payment_labels.append(status.payment_status)
                if status.pay_stat_sum is not None:
                    payment_data.append(status.pay_stat_sum)
                else:
                    payment_data.append(0.00)

            pay_terms = PaymentTerm.objects.filter(orders_payment_terms__order_date__year=today.year, orders_payment_terms__order_date__month=today.month).annotate(pay_term_count=Count('orders_payment_terms'), pay_term_sum=Sum('orders_payment_terms__value')).order_by('-pay_term_count')
            term_labels = []
            term_data = []
            for term in pay_terms:
                term_labels.append(term.payment_terms)
                if term.pay_term_sum is not None:
                    term_data.append(term.pay_term_sum)
                else:
                    term_data.append(0.00)
            
            received_payments = PaymentReceipt.objects.filter(payment_received_date__year=today.year, payment_received_date__month=today.month)




        # ------------------- CURRENT YEAR DATA -----------------------------------
        elif dataperiod == 'current_year':
            range = "Current Year's"
            today = datetime.date.today()
            payments_status = PaymentStatus.objects.filter(orders_payment_status__order_date__year=today.year).annotate(pay_stat_count=Count('orders_payment_status'), pay_stat_sum=Sum('orders_payment_status__value')).order_by('-pay_stat_count')
            
            payment_labels = []
            payment_data = []
            for status in payments_status:
                payment_labels.append(status.payment_status)
                if status.pay_stat_sum is not None:
                    payment_data.append(status.pay_stat_sum)
                else:
                    payment_data.append(0.00)

            pay_terms = PaymentTerm.objects.filter(orders_payment_terms__order_date__year=today.year).annotate(pay_term_count=Count('orders_payment_terms'), pay_term_sum=Sum('orders_payment_terms__value')).order_by('-pay_term_count')
            term_labels = []
            term_data = []
            for term in pay_terms:
                term_labels.append(term.payment_terms)
                if term.pay_term_sum is not None:
                    term_data.append(term.pay_term_sum)
                else:
                    term_data.append(0.00)
            
            received_payments = PaymentReceipt.objects.filter(payment_received_date__year=today.year)
    
    myFilter = PaymentReceiptFilter(request.GET, queryset=received_payments)
    received_payments = myFilter.qs
    
    context = {
        'range': range,
        'payments_status': payments_status,
        'payment_labels': payment_labels,
        'payment_data': payment_data,
        'pay_terms': pay_terms,
        'term_labels': term_labels,
        'term_data': term_data,
        'received_payments': received_payments,
        'myFilter': myFilter,
    }
    return render(request,'accounts/payment-receipts/payment-receipts.html', context)



@login_required(login_url='login')
def payment_receipts_add(request, pk):
    order = Order.objects.get(order_ref=pk)
    form = PaymentReceiptForm(initial={'order_ref': order.order_ref})
    if request.method == 'POST':
        form = PaymentReceiptForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/orders/')
    context = {
        'order': order,
        'form': form,
    }
    return render(request,'accounts/payment-receipts/payment-receipts-add.html', context)




@login_required(login_url='login')
def payment_receipts_delete(request, pk):
    payment = PaymentReceipt.objects.get(id=pk)
    if request.method == 'POST':
        payment.delete()
        return redirect('/payment-receipts/')
    context = {
        'payment': payment,
    }
    return render(request,'accounts/payment-receipts/payment-receipts-delete.html', context)




@login_required(login_url='login')
def payment_receipts_edit(request, pk):
    payment = PaymentReceipt.objects.get(id=pk)
    form = PaymentReceiptForm(instance=payment)
    if request.method == 'POST':
        form = PaymentReceiptForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()
            return redirect('/payment-receipts/')
    context = {
        'form': form,
    }
    return render(request,'accounts/payment-receipts/payment-receipts-edit.html', context)





@login_required(login_url='login')
def payment_modes(request):

    range = "All"
    payment_modes = PaymentMode.objects.annotate(mode_count=Count('payment_receive_mode'), mode_sum=Sum('payment_receive_mode__received_amount'))
    mode_labels = []
    mode_data = []
    for mode in payment_modes:
        mode_labels.append(mode.payment_mode)
        if mode.mode_sum is not None:
            mode_data.append(mode.mode_sum)
        else:
            mode_data.append(0.00)

    if request.method == 'POST':
        dataperiod = request.POST.get('dataperiod')

        # ------------------- TODAY'S DATA -----------------------------------
        if dataperiod == 'today':
            range = "Today's"
            payment_modes = PaymentMode.objects.filter(payment_receive_mode__payment_received_date__gte=datetime.datetime.now()-timedelta(days=0)).annotate(mode_count=Count('payment_receive_mode'), mode_sum=Sum('payment_receive_mode__received_amount'))
            mode_labels = []
            mode_data = []
            for mode in payment_modes:
                mode_labels.append(mode.payment_mode)
                if mode.mode_sum is not None:
                    mode_data.append(mode.mode_sum)
                else:
                    mode_data.append(0.00)



        # ------------------- LAST 7 DAYS DATA -----------------------------------
        elif dataperiod == 'last_7_days':
            range = "Last 7 Days"
            payment_modes = PaymentMode.objects.filter(payment_receive_mode__payment_received_date__gte=datetime.datetime.now()-timedelta(days=7)).annotate(mode_count=Count('payment_receive_mode'), mode_sum=Sum('payment_receive_mode__received_amount'))
            mode_labels = []
            mode_data = []
            for mode in payment_modes:
                mode_labels.append(mode.payment_mode)
                if mode.mode_sum is not None:
                    mode_data.append(mode.mode_sum)
                else:
                    mode_data.append(0.00)




        # ------------------- LAST 30 DAYS DATA -----------------------------------
        elif dataperiod == 'last_30_days':
            range = "Last 30 Days"
            payment_modes = PaymentMode.objects.filter(payment_receive_mode__payment_received_date__gte=datetime.datetime.now()-timedelta(days=30)).annotate(mode_count=Count('payment_receive_mode'), mode_sum=Sum('payment_receive_mode__received_amount'))
            mode_labels = []
            mode_data = []
            for mode in payment_modes:
                mode_labels.append(mode.payment_mode)
                if mode.mode_sum is not None:
                    mode_data.append(mode.mode_sum)
                else:
                    mode_data.append(0.00)



        # ------------------- LAST 60 DAYS DATA -----------------------------------
        elif dataperiod == 'last_60_days':
            range = "Last 60 Days"
            payment_modes = PaymentMode.objects.filter(payment_receive_mode__payment_received_date__gte=datetime.datetime.now()-timedelta(days=60)).annotate(mode_count=Count('payment_receive_mode'), mode_sum=Sum('payment_receive_mode__received_amount'))
            mode_labels = []
            mode_data = []
            for mode in payment_modes:
                mode_labels.append(mode.payment_mode)
                if mode.mode_sum is not None:
                    mode_data.append(mode.mode_sum)
                else:
                    mode_data.append(0.00)



        # ------------------- LAST 90 DAYS DATA -----------------------------------
        elif dataperiod == 'last_90_days':
            range = "Last 90 Days"
            payment_modes = PaymentMode.objects.filter(payment_receive_mode__payment_received_date__gte=datetime.datetime.now()-timedelta(days=90)).annotate(mode_count=Count('payment_receive_mode'), mode_sum=Sum('payment_receive_mode__received_amount'))
            mode_labels = []
            mode_data = []
            for mode in payment_modes:
                mode_labels.append(mode.payment_mode)
                if mode.mode_sum is not None:
                    mode_data.append(mode.mode_sum)
                else:
                    mode_data.append(0.00)



        # ------------------- CURRENT MONTH DATA -----------------------------------
        elif dataperiod == 'current_month':
            range = "Current Month's"
            today = datetime.date.today()
            payment_modes = PaymentMode.objects.filter(payment_receive_mode__payment_received_date__year=today.year,payment_receive_mode__payment_received_date__month=today.month).annotate(mode_count=Count('payment_receive_mode'), mode_sum=Sum('payment_receive_mode__received_amount'))
            mode_labels = []
            mode_data = []
            for mode in payment_modes:
                mode_labels.append(mode.payment_mode)
                if mode.mode_sum is not None:
                    mode_data.append(mode.mode_sum)
                else:
                    mode_data.append(0.00)



        # ------------------- CURRENT YEAR DATA -----------------------------------
        elif dataperiod == 'current_year':
            range = "Current Year's"
            today = datetime.date.today()
            payment_modes = PaymentMode.objects.filter(payment_receive_mode__payment_received_date__year=today.year).annotate(mode_count=Count('payment_receive_mode'), mode_sum=Sum('payment_receive_mode__received_amount'))
            mode_labels = []
            mode_data = []
            for mode in payment_modes:
                mode_labels.append(mode.payment_mode)
                if mode.mode_sum is not None:
                    mode_data.append(mode.mode_sum)
                else:
                    mode_data.append(0.00)


    context = {
        'range': range,
        'payment_modes': payment_modes,
        'mode_labels': mode_labels,
        'mode_data': mode_data,
    }
    return render(request,'accounts/payment-modes/payment-modes.html', context)




@login_required(login_url='login')
def payment_modes_add(request):
    form = PaymentModeForm
    if request.method == 'POST':
        form = PaymentModeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/payment-modes/')
    context = {
        'form': form,
    }
    return render(request,'accounts/payment-modes/payment-modes-add.html', context)




@login_required(login_url='login')
def payment_modes_delete(request, pk):
    mode = PaymentMode.objects.get(id=pk)
    payment_mode = mode.payment_mode
    if request.method == 'POST':
        mode.delete()
        return redirect('/payment-modes/')
    context = {
        'mode': mode,
        'payment_mode': payment_mode,
    }
    return render(request,'accounts/payment-modes/payment-modes-delete.html', context)




@login_required(login_url='login')
def payment_modes_edit(request, pk):
    mode = PaymentMode.objects.get(id=pk)
    payment_mode = mode.payment_mode
    form = PaymentModeForm(instance=mode)
    if request.method == 'POST':
        form = PaymentModeForm(request.POST, instance=mode)
        if form.is_valid():
            form.save()
            return redirect('/payment-modes/')
    context = {
        'payment_mode': payment_mode,
        'form': form,
    }
    return render(request,'accounts/payment-modes/payment-modes-edit.html', context)






@login_required(login_url='login')
def vendor_cities(request):
    cities_info = VendorCity.objects.all()
    cities = Vendor.objects.values('vendor_city').annotate(purchase_count=Count('paid_to'), purchase_sum=Sum('paid_to__expense_amount'), aov=Sum('paid_to__expense_amount')/Count('paid_to'))
    # cities = cities_info.annotate(purchase_count=Count('paid_to'), purchase_sum=Sum('paid_to__expense_amount'), aov=Sum('paid_to__expense_amount')/Count('paid_to'))
    context = {
        'cities': cities,
        'cities_info': cities_info,
    }
    return render(request, 'accounts/vendor-cities/vendor-cities.html', context)



@login_required(login_url='login')
def vendor_cities_add(request):
    form = VendorCityForm
    if request.method == 'POST':
        form = VendorCityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/vendor-cities/')
    context = {
        'form': form,
    }
    return render(request, 'accounts/vendor-cities/vendor-cities-add.html', context)



@login_required(login_url='login')
def vendor_cities_delete(request, pk):
    city = VendorCity.objects.get(id=pk)
    city_name = city.vendor_city
    if request.method == 'POST':
        city.delete()
        return redirect('/vendor-cities/')
    context = {
        'city': city,
        'city_name': city_name,
    }
    return render(request, 'accounts/vendor-cities/vendor-cities-delete.html', context)



@login_required(login_url='login')
def vendor_cities_edit(request, pk):
    city = VendorCity.objects.get(id=pk)
    city_name = city.vendor_city
    form = VendorCityForm(instance=city)
    if request.method == 'POST':
        form = VendorCityForm(request.POST, instance=city)
        if form.is_valid():
            form.save()
            return redirect('/vendor-cities/')
    context = {
        'city_name': city_name,
        'form': form,
    }
    return render(request, 'accounts/vendor-cities/vendor-cities-edit.html', context)



@login_required(login_url='login')
def vendor(request, pk):
    vendor = Vendor.objects.get(vendor_id=pk)
    purchases = vendor.paid_to.all()
    purchase_count = purchases.count()
    purchase_sum = purchases.aggregate(Sum('expense_amount'))['expense_amount__sum']
   
    if purchase_sum is None or purchase_count is None:
        average_purchase_value = 0.00
    else:
        average_purchase_value = purchase_sum / purchase_count
    
    if purchase_sum is None:
        purchase_sum = 0.00
    
    vendor_purchase = vendor.paid_to.aggregate(first=Min('expense_date'), last=Max('expense_date'))
    total_purchases = OrderExpense.objects.aggregate(Sum('expense_amount'))['expense_amount__sum']
    
    if purchase_sum is None or total_purchases is None:
        percentage_share = 0.00
    else:
        percentage_share = ((purchase_sum) / (total_purchases)) * 100
    
    
    context = {
        'vendor': vendor,
        'purchases': purchases,
        'purchase_count': purchase_count,
        'purchase_sum': purchase_sum,
        'average_purchase_value': average_purchase_value,
        'vendor_purchase': vendor_purchase,
        'total_purchases': total_purchases,
        'percentage_share': percentage_share,
    }
    return render(request,'accounts/vendors/vendor.html', context)



@login_required(login_url='login')
def vendors_add(request):
    form = VendorForm
    if request.method == 'POST':
        form = VendorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/vendors/')
    context = {
        'form': form,
    }
    return render(request,'accounts/vendors/vendors-add.html', context)



@login_required(login_url='login')
def vendors_delete(request, pk):
    vendor = Vendor.objects.get(vendor_id=pk)
    vendor_name = vendor.vendor
    if request.method == 'POST':
        vendor.delete()
        return redirect('/vendors/')
    context = {
        'vendor': vendor,
        'vendor_name': vendor_name,
    }
    return render(request, 'accounts/vendors/vendors-delete.html', context)



@login_required(login_url='login')
def vendors_edit(request, pk):
    vendor = Vendor.objects.get(vendor_id=pk)
    vendor_name = vendor.vendor
    form = VendorForm(instance=vendor)
    if request.method == 'POST':
        form = VendorForm(request.POST, instance=vendor)
        if form.is_valid():
            form.save()
            return redirect('/vendors/')
    context = {
        'vendor_name': vendor_name,
        'form': form,
    }
    return render(request, 'accounts/vendors/vendors-edit.html', context)



@login_required(login_url='login')
def vendors(request):
    range = "All Time"
    vendors_count = Vendor.objects.all().count()
    total_purchases = OrderExpense.objects.all().count()
    purchase_value = OrderExpense.objects.all().aggregate(Sum('expense_amount'))['expense_amount__sum']
    if total_purchases is not None and purchase_value is not None:
        average_purchase_value = purchase_value / vendors_count
    else:
        average_purchase_value = 0.00
    
    vendors_top_five = Vendor.objects.annotate(purchases_count=Count('paid_to'), purchases_sum=Sum('paid_to__expense_amount')).order_by('-purchases_sum')[:5]
    vendor_labels = []
    vendor_data = []
    for vendor in vendors_top_five:
        vendor_labels.append(vendor.vendor)
        if vendor.purchases_sum is not None:
            vendor_data.append(vendor.purchases_sum)
        else:
            vendor_data.append(0.00)

    vendors = Vendor.objects.annotate(purchases_count=Count('paid_to'), purchases_sum=Sum('paid_to__expense_amount'), apv=Sum('paid_to__expense_amount') / Count('paid_to')).order_by('vendor_id')

    if request.method == 'POST':
        dataperiod = request.POST.get('dataperiod')

        # ------------------- TODAY'S DATA -----------------------------------
        if dataperiod == 'today':
            range = "Today's"
            range_purchases = OrderExpense.objects.filter(expense_date__gte=datetime.datetime.now()-timedelta(days=0))

            vendors_count = range_purchases.values('vendor').distinct().count()
            total_purchases = range_purchases.count()
            purchase_value = range_purchases.aggregate(Sum('expense_amount'))['expense_amount__sum']
            if purchase_value is None:
                purchase_value = 0.00
            if vendors_count == 0:
                average_purchase_value = 0.00
            else:
                average_purchase_value = purchase_value / vendors_count
            
            vendors_top_five = Vendor.objects.filter(paid_to__expense_date__gte=datetime.datetime.now()-timedelta(days=0)).annotate(purchases_count=Count('paid_to'), purchases_sum=Sum('paid_to__expense_amount')).order_by('-purchases_sum')[:5]
            vendor_labels = []
            vendor_data = []
            for vendor in vendors_top_five:
                vendor_labels.append(vendor.vendor)
                if vendor.purchases_sum is not None:
                    vendor_data.append(vendor.purchases_sum)
                else:
                    vendor_data.append(0.00)

            vendors = Vendor.objects.filter(paid_to__expense_date__gte=datetime.datetime.now()-timedelta(days=0)).annotate(purchases_count=Count('paid_to'), purchases_sum=Sum('paid_to__expense_amount'), apv=Sum('paid_to__expense_amount') / Count('paid_to')).order_by('vendor_id')


        # ------------------- LAST 7 DAYS DATA -----------------------------------
        elif dataperiod == 'last_7_days':
            range = "Last 7 Days"
            range_purchases = OrderExpense.objects.filter(expense_date__gte=datetime.datetime.now()-timedelta(days=7))

            vendors_count = range_purchases.values('vendor').distinct().count()
            total_purchases = range_purchases.count()
            purchase_value = range_purchases.aggregate(Sum('expense_amount'))['expense_amount__sum']
            if purchase_value is None:
                purchase_value = 0.00
            if vendors_count == 0:
                average_purchase_value = 0.00
            else:
                average_purchase_value = purchase_value / vendors_count
            
            vendors_top_five = Vendor.objects.filter(paid_to__expense_date__gte=datetime.datetime.now()-timedelta(days=7)).annotate(purchases_count=Count('paid_to'), purchases_sum=Sum('paid_to__expense_amount')).order_by('-purchases_sum')[:5]
            vendor_labels = []
            vendor_data = []
            for vendor in vendors_top_five:
                vendor_labels.append(vendor.vendor)
                if vendor.purchases_sum is not None:
                    vendor_data.append(vendor.purchases_sum)
                else:
                    vendor_data.append(0.00)

            vendors = Vendor.objects.filter(paid_to__expense_date__gte=datetime.datetime.now()-timedelta(days=7)).annotate(purchases_count=Count('paid_to'), purchases_sum=Sum('paid_to__expense_amount'), apv=Sum('paid_to__expense_amount') / Count('paid_to')).order_by('vendor_id')



        # ------------------- LAST 30 DAYS DATA -----------------------------------
        elif dataperiod == 'last_30_days':
            range = "Last 30 Days"
            range_purchases = OrderExpense.objects.filter(expense_date__gte=datetime.datetime.now()-timedelta(days=30))

            vendors_count = range_purchases.values('vendor').distinct().count()
            total_purchases = range_purchases.count()
            purchase_value = range_purchases.aggregate(Sum('expense_amount'))['expense_amount__sum']
            if purchase_value is None:
                purchase_value = 0.00
            if vendors_count == 0:
                average_purchase_value = 0.00
            else:
                average_purchase_value = purchase_value / vendors_count
            
            vendors_top_five = Vendor.objects.filter(paid_to__expense_date__gte=datetime.datetime.now()-timedelta(days=30)).annotate(purchases_count=Count('paid_to'), purchases_sum=Sum('paid_to__expense_amount')).order_by('-purchases_sum')[:5]
            vendor_labels = []
            vendor_data = []
            for vendor in vendors_top_five:
                vendor_labels.append(vendor.vendor)
                if vendor.purchases_sum is not None:
                    vendor_data.append(vendor.purchases_sum)
                else:
                    vendor_data.append(0.00)

            vendors = Vendor.objects.filter(paid_to__expense_date__gte=datetime.datetime.now()-timedelta(days=30)).annotate(purchases_count=Count('paid_to'), purchases_sum=Sum('paid_to__expense_amount'), apv=Sum('paid_to__expense_amount') / Count('paid_to')).order_by('vendor_id')



        # ------------------- LAST 60 DAYS DATA -----------------------------------
        elif dataperiod == 'last_60_days':
            range = "Last 60 Days"
            range_purchases = OrderExpense.objects.filter(expense_date__gte=datetime.datetime.now()-timedelta(days=60))

            vendors_count = range_purchases.values('vendor').distinct().count()
            total_purchases = range_purchases.count()
            purchase_value = range_purchases.aggregate(Sum('expense_amount'))['expense_amount__sum']
            if purchase_value is None:
                purchase_value = 0.00
            if vendors_count == 0:
                average_purchase_value = 0.00
            else:
                average_purchase_value = purchase_value / vendors_count
            
            vendors_top_five = Vendor.objects.filter(paid_to__expense_date__gte=datetime.datetime.now()-timedelta(days=60)).annotate(purchases_count=Count('paid_to'), purchases_sum=Sum('paid_to__expense_amount')).order_by('-purchases_sum')[:5]
            vendor_labels = []
            vendor_data = []
            for vendor in vendors_top_five:
                vendor_labels.append(vendor.vendor)
                if vendor.purchases_sum is not None:
                    vendor_data.append(vendor.purchases_sum)
                else:
                    vendor_data.append(0.00)

            vendors = Vendor.objects.filter(paid_to__expense_date__gte=datetime.datetime.now()-timedelta(days=60)).annotate(purchases_count=Count('paid_to'), purchases_sum=Sum('paid_to__expense_amount'), apv=Sum('paid_to__expense_amount') / Count('paid_to')).order_by('vendor_id')




        # ------------------- LAST 90 DAYS DATA -----------------------------------
        elif dataperiod == 'last_90_days':
            range = "Last 90 Days"
            range_purchases = OrderExpense.objects.filter(expense_date__gte=datetime.datetime.now()-timedelta(days=90))

            vendors_count = range_purchases.values('vendor').distinct().count()
            total_purchases = range_purchases.count()
            purchase_value = range_purchases.aggregate(Sum('expense_amount'))['expense_amount__sum']
            if purchase_value is None:
                purchase_value = 0.00
            if vendors_count == 0:
                average_purchase_value = 0.00
            else:
                average_purchase_value = purchase_value / vendors_count
            
            vendors_top_five = Vendor.objects.filter(paid_to__expense_date__gte=datetime.datetime.now()-timedelta(days=90)).annotate(purchases_count=Count('paid_to'), purchases_sum=Sum('paid_to__expense_amount')).order_by('-purchases_sum')[:5]
            vendor_labels = []
            vendor_data = []
            for vendor in vendors_top_five:
                vendor_labels.append(vendor.vendor)
                if vendor.purchases_sum is not None:
                    vendor_data.append(vendor.purchases_sum)
                else:
                    vendor_data.append(0.00)

            vendors = Vendor.objects.filter(paid_to__expense_date__gte=datetime.datetime.now()-timedelta(days=90)).annotate(purchases_count=Count('paid_to'), purchases_sum=Sum('paid_to__expense_amount'), apv=Sum('paid_to__expense_amount') / Count('paid_to')).order_by('vendor_id')



        # ------------------- CURRENT MONTH DATA -----------------------------------
        elif dataperiod == 'current_month':
            range = "Current Month"
            today = datetime.date.today()
            range_purchases = OrderExpense.objects.filter(expense_date__year=today.year, expense_date__month=today.month)

            vendors_count = range_purchases.values('vendor').distinct().count()
            total_purchases = range_purchases.count()
            purchase_value = range_purchases.aggregate(Sum('expense_amount'))['expense_amount__sum']
            if purchase_value is None:
                purchase_value = 0.00
            if vendors_count == 0:
                average_purchase_value = 0.00
            else:
                average_purchase_value = purchase_value / vendors_count
            
            vendors_top_five = Vendor.objects.filter(paid_to__expense_date__year=today.year, paid_to__expense_date__month=today.month).annotate(purchases_count=Count('paid_to'), purchases_sum=Sum('paid_to__expense_amount')).order_by('-purchases_sum')[:5]
            vendor_labels = []
            vendor_data = []
            for vendor in vendors_top_five:
                vendor_labels.append(vendor.vendor)
                if vendor.purchases_sum is not None:
                    vendor_data.append(vendor.purchases_sum)
                else:
                    vendor_data.append(0.00)

            vendors = Vendor.objects.filter(paid_to__expense_date__year=today.year, paid_to__expense_date__month=today.month).annotate(purchases_count=Count('paid_to'), purchases_sum=Sum('paid_to__expense_amount'), apv=Sum('paid_to__expense_amount') / Count('paid_to')).order_by('vendor_id')



        # ------------------- CURRENT YEAR DATA -----------------------------------
        elif dataperiod == 'current_year':
            range = "Current Year"
            today = datetime.date.today()
            range_purchases = OrderExpense.objects.filter(expense_date__year=today.year)

            vendors_count = range_purchases.values('vendor').distinct().count()
            total_purchases = range_purchases.count()
            purchase_value = range_purchases.aggregate(Sum('expense_amount'))['expense_amount__sum']
            if purchase_value is None:
                purchase_value = 0.00
            if vendors_count == 0:
                average_purchase_value = 0.00
            else:
                average_purchase_value = purchase_value / vendors_count
            
            vendors_top_five = Vendor.objects.filter(paid_to__expense_date__year=today.year).annotate(purchases_count=Count('paid_to'), purchases_sum=Sum('paid_to__expense_amount')).order_by('-purchases_sum')[:5]
            vendor_labels = []
            vendor_data = []
            for vendor in vendors_top_five:
                vendor_labels.append(vendor.vendor)
                if vendor.purchases_sum is not None:
                    vendor_data.append(vendor.purchases_sum)
                else:
                    vendor_data.append(0.00)

            vendors = Vendor.objects.filter(paid_to__expense_date__year=today.year).annotate(purchases_count=Count('paid_to'), purchases_sum=Sum('paid_to__expense_amount'), apv=Sum('paid_to__expense_amount') / Count('paid_to')).order_by('vendor_id')


    myFilter = VendorFilter(request.GET, queryset=vendors)
    vendors = myFilter.qs


    context = {
        'range': range,
        'vendors_count': vendors_count,
        'total_purchases': total_purchases,
        'purchase_value': purchase_value,
        'average_purchase_value': average_purchase_value,
        'vendors_top_five': vendors_top_five,
        'vendor_labels': vendor_labels,
        'vendor_data': vendor_data,
        'vendors': vendors,
        'myFilter': myFilter,
    }
    return render(request,'accounts/vendors/vendors.html', context)




@login_required(login_url='login')
def delivery_status(request):

    range = "All Time"
    deliveries_status = DeliveryStatus.objects.annotate(del_stat_count=Count('orders_delivery_status'), del_stat_sum=Sum('orders_delivery_status__value')).order_by('-del_stat_count')
    delivery_labels = []
    delivery_data = []
    for status in deliveries_status:
        delivery_labels.append(status.delivery_status)
        if status.del_stat_sum is not None:
            delivery_data.append(status.del_stat_sum)
        else:
            delivery_data.append(0.00)
    

    if request.method == 'POST':
        dataperiod = request.POST.get('dataperiod')

        # ------------------- TODAY'S DATA -----------------------------------

        if dataperiod == 'today':
            range = "Today's"
            deliveries_status = DeliveryStatus.objects.filter(orders_delivery_status__order_date__gte=datetime.datetime.now()-timedelta(days=0)).annotate(del_stat_count=Count('orders_delivery_status'), del_stat_sum=Sum('orders_delivery_status__value')).order_by('-del_stat_count')
            delivery_labels = []
            delivery_data = []
            for status in deliveries_status:
                delivery_labels.append(status.delivery_status)
                if status.del_stat_sum is not None:
                    delivery_data.append(status.del_stat_sum)
                else:
                    delivery_data.append(0.00)



        # ------------------- LAST 7 DAYS DATA -----------------------------------

        elif dataperiod == 'last_7_days':
            range = "Last 7 Days"
            deliveries_status = DeliveryStatus.objects.filter(orders_delivery_status__order_date__gte=datetime.datetime.now()-timedelta(days=7)).annotate(del_stat_count=Count('orders_delivery_status'), del_stat_sum=Sum('orders_delivery_status__value')).order_by('-del_stat_count')
            delivery_labels = []
            delivery_data = []
            for status in deliveries_status:
                delivery_labels.append(status.delivery_status)
                if status.del_stat_sum is not None:
                    delivery_data.append(status.del_stat_sum)
                else:
                    delivery_data.append(0.00)




        # ------------------- LAST 30 DAYS DATA -----------------------------------

        elif dataperiod == 'last_30_days':
            range = "Last 30 Days"
            deliveries_status = DeliveryStatus.objects.filter(orders_delivery_status__order_date__gte=datetime.datetime.now()-timedelta(days=30)).annotate(del_stat_count=Count('orders_delivery_status'), del_stat_sum=Sum('orders_delivery_status__value')).order_by('-del_stat_count')
            delivery_labels = []
            delivery_data = []
            for status in deliveries_status:
                delivery_labels.append(status.delivery_status)
                if status.del_stat_sum is not None:
                    delivery_data.append(status.del_stat_sum)
                else:
                    delivery_data.append(0.00)




        # ------------------- LAST 60 DAYS DATA -----------------------------------

        elif dataperiod == 'last_60_days':
            range = "Last 60 Days"
            deliveries_status = DeliveryStatus.objects.filter(orders_delivery_status__order_date__gte=datetime.datetime.now()-timedelta(days=60)).annotate(del_stat_count=Count('orders_delivery_status'), del_stat_sum=Sum('orders_delivery_status__value')).order_by('-del_stat_count')
            delivery_labels = []
            delivery_data = []
            for status in deliveries_status:
                delivery_labels.append(status.delivery_status)
                if status.del_stat_sum is not None:
                    delivery_data.append(status.del_stat_sum)
                else:
                    delivery_data.append(0.00)




        # ------------------- LAST 90 DAYS DATA -----------------------------------

        elif dataperiod == 'last_90_days':
            range = "Last 90 Days"
            deliveries_status = DeliveryStatus.objects.filter(orders_delivery_status__order_date__gte=datetime.datetime.now()-timedelta(days=90)).annotate(del_stat_count=Count('orders_delivery_status'), del_stat_sum=Sum('orders_delivery_status__value')).order_by('-del_stat_count')
            delivery_labels = []
            delivery_data = []
            for status in deliveries_status:
                delivery_labels.append(status.delivery_status)
                if status.del_stat_sum is not None:
                    delivery_data.append(status.del_stat_sum)
                else:
                    delivery_data.append(0.00)




        # ------------------- CURRENT MONTH DATA -----------------------------------

        elif dataperiod == 'current_month':
            range = "Current Month's"
            today = datetime.date.today()
            deliveries_status = DeliveryStatus.objects.filter(orders_delivery_status__order_date__year=today.year, orders_delivery_status__order_date__month=today.month).annotate(del_stat_count=Count('orders_delivery_status'), del_stat_sum=Sum('orders_delivery_status__value')).order_by('-del_stat_count')
            delivery_labels = []
            delivery_data = []
            for status in deliveries_status:
                delivery_labels.append(status.delivery_status)
                if status.del_stat_sum is not None:
                    delivery_data.append(status.del_stat_sum)
                else:
                    delivery_data.append(0.00)



        # ------------------- CURRENT YEAR DATA -----------------------------------

        if dataperiod == 'current_year':
            range = "Current Year's"
            today = datetime.date.today()
            deliveries_status = DeliveryStatus.objects.filter(orders_delivery_status__order_date__year=today.year).annotate(del_stat_count=Count('orders_delivery_status'), del_stat_sum=Sum('orders_delivery_status__value')).order_by('-del_stat_count')
            delivery_labels = []
            delivery_data = []
            for status in deliveries_status:
                delivery_labels.append(status.delivery_status)
                if status.del_stat_sum is not None:
                    delivery_data.append(status.del_stat_sum)
                else:
                    delivery_data.append(0.00)


    context = {
        'range': range,
        'deliveries_status': deliveries_status,
        'delivery_labels': delivery_labels,
        'delivery_data': delivery_data,
    }
    return render(request, 'accounts/delivery-status/delivery-status.html', context)



@login_required(login_url='login')
def delivery_status_add(request):
    form = DeliveryStatusForm
    if request.method == 'POST':
        form = DeliveryStatusForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/delivery-status/')
    context = {
        'form': form,
    }
    return render(request, 'accounts/delivery-status/delivery-status-add.html', context)



@login_required(login_url='login')
def delivery_status_delete(request, pk):
    status = DeliveryStatus.objects.get(id=pk)
    delivery_status = status.delivery_status
    if request.method == 'POST':
        status.delete()
        return redirect('/delivery-status/')
    context = {
        'status': status,
        'delivery_status': delivery_status,
    }
    return render(request, 'accounts/delivery-status/delivery-status-delete.html', context)



@login_required(login_url='login')
def delivery_status_edit(request, pk):
    status = DeliveryStatus.objects.get(id=pk)
    delivery_status = status.delivery_status
    form = DeliveryStatusForm(instance=status)
    if request.method == 'POST':
        form = DeliveryStatusForm(request.POST, instance=status)
        if form.is_valid():
            form.save()
            return redirect('/delivery_status/')
    context = {
        'delivery_status': delivery_status,
        'form': form,
    }
    return render(request, 'accounts/delivery-status/delivery-status-edit.html', context)




@login_required(login_url='login')
def payment_status(request):

    range = "All Time"
    payments_status = PaymentStatus.objects.annotate(pay_stat_count=Count('orders_payment_status'), pay_stat_sum=Sum('orders_payment_status__value')).order_by('-pay_stat_count')
    
    payment_labels = []
    payment_data = []
    for status in payments_status:
        payment_labels.append(status.payment_status)
        if status.pay_stat_sum is not None:
            payment_data.append(status.pay_stat_sum)
        else:
            payment_data.append(0.00)

    
    if request.method == 'POST':
        dataperiod = request.POST.get('dataperiod')

        # ------------------- TODAY'S DATA -----------------------------------

        if dataperiod == 'today':
            range = "Today's"

            payments_status = PaymentStatus.objects.filter(orders_payment_status__order_date__gte=datetime.datetime.now()-timedelta(days=0)).annotate(pay_stat_count=Count('orders_payment_status'), pay_stat_sum=Sum('orders_payment_status__value')).order_by('-pay_stat_count')
            payment_labels = []
            payment_data = []
            for status in payments_status:
                payment_labels.append(status.payment_status)
                if status.pay_stat_sum is not None:
                    payment_data.append(status.pay_stat_sum)
                else:
                    payment_data.append(0.00)




        # ------------------- LAST 7 DAYS DATA -----------------------------------

        if dataperiod == 'last_7_days':
            range = "Last 7 Days"

            payments_status = PaymentStatus.objects.filter(orders_payment_status__order_date__gte=datetime.datetime.now()-timedelta(days=7)).annotate(pay_stat_count=Count('orders_payment_status'), pay_stat_sum=Sum('orders_payment_status__value')).order_by('-pay_stat_count')
            payment_labels = []
            payment_data = []
            for status in payments_status:
                payment_labels.append(status.payment_status)
                if status.pay_stat_sum is not None:
                    payment_data.append(status.pay_stat_sum)
                else:
                    payment_data.append(0.00)




        # ------------------- LAST 30 DAYS DATA -----------------------------------

        if dataperiod == 'last_30_days':
            range = "Last 30 Days"

            payments_status = PaymentStatus.objects.filter(orders_payment_status__order_date__gte=datetime.datetime.now()-timedelta(days=30)).annotate(pay_stat_count=Count('orders_payment_status'), pay_stat_sum=Sum('orders_payment_status__value')).order_by('-pay_stat_count')
            payment_labels = []
            payment_data = []
            for status in payments_status:
                payment_labels.append(status.payment_status)
                if status.pay_stat_sum is not None:
                    payment_data.append(status.pay_stat_sum)
                else:
                    payment_data.append(0.00)



        # ------------------- LAST 60 DAYS DATA -----------------------------------

        if dataperiod == 'last_60_days':
            range = "Last 60 Days"

            payments_status = PaymentStatus.objects.filter(orders_payment_status__order_date__gte=datetime.datetime.now()-timedelta(days=60)).annotate(pay_stat_count=Count('orders_payment_status'), pay_stat_sum=Sum('orders_payment_status__value')).order_by('-pay_stat_count')
            payment_labels = []
            payment_data = []
            for status in payments_status:
                payment_labels.append(status.payment_status)
                if status.pay_stat_sum is not None:
                    payment_data.append(status.pay_stat_sum)
                else:
                    payment_data.append(0.00)




        # ------------------- LAST 90 DAYS DATA -----------------------------------

        if dataperiod == 'last_90_days':
            range = "Last 90 Days"

            payments_status = PaymentStatus.objects.filter(orders_payment_status__order_date__gte=datetime.datetime.now()-timedelta(days=90)).annotate(pay_stat_count=Count('orders_payment_status'), pay_stat_sum=Sum('orders_payment_status__value')).order_by('-pay_stat_count')
            payment_labels = []
            payment_data = []
            for status in payments_status:
                payment_labels.append(status.payment_status)
                if status.pay_stat_sum is not None:
                    payment_data.append(status.pay_stat_sum)
                else:
                    payment_data.append(0.00)



        # ------------------- CURRENT MONTH DATA -----------------------------------

        if dataperiod == 'current_month':
            range = "Current Month's"
            today = datetime.date.today()
            payments_status = PaymentStatus.objects.filter(orders_payment_status__order_date__year=today.year, orders_payment_status__order_date__month=today.month).annotate(pay_stat_count=Count('orders_payment_status'), pay_stat_sum=Sum('orders_payment_status__value')).order_by('-pay_stat_count')
            payment_labels = []
            payment_data = []
            for status in payments_status:
                payment_labels.append(status.payment_status)
                if status.pay_stat_sum is not None:
                    payment_data.append(status.pay_stat_sum)
                else:
                    payment_data.append(0.00)




        # ------------------- CURRENT YEAR DATA -----------------------------------

        if dataperiod == 'current_year':
            range = "Current Year's"
            today = datetime.date.today()
            payments_status = PaymentStatus.objects.filter(orders_payment_status__order_date__year=today.year).annotate(pay_stat_count=Count('orders_payment_status'), pay_stat_sum=Sum('orders_payment_status__value')).order_by('-pay_stat_count')
            payment_labels = []
            payment_data = []
            for status in payments_status:
                payment_labels.append(status.payment_status)
                if status.pay_stat_sum is not None:
                    payment_data.append(status.pay_stat_sum)
                else:
                    payment_data.append(0.00)


    context = {
        'range': range,
        'payments_status': payments_status,
        'payment_labels': payment_labels,
        'payment_data': payment_data,
    }
    return render(request, 'accounts/payment-status/payment-status.html', context)



@login_required(login_url='login')
def payment_status_add(request):
    form = PaymentStatusForm
    if request.method == 'POST':
        form = PaymentStatusForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/payment-status/')
    context = {
        'form': form,
    }
    return render(request, 'accounts/payment-status/payment-status-add.html', context)



@login_required(login_url='login')
def payment_status_delete(request, pk):
    status = PaymentStatus.objects.get(id=pk)
    payment_status = status.payment_status
    if request.method == 'POST':
        status.delete()
        return redirect('/payment-status/')
    context = {
        'status': status,
        'payment_status': payment_status,
    }
    return render(request, 'accounts/payment-status/payment-status-delete.html', context)



@login_required(login_url='login')
def payment_status_edit(request, pk):
    status = PaymentStatus.objects.get(id=pk)
    payment_status = status.payment_status
    form = PaymentStatusForm(instance=status)
    if request.method == 'POST':
        form = PaymentStatusForm(request.POST, instance=status)
        if form.is_valid():
            form.save()
            return redirect('/payment_status/')
    context = {
        'payment_status': payment_status,
        'form': form,
    }
    return render(request, 'accounts/payment-status/payment-status-edit.html', context)




@login_required(login_url='login')
def payment_terms(request):
    range = "All Time"
    pay_terms = PaymentTerm.objects.annotate(pay_term_count=Count('orders_payment_terms'), pay_term_sum=Sum('orders_payment_terms__value')).order_by('-pay_term_count')
    term_labels = []
    term_data = []
    for term in pay_terms:
        term_labels.append(term.payment_terms)
        if term.pay_term_sum is not None:
            term_data.append(term.pay_term_sum)
        else:
            term_data.append(0.00)
    

    if request.method == 'POST':
        dataperiod = request.POST.get('dataperiod')

        # ------------------- TODAY'S DATA -----------------------------------

        if dataperiod == 'today':
            range = "Today's"

            pay_terms = PaymentTerm.objects.filter(orders_payment_terms__order_date__gte=datetime.datetime.now()-timedelta(days=0)).annotate(pay_term_count=Count('orders_payment_terms'), pay_term_sum=Sum('orders_payment_terms__value')).order_by('-pay_term_count')
            term_labels = []
            term_data = []
            for term in pay_terms:
                term_labels.append(term.payment_terms)
                if term.pay_term_sum is not None:
                    term_data.append(term.pay_term_sum)
                else:
                    term_data.append(0.00)



        # ------------------- LAST 7 DAYS DATA -----------------------------------

        elif dataperiod == 'last_7_days':
            range = "Last 7 Days"

            pay_terms = PaymentTerm.objects.filter(orders_payment_terms__order_date__gte=datetime.datetime.now()-timedelta(days=7)).annotate(pay_term_count=Count('orders_payment_terms'), pay_term_sum=Sum('orders_payment_terms__value')).order_by('-pay_term_count')
            term_labels = []
            term_data = []
            for term in pay_terms:
                term_labels.append(term.payment_terms)
                if term.pay_term_sum is not None:
                    term_data.append(term.pay_term_sum)
                else:
                    term_data.append(0.00)




        # ------------------- LAST 30 DAYS DATA -----------------------------------

        elif dataperiod == 'last_30_days':
            range = "Last 30 Days"

            pay_terms = PaymentTerm.objects.filter(orders_payment_terms__order_date__gte=datetime.datetime.now()-timedelta(days=30)).annotate(pay_term_count=Count('orders_payment_terms'), pay_term_sum=Sum('orders_payment_terms__value')).order_by('-pay_term_count')
            term_labels = []
            term_data = []
            for term in pay_terms:
                term_labels.append(term.payment_terms)
                if term.pay_term_sum is not None:
                    term_data.append(term.pay_term_sum)
                else:
                    term_data.append(0.00)



        # ------------------- LAST 60 DAYS DATA -----------------------------------

        elif dataperiod == 'last_60_days':
            range = "Last 60 Days"

            pay_terms = PaymentTerm.objects.filter(orders_payment_terms__order_date__gte=datetime.datetime.now()-timedelta(days=60)).annotate(pay_term_count=Count('orders_payment_terms'), pay_term_sum=Sum('orders_payment_terms__value')).order_by('-pay_term_count')
            term_labels = []
            term_data = []
            for term in pay_terms:
                term_labels.append(term.payment_terms)
                if term.pay_term_sum is not None:
                    term_data.append(term.pay_term_sum)
                else:
                    term_data.append(0.00)




        # ------------------- LAST 90 DAYS DATA -----------------------------------

        elif dataperiod == 'last_90_days':
            range = "Last 90 Days"

            pay_terms = PaymentTerm.objects.filter(orders_payment_terms__order_date__gte=datetime.datetime.now()-timedelta(days=90)).annotate(pay_term_count=Count('orders_payment_terms'), pay_term_sum=Sum('orders_payment_terms__value')).order_by('-pay_term_count')
            term_labels = []
            term_data = []
            for term in pay_terms:
                term_labels.append(term.payment_terms)
                if term.pay_term_sum is not None:
                    term_data.append(term.pay_term_sum)
                else:
                    term_data.append(0.00)



        # ------------------- CURRENT MONTH DATA -----------------------------------

        elif dataperiod == 'current_month':
            range = "Current Month's"
            today = datetime.date.today()
            pay_terms = PaymentTerm.objects.filter(orders_payment_terms__order_date__year=today.year, orders_payment_terms__order_date__month=today.month).annotate(pay_term_count=Count('orders_payment_terms'), pay_term_sum=Sum('orders_payment_terms__value')).order_by('-pay_term_count')
            term_labels = []
            term_data = []
            for term in pay_terms:
                term_labels.append(term.payment_terms)
                if term.pay_term_sum is not None:
                    term_data.append(term.pay_term_sum)
                else:
                    term_data.append(0.00)



        # ------------------- CURRENT YEAR DATA -----------------------------------

        elif dataperiod == 'current_year':
            range = "Current Year's"
            today = datetime.date.today()
            pay_terms = PaymentTerm.objects.filter(orders_payment_terms__order_date__year=today.year).annotate(pay_term_count=Count('orders_payment_terms'), pay_term_sum=Sum('orders_payment_terms__value')).order_by('-pay_term_count')
            term_labels = []
            term_data = []
            for term in pay_terms:
                term_labels.append(term.payment_terms)
                if term.pay_term_sum is not None:
                    term_data.append(term.pay_term_sum)
                else:
                    term_data.append(0.00)


    context = {
        'range': range,
        'pay_terms': pay_terms,
        'term_labels': term_labels,
        'term_data': term_data,
    }
    return render(request, 'accounts/payment-terms/payment-terms.html', context)



@login_required(login_url='login')
def payment_terms_add(request):
    form = PaymentTermForm
    if request.method == 'POST':
        form = PaymentTermForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/payment-terms/')
    context = {
        'form': form,
    }
    return render(request, 'accounts/payment-terms/payment-terms-add.html', context)



@login_required(login_url='login')
def payment_terms_delete(request, pk):
    term = PaymentTerm.objects.get(id=pk)
    payment_term = term.payment_terms
    if request.method == 'POST':
        term.delete()
        return redirect('/payment-terms/')
    context = {
        'term': term,
        'payment_term': payment_term,
    }
    return render(request, 'accounts/payment-terms/payment-terms-delete.html', context)



@login_required(login_url='login')
def payment_terms_edit(request, pk):
    term = PaymentTerm.objects.get(id=pk)
    payment_term = term.payment_terms
    form = PaymentTermForm(instance=term)
    if request.method == 'POST':
        form = PaymentTermForm(request.POST, instance=term)
        if form.is_valid():
            form.save()
            return redirect('/payment_terms/')
    context = {
        'payment_term': payment_term,
        'form': form,
    }
    return render(request, 'accounts/payment-terms/payment-terms-edit.html', context)




@login_required(login_url='login')
def employee_names(request):
    employees_info = EmployeeName.objects.all()
    
    context = {
        'employees_info': employees_info,
    }
    return render(request, 'accounts/employee-names/employee-names.html', context)



@login_required(login_url='login')
def employee_names_add(request):
    form = EmployeeNameForm
    if request.method == 'POST':
        form = EmployeeNameForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/employee-names/')
    context = {
        'form': form,
    }
    return render(request, 'accounts/employee-names/employee-names-add.html', context)


@login_required(login_url='login')
def employee_names_delete(request, pk):
    employee = EmployeeName.objects.get(id=pk)
    employee_name = employee.employee_name
    if request.method == 'POST':
        employee.delete()
        return redirect('/employee-names/')
    context = {
        'employee': employee,
        'employee_name': employee_name,
    }
    return render(request, 'accounts/employee-names/employee-names-delete.html', context)



@login_required(login_url='login')
def employee_names_edit(request, pk):
    employee = EmployeeName.objects.get(id=pk)
    employee_name = employee.employee_name
    form = EmployeeNameForm(instance=employee)
    if request.method == 'POST':
        form = EmployeeNameForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('/employee-names/')
    context = {
        'employee_name': employee_name,
        'form': form,
    }
    return render(request, 'accounts/employee-names/employee-names-edit.html', context)



@login_required(login_url='login')
def autosuggest(request):
    query_original = request.GET.get('term')
    queryset = Customer.objects.filter(customer__icontains=query_original)
    mylist = []
    mylist += [x.customer for x in queryset]
    return JsonResponse(mylist, safe=False)



@login_required(login_url='login')
def search_customers(request):    
    if request.method == "POST":
        searched = request.POST['searched']
        customers = Customer.objects.filter(customer__icontains=searched)
        context = {
            'searched': searched,
            'customers': customers,
        }
        return render(request, 'accounts/search-customers.html', context)
    else:
        return render(request, 'accounts/search-customers.html')
