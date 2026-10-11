import os
import json
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'rizq_allah_secret_key_2026'
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

DATA_FILE = 'data.json'

DEFAULT_DATA = {
    "owner_password_hash": generate_password_hash("7243"),
    "company_info": {
        "brand_name": "Rizq Allah",
        "brand_sub": "RENT CAR ALGERIE",
        "phone1": "+213 55 99 32 64",
        "phone2": "+213 781 92 73 19",
        "notification_email": "saidziani567@gmail.com",
        "address": "Tizi ouzou maatkas",
        "theme_color": "#2563eb",
        "logo_url": "",
        "banner_url": ""
    },
    "cars": [
        {
            "id": 1,
            "name": "Dacia Sandero Stepway",
            "category": "Économique",
            "price": 6500,
            "transmission": "Manuelle",
            "fuel": "Essence",
            "seats": 5,
            "location": "Alger / Oran",
            "status": "Disponible",
            "image": "https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=600&q=80"
        },
        {
            "id": 2,
            "name": "Renault Symbol 1.6",
            "category": "Berline",
            "price": 5500,
            "transmission": "Manuelle",
            "fuel": "Essence",
            "seats": 5,
            "location": "Alger",
            "status": "Disponible",
            "image": "https://images.unsplash.com/photo-1541899481282-d53bffe3c35d?auto=format&fit=crop&w=600&q=80"
        },
        {
            "id": 3,
            "name": "Volkswagen Golf 8 R-Line",
            "category": "Luxe / Sport",
            "price": 18000,
            "transmission": "Automatique",
            "fuel": "Essence",
            "seats": 5,
            "location": "Alger Centre",
            "status": "Disponible",
            "image": "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?auto=format&fit=crop&w=600&q=80"
        },
        {
            "id": 4,
            "name": "Hyundai Tucson 4WD",
            "category": "SUV / 4x4",
            "price": 14000,
            "transmission": "Automatique",
            "fuel": "Gasoil (Diesel)",
            "seats": 5,
            "location": "Oran / Tizi Ouzou",
            "status": "En Location",
            "image": "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?auto=format&fit=crop&w=600&q=80"
        }
    ],
    "bookings": []
}

def load_data():
    if not os.path.exists(DATA_FILE):
        save_data(DEFAULT_DATA)
        return DEFAULT_DATA
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        save_data(DEFAULT_DATA)
        return DEFAULT_DATA

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Routes
@app.route('/')
def index():
    data = load_data()
    return render_template('index.html', company=data['company_info'], cars=data['cars'])

@app.route('/admin')
def admin():
    if not session.get('is_owner'):
        return render_template('login.html', company=load_data()['company_info'])
    data = load_data()
    return render_template('admin.html', company=data['company_info'], cars=data['cars'], bookings=data['bookings'])

@app.route('/api/login', methods=['POST'])
def login():
    req_data = request.get_json()
    password = req_data.get('password', '')
    data = load_data()
    
    if check_password_hash(data['owner_password_hash'], password):
        session['is_owner'] = True
        return jsonify({"success": True, "message": "Connexion réussie"})
    return jsonify({"success": False, "message": "Mot de passe incorrect"}), 401

@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop('is_owner', None)
    return jsonify({"success": True})

