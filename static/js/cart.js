// AJAX cart interactions: add, update, delete, and cart count refresh

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

function updateCartCount(qty) {
    const el = document.getElementById('cart-count');
    if (el) el.textContent = qty;
}

async function fetchCartCount() {
    try {
        const response = await fetch('/cart/count/');
        if (!response.ok) return;
        const data = await response.json();
        updateCartCount(data.qty);
    } catch (err) {
        // ignore
        console.error('Error fetching cart count', err);
    }
}

async function addToCart(productId, quantity){
    try{
        const formData = new FormData();
        formData.append('action','post');
        formData.append('product_id', productId);
        formData.append('product_qty', quantity);

        const res = await fetch('/cart/add/', {
            method: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            body: formData
        });
        if (!res.ok) throw new Error('Network response was not ok');
        const data = await res.json();
        if (data.qty !== undefined) updateCartCount(data.qty);
        // Optional: show a small toast or message
    } catch (err){
        console.error('Error adding to cart', err);
    }
}

async function updateCart(productId, quantity){
    try{
        const formData = new FormData();
        formData.append('action','post');
        formData.append('product_id', productId);
        formData.append('product_qty', quantity);

        const res = await fetch('/cart/update/', {
            method: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            body: formData
        });
        if (!res.ok) throw new Error('Network response was not ok');
        const data = await res.json();
        // On success we reload to refresh totals and quantities
        window.location.reload();
    } catch (err){
        console.error('Error updating cart', err);
    }
}

async function deleteFromCart(productId){
    try{
        const formData = new FormData();
        formData.append('action','post');
        formData.append('product_id', productId);

        const res = await fetch('/cart/delete/', {
            method: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            body: formData
        });
        if (!res.ok) throw new Error('Network response was not ok');
        const data = await res.json();
        // Remove the row from DOM if present
        const row = document.querySelector(`[data-cart-row="${productId}"]`);
        if (row) row.remove();
        // Refresh page to update totals
        window.location.reload();
    } catch (err){
        console.error('Error deleting cart item', err);
    }
}

// Event bindings
document.addEventListener('DOMContentLoaded', function(){
    fetchCartCount();

    // Add to cart buttons
    document.querySelectorAll('.add-cart-btn').forEach(function(btn){
        btn.addEventListener('click', function(e){
            const productId = this.dataset.id;
            // find a nearby qty select, else default 1
            let qty = 1;
            const parent = this.closest('.product-card') || document;
            const qtySelect = parent.querySelector('.product-qty') || document.getElementById('qty-cart');
            if (qtySelect) qty = qtySelect.value || 1;
            addToCart(productId, qty);
        });
    });

    // Quantity inputs in cart summary
    document.querySelectorAll('.qty-input').forEach(function(input){
        input.addEventListener('change', function(e){
            const productId = this.dataset.product;
            const qty = this.value;
            updateCart(productId, qty);
        });
    });

    // Delete buttons in cart summary
    document.querySelectorAll('.delete-cart-item').forEach(function(btn){
        btn.addEventListener('click', function(e){
            const productId = this.dataset.product;
            if (!confirm('Remove this item from your cart?')) return;
            deleteFromCart(productId);
        });
    });
});
