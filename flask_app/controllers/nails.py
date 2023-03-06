from flask_app import app, render_template, request, redirect, session
from flask_app.models.nail import Nail


# @app.route('/nails/filter')
# def filter_nails():
#     data = {
#         'shape': request.args.get('shape')
#     }
#     print("***************************************")
#     print(data)
#     print("***************************************")
#     return render_template('index.html', nails = Nail.filter_nails(data) )