
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import Product
from django.urls import reverse

import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

def payment_success_view(request):
    return render(request, 'main/payment_success.html')

def payment_cancel_view(request):
    return render(request, 'main/payment_cancel.html')

def confirm_reservation_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        reservation_date = request.POST.get('reservation_date')

        # Crear una sesión de Stripe Checkout
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': product.name,
                    },
                    'unit_amount': int(product.price * 100),  # Stripe trabaja en centavos
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri(reverse('main/payment_success')),
            cancel_url=request.build_absolute_uri(reverse('main/payment_cancel')),
        )
        return redirect(session.url, code=303)
    else:
        reservation_date = request.GET.get('date')

    return render(request, 'main/confirm_reservation.html', {
        'product': product,
        'reservation_date': reservation_date,
    })

def payment_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'main/payment.html', {
        'product': product,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
    })

@csrf_exempt
def create_checkout_session(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    YOUR_DOMAIN = "http://127.0.0.1:8000"
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': product.name,
                        },
                        'unit_amount': int(product.price * 100),
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/success/',
            cancel_url=YOUR_DOMAIN + '/cancel/',
        )
        return JsonResponse({
            'id': checkout_session.id
        })
    except Exception as e:
        return JsonResponse({'error': str(e)})

def success_view(request):
    return render(request, 'main/success.html')

def cancel_view(request):
    return render(request, 'main/cancel.html')

#mapeo de las direcciones
def index(request):
    return render(request, 'main/base.html')

def crear_varios_productos(request):
    # Crear productos utilizando Product.objects.create()
    product1 = Product.objects.create(
        name="Oficina Privada",
        description="Espacio de oficina equipado con escritorio y sillas.",
        price=100.00  # Precio por día
    )

    product2 = Product.objects.create(
        name="Sala de Reuniones",
        description="Espacio de reuniones con capacidad para 8 personas.",
        price=150.00  # Precio por día
    )

    product3 = Product.objects.create(
        name="Escritorio Flexible",
        description="Escritorio flexible en un espacio compartido.",
        price=50.00  # Precio por día
    )

    product4 = Product.objects.create(
        name="Espacios Abiertos",
        description="Escritorio flexible en un espacio compartido.",
        price=50.00  # Precio por día
    )

    # Guardar los productos en la base de datos
    product1.save()
    product2.save()
    product3.save()
    product4.save()

    # Aquí podrías redirigir a otra vista o renderizar una plantilla
    return render(request, 'espacios.html')

#logica para reservar

def product_detail(request, product_id):
    product = Product.objects.get(pk=product_id)
    # Lógica para reservas, fechas disponibles, etc.
    return render(request, 'main/product_detail.html', {'product': product})

#consultar todos los productos

def espacios_view(request):
    products = Product.objects.all()  # Consulta todos los productos desde la base de datos
    return render(request, 'main/espacios.html', {'products': products})

#vista de detalles de producto

def product_detail_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'main/product_detail.html', {'product': product})
#plantilla dde confirmacion 
def confirm_reservation_view(request, product_id):
    if request.method == 'POST':
        reservation_date = request.POST.get('reservation_date')
        product = get_object_or_404(Product, id=product_id)
        return render(request, 'main/confirm_reservation.html', {
            'product': product,
            'reservation_date': reservation_date,
        })
    return HttpResponse(status=405)

#inicio de login

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Asume que tienes una vista llamada 'home'
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'accounts/login.html')