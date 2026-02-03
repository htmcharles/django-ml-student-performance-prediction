import joblib
import numpy as np
import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings

from django.shortcuts import render

from .serializers import StudentPerformanceSerializer
from rest_framework import status

MODEL_PATH = os.path.join(settings.BASE_DIR, 'performance', 'model.pkl')

def perform_prediction(data):
    model = joblib.load(MODEL_PATH)
    features = np.array([[
        data['hours_studied'],
        data['previous_scores'],
        1 if data['extracurricular'] else 0,
        data['sleep_hours'],
        data['sample_papers'],
    ]])
    prediction = model.predict(features)[0]
    return round(float(prediction), 2)

@api_view(['POST'])
def predict_performance(request):
    serializer = StudentPerformanceSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response({
            "error": "Input abnormality detected",
            "details": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    prediction = perform_prediction(serializer.validated_data)

    return Response({
        'predicted_performance_index': prediction
    })

def predict_ui(request):
    context = {}
    if request.method == 'POST':
        # Convert QueryDict to a dict that serializer can handle
        data = request.POST.copy()
        # Handle boolean conversion for extracurricular
        data['extracurricular'] = data.get('extracurricular') == 'true'
        
        serializer = StudentPerformanceSerializer(data=data)
        if serializer.is_valid():
            context['prediction'] = perform_prediction(serializer.validated_data)
        else:
            context['error'] = "Input abnormality detected"
            context['details'] = serializer.errors
        
        context['data'] = data
        
    return render(request, 'performance/predict.html', context)
