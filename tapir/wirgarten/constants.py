from django.utils.translation import gettext_lazy as _


DeliveryCycle = [
    NO_DELIVERY := ("no_delivery", _("Keine Lieferung/Abholung")),
    WEEKLY := ("weekly", _("1x pro Woche")),
    ODD_WEEKS := ("odd_weeks", _("2x pro Monat (1. und 3. Woche)")),
    EVEN_WEEKS := ("even_weeks", _("2x pro Monat (2. und 4. Woche)")),
    MONTHLY := ("monthly", _("1x pro Monat")),
]
