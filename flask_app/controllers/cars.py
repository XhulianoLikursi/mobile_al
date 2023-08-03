import os
from flask_app import app
from flask_app.models.user import User
from flask_app.models.car import Car
from flask import render_template, redirect, session, request, flash
from datetime import datetime

from .env import UPLOAD_FOLDER
from .env import ALLOWED_EXTENSIONS
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
from werkzeug.utils import secure_filename

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/add/car')
def addCar():
    if 'user_id' in session:
        data = {
            'user_id': session['user_id']
        }
        loggedUser = User.get_user_by_id(data)
        return render_template('addCar.html', loggedUser = loggedUser)
    return redirect('/')

@app.route('/create/car', methods = ['POST'])
def createCar():
    if 'user_id' in session:
        if not request.files['image']:
            flash('Car image is required!', 'postImage')
            return redirect(request.referrer)
   
        image = request.files['image']
        if not allowed_file(image.filename):
            flash('Image should be in png, jpg, jpeg format!', 'postImage')
            return redirect(request.referrer)
        
        if image and allowed_file(image.filename):
            filename1 = secure_filename(image.filename)
            time = datetime.now().strftime("%d%m%Y%S%f")
            time += filename1
            filename1 = time
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))

        data = {
            'make': request.form['make'],
            'model': request.form['model'],
            'price': request.form.get('price', ''),
            'year': request.form.get('year', ''),
            'kilometer': request.form['kilometer'],
            'fuel': request.form['fuel'],
            'transmission': request.form['transmission'],
            'description': request.form['description'],
            'user_id': session['user_id'],
            'phone_number': request.form['phone_number'],
            'image': filename1
        }
        if not Car.validate_car(data):
            return redirect(request.referrer)
        Car.save(data)
        return redirect('/dashboard')
    return redirect('/')

@app.route('/edit/car/<int:id>')
def editCar(id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'car_id': id
        }
        loggedUser = User.get_user_by_id(data)
        car = Car.get_car_by_id(data)
        if loggedUser['id'] == car['user_id']:
            return render_template('editCar.html', loggedUser = loggedUser, car= car)
        return redirect('/dashboard')
    return redirect('/')

@app.route('/car/<int:id>')
def viewCar(id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'car_id': id
        }
        loggedUser = User.get_user_by_id(data)

        car = Car.get_car_by_id(data)
        soldCars = Car.get_parked_cars()
        if car['id'] in soldCars:
            return redirect('/dashboard')
        return render_template('showOne.html', loggedUser = loggedUser, car= car,)
    return redirect('/')

@app.route('/update/car/<int:id>', methods = ['POST'])
def updateCar(id):
    if 'user_id' in session:
        data1 = {
            'user_id': session['user_id'],
            'car_id': id
        }
        loggedUser = User.get_user_by_id(data1)
        car = Car.get_car_by_id(data1)
        if loggedUser['id'] == car['user_id']:
            data = {
                'make': request.form['make'],
                'model': request.form['model'],
                'price': request.form['price'],
                'year': request.form['year'],
                'kilometer': request.form['kilometer'],
                'fuel': request.form['fuel'],
                'transmission': request.form['transmission'],
                'description': request.form['description'],
                'car_id' : id
                }
            if not Car.validate_car(request.form):
                return redirect(request.referrer)
            Car.update(data)
        return redirect('/dashboard')
    return redirect('/')

@app.route('/delete/car/<int:id>')
def deleteCar(id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'car_id': id
        }
        loggedUser = User.get_user_by_id(data)
        car = Car.get_car_by_id(data)
        if loggedUser['id'] == car['user_id']:
            Car.deleteAllParkings(data)
            Car.delete(data)
            return redirect(request.referrer)

        return redirect('/dashboard')
    return redirect('/')

@app.route('/parked/<int:id>')
def buyCar(id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'car_id': id
        }
        soldCars = Car.get_parked_cars()

        if id not in soldCars:
            Car.buy(data)
            return redirect('/dashboard')
        return redirect(request.referrer)
    return redirect('/')

