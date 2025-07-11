from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Q
from django.core.mail import send_mail
from .models import MenuItem, OrderModel, Category

# Create your views here.
class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/index.html')
    
class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/about.html')
    
class Order(View):
    def get(self, request, *args, **kwargs):
        # Get every Item from each category 
        appetizers = MenuItem.objects.filter(category__name__contains = 'Appetizer')
        entres = MenuItem.objects.filter(category__name__contains = 'Entre')
        desserts = MenuItem.objects.filter(category__name__contains = 'Dessert')
        drinks = MenuItem.objects.filter(category__name__contains = 'Drink')
        # Pass into context
        context = {
            'appetizers':appetizers,
            'entres':entres,
            'desserts':desserts,
            'drinks':drinks,
        }
        # Render the template
        return render(request, 'customer/order.html', context)
    
    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        tel = request.POST.get('tel')
        email = request.POST.get('email')
        street = request.POST.get('street')

        order_items = {
            'items' : []
        }
        items = request.POST.getlist('items[]')
        for item in items:
            menu_item = MenuItem.objects.get(pk__contains=int(item))
            item_data = {
                'id' : menu_item.pk,
                'name' : menu_item.name,
                'price' : menu_item.price,
            }
            order_items['items'].append(item_data)

            price = 0
            item_ids = []
        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])

        order = OrderModel.objects.create(
            price=price,
            name=name,
            tel=tel,
            email=email,
            street=street
            )
        order.items.add(*item_ids)

        # After everything is done, send confirmation email to the user
        body = ('Thank you for your order. Your food is being made and will be delivered soon \n'
                f'Your Total: {price} \n'
                'Thank you for ordering at City Fast Food Restaurant')
        
        send_mail(
            'Thank You for Your Order',
            body,
            'example@emplae.com',
            [email],
            fail_silently=False
            )


        context = {
            'items' : order_items['items'],
            'price' : price,
        }
        
        return redirect('order-confirmation', pk=order.pk)

class OrderConfirmation(View):
    def get(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)
        context = {
            'pk': order.pk,
            'items': order.items,
            'price': order.price,
        }
        return render(request, 'customer/order_confirmation.html', context)
    
    def post(self, request, pk, *args, **kwargs):
        print(request.body)

class OrderPayConfirmation(View):
    def get(self, request, pk, *args, **kwargs):
        return render(request, 'customer/order_pay_confirmation.html')
    
class Menu(View):
    def get(self, request, *args, **kwargs):
        menu_items = MenuItem.objects.all()
        context = {
            'menu_items' : menu_items
        }
        return render(request, 'customer/menu.html', context)
    
class MenuSearch(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('q')
        menu_items = MenuItem.objects.filter(
            Q(name__icontains=query) |
            Q(price__icontains=query) |
            Q(description__icontains=query)
        )
        context = {
            'menu_items' : menu_items
        }
        return render(request, 'customer/menu.html', context)