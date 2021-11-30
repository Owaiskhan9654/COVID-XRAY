

from __future__ import division, print_function
import sys
import os
import glob
import re
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from flask_ngrok import run_with_ngrok
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from pixellib.semantic import semantic_segmentation


app = Flask(__name__)

def model_predict(img_path,segment_img_path):
    print(img_path)

    interpreter = tf.lite.Interpreter(model_path=r"static/modeltest.tflite")
    interpreter.allocate_tensors()

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    img = image.load_img(img_path, target_size=(512,512))

    x = image.img_to_array(img)

    x = x / 255
    x = np.expand_dims(x, axis=0)


    print(x.shape)
    input_data = np.array(x, dtype=np.float32)

    interpreter.set_tensor(input_details[0]['index'], input_data)

    interpreter.invoke()

    output_data = interpreter.get_tensor(output_details[0]['index'])
    print(output_data)


    preds=np.argmax(output_data, axis=1)
    print(preds)
    if preds==0:
        probability0 = output_data[0][0]
        probability1 = output_data[0][1]
        preds="The X-RAY Sample illustrate COVID Negative with probability of "+str(probability0)+\
              " and COVID Positive with probability of " +str(probability1)
    elif preds==1:
        probability0 = output_data[0][0]
        probability1=output_data[0][1]
        preds="The X-RAY Sample illustrate COVID Positive with probability of " +str(probability1)+ \
              " and COVID Negative with probability of " + str(probability0)

    #try:
    from tensorflow.keras.models import load_model
    models = load_model('static/model_covid_500_epochs.h5')

    modelss = semantic_segmentation(models)
    output_image_name = segment_img_path
    modelss.segmentAsPascalvoc(img_path, output_image_name=output_image_name)

    return preds,output_image_name

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    i=0
    if request.method == 'POST':

        f = request.files['file']

        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)
        i=i+1
        segment_img_path="static/Segmented-Positive"+str(i)+".jpg"
        preds,semantic_segment_path = model_predict(file_path,segment_img_path)
        result=preds
        return result,semantic_segment_path
    return None


if __name__ == '__main__':
    app.run(debug=True)
