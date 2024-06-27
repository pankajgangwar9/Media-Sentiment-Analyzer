import os 
import sys
sys.path.insert(0, 'E:/FinalYearProject/FinalYearProject')
sys.path.insert(0, 'E:/FinalYearProject/FinalYearProject/src/')
from src.exception import CostumException
from src.logger import logging 
import pandas as pd
import matplotlib.pyplot as plt

from flask import Flask, render_template, redirect, url_for, session, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired, Email, ValidationError
import bcrypt
from flask_mysqldb import MySQL
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from src.pipeline.predict_pipeline import CustomData
from src.pipeline.train_pipeline import TrainPipeline


app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'pan@9911'
app.config['MYSQL_DB'] = 'youtube'
app.secret_key = 'your_secret_key_here'

mysql = MySQL(app)

class RegisterForm(FlaskForm):
    name = StringField("Name",validators=[DataRequired()])
    email = StringField("Email",validators=[DataRequired(), Email()])
    password = PasswordField("Password",validators=[DataRequired()])
    submit = SubmitField("Register")

    def validate_email(self,field):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users where email=%s",(field.data,))
        user = cursor.fetchone()
        cursor.close()
        if user:
            raise ValidationError('Email Already Taken')

class LoginForm(FlaskForm):
    email = StringField("Email",validators=[DataRequired(), Email()])
    password = PasswordField("Password",validators=[DataRequired()])
    submit = SubmitField("Login")

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    image_filename = 'example.jpg'
    return render_template('about.html',image_filename=image_filename)

@app.route('/prapna')
def prapna():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        try:
            # store data into database 
            cursor = mysql.connection.cursor()
            cursor.execute("INSERT INTO users (name,email,password) VALUES (%s,%s,%s)", (name, email, hashed_password))
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for('login'))
        except Exception as e:
            print("Error occurred during registration:", e)

    return render_template('register.html', form=form)

@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email=%s",(email,))
        user = cursor.fetchone()
        cursor.close()
        if user and bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')):
            session['user_id'] = user[0]
            return redirect(url_for('dashboard'))
        else:
            flash("Login failed. Please check your email and password")
            return redirect(url_for('login'))

    return render_template('login.html',form=form)
@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        user_id = session['user_id']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users where id=%s",(user_id,))
        user = cursor.fetchone()
        cursor.close()

        if user:
            return render_template('dashboard.html',user=user)
            
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("You have been logged out successfully.")
    return redirect(url_for('login'))

@app.route('/youtube',methods=['GET','POST'])
def youtube():
    if request.method=='GET':
        return render_template('youtube.html')
    else:
        data=CustomData(
                link=request.form.get('link')
            )
        data.send_link()
        file = 'E:/FinalYearProject/FinalYearProject/src/components/output.csv'
        data = pd.read_csv(file)

        categories = ["Positive","Negative"]
        value_map = {"Positive": 1, "Negative": 0}
    
        # Replace values in the list
        replaced_data = [value_map[value] if value in value_map else value for value in list(data['Sentiment'])]
        values=[replaced_data.count(1),replaced_data.count(0)]

        # Plotting pie chart
        plt.figure(figsize=(8, 6))
        plt.pie(values, labels=categories, autopct='%.1f%%', startangle=140,shadow=True)
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.title('Pie Chart of Categorical Data')
        plt.legend(loc="upper left")
        circle=plt.Circle(xy=(0,0), radius=.75, facecolor='white')
        plt.gca().add_artist(circle)
        
        # Save the plot to a file or render it directly
        plt.savefig('E:/FinalYearProject/FinalYearProject/static/images/pie_chart.png')  # Save as a file
        #plt.show()  # Render directly

        return render_template('result.html', data=data)


@app.route('/movie',methods=['GET','POST'])
def movie():
        if request.method=='GET':
            return render_template('movie.html')
        else:
            data=CustomData(
                link=request.form.get('link')
            )
            data.send_link()
        file = 'E:/FinalYearProject/FinalYearProject/src/components/output.csv'
        data = pd.read_csv(file)

        categories = ["Positive","Negative"]
        value_map = {"Positive": 1, "Negative": 0}
    
        # Replace values in the list
        replaced_data = [value_map[value] if value in value_map else value for value in list(data['Sentiment'])]
        values=[replaced_data.count(1),replaced_data.count(0)]

        # Plotting pie chart
        plt.figure(figsize=(8, 6))
        plt.pie(values, labels=categories, autopct='%.1f%%', startangle=140,shadow=True)
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.title('Pie Chart of Categorical Data')
        plt.legend(loc="upper left")
        circle=plt.Circle(xy=(0,0), radius=.75, facecolor='white')
        plt.gca().add_artist(circle)
        
        # Save the plot to a file or render it directly
        plt.savefig('E:/FinalYearProject/FinalYearProject/static/images/pie_chart.png')  # Save as a file
        #plt.show()  # Render directly

        return render_template('result.html', data=data)

@app.route('/flipkart',methods=['GET','POST'])
def flipkart():
        if request.method=='GET':
            return render_template('flipkart.html')
        else:
            data=CustomData(
                link=request.form.get('link')
            )
            data.send_link()
        file = 'E:/FinalYearProject/FinalYearProject/src/components/output.csv'
        data = pd.read_csv(file)

        categories = ["Positive","Negative"]
        value_map = {"Positive": 1, "Negative": 0}
    
        # Replace values in the list
        replaced_data = [value_map[value] if value in value_map else value for value in list(data['Sentiment'])]
        values=[replaced_data.count(1),replaced_data.count(0)]

        # Plotting pie chart
        plt.figure(figsize=(8, 6))
        plt.pie(values, labels=categories, autopct='%.1f%%', startangle=140,shadow=True)
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.title('Pie Chart of Categorical Data')
        plt.legend(loc="upper left")
        circle=plt.Circle(xy=(0,0), radius=.75, facecolor='white')
        plt.gca().add_artist(circle)
        
        # Save the plot to a file or render it directly
        plt.savefig('E:/FinalYearProject/FinalYearProject/static/images/pie_chart.png')  # Save as a file
        #plt.show()  # Render directly

        return render_template('result.html', data=data)

if __name__=="__main__":
    app.run(debug=True)