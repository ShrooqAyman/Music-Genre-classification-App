from django.shortcuts import render

from django.shortcuts import render
from django.http import JsonResponse
from sklearn.preprocessing import StandardScaler

from joblib import load
import pandas as pd
import json

model = load('model.joblib')

def indexView(request):
    return render(request, 'index.html')
# Create your views here.
def predictfile(request):
    if request.method == 'POST':
        data = request.POST
        field_example = request.FILES['nameFile']
        df = pd.read_csv(field_example)
        clarity = {'I1':7,'SI2':6,'SI1':5, 'VS2':4, 'VS1':3, 'VVS2':2, 'VVS1':1, 'IF':0}
        color = {'J':6,'I':5,'H':4, 'G':3, 'F':2, 'E':1, 'D':0}
        cut = {'Fair':4,'Good':3,'Very Good':2, 'Premium':1, 'Ideal':0}
        df.clarity.replace(clarity, inplace=True)
        df.color.replace(color, inplace=True)
        df.cut.replace(cut, inplace=True)
        df = df.drop('x', axis=1)
        df = df.drop('y', axis=1)
        df = df.drop('Id', axis=1)
        test_scaled = StandardScaler.fit_transform(df)
        test_scaled = pd.DataFrame(test_scaled,columns=df.columns)


        cat_cols = ['Artist Name', 'Track Name']
        cont_cols =['Popularity','danceability','energy','key','loudness','mode','speechiness','acousticness','instrumentalness','liveness','valence','tempo','duration_in min/ms','time_signature']
        print(test_scaled)
        y_pred = model.predict(test_scaled)
        out = pd.DataFrame(y_pred)
        print(out)
        df['price'] = out
       
        json.dumps(json.loads(df.to_json(orient="records")))


        return JsonResponse(json.dumps(json.loads(df.to_json(orient="records"))),safe=False)