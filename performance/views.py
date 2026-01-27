import joblib
import numpy as np
import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings

MODEL_PATH = os.path.join(settings.BASE_DIR, 'performance', 'model.pkl')

@api_view(['POST'])
def predict_performance(request):
    model = joblib.load(MODEL_PATH)   # load ONLY when API is called

    data = request.data

    features = np.array([[
        data['hours_studied'],
        data['previous_scores'],
        1 if data['extracurricular'] else 0,
        data['sleep_hours'],
        data['sample_papers'],
    ]])

    prediction = model.predict(features)[0]

    return Response({
        'predicted_performance_index': round(float(prediction), 2)
    })
