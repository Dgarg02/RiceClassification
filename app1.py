import tensorflow as tf
import tensorflow_hub as hub
import warnings
warnings.filterwarnings('ignore')
import h5py
import numpy as np
import os
from flask import Flask, app, request, render_template
from tensorflow import keras
import cv2
from flask import Flask

model = tf.keras.models.load_model(filepath='rice.h5', custom_objects={'KerasLayer': hub.KerasLayer})
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/details')
def pred():
    return render_template('details.html')


@app.route('/result', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        f = request.files['image']
        basepath = os.path.dirname(__file__)  # getting the current path i.e. where app.py is present
        filepath = os.path.join(basepath, 'Data', 'val', f.filename)  # saving the file
        f.save(filepath)

        a2 = cv2.imread(filepath)
        a2 = cv2.resize(a2, (224, 224))
        a2 = np.array(a2)
        a2 = a2 / 255
        a2 = np.expand_dims(a2, 0)

        pred = model.predict(a2)
        pred = pred.argmax()

        df_labels = {
            'arborio': 0,
            'basmati': 1,
            'ipsala': 2,
            'jasmine': 3,
            'karacadag': 4
        }

        for i, j in df_labels.items():
            if pred == j:
                prediction = i

        return render_template('results.html', prediction_text=prediction)    

if __name__=="__main__":
    app.run(debug= True)
