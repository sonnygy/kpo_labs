from django.contrib import admin
from django.urls import path
from users.views import home, user_login, user_signup, create_order, create_order_success
urlpatterns = [
    path('admin/', admin.site.urls),
    # user
    path('', home, name='home'),
    #path('orders/list/', list_orders, name='list_orders'),
    path('orders/create/', create_order, name='create_order'),
    path('orders/create/success/', create_order_success, name='create_order_success'),
    path('signup/', user_signup, name='user_signup'),
    path('login/', user_login, name='user_login'),

    #admin

    #master
]
