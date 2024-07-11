"""
URL configuration for colaboratorio project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from main import views
#login



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('espacios/', views.espacios_view, name='espacios'),  # Ruta para la vista espacios_view
    path('producto/<int:product_id>/', views.product_detail_view, name='product_detail'),
    path('confirm_reservation/<int:product_id>/', views.confirm_reservation_view, name='confirm_reservation'),

    path('payment/<int:product_id>/', views.payment_view, name='payment'),
    path('create-checkout-session/<int:product_id>/', views.create_checkout_session, name='create_checkout_session'),
    path('success/', views.success_view, name='success'),
    path('cancel/', views.cancel_view, name='cancel'),

    path('producto/<int:product_id>/confirmar/', views.confirm_reservation_view, name='confirm_reservation'),
    path('pago/exito/', views.payment_success_view, name='payment_success'),
    path('pago/cancelado/', views.payment_cancel_view, name='payment_cancel'),
]
    # Otras rutas según sea necesario
    #login
    

