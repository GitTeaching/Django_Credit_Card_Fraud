from django.shortcuts import render
import joblib
import os
from pathlib import Path
import numpy as np
import requests
import json

#-----------------------------------------------------------------------

# Loading model at runtime
base_dir = Path(__file__).resolve(strict=True).parent.parent
model = os.path.join(base_dir, 'model.pkl')
joblib_model = joblib.load(model)

#-----------------------------------------------------------------------

# Views 
def home(request):
	txt = "-0.35318941,  0.92823624, -1.29844323,  1.94810045, -4.50994689, 1.30580477, -0.01948593, -0.50923778, -2.64339762,  1.28354519, -2.5153557 , -4.50131481,  2.09307501, -5.41888894, -1.24701371, -3.82826818,  0.39905034, -6.36649951, -7.55096809, -4.90276667, 0.15289203,  0.25041544,  1.17803195,  1.36098858, -0.27201306, -0.3259479 ,  0.29070267,  0.84129459,  0.64309425,  0.20115575"
	context = {'preds':'', 'txt':txt}
	return render(request, 'cardfraud/base.html', context)


def predict_view(request):
	result = -1
	preds = ''
	data = request.GET.get('data')
	if request.method == 'GET':
		try:
			test = np.fromstring(data[1:-1], dtype=np.float, sep=',')
			test = test.reshape(1, -1)
			result = joblib_model.predict(test)
			if result == 0:
				preds = 'Not Fraud'
			elif result == 1:
				preds= 'Fraud'
			else:
				preds = 'Not available'
		except ValueError:
			preds = 'Please, enter correct array data - 30 features'
	context = {'preds':preds, 'txt':data}
	return render(request, 'cardfraud/base.html', context)


def predict_using_api(request):
	array_data = request.GET.get('data')	
	json_data = {"array_data" : array_data}
	preds = requests.post('http://127.0.0.1:8000/api/get_preds_api/', json=json_data).json()
	context = {'preds':preds, 'txt':array_data}
	return render(request, 'cardfraud/base.html', context)


def notebook(request):
	return render(request, 'cardfraud/notebook.html', {})