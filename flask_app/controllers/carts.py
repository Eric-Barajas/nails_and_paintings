from flask_app import app, render_template, request, redirect, session
from flask_app.models.cart import Cart
from flask_app.models.painting import Painting

@app.route('/cart')
def shopping_cart():
    data = {'id': session['user_id']}
    print(data)
    return render_template('cart.html', paintings = Cart.show_items_in_cart(data))