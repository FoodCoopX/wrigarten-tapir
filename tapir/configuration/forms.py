from importlib.resources import _

from django import forms

from tapir.configuration.models import TapirParameter, TapirParameterDatatype
from tapir.configuration.parameter import (
    get_parameter_meta,
)


def create_field(param: TapirParameter):
    description = f"""<small><i>{param.key}</i></small><br/>{_(param.description)}"""

    param_meta = get_parameter_meta(param.key)
    if param_meta is None:
        return None

    param_value = param.get_value()

    if param_meta.options is not None:
        return forms.ChoiceField(
            label=_(param.label),
            help_text=description,
            choices=param_meta.options,
            required=True,
            initial=param_value,
            validators=param_meta.validators,
        )
    elif param.datatype == TapirParameterDatatype.STRING.value:
        return forms.CharField(
            label=_(param.label),
            help_text=description,
            required=True,
            initial=param_value,
            validators=param_meta.validators,
        )
    elif param.datatype == TapirParameterDatatype.INTEGER.value:
        return forms.IntegerField(
            label=_(param.label),
            help_text=description,
            required=True,
            initial=param_value,
            validators=param_meta.validators,
        )
    elif param.datatype == TapirParameterDatatype.DECIMAL.value:
        return forms.DecimalField(
            label=_(param.label),
            help_text=description,
            required=True,
            initial=param_value,
            validators=param_meta.validators,
        )
    elif param.datatype == TapirParameterDatatype.BOOLEAN.value:
        return forms.BooleanField(
            label=_(param.label),
            help_text=description,
            required=False,
            initial=param_value,
            validators=param_meta.validators,
        )
    else:
        raise NotImplementedError(
            """Unknown ParameterDatatype for parameter {param.key}: {param.datatype}""".format(
                param=param
            )
        )


class ParameterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ParameterForm, self).__init__(*args, **kwargs)

        params = TapirParameter.objects.order_by("category", "-order_priority", "key")

        categories = list(set(map(lambda p: p.category, params)))
        categories.sort()

        self.categories = categories

        for param in params:
            field = create_field(param)
            if field is not None:
                self.fields[param.key] = field

        def get_category(name):
            for p in params:
                if p.key == name:
                    return p.category

        for visible in self.visible_fields():
            visible.category = get_category(visible.name)
