from rest_framework import serializers
from .models import StudentPerformance

class StudentPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentPerformance
        fields = ['hours_studied', 'previous_scores', 'extracurricular', 'sleep_hours', 'sample_papers']

    def validate_hours_studied(self, value):
        if value < 0 or value > 16:
            raise serializers.ValidationError("Hours studied must be between 0 and 16 hours per day. Any other value is considered an abnormality.")
        return value

    def validate_previous_scores(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError("Previous scores must be between 0 and 100. Values outside this range are not possible.")
        return value

    def validate_sleep_hours(self, value):
        if value < 4:
            raise serializers.ValidationError(f"Sleep hours of {value} is dangerously low and not possible for a functional student. Minimum should be 4 hours.")
        if value > 12:
            raise serializers.ValidationError("Sleep hours above 12 is considered abnormal for a regular student schedule.")
        return value

    def validate_sample_papers(self, value):
        if value < 0:
            raise serializers.ValidationError("Sample papers practiced cannot be negative.")
        if value > 20:
            raise serializers.ValidationError("Practicing more than 20 sample papers is highly unusual.")
        return value

    def validate(self, data):
        hours_studied = data.get('hours_studied', 0)
        sleep_hours = data.get('sleep_hours', 0)
        
        if hours_studied + sleep_hours > 24:
            raise serializers.ValidationError({
                "non_field_errors": ["TIME PARADOX: You cannot study and sleep for more than 24 hours. Reality is breaking!"]
            })
        return data
