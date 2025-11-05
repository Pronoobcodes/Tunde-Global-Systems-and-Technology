from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from store.models import Product
from .cart import Cart


# Create your views here.

def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    totals = cart.cart_total()
    quantities = cart.get_qyt()
    return render(request, 'cart/cart_summary.html', {"cart_products":cart_products, "quantities":quantities, "totals":totals})


def cart_add(request):
    try:
        cart = Cart(request)
        if request.POST.get('action') == 'post':
            product_id = int(request.POST.get('product_id'))
            product_qty = int(request.POST.get('product_qty'))
            
            # Validate quantity
            if product_qty <= 0:
                return JsonResponse({
                    'error': 'Quantity must be greater than 0'
                }, status=400)
                
            product = get_object_or_404(Product, id=product_id)
            cart.add(product=product, quantity=product_qty)
            
            cart_quantity = cart.__len__()
            cart_total = float(cart.cart_total())  # Convert Decimal to float
            
            response = JsonResponse({
                'qty': cart_quantity,
                'total': cart_total,
                'message': f"Added {product_qty} {product.name} to cart"
            })
            messages.success(request, f"Added {product_qty} {product.name} to cart")
            return response
            
    except ValueError as e:
        return JsonResponse({
            'error': 'Invalid quantity or product ID'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'error': 'Error adding product to cart'
        }, status=500)


def cart_delete(request):
    try:
        cart = Cart(request)
        if request.POST.get('action') == 'post':
            product_id = int(request.POST.get('product_id'))
            product = get_object_or_404(Product, id=product_id)
            cart.delete(product=product)
            
            cart_quantity = cart.__len__()
            cart_total = float(cart.cart_total())  # Convert Decimal to float
            
            response = JsonResponse({
                'qty': cart_quantity,
                'total': cart_total,
                'product_id': product_id,
                'message': f"Removed {product.name} from cart"
            })
            messages.success(request, f"Removed {product.name} from cart")
            return response
            
    except ValueError as e:
        return JsonResponse({
            'error': 'Invalid product ID'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'error': 'Error removing product from cart'
        }, status=500)


def cart_update(request):
    try:
        cart = Cart(request)
        if request.POST.get('action') == 'post':
            product_id = int(request.POST.get('product_id'))
            product_qty = int(request.POST.get('product_qty'))
            
            # Validate quantity
            if product_qty <= 0:
                return JsonResponse({
                    'error': 'Quantity must be greater than 0'
                }, status=400)
            elif product_qty > 5:
                return JsonResponse({
                    'error': 'Maximum quantity allowed is 5'
                }, status=400)
                
            product = get_object_or_404(Product, id=product_id)
            cart.update(product=product, quantity=product_qty)
            
            cart_total = float(cart.cart_total())  # Convert Decimal to float
            
            response = JsonResponse({
                'qty': product_qty,
                'total': cart_total,
                'message': f"Updated {product.name} quantity to {product_qty}"
            })
            messages.success(request, f"Updated {product.name} quantity to {product_qty}")
            return response
            
    except ValueError as e:
        return JsonResponse({
            'error': 'Invalid quantity or product ID'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'error': 'Error updating cart'
        }, status=500)
        
    return redirect('cart_summary')


def cart_count(request):
    cart = Cart(request)
    return JsonResponse({'qty': cart.__len__()})

def clear(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        cart.clear()
        return cart