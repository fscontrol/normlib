import os
from flask import Flask, request, render_template, session, redirect, url_for
from normlib.ro_normalizer import RONormalizer
from normlib.ro_parameters import ROParameters
from normlib.ro_state import ROState
from dotenv import load_dotenv
from flask import jsonify

load_dotenv()
secret_key = os.getenv('SECRET_KEY')
app = Flask(__name__)
app.secret_key = secret_key


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/save', methods=['POST'])
def save():
    for key, value in request.form.items():
        session[key] = value
    return redirect(url_for('home'))


@app.route('/calc', methods=['POST'])
def calc():
    data = request.get_json()
    standard_params = data.get('standard')
    current_params = data.get('current')
    standard = {}
    current = {}
    result = {}
    try:
        for key, value in standard_params.items():
            k = "_".join(key.split('_')[:-1])
            standard[k] = float(value)
        for key, value in current_params.items():
            k = "_".join(key.split('_')[:-1])
            current[k] = float(value)
        standard_p = ROParameters(**standard)
        current_p = ROParameters(**current)
        normalizer = RONormalizer(ROState(standard_p))
        result["message"] = normalizer.normalize(ROState(current_p))
    except Exception as e:
        result["message"] = str(e)
    finally:
        return jsonify(result)


app.run(debug=True)