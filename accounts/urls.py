from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index-bkp/', views.index_bkp, name='index-bkp'),
    

    path('customer-cities/', views.customer_cities, name='customer-cities'),
    path('customer-cities-add/', views.customer_cities_add, name='customer-cities-add'),
    path('customer-cities-delete/<str:pk>/', views.customer_cities_delete, name='customer-cities-delete'),
    path('customer-cities-edit/<str:pk>/', views.customer_cities_edit, name='customer-cities-edit'),
    

    path('customers/', views.customers, name='customers'),
    path('customers-add/', views.customers_add, name='customers-add'),
    path('customers-delete/<str:pk>/', views.customers_delete, name='customers-delete'),
    path('customers-edit/<str:pk>/', views.customers_edit, name='customers-edit'),
    path('customer/<str:pk>/', views.customer, name='customer'),
    

    path('expense-categories-general/', views.expense_categories_general, name='expense-categories-general'),
    path('expense-categories-general-add/', views.expense_categories_general_add, name='expense-categories-general-add'),
    path('expense-categories-general-delete/<str:pk>/', views.expense_categories_general_delete, name='expense-categories-general-delete'),
    path('expense-categories-general-edit/<str:pk>/', views.expense_categories_general_edit, name='expense-categories-general-edit'),
    

    path('expense-modes-general/', views.expense_modes_general, name='expense-modes-general'),
    path('expense-modes-general-add/', views.expense_modes_general_add, name='expense-modes-general-add'),
    path('expense-modes-general-delete/<str:pk>/', views.expense_modes_general_delete, name='expense-modes-general-delete'),
    path('expense-modes-general-edit/<str:pk>/', views.expense_modes_general_edit, name='expense-modes-general-edit'),
    

    path('expenses-general/', views.expenses_general, name='expenses-general'),
    path('expenses-general-add/', views.expenses_general_add, name='expenses-general-add'),
    path('expenses-general-delete/<str:pk>/', views.expenses_general_delete, name='expenses-general-delete'),
    path('expenses-general-edit/<str:pk>/', views.expenses_general_edit, name='expenses-general-edit'),


    path('expense-categories-orders/', views.expense_categories_orders, name='expense-categories-orders'),
    path('expense-categories-orders-add/', views.expense_categories_orders_add, name='expense-categories-orders-add'),
    path('expense-categories-orders-delete/<str:pk>/', views.expense_categories_orders_delete, name='expense-categories-orders-delete'),
    path('expense-categories-orders-edit/<str:pk>/', views.expense_categories_orders_edit, name='expense-categories-orders-edit'),
    

    path('expense-modes-orders/', views.expense_modes_orders, name='expense-modes-orders'),
    path('expense-modes-orders-add/', views.expense_modes_orders_add, name='expense-modes-orders-add'),
    path('expense-modes-orders-delete/<str:pk>/', views.expense_modes_orders_delete, name='expense-modes-orders-delete'),
    path('expense-modes-orders-edit/<str:pk>/', views.expense_modes_orders_edit, name='expense-modes-orders-edit'),

    
    path('expenses-orders/', views.expenses_orders, name='expenses-orders'),
    path('expenses-orders-add/<str:pk>/', views.expenses_orders_add, name='expenses-orders-add'),
    path('expenses-orders-delete/<str:pk>/', views.expenses_orders_delete, name='expenses-orders-delete'),
    path('expenses-orders-edit/<str:pk>/', views.expenses_orders_edit, name='expenses-orders-edit'),
    
    
    path('orders/', views.orders, name='orders'),
    path('orders-create/', views.orders_create, name='orders-create'),
    path('orders-delete/<str:pk>/', views.orders_delete, name='orders-delete'),
    path('orders-edit/<str:pk>/', views.orders_edit, name='orders-edit'),
    path('order/<str:pk>/', views.order, name='order'),
    
     
    path('payment-receipts/', views.payment_receipts, name='payment-receipts'),
    path('payment-receipts-add/<str:pk>/', views.payment_receipts_add, name='payment-receipts-add'),
    path('payment-receipts-delete/<str:pk>/', views.payment_receipts_delete, name='payment-receipts-delete'),
    path('payment-receipts-edit/<str:pk>/', views.payment_receipts_edit, name='payment-receipts-edit'),


    path('payment-modes/', views.payment_modes, name='payment-modes'),
    path('payment-modes-add/', views.payment_modes_add, name='payment-modes-add'),
    path('payment-modes-delete/<str:pk>/', views.payment_modes_delete, name='payment-modes-delete'),
    path('payment-modes-edit/<str:pk>/', views.payment_modes_edit, name='payment-modes-edit'),

    
    path('vendor-cities/', views.vendor_cities, name='vendor-cities'),
    path('vendor-cities-add/', views.vendor_cities_add, name='vendor-cities-add'),
    path('vendor-cities-delete/<str:pk>/', views.vendor_cities_delete, name='vendor-cities-delete'),
    path('vendor-cities-edit/<str:pk>/', views.vendor_cities_edit, name='vendor-cities-edit'),
    

    path('vendors/', views.vendors, name='vendors'),
    path('vendors-add/', views.vendors_add, name='vendors-add'),
    path('vendors-delete/<str:pk>/', views.vendors_delete, name='vendors-delete'),
    path('vendors-edit/<str:pk>/', views.vendors_edit, name='vendors-edit'),
    path('vendor/<str:pk>/', views.vendor, name='vendor'),


    path('delivery-status/', views.delivery_status, name='delivery-status'),
    path('delivery-status-add/', views.delivery_status_add, name='delivery-status-add'),
    path('delivery-status-delete/<str:pk>/', views.delivery_status_delete, name='delivery-status-delete'),
    path('delivery-status-edit/<str:pk>/', views.delivery_status_edit, name='delivery-status-edit'),
    

    path('payment-status/', views.payment_status, name='payment-status'),
    path('payment-status-add/', views.payment_status_add, name='payment-status-add'),
    path('payment-status-delete/<str:pk>/', views.payment_status_delete, name='payment-status-delete'),
    path('payment-status-edit/<str:pk>/', views.payment_status_edit, name='payment-status-edit'),


    path('payment-terms/', views.payment_terms, name='payment-terms'),
    path('payment-terms-add/', views.payment_terms_add, name='payment-terms-add'),
    path('payment-terms-delete/<str:pk>/', views.payment_terms_delete, name='payment-terms-delete'),
    path('payment-terms-edit/<str:pk>/', views.payment_terms_edit, name='payment-terms-edit'),


    path('employee-names/', views.employee_names, name='employee-names'),
    path('employee-names-add/', views.employee_names_add, name='employee-names-add'),
    path('employee-names-delete/<str:pk>/', views.employee_names_delete, name='employee-names-delete'),
    path('employee-names-edit/<str:pk>/', views.employee_names_edit, name='employee-names-edit'),

    path('autosuggest/', views.autosuggest, name='autosuggest'),
    path('search-customers/', views.search_customers, name='search-customers'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
]
