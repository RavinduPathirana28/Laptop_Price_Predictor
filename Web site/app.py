from functools import lru_cache
from pathlib import Path
import pickle
import sys

BASE_DIR = Path(__file__).resolve().parent
LOCAL_SITE_PACKAGES = BASE_DIR / 'env' / 'Lib' / 'site-packages'

if LOCAL_SITE_PACKAGES.exists():
   sys.path.insert(0, str(LOCAL_SITE_PACKAGES))

from flask import Flask, jsonify, render_template, request, send_from_directory

app = Flask(__name__)


@lru_cache(maxsize=1)
def load_model():
   candidate_paths = [
      BASE_DIR / 'Model' / 'predictor.pickle',
      BASE_DIR.parent / 'Model' / 'predictor.pickle',
   ]

   for filename in candidate_paths:
      if filename.exists():
         with open(filename, 'rb') as file:
            return pickle.load(file)

   raise FileNotFoundError('Could not find predictor.pickle in the project Model folders.')


def prediction(features):
   model = load_model()
   pred_values = model.predict([features])
   return pred_values
@app.route('/',methods=['GET', 'POST'])
def index():
   if request.method=='POST':
      payload = request.get_json(silent=True) or request.form.to_dict(flat=False)
      features = payload.get('features') if isinstance(payload, dict) else None

      if features is not None:
         pred = prediction(features)
         print(pred)
   return render_template("index.html")


@app.route('/predict', methods=['POST'])
def predict():
   payload = request.get_json(silent=True) or request.form.to_dict(flat=False)
   features = payload.get('features') if isinstance(payload, dict) else None

   if not features:
      return jsonify({
         "error": "Missing 'features' payload.",
      }), 400

   pred_values = prediction(features)
   price = float(pred_values[0])

   return jsonify({
      "price": price,
   })


@app.route('/styles.css')
def styles_css():
   return send_from_directory('templates', 'styles.css')


if __name__== '__main__':
    app.run(debug=True)
