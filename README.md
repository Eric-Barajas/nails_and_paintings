# 👋 Introducing `Studio Design Shop Repo`

## Table of Contents
* [Description](#Description)
* [Features](#Features)
* [Technologies Used](#Technologies-Used)
* [Functionality](#Functionality)

___

## Description
A full stack e-commerce website that sells handmade paintings and nails

[Return to Table of Contents](#Table-of-Contents)

___

## Features
* Displays various types of nails and paintings 
* Can create your own account
* Can add however many items you want to your personal cart
* In order to add items to your cart you have to be signed in

[Return to Table of Contents](#Table-of-Contents)

___

## Technologies Used
* Python <img align="left" alt="Python" width="20px" style="padding-right:10px;" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-plain.svg" />

* MySql <img align="left" alt="MySQL" width="20px" style="padding-right:10px;" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/mysql/mysql-original-wordmark.svg" />

* VSCode <img align="left" alt="VSCode" width="20px" style="padding-right:10px;" src="https://www.vectorlogo.zone/logos/visualstudio_code/visualstudio_code-icon.svg" />

* Flask <img style="background-color:white; overflow:hidden;" align="left" alt="Flask" width="20px" style="padding-right:10px;" src="https://www.vectorlogo.zone/logos/pocoo_flask/pocoo_flask-icon.svg" />

* HTML5 <img align="left" alt="html" width="20px" style="padding-right:10px;" src="https://www.vectorlogo.zone/logos/w3_html5/w3_html5-icon.svg" />

* CSS <img align="left" alt="css" width="20px" style="padding-right:10px;" src="https://www.vectorlogo.zone/logos/w3_css/w3_css-icon.svg" />

* BOOTSTRAP <img align="left" alt="Bootstrap" width="20px" style="padding-right:10px;" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/bootstrap/bootstrap-original.svg" />

* Jinja2 <img align="left" alt="jinja2" width="20px" style="padding-right:10px;" src="https://www.vectorlogo.zone/logos/pocoo_jinja/pocoo_jinja-icon.svg" />

[Return to Table of Contents](#Table-of-Contents)


___

## Functionality
You first Log in or make an account 

<img src="https://github.com/Purposefully/PurposefulGroups/blob/main/images/survey_question.png?raw=true" alt="Survey questions" width="500">  

You browse the items and select add whatever item you want to your cart

<img src="https://github.com/Purposefully/PurposefulGroups/blob/main/images/choose_file.png?raw=true" alt="Choose a data file" width="500">  

You can click on the cart icon to see the list of items you have added to your cart 

<img src="https://github.com/Purposefully/PurposefulGroups/blob/main/images/teacher_options.png?raw=true" alt="Teacher Options" width="500">  

[Return to Table of Contents](#Table-of-Contents)

___

# flask_checklist

# Set Up Database

- [ ] create a sample [database](db/template.sql) to work with your sample app.
- [ ] The `.sql` file above will create a database from the following ERD:

![ ](./flask_app/static/images/erd.png) 

## Initial Setup

- [x] create directory
- [ ] create the virtual environment:

```
pipenv install flask pymysql flask-bcrypt
```
- [ ] activate the virtual environment:

```
pipenv shell
```

- [ ] create [server.py](server.py) with the following content:

```py
from flask_app import app
from flask_app.controllers import things, users

if __name__=="__main__":    
    app.run(debug=True)
```


- [ ] create database connection with [mysqlconnection.py](flask_app/config/mysqlconnection.py) with the following content:

```py
# a cursor is the object we use to interact with the database
import pymysql.cursors
# this class will give us an instance of a connection to our database
class MySQLConnection:
    def __init__(self, db):
        # change the user and password as needed
        connection = pymysql.connect(host = 'localhost',
                                    user = 'root', 
                                    password = 'root', 
                                    db = db,
                                    charset = 'utf8mb4',
                                    cursorclass = pymysql.cursors.DictCursor,
                                    autocommit = True)
        # establish the connection to the database
        self.connection = connection
    # the method to query the database
    def query_db(self, query, data=None):
        with self.connection.cursor() as cursor:
            try:
                query = cursor.mogrify(query, data)
                print("Running Query:", query)
     
                cursor.execute(query, data)
                if query.lower().find("insert") >= 0:
                    # INSERT queries will return the ID NUMBER of the row inserted
                    self.connection.commit()
                    return cursor.lastrowid
                elif query.lower().find("select") >= 0:
                    # SELECT queries will return the data from the database as a LIST OF DICTIONARIES
                    result = cursor.fetchall()
                    return result
                else:
                    # UPDATE and DELETE queries will return nothing
                    self.connection.commit()
            except Exception as e:
                # if the query fails the method will return FALSE
                print("Something went wrong", e)
                return False
            finally:
                # close the connection
                self.connection.close() 
# connectToMySQL receives the database we're using and uses it to create an instance of MySQLConnection
def connectToMySQL(db):
    return MySQLConnection(db)
```

## Create `flask_app` Package

- all flask files except `server.py` will now be in [flask_app](flask_app/__init__.py)
- [ ] the [`__init__.py`](./flask_app/__init__.py) is what makes `flask_app` a package. It has the following content:

```py
from flask import Flask, session, flash
from flask_bcrypt import Bcrypt
import re
app = Flask(__name__)
app.secret_key = "This can be any string you want"

bcrypt = Bcrypt(app)
```
### Models

- [ ] add a [models](flask_app/models/thing.py) directory with the following content:

```py
from flask_app.config.mysqlconnection import connectToMySQL
from pprint import pprint
DATABASE = 'template'

class Thing:
    def __init__(self, data:dict) -> None:
        self.id = data['id']
        self.column1 = data['column1']
        self.column2 = data['column2']
        self.column3 = data['column3']
        self.column4 = data['column4']
        self.column5 = data['column5']
        self.user_id = data['user_id']
        if 'first_name' in data:
            self.user = data['first_name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    # ! CREATE
    @classmethod
    def save(cls, data:dict) -> int:
        query = "INSERT INTO things (column1,column2,column3,column4,column5, user_id) VALUES (%(column1)s, %(column2)s, %(column3)s, %(column4)s, %(column5)s, %(user_id)s);"
        result = connectToMySQL(DATABASE).query_db(query,data)
        return result

    # ! READ/RETRIEVE ALL
    @classmethod
    def get_all(cls) -> list:
        query = "SELECT * FROM things;"
        results = connectToMySQL(DATABASE).query_db(query)
        things = []
        for u in results:
            things.append( cls(u) )
        return things
 
    # ! READ/RETRIEVE ALL
    @classmethod
    def get_all_with_user(cls) -> list:
        query = "SELECT * FROM things JOIN users ON users.id = things.user_id;"
        results = connectToMySQL(DATABASE).query_db(query)
        pprint(results)
        things = []
        for u in results:
            things.append( cls(u) )
        return things
    
    # ! READ/RETRIEVE ONE
    @classmethod
    def get_one(cls,data:dict) -> object:
        query  = "SELECT * FROM things WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        return cls(result[0])

    # ! UPDATE
    @classmethod
    def update(cls,data:dict) -> int:
        query = "UPDATE things SET column1=%(column1)s,column2=%(column2)s,column3=%(column3)s, column4=%(column4)s, column5=%(column5)s, user_id=%(user_id)s WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)

    # ! DELETE
    @classmethod
    def destroy(cls,data:dict):
        query  = "DELETE FROM things WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)
```


### Templates(aka Views)

#### Index

- [ ] create a [templates](flask_app/templates/index.html) directory with an `index.html` file as follows:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <title>index</title>
</head>
<body>
    <div class="container">
        <div class="row">
            <div class="col">
                <h1>Register</h1>
                <p class="text-right"><a href="/">Home</a></p>
                {% with messages = get_flashed_messages() %}    
                {% if messages %}                        
                    {% for message in messages %}     
                        <p>{{message}}</p>          
                    {% endfor %}
                {% endif %}
            {% endwith %}
                <form action="/register/user" method="post">
                  <div class="form-group">
                    <label>First Name</label>
                    <input type="text" class="form-control" placeholder="first name" name="first_name"> 
                  </div>
                  <div class="form-group">
                    <label>Last Name</label>
                    <input type="text" class="form-control" placeholder="last name" name="last_name"> 
                  </div>
                  <div class="form-group">
                    <label>Email</label>
                    <input type="text" class="form-control" placeholder="email" name="email"> 
                  </div>
                  <div class="form-group">
                    <label>Password</label>
                    <input type="password" class="form-control" placeholder="Password" value="password" name="password">
                  </div>
                  <div class="form-group">
                    <label>Confirm Password</label>
                    <input type="password" class="form-control" placeholder="Password" value="password" name="confirm-password">
                  </div>
                  <button type="submit" class="btn btn-primary">Submit</button>
                </form>
            </div>
            <div class="col">
                <h1>Login</h1>
                <p class="text-right"><a href="/">Home</a></p>
                {% with messages = get_flashed_messages() %}    
                {% if messages %}                        
                    {% for message in messages %}     
                        <p>{{message}}</p>          
                    {% endfor %}
                {% endif %}
            {% endwith %}
                <form action="/login" method="post">
                  <div class="form-group">
                    <label>Email</label>
                    <input type="text" class="form-control" placeholder="email" name="email"> 
                  </div>
                  <div class="form-group">
                    <label>Password</label>
                    <input type="password" class="form-control" placeholder="Password" value="password" name="password">
                  </div>
                  <button type="submit" class="btn btn-primary">Submit</button>
                </form>
            </div>
        </div>
    </div>
</body>
</html>
```

#### Models (show all models)

- [ ] add [models.html](flask_app/templates/models.html):

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- CSS only -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
    <title>models</title>
</head>
<body>
    <div class="container">
        <div class="row"></div>
            <div class="float-end mt-3 mb-3">
                <a class="btn btn-danger" href="/logout">logout</a>
                <a class="btn btn-secondary" href="/models">home</a>
            </div>

            <h1 class="text-center">Here are our models!!!</h1>
            <table class="table table-hover">
                <thead>
                    <tr>
                        <th>Column One</th>
                        <th>Column Two</th>
                        <th>Column Three</th>
                        <th>Created At</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {% for model in models %}
                    <tr>
                        <td>{{ model.column1 }}</td>
                        <td>{{ model.column2 }}</td>
                        <td>{{ model.column3}}</td>
                    <td>{{ model.created_at.strftime("%b %d %Y") }}</td>
                    <td>
                        <a href="/model/show/{{ model.id }}">Show</a> |
                        <a href="/model/edit/{{ model.id }}">Edit</a> |
                        <a href="/model/destroy/{{ model.id }}">Delete</a>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        <a href="/model/new" class="btn btn-primary">Add a model</a>
    </div>

</body>
</html>
```
#### New (create a model)

  - [ ] add [new_model.html](flask_app/templates/new_model.html):

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- CSS only -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
    <title>Create model</title>
</head>
<body>
    <div class="container">
        <div class="float-end mt-3 mb-3">
            <a class="btn btn-danger" href="/logout">logout</a>
            <a class="btn btn-secondary" href="/models">home</a>
        </div>
        <form action="/model/create" method="post" class="col-6 mx-auto">
            <h2 class="text-center">Add model</h2>
            <div class="form-group">
                <label for="column1">column1:</label>
                <input type="text" name="column1"  class="form-control">
        </div>
        <div class="form-group">
            <label for="column2">column2:</label>
            <input type="text" name="column2"  class="form-control">
        </div>
        <div class="form-group">
            <label for="column3">column3:</label>
            <input type="text" name="column3"  class="form-control">
        </div>
        <input type="submit" value="Add model" class="btn btn-success">
    </form>
</div>
</body>
</html>
```

#### Edit (edit a model)

  - [ ] add [edit_model.html](flask_app/templates/edit_model.html):

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- CSS only -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
    <title>Edit model</title>
</head>
<body>
    <div class="container">
        <div class="float-end mt-3 mb-3">
            <a class="btn btn-danger" href="/logout">logout</a>
            <a class="btn btn-secondary" href="/models">home</a>
        </div>
        <form action="/model/update" method="post" class="col-6 mx-auto">
            <h2 class="text-center">Edit {{model.id}}</h2>
        <input type="hidden" name="id" value={{model.id}}>
        <div class="form-group">
            <label for="column1">column1:</label>
            <input type="text" name="column1"  class="form-control" value="{{model.column1}}">
        </div>
        <div class="form-group">
            <label for="column2">column2:</label>
            <input type="text" name="column2" class="form-control" value="{{model.column2}}">
        </div>
        <div class="form-group">
            <label for="column3">column3:</label>
            <input type="text" name="column3"  class="form-control" value="{{model.column3}}">
        </div>
        <input type="submit" value="Update model" class="btn btn-success">
    </form>
</div>
</body>
</html>
```

#### Show (show an individual model)

- [ ] add [show_model.html](flask_app/templates/show_model.html):

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
    <title>model</title>
</head>
<body>
    <div class="container">
        <div class="float-end mt-3 mb-3">
            <a class="btn btn-danger" href="/logout">logout</a>
            <a class="btn btn-secondary" href="/models">home</a>
        </div>
        <h2 class="text-center">model {{model.id}}</h2>
        <p>column1 {{model.column1}}</p>
        <p>column2: {{model.column2}}</p>
        <p>column3: {{model.column3}}</p>
        
        <p>Created ON: {{model.created_at.strftime("%b %d %Y")}}</p>
        <p>Last Updated: {{  model.updated_at.strftime("%b %d %Y")}}</p>
    </div>
</body>
</html>
```


### Controllers

- [ ] add a [controllers](flask_app/controllers/things.py) directory:

```py
from flask import render_template, request, redirect
from flask_app import app
from flask_app.models.thing import Thing

# ! ////// CREATE  //////
# TODO CREATE REQUIRES TWO ROUTES:
# TODO ONE TO DISPLAY THE FORM:
@app.route('/thing/new')
def new_thing():
    return render_template("new_thing.html")

# TODO ONE TO HANDLE THE DATA FROM THE FORM
@app.route('/thing/create',methods=['POST'])
def create_thing():
    print(request.form)
    Thing.save(request.form)
    return redirect('/things')

# TODO READ ALL
@app.route('/things')
def things():
    return render_template("things.html",things=Thing.get_all_with_user())

# TODO READ ONE
@app.route('/thing/show/<int:id>')
def show_things(id):
    data ={ 
        "id":id
    }
    return render_template("show_thing.html",thing=Thing.get_one(data))

# ! ///// UPDATE /////
# TODO UPDATE REQUIRES TWO ROUTES
# TODO ONE TO SHOW THE FORM
@app.route('/thing/edit/<int:id>')
def edit_thing(id):
    data ={ 
        "id":id
    }
    return render_template("edit_thing.html",thing=Thing.get_one(data))

# TODO ONE TO HANDLE THE DATA FROM THE FORM
@app.route('/thing/update',methods=['POST'])
def update_thing():
    Thing.update(request.form)
    return redirect('/things')

# ! ///// DELETE //////
@app.route('/thing/destroy/<int:id>')
def destroy_thing(id):
    data ={
        'id': id
    }
    Thing.destroy(data)
    return redirect('/things')

```


### Static files

- [ ] add [static](flask_app/static) directory. File structure should look like this:

![](flask_app/static/images/static-file.png)

## Start the server

```
python server.py
```
 - [ ] visit [localhost:5000](http://localhost:5000/)

# Registration and Login

- [ ] install bcrypt:

```
pipenv install flask-bcrypt
```

- [ ] add a [users.py](flask_app/controllers/users.py) controller with the following content:

```py
from flask import render_template, request, redirect, session, flash
from flask_app import app, bcrypt
from flask_app.models.user import User

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/register/user", methods=['POST'])
def register():
    print(request.form)
    if not User.validate_user(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password" : pw_hash
    }
    user_id = User.save(data)
    session['user_id'] = user_id
    session['user_name'] = f"{request.form['first_name']} {request.form['last_name']}"
    return redirect('/things')

@app.route('/login', methods=['post'])
def login():
    data = {'email': request.form['email']}
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash('invalid credentials')
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('invalid credentials')
        return redirect('/')
    session['user_id'] = user_in_db.id
    session['user_name'] =f"{user_in_db.first_name} {user_in_db.last_name}" 
    return redirect('/things')

@app.route('/user/show/<int:id>')
def user_show(id):
    data = {'id': id}
    
    return render_template('show_user.html', user=User.get_user_with_things(data))

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

```

- [ ] add a [user.py](flask_app/models/user.py) model with the following content:

```py
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash, re
from pprint import pprint
from flask_app.models.thing import Thing

DATABASE = 'template'
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.things = []
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def save(cls, data:dict ) -> int:
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(DATABASE).query_db( query, data )

    ## ! used in user validation
    @classmethod
    def get_by_email(cls,data:dict) -> object or bool:
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        print(result)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_user_with_things(cls, data:dict):
        query = "SELECT * FROM users LEFT JOIN things ON users.id = things.user_id WHERE users.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        pprint(results)
        user = cls(results[0])
        for result in results:
            thing_dict = {
                'id': result['things.id'],
                'column1': result['column1'],
                'column2': result['column2'],
                'column3': result['column3'],
                'column4': result['column4'],
                'column5': result['column5'],
                'user_id': result['user_id'],
                'created_at': result['things.created_at'],
                'updated_at': result['things.updated_at']
            }
            user.things.append(Thing(thing_dict))
        return user


    @staticmethod
    def validate_user(user:dict) -> bool:
        is_valid = True # ! we assume this is true
        if len(user['first_name']) < 3:
            flash("Name must be at least 3 characters.")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Name must be at least 3 characters.")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False
        if user['password'] != user['confirm-password']:
            flash("Passwords do not match")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 character long.")
            is_valid = False
        return is_valid

```
[Return to Table of Contents](#Table-of-Contents)


