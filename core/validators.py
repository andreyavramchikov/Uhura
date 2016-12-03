from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

SIZE_OF_DISCOUNT_PROMO_CODE = 16


def validate_size(value):
    if len(value) != SIZE_OF_DISCOUNT_PROMO_CODE:
        raise ValidationError(
            _('%(value)s is not 16 number digits'),
            params={'value': value},
        )
