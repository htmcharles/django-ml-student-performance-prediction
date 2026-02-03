import joblib
import numpy as np
import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings

from .serializers import StudentPerformanceSerializer
from rest_framework import status

MODEL_PATH = os.path.join(settings.BASE_DIR, 'performance', 'model.pkl')

@api_view(['POST'])
def predict_performance(request):
    serializer = StudentPerformanceSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response({
            "error": "Input abnormality detected",
            "details": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    model = joblib.load(MODEL_PATH)
    data = serializer.validated_data

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
