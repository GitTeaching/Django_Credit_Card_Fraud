from rest_framework.decorators import api_view
from rest_framework.response import Response
import joblib
import os
from pathlib import Path
import numpy as np

#-----------------------------------------------------------------------

# Loading model at runtime
base_dir = Path(__file__).resolve(strict=True).parent.parent
model = os.path.join(base_dir, 'model.pkl')
joblib_model = joblib.load(model)

#-----------------------------------------------------------------------
# Datapoints samples for testing
# -0.35318941,0.92823624,-1.29844323, 1.94810045,-4.50994689,1.30580477,-0.01948593,-0.50923778,-2.64339762,1.28354519,-2.5153557,-4.50131481,2.09307501,-5.41888894,-1.24701371,-3.82826818,0.39905034,-6.36649951,-7.55096809,-4.90276667,0.15289203,0.25041544,1.17803195,1.36098858,-0.27201306,-0.3259479,0.29070267,0.84129459,0.64309425,0.20115575
# -0.331160,-1.140852,-0.258122,0.557335,0.190181,-0.251512,2.437678,3.673470,-0.226081,0.974771,-0.496447,-0.187835,-0.328845,-0.270236,0.059288,0.270680,1.425708,0.278540,-0.805234,0.768660,0.692110,0.157654,0.122859,0.226644,-0.122199,0.998750,-0.285464,-0.369937,0.198380,0.169892	
#-----------------------------------------------------------------------

# API Views 
@api_view(['GET'])
def api_overview(request):
	api_urls = {
		'Predict - Data as String': '/get_preds_api',
		'Predict - Data as Columns': '/get_preds_api_columns'
	}
	return Response(api_urls)


# 1 - request.data as json, but array data as string. Example :
# {
#    "array_data" : "-0.331160,-1.140852,-0.258122,0.557335,0.190181,-0.251512,2.437678,3.673470,-0.226081,0.974771,-0.496447,-0.187835,-0.328845,-0.270236,0.059288,0.270680,1.425708,0.278540,-0.805234,0.768660,0.692110,0.157654,0.122859,0.226644,-0.122199,0.998750,-0.285464,-0.369937,0.198380,0.169892"
# }
@api_view(['POST'])
def get_preds_api(request):
	result = -1
	preds = ''
	data = request.data['array_data']
	if request.method == 'POST':
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
	return Response(preds)


# 2 - request.data as json, but array data as columns. Example :
# {
# 	 "scaled_amount" : -0.331160,
# 	 "scaled_time" : -1.140852,
# 	 "V1" : -1.3598071336738,
# 	 "V2" : -0.0727811733098497,
# 	  ...
# 	 "V28" : -0.0210530534538215
# }
@api_view(['POST'])
def get_preds_api_columns(request):
	result = -1
	preds = ''
	data = str(request.data['scaled_amount']) + "," + str(request.data['scaled_time']) 
	for i in range(1, 29):
		data = data + "," + str(request.data['V'+str(i)])
	if request.method == 'POST':
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
	return Response(preds)


