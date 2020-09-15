# Django_Credit_Card_Fraud
Django **REST API** that uses Machine Learning models to predict and detect fraud in online credit card transactions.

"It is important that banks and credit card companies are able to recognize fraudulent credit card transactions so that customers are not charged for items that they did not purchase."

## Dataset
- Credit Card Fraud Detection Dataset on Kaggle : https://www.kaggle.com/mlg-ulb/creditcardfraud

- The datasets contains transactions made by credit cards in September 2013 by european cardholders.

- This dataset presents transactions that occurred in two days, where we have **492 frauds out of 284,807** transactions

- Columns (30 features + class) : [scaled_amount,	scaled_time,	V1,	V2,	V3,	V4,	V5,	V6,	V7,	V8,	V9,	V10,	V11,	V12,	V13,	V14,	V15,	V16,	V17,	V18,	V19,	V20,	V21,	V22,	V23,	V24,	V25,	V26,	V27,	V28,	Class]

- Columns from V1 to V28 have already (originally) been scaled and transformed using PCA. scaled_amount and scaled_time features have been scaled using StandardScaler.

- The dataset is highly umbalanced, the positive class (frauds) account for 0.172% of all transactions. A need for **sampling (udersampling or oversamplig)** before traning machine learning models.

<img src="https://github.com/GitTeaching/Django_Credit_Card_Fraud/blob/master/Django_Credit_Card_Fraud/resources/umbalanced%20dataset.png">

- EDA and processing steps could be found in the notebook : https://github.com/GitTeaching/Django_Credit_Card_Fraud/blob/master/Credit%20Card%20Fraud%20Detection.ipynb

#### Correlations : 
- Negative Correlations: **V17, V14, V12 and V10** are negatively correlated. Notice how the lower these values are, the more likely the end result will be a fraud transaction.
- Positive Correlations: **V2, V4, V11, and V19** are positively correlated. Notice how the higher these values are, the more likely the end result will be a fraud transaction.

<img src="https://github.com/GitTeaching/Django_Credit_Card_Fraud/blob/master/Django_Credit_Card_Fraud/resources/boxplot%201.png">

<img src="https://github.com/GitTeaching/Django_Credit_Card_Fraud/blob/master/Django_Credit_Card_Fraud/resources/boxplot%202.png">

## Modelling

- Tested **classifiers** : Logistic Regression, RandomForest, SVM - with GridSearch for optimization. Best - used in API : Logistic Regression.

- **Sampling approches for umbalanced dataset** : random undersampling before cross-validation, NearMiss undersampling during cross-validation, oversampling before cross-validation, and SMOTE oversampling during cross-validation. 

- Performance metrics : roc_auc_score = 0.9279491847035141.

- Details on the notebook : https://github.com/GitTeaching/Django_Credit_Card_Fraud/blob/master/Credit%20Card%20Fraud%20Detection.ipynb

## The API acces points : "api" app in django project

- **/api/get_preds_api/** : 

This endpoint get a JSON object in a post method, that represents the new transaction as an array data in a string format :

```json
{
"array_data" : "-0.331160, -1.140852, -0.258122, 0.557335, 0.190181, -0.251512, 2.437678, 3.673470, -0.226081, 0.974771, -0.496447, -0.187835, -0.328845, -0.270236, 0.059288, 0.270680, 1.425708, 0.278540, -0.805234, 0.768660, 0.692110, 0.157654, 0.122859, 0.226644, -0.122199, 0.998750, -0.285464, -0.369937, 0.198380, 0.169892"
}
```
- **/api/get_preds_api_columns/** : 

This endpoint get a JSON object in a post method, that represents the new transaction as an array data in a list columns format :

```json
{
 	 "scaled_amount" : -0.331160,
 	 "scaled_time" : -1.140852,
 	 "V1" : -1.3598071336738,
 	 "V2" : -0.0727811733098497,
 	  ....
 	 "V28" : -0.0210530534538215
}
```
Test example could be found here : https://github.com/GitTeaching/Django_Credit_Card_Fraud/blob/master/Django_Credit_Card_Fraud/resources/arraydata%20-%20json%20columns%20-%20for%20testing.txt

## Django web application consuming the API (/api/get_preds_api/): 

"cardfraud" app in django project.

```python
def predict_using_api(request):
	array_data = request.GET.get('data')	
	json_data = {"array_data" : array_data}
	preds = requests.post('http://127.0.0.1:8000/api/get_preds_api/', json=json_data).json()
	context = {'preds':preds, 'txt':array_data}
	return render(request, 'cardfraud/base.html', context)
```
- **Screenshot:**

<img src="https://github.com/GitTeaching/Django_Credit_Card_Fraud/blob/master/Django_Credit_Card_Fraud/resources/Screenshots%201.png" width="700">


