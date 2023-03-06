from flask_app import app, render_template, request, redirect, session
from flask_app.models.painting import Painting
from flask_app.models.nail import Nail
from flask_app.models.user import User


# ! ////// CREATE  //////
# TODO CREATE REQUIRES TWO ROUTES:
# TODO ONE TO DISPLAY THE FORM:
@app.route('/painting/new')
def new_painting():
    if 'user_id' not in session:
        return redirect('/logout')
        # stops anybody from visiting the page through the url without signing in
    return render_template("new_painting.html")

@app.post("/nails/filter")
def filter_nails():
    session['shape'] = request.form['shape']
    return redirect('/paintings')

@app.post('/paintings/filter')
def filter_paintings():
    session['category'] = request.form['category']
    return redirect('/paintings')

# TODO ONE TO HANDLE THE DATA FROM THE FORM
@app.route('/painting/create',methods=['POST'])
def create_painting():
    print(request.form)
    if not Painting.validate_painting(request.form):
        return redirect('/painting/new')
    Painting.save(request.form)
    return redirect('/paintings')

# TODO READ ALL
@app.route('/paintings')
def paintings():
    if 'user_id' not in session:
        return redirect('/logout')
    if 'shape' not in session:
        nails = Nail.get_all_nails()
    if 'category' not in session:
        paintings = Painting.get_all_with_user()
    if 'shape' in session:
        nail_data = {
            'shape': session['shape']
        }
        nails = Nail.filter_nails(nail_data)
    if 'category' in session:
        painting_data = {
            'category': session['category']
        }
        paintings = Painting.filter_paintings(painting_data)


    return render_template("index.html", paintings=paintings, nails = nails)

# TODO READ ONE
@app.route('/painting/show/<int:id>')
def show_paintings(id):
    data ={ "id": id}
    return render_template("show_painting.html",painting = Painting.get_one(data))

# ! ///// UPDATE /////
# TODO UPDATE REQUIRES TWO ROUTES
# TODO ONE TO SHOW THE FORM
@app.route('/painting/edit/<int:id>')
def edit_painting(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data ={ "id": id}
    return render_template("edit_painting.html",painting=Painting.get_one(data))

# TODO ONE TO HANDLE THE DATA FROM THE FORM
@app.route('/painting/update',methods=['POST'])
def update_painting():
    if not Painting.validate_painting(request.form):
        return redirect(f"/painting/edit/{request.form['id']}")
    Painting.update(request.form)
    return redirect('/paintings')

# ! ///// DELETE //////
@app.route('/painting/destroy/<int:id>')
def destroy_painting(id):
    data ={'id': id}
    Painting.destroy(data)
    return redirect('/paintings')

@app.route('/painting/add/<int:id>')
def add_to_cart(id):
    data = {'painting_id': id, 'cart_id': session['user_id']}
    Painting.add_painting_to_cart(data)
    return redirect('/paintings')
