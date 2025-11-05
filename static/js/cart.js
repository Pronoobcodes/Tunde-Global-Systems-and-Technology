// Get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Show toast message
function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `alert alert-${type} alert-dismissible fade show position-fixed bottom-0 end-0 m-3`;
    toast.style.zIndex = '1050';
    toast.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
}

// Update cart badge count
function updateCartBadge(qty) {
    const badge = document.getElementById('cart-count');
    if (badge) {
        badge.textContent = qty;
        badge.classList.add('badge-bounce');
        setTimeout(() => badge.classList.remove('badge-bounce'), 300);
    }
}

// Add to cart
async function addToCart(btn) {
    try {
        const productId = btn.dataset.id;
        const qtySelect = document.getElementById('qty-cart');
        if (!qtySelect) return;

        const quantity = parseInt(qtySelect.value);
        if (isNaN(quantity) || quantity < 1) {
            showToast('Please select a valid quantity', 'warning');
            return;
        }

        // Disable button while processing
        btn.disabled = true;
        btn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Adding...';

        const formData = new FormData();
        formData.append('action', 'post');
        formData.append('product_id', productId);
        formData.append('product_qty', quantity);

        const response = await fetch('/cart/add/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: formData
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to add to cart');
        }
        
        updateCartBadge(data.qty);
        showToast(data.message || 'Item added to cart successfully!');
        
        // Update cart total if we're on the cart page
        const totalElement = document.getElementById('cart-total');
        if (totalElement && data.total) {
            totalElement.textContent = `$${data.total.toFixed(2)}`;
        }

    } catch (error) {
        console.error('Error adding to cart:', error);
        showToast(error.message || 'Failed to add item to cart', 'danger');
    } finally {
        // Re-enable button
        btn.disabled = false;
        btn.innerHTML = '<i class="bi bi-cart-plus"></i> Add to Cart';
    }
}

// Update cart quantity
async function updateCartQuantity(select) {
    const row = select.closest('[data-cart-row]');
    const originalValue = select.getAttribute('data-original-value');
    
    try {
        const productId = select.dataset.product;
        const quantity = parseInt(select.value);
        
        if (isNaN(quantity) || quantity < 1) {
            showToast('Please select a valid quantity', 'warning');
            select.value = originalValue;
            return;
        }

        const formData = new FormData();
        formData.append('action', 'post');
        formData.append('product_id', productId);
        formData.append('product_qty', quantity);

        // Show loading state
        if (row) {
            row.style.opacity = '0.5';
            const spinner = document.createElement('div');
            spinner.className = 'position-absolute top-50 start-50 translate-middle';
            spinner.innerHTML = '<div class="spinner-border spinner-border-sm" role="status"></div>';
            row.style.position = 'relative';
            row.appendChild(spinner);
        }

        const response = await fetch('/cart/update/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: formData
        });

        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to update cart');
        }

        // Update cart total and item subtotal
        const totalElement = document.getElementById('cart-total');
        if (totalElement && data.total) {
            totalElement.textContent = `$${data.total.toFixed(2)}`;
        }
        
        showToast(data.message || 'Cart updated successfully');
        select.setAttribute('data-original-value', quantity);

    } catch (error) {
        console.error('Error updating cart:', error);
        showToast(error.message || 'Failed to update quantity', 'danger');
        select.value = originalValue;
    } finally {
        if (row) {
            row.style.opacity = '1';
            const spinner = row.querySelector('.spinner-border');
            if (spinner) spinner.parentElement.remove();
        }
    }
}

// Delete from cart
async function deleteCartItem(btn) {
    try {
        if (!confirm('Are you sure you want to remove this item?')) return;

        const productId = btn.dataset.product;
        const formData = new FormData();
        formData.append('action', 'post');
        formData.append('product_id', productId);

        // Show loading state
        btn.disabled = true;
        const row = btn.closest('[data-cart-row]');
        if (row) {
            row.style.opacity = '0.5';
            const spinner = document.createElement('div');
            spinner.className = 'position-absolute top-50 start-50 translate-middle';
            spinner.innerHTML = '<div class="spinner-border spinner-border-sm" role="status"></div>';
            row.style.position = 'relative';
            row.appendChild(spinner);
        }

        const response = await fetch('/cart/delete/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: formData
        });

        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to delete item');
        }

        // Update cart badge
        updateCartBadge(data.qty);
        
        // Update cart total
        const totalElement = document.getElementById('cart-total');
        if (totalElement && data.total) {
            totalElement.textContent = `$${data.total.toFixed(2)}`;
        }

        if (row) {
            // Fade out animation
            row.style.transition = 'opacity 0.3s ease';
            row.style.opacity = '0';
            
            setTimeout(() => {
                row.remove();
                showToast(data.message || 'Item removed from cart');
                
                // If no items left, refresh to show empty cart template
                const remainingItems = document.querySelectorAll('[data-cart-row]');
                if (remainingItems.length === 0) {
                    window.location.reload();
                }
            }, 300);
        }

    } catch (error) {
        console.error('Error deleting item:', error);
        showToast(error.message || 'Failed to remove item', 'danger');
        if (btn) btn.disabled = false;
        if (row) {
            row.style.opacity = '1';
            const spinner = row.querySelector('.spinner-border');
            if (spinner) spinner.parentElement.remove();
        }
    }
}

// Event Listeners
document.addEventListener('DOMContentLoaded', function() {
    // Add to cart buttons
    document.querySelectorAll('.add-cart-btn').forEach(btn => {
        btn.addEventListener('click', () => addToCart(btn));
    });

    // Cart quantity updates
    document.querySelectorAll('.qty-input').forEach(select => {
        select.addEventListener('change', () => updateCartQuantity(select));
    });

    // Delete cart items
    document.querySelectorAll('.delete-cart-item').forEach(btn => {
        btn.addEventListener('click', () => deleteCartItem(btn));
    });
});

// Add some style for the badge animation
const style = document.createElement('style');
style.textContent = `
    .badge-bounce {
        animation: badge-bounce 0.3s ease-in-out;
    }
    @keyframes badge-bounce {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.2); }
    }
`;
document.head.appendChild(style);