import os
import re
import numpy

import tensorflow as tf
import pandas as pd

from keras.models import load_model
from keras.preprocessing import sequence
from keras.preprocessing.text import Tokenizer
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from .forms import QuestionForm

MODEL_PATH = os.path.join(settings.MEDIA_ROOT, "models/IM_LSTM_Model.h5")
DATASET_PATH = os.path.join(settings.MEDIA_ROOT, "datasets/im_ds.xlsx")
QUESTION_DIC = {0:'IM 問題', 1:'EC 問題', 2:'物流問題'}

def filter_chinese_letter(contexts):
    # \u4E00-\u9FA5 Chinese unicode range
    # a-zA-Z English range
    filter_re = re.compile('[^\u4E00-\u9FA5]') # non Chinese
    i = 0
    for context in contexts:
        contexts[i] = filter_re.sub('', str(context)) # remove all non Chinese letters                   
        i = i + 1
    return contexts

def get_token():
	data_frame = pd.read_excel(DATASET_PATH)
	nd_array = data_frame.values
	features = nd_array[:,0].tolist()
	features = filter_chinese_letter(features)
	tmp_token = Tokenizer(num_words=1000,
                  	  char_level=True)
	tmp_token.fit_on_texts(features)

	return tmp_token

model = load_model(MODEL_PATH)
token = get_token()
graph = tf.get_default_graph() # important

def get_prediction(request):
	predict = ''
	if request.method == 'POST':
		form = QuestionForm(request.POST)
		with graph.as_default(): # important
			predict = predict_question(form['question'].value())
	else:
		form = QuestionForm()
	return render(request, 'predict.html', {'form': form, 'predict': predict})

def predict_question(question):
	input_seq = token.texts_to_sequences([question])
	pad_input_seq = sequence.pad_sequences(input_seq, maxlen=20)
	predict_result = model.predict_classes(pad_input_seq)

	return QUESTION_DIC[predict_result[0]]