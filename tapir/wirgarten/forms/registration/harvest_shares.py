from importlib.resources import _

from django import forms

from tapir.configuration.parameter import get_parameter_value
from tapir.wirgarten.models import HarvestShareProduct
from tapir.wirgarten.parameters import Parameter
from tapir.wirgarten.service.payment import get_solidarity_overplus
from tapir.wirgarten.service.products import (
    get_product_price,
    get_available_product_types,
    get_free_product_capacity,
)

SOLIDARITY_PRICES = [
    (0.0, _("Ich möchte keinen Solidarpreis zahlen")),
    (0.25, "+ 25% 🤩"),
    (0.2, "+ 20% 😍"),
    (0.15, "+ 15% 🚀"),
    (0.1, "+ 10% 🥳"),
    (0.05, "+ 5% 💚"),
    (-0.05, "- 5%"),
    (-0.10, "- 10%"),
    (-0.15, "- 15%"),
]


def get_solidarity_total() -> float:
    val = get_parameter_value(Parameter.HARVEST_NEGATIVE_SOLIPRICE_ENABLED)
    if val == 0:  # disabled
        return 0.0
    elif val == 1:  # enabled
        return 1000.0
    elif val == 2:  # automatic calculation
        return get_solidarity_overplus() or 0.0


def is_separate_coop_shares_allowed() -> bool:
    return get_parameter_value(Parameter.COOP_SHARES_INDEPENDENT_FROM_HARVEST_SHARES)


def is_minimum_harvest_shares_reached(data, products) -> bool:
    for chk_key in products.keys():
        if data[chk_key] > 0:
            return True

    return False


HARVEST_SHARE_FIELD_PREFIX = "harvest_shares_"


class HarvestShareForm(forms.Form):
    intro_text_skip_hr = True

    intro_template = "wirgarten/registration/steps/harvest_shares.intro.html"
    outro_template = "wirgarten/registration/steps/harvest_shares.outro.html"

    def __init__(self, *args, **kwargs):
        super(HarvestShareForm, self).__init__(*args, **kwargs)

        harvest_share_products = list(
            HarvestShareProduct.objects.filter(
                deleted=False, type_id__in=get_available_product_types()
            )
        )
        prices = {
            prod.id: get_product_price(prod).price for prod in harvest_share_products
        }

        harvest_share_products = sorted(
            harvest_share_products, key=lambda x: prices[x.id]
        )

        self.products = {
            """harvest_shares_{variation}""".format(
                variation=p.product_ptr.name.lower()
            ): p
            for p in harvest_share_products
        }

        self.field_order = list(self.products.keys()) + ["solidarity_price"]
        self.n_columns = len(self.products)
        self.colspans = {"solidarity_price": self.n_columns}

        self.solidarity_total = get_solidarity_total()

        self.free_capacity = get_free_product_capacity(
            harvest_share_products[0].type.id
        )

        for prod in harvest_share_products:
            self.fields[
                f"{HARVEST_SHARE_FIELD_PREFIX}{prod.name.lower()}"
            ] = forms.IntegerField(
                required=True,
                max_value=10,
                min_value=0,
                initial=0,
                label=_(f"{prod.name}-Ernteanteile"),
                help_text="""{:.2f} € / Monat""".format(prices[prod.id]),
            )

        self.fields["solidarity_price"] = forms.ChoiceField(
            required=True,
            label=_("Solidarpreis"),
            choices=SOLIDARITY_PRICES,
        )

        self.harvest_shares = ",".join(
            map(
                lambda p: HARVEST_SHARE_FIELD_PREFIX
                + p.name.lower()
                + ":"
                + str(prices[p.id]),
                harvest_share_products,
            )
        )

    def clean(self):
        cleaned_data = super().clean()
        if not is_separate_coop_shares_allowed():
            if not is_minimum_harvest_shares_reached(cleaned_data, self.products):
                is_first: bool = True
                for product_name in self.products.keys():
                    if is_first:
                        self.add_error(
                            product_name,
                            _(
                                "Die Zeichnung von mindestens einem der Ernteprodukte ist erforderlich."
                            ),
                        )
                        is_first = False
                    else:
                        self.add_error(
                            product_name,
                            _(""),
                        )
