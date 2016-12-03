from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from .models import Order, Discount


class CreateOrder(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'


class DiscountForm(forms.Form):
    code = forms.CharField(required=False, max_length=16,
                               widget=forms.TextInput(attrs={'class': 'input',
                                                             'placeholder': 'Apply Discount'})
                               )

    def clean(self):
        cleaned_data = super(DiscountForm, self).clean()
        discount_code = cleaned_data['code']
        try:
            discount = Discount.objects.get(code=discount_code)
            cleaned_data['discount'] = discount.discount
        except ObjectDoesNotExist:
            raise ValidationError(_('No matched code'))
        return cleaned_data
