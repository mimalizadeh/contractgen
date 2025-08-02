from django import forms
from .models import Contract

class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = [
            'employer',
            'presenter',
            'start_date',
            'total_amount',
            'long_term',
            'monthly_salary'
        ]