from flask import Flask, render_template, redirect, url_for, session, flash ,request

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your actual secret key

# Sample products
products = {
    1: {'name': 'Potting Soil Mix', 'price': 19.99, 'image_url': '/static/images/1.webp', 'description': 'High-quality potting soil mix.'},
    2: {'name': 'VermiCompost', 'price': 9.99, 'image_url': '/static/images/2.webp', 'description': 'Natural compost made from earthworms.'},
    3: {'name': 'Coco Peat', 'price': 12.99, 'image_url': '/static/images/3.webp', 'description': 'Organic coconut fiber for plants.'},
    4: {'name': 'Root Master', 'price': 15.49, 'image_url': '/static/images/4.webp', 'description': 'Enhances root growth for all plants.'}
}

@app.route('/')
def product_list():
    cart_items = session.get('cart', [])
    total_price = sum(item['price'] for item in cart_items)
    cart_item_count = len(cart_items)  # Count of items in the cart
    return render_template('index.html', products=products, cart_items=cart_items, total_price=total_price, cart_item_count=len(cart_items))

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    product = products.get(product_id)
    if product:
        if 'cart' not in session:
            session['cart'] = []

        # Add the product to the cart
        session['cart'].append({
            'product_name': product['name'],
            'description': product['description'],
            'price': product['price'],
            'image_url': product['image_url']  # Store the image URL for cart display
        })
        session.modified = True  # Mark session as modified
    return redirect(url_for('product_list'))

@app.route('/view_cart')
def view_cart():
    cart_items = session.get('cart', [])
    total_price = sum(item['price'] for item in cart_items)
    return render_template('index.html', cart_items=cart_items, total_price=total_price, cart_item_count=len(cart_items))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    cart_items = session.get('cart', [])
    total_price = sum(item['price'] for item in cart_items)

    if request.method == 'POST':
        # Optionally handle the checkout process here
        session.pop('cart', None)  # Clear the cart after checkout
        return redirect(url_for('thank_you'))  # Redirect to thank you page

    return render_template('checkout.html', cart_items=cart_items, total_price=total_price)


@app.route('/clear_cart', methods=['POST'])
def clear_cart():
    # Clear the cart from the session
    session.pop('cart', None)  # Remove the cart from the session
    flash('Your cart has been cleared.', 'success')  # Show success message
    return redirect(url_for('view_cart'))  # Redirect back to the cart view