@app.route('/api/cars', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api_cars():
    data = load_data()
    
    if request.method == 'GET':
        return jsonify(data['cars'])
        
    if not session.get('is_owner'):
        return jsonify({"error": "Non autorisé"}), 403

    if request.method == 'POST':
        car_data = request.form.to_dict()
        file = request.files.get('image_file')
        image_url = car_data.get('image_url', '')

        if file and file.filename != '':
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            image_url = f"/static/uploads/{filename}"

        new_car = {
            "id": int(os.urandom(4).hex(), 16),
            "name": car_data.get('name'),
            "category": car_data.get('category'),
            "price": float(car_data.get('price', 0)),
            "transmission": car_data.get('transmission'),
            "fuel": car_data.get('fuel'),
            "seats": int(car_data.get('seats', 5)),
            "location": car_data.get('location'),
            "status": car_data.get('status', 'Disponible'),
            "image": image_url or "https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=600&q=80"
        }
        data['cars'].insert(0, new_car)
        save_data(data)
        return jsonify({"success": True, "car": new_car})

    if request.method == 'PUT':
        car_id = int(request.form.get('id'))
        car = next((c for c in data['cars'] if c['id'] == car_id), None)
        if car:
            car['name'] = request.form.get('name', car['name'])
            car['category'] = request.form.get('category', car['category'])
            car['price'] = float(request.form.get('price', car['price']))
            car['transmission'] = request.form.get('transmission', car['transmission'])
            car['fuel'] = request.form.get('fuel', car['fuel'])
            car['seats'] = int(request.form.get('seats', car['seats']))
            car['location'] = request.form.get('location', car['location'])
            car['status'] = request.form.get('status', car['status'])
            
            file = request.files.get('image_file')
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                car['image'] = f"/static/uploads/{filename}"

            save_data(data)
            return jsonify({"success": True, "car": car})
        return jsonify({"error": "Véhicule introuvable"}), 404

    if request.method == 'DELETE':
        car_id = request.json.get('id')
        data['cars'] = [c for c in data['cars'] if c['id'] != car_id]
        save_data(data)
        return jsonify({"success": True})

@app.route('/api/bookings', methods=['POST'])
def api_bookings():
    req = request.get_json()
    data = load_data()
    booking = {
        "id": int(os.urandom(4).hex(), 16),
        "clientName": req.get('clientName'),
        "clientPhone": req.get('clientPhone'),
        "clientWilaya": req.get('clientWilaya'),
        "clientPermit": req.get('clientPermit'),
        "carName": req.get('carName'),
        "startDate": req.get('startDate'),
        "endDate": req.get('endDate'),
        "totalPrice": req.get('totalPrice'),
        "timestamp": request.headers.get('Date', '')
    }
    data['bookings'].insert(0, booking)
    save_data(data)
    return jsonify({"success": True, "booking": booking})

@app.route('/api/settings', methods=['POST'])
def api_settings():
    if not session.get('is_owner'):
        return jsonify({"error": "Non autorisé"}), 403

    data = load_data()
    info = data['company_info']

    info['brand_name'] = request.form.get('brand_name', info['brand_name'])
    info['brand_sub'] = request.form.get('brand_sub', info['brand_sub'])
    info['phone1'] = request.form.get('phone1', info['phone1'])
    info['phone2'] = request.form.get('phone2', info['phone2'])
    info['notification_email'] = request.form.get('notification_email', info['notification_email'])
    info['address'] = request.form.get('address', info['address'])
    info['theme_color'] = request.form.get('theme_color', info['theme_color'])

    # Logo Upload
    logo_file = request.files.get('logo_file')
    if logo_file and logo_file.filename != '':
        fname = secure_filename(f"logo_{logo_file.filename}")
        fpath = os.path.join(app.config['UPLOAD_FOLDER'], fname)
        logo_file.save(fpath)
        info['logo_url'] = f"/static/uploads/{fname}"

    # Banner Upload
    banner_file = request.files.get('banner_file')
    if banner_file and banner_file.filename != '':
        fname = secure_filename(f"banner_{banner_file.filename}")
        fpath = os.path.join(app.config['UPLOAD_FOLDER'], fname)
        banner_file.save(fpath)
        info['banner_url'] = f"/static/uploads/{fname}"

    save_data(data)
    return jsonify({"success": True})

@app.route('/api/change-password', methods=['POST'])
def change_password():
    if not session.get('is_owner'):
        return jsonify({"error": "Non autorisé"}), 403

    req = request.get_json()
    data = load_data()
    current_p = req.get('currentPassword')
    new_p = req.get('newPassword')

    if not check_password_hash(data['owner_password_hash'], current_p):
        return jsonify({"success": False, "message": "Mot de passe actuel incorrect"}), 400

    data['owner_password_hash'] = generate_password_hash(new_p)
    save_data(data)
    return jsonify({"success": True, "message": "Mot de passe mis à jour avec succès"})

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(host='0.0.0.0', port=5000, debug=True)
