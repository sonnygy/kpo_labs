from django.contrib import admin
from django.urls import path
from users.views import home, user_login, user_signup, create_order, create_order_success, redirect_by_role, user_logout
from orders.views import orders_list, master_page, order_assign_master_view, order_list_view, admin_order_list_view, order_detail_view, order_update_view, create_estimate_view
from warehouse.views import WarehouseListView, WarehouseCreateView, WarehouseUpdateView, admin_page
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('redirect_by_role/', redirect_by_role, name='redirect_by_role'),
    # user
    path('', home, name='home'),
    path('orders/list/', orders_list, name='orders_list'),
    path('orders/create/', create_order, name='create_order'),
    path('orders/create/success/', create_order_success, name='create_order_success'),
    path('signup/', user_signup, name='user_signup'),
    path('login/', user_login, name='user_login'),
    path('logout/', user_logout, name='logout'),

    #admin
    path('administrator/home/', admin_page, name='admin_page'),
    path(
        'administrator/orders/',
        admin_order_list_view.as_view(),
        name='admin_orders'
    ),
    path(
        'administrator/orders/<int:pk>/assign/',
        order_assign_master_view.as_view(),
        name='order_assign_master'
    ),
    path('administrator/warehouse', WarehouseListView.as_view(), name='warehouse_list'),
    path('administrator/warehouse/add', WarehouseCreateView.as_view(), name='warehouse_add'),
    path('administrator/warehouse/<int:pk>/edit', WarehouseUpdateView.as_view(), name='warehouse_update'),
     
    #master
    path('master/home/', master_page, name='master_page'),
    path('master/order/',order_list_view.as_view(), name='master_orders'),
    path('master/order/<int:pk>/', order_detail_view.as_view(), name='master_order_detail'),
    path('master/order/<int:pk>/update', order_update_view.as_view(), name='master_order_update'),
    path('master/order/<int:pk>/estimate', create_estimate_view.as_view(), name='create_estimate'),
]
