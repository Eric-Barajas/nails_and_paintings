from flask import Flask, session, flash, request, redirect, render_template
from flask_bcrypt import Bcrypt
import re #regular expression
app = Flask(__name__)
app.secret_key = "This can be any string you want"

bcrypt = Bcrypt(app)