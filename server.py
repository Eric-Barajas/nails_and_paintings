from flask_app import app
from flask_app.controllers import nails, paintings, users, carts

if __name__=="__main__":    
    app.run(debug=True)