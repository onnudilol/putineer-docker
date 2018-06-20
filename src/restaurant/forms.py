from django.forms import ModelForm
from restaurant.models import VerificationRequest


class VerificationForm(ModelForm):

    class Meta:
        model = VerificationRequest
        fields = ['text']
