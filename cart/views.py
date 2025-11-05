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

    # Build line items for the summary: product, quantity, unit_price, line_total
    line_items = []
    try:
        for product in cart_products:
            pid = str(product.id)
            qty = int(quantities.get(pid, 0)) if quantities else 0
            unit_price = product.sale_price if getattr(product, 'is_sale', False) else product.price
            try:
                line_total = float(unit_price) * int(qty)
            except Exception:
                line_total = 0.0
            line_items.append({
                'product': product,
                'qty': qty,
                'unit_price': unit_price,
                'line_total': round(line_total, 2)
            })
    except Exception:
        line_items = []

    return render(request, 'cart/cart_summary.html', {"cart_products": cart_products, "quantities": quantities, "totals": totals, "line_items": line_items})


def cart_add(request):
    try:
        cart = Cart(request)
        if request.POST.get('action') == 'post':
            product_id = int(request.POST.get('product_id'))
            product_qty = int(request.POST.get('product_qty'))
            
            if product_qty <= 0:
                return JsonResponse({'error': 'Quantity must be greater than 0'}, status=400)
            elif product_qty > 5:
                return JsonResponse({'error': 'Maximum quantity allowed is 5'}, status=400)
                
            product = get_object_or_404(Product, id=product_id)
            cart.add(product=product, quantity=product_qty)
            
            cart_quantity = cart.__len__()
            cart_total = float(cart.cart_total())
            
            response = JsonResponse({
                'qty': cart_quantity,
                'total': cart_total,
            })
            return response
            
    except ValueError as e:
        return JsonResponse({'error': 'Invalid quantity or product ID'}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'Error adding product to cart'}, status=500)

def cart_delete(request):
    try:
        cart = Cart(request)
        if request.POST.get('action') == 'post':
            product_id = int(request.POST.get('product_id'))
            product = get_object_or_404(Product, id=product_id)
            cart.delete(product=product)

            cart_quantity = cart.__len__()
            cart_total = float(cart.cart_total())

            response = JsonResponse({
                'qty': cart_quantity,
                'total': cart_total,
                'message': f"Removed {product.name} from cart"
            })
            return response
    except ValueError:
        return JsonResponse({'error': 'Invalid product ID'}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'Error removing product from cart'}, status=500)


def cart_update(request):
    try:
        cart = Cart(request)
        if request.POST.get('action') == 'post':
            product_id = int(request.POST.get('product_id'))
            product_qty = int(request.POST.get('product_qty'))
            
            if product_qty <= 0:
                return JsonResponse({'error': 'Quantity must be greater than 0'}, status=400)
            elif product_qty > 5:
                return JsonResponse({'error': 'Maximum quantity allowed is 5'}, status=400)
                
            product = get_object_or_404(Product, id=product_id)
            cart.update(product=product, quantity=product_qty)

            cart_quantity = cart.__len__()
            cart_total = float(cart.cart_total())
            
            response = JsonResponse({
                'qty': cart_quantity,
                'total': cart_total,
                'message': f"Updated {product.name} quantity to {product_qty}"
            })
            return response
            
    except ValueError:
        return JsonResponse({'error': 'Invalid quantity or product ID'}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'Error updating product quantity'}, status=500)

def cart_clear(request):
    try:
        if request.POST.get('action') == 'post':
            cart = Cart(request)
            cart.clear()
            response = JsonResponse({
                'qty': 0,
                'total': 0.0,
                'message': 'Cart cleared successfully'
            })
            return response
    except Exception as e:
        return JsonResponse({'error': 'Error clearing cart'}, status=500)