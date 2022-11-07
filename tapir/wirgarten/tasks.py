import itertools
from copy import copy
from datetime import datetime

from celery import shared_task
from django.db import transaction
from django.db.models import Sum

from tapir.configuration.parameter import get_parameter_value
from tapir.wirgarten.models import (
    ExportedFile,
    Payment,
    Subscription,
    ProductType,
    PaymentTransaction,
)
from tapir.wirgarten.parameters import Parameter
from tapir.wirgarten.service.file_export import export_file, begin_csv_string
from tapir.wirgarten.service.payment import is_mandate_ref_for_coop_shares
from tapir.wirgarten.service.products import get_total_price_for_sub_or_share_ownership


@shared_task
def export_pick_list_csv():
    """
    Sums the quantity of product variants per pickup location and exports the list as CSV.
    """

    KEY_PRODUCT = "Produkt"
    KEY_QUANTITY = "Anzahl"
    KEY_VARIANT = "Variante"
    KEY_PICKUPLOCATION = "Abholort"
    KEY_STREET = "Straße"
    KEY_CITY = "Ort"

    sums = (
        Subscription.objects.filter(product__type__pickup_enabled=True)
        .values(
            "member__pickup_location__name",
            "member__pickup_location__street",
            "member__pickup_location__postcode",
            "member__pickup_location__city",
            "product__type__name",
            "product__name",
        )
        .annotate(quantity_sum=Sum("quantity"))
        .order_by(
            "member__pickup_location__name", "product__type__name", "product__name"
        )
    )

    output, writer = begin_csv_string(
        [
            KEY_PICKUPLOCATION,
            KEY_STREET,
            KEY_CITY,
            KEY_PRODUCT,
            KEY_VARIANT,
            KEY_QUANTITY,
        ]
    )
    for row in sums:
        writer.writerow(
            {
                KEY_PICKUPLOCATION: row["member__pickup_location__name"],
                KEY_STREET: row["member__pickup_location__street"],
                KEY_CITY: f"""{row["member__pickup_location__postcode"]} {row["member__pickup_location__city"]}""",
                KEY_PRODUCT: row["product__type__name"],
                KEY_VARIANT: row["product__name"],
                KEY_QUANTITY: row["quantity_sum"],
            }
        )

    export_file(
        filename="Kommissionierliste",
        filetype=ExportedFile.FileType.CSV,
        content=bytes("".join(output.csv_string), "utf-8"),
        send_email=get_parameter_value(Parameter.PICK_LIST_SEND_ADMIN_EMAIL),
    )


@shared_task
def export_supplier_list_csv():
    """
    Sums the quantity of product variants exports a list as CSV per product type.
    """

    KEY_PRODUCT = "Produkt"
    KEY_QUANTITY = "Anzahl"

    def create_csv_string(product_type: str):
        product_type = all_product_types[product_type]

        if product_type is None:
            print(
                f"""export_supplier_list_csv(): Ignoring unknown product type value in parameter '{Parameter.SUPPLIER_LIST_PRODUCT_TYPES}': {product_type}. Possible values: {all_product_types.keys}"""
            )
            return None

        now = datetime.now()
        sums = (
            Subscription.objects.filter(
                start_date__lte=now, end_date__gte=now, product__type=product_type
            )
            .order_by("product__name")
            .values("product__name")
            .annotate(quantity_sum=Sum("quantity"))
        )

        output, writer = begin_csv_string([KEY_PRODUCT, KEY_QUANTITY])

        for variant in sums:
            writer.writerow(
                {
                    KEY_PRODUCT: variant["product__name"],
                    KEY_QUANTITY: variant["quantity_sum"],
                }
            )

        return "".join(output.csv_string)

    all_product_types = {pt.name: pt for pt in ProductType.objects.all()}
    include_product_types = get_parameter_value(
        Parameter.SUPPLIER_LIST_PRODUCT_TYPES
    ).split(",")
    for _type_name in include_product_types:
        type_name = _type_name.strip()
        data = create_csv_string(type_name)

        if data is not None:
            export_file(
                filename=f"Lieferant_{type_name}",
                filetype=ExportedFile.FileType.CSV,
                content=bytes(data, "utf-8"),
                send_email=get_parameter_value(
                    Parameter.SUPPLIER_LIST_SEND_ADMIN_EMAIL
                ),
            )


def windata_date_format(due_date):
    return due_date.strftime("%d.%m.%Y")


@shared_task
@transaction.atomic
def export_sepa_payments():
    """
    Creates payments for now. This should usually only run once a month.
    """
    KEY_SEPA_ZAHLPFL_NAME = "Beg/Zahlpfl Name"
    KEY_SEPA_ZAHLPFL_STREET = "Beg/Zahlpfl Strasse"
    KEY_SEPA_ZAHLPFL_CITY = "Beg/Zahlpfl Ort"
    KEY_SEPA_ZAHLPFL_IBAN = "Beg/Zahlpfl KontoNr bzw. IBAN"
    KEY_SEPA_ZAHLPFL_BIC = "Beg/Zahlpfl BLZ bzw. BIC"
    KEY_SEPA_AG_NAME = "AG Name"
    KEY_SEPA_AG_IBAN = "AG KontoNr bzw. AG IBAN"
    KEY_SEPA_AG_BIC = "AG BLZ bzw. AG BIC"
    KEY_SEPA_AMOUNT = "Betrag"
    KEY_SEPA_DUE_DATE = "Termin"
    KEY_SEPA_VWZ1 = "VWZ1"
    KEY_SEPA_VWZ2 = "VWZ2"
    KEY_SEPA_MANDATE_REF = "Mandat-ID"
    KEY_SEPA_MANDATE_DATE = "Mandat-Datum"
    KEY_SEPA_CURRENCY = "Währung"
    KEY_SEPA_AG_GLA_ID = "AG Gläubiger-ID"
    KEY_SEPA_SEQUENCE = "Sequenz"
    KEY_SEPA_ZAHLWEISE = "zahlweise"
    KEY_SEPA_ZAHLART = "Textschlüssel bzw. Zahlart"

    def generate_current_payments(due_date):
        payments = []

        for mandate_ref, subs in itertools.groupby(
            iterable=Subscription.objects.filter(
                start_date__lte=due_date, end_date__gte=due_date
            ).order_by("mandate_ref"),
            key=lambda x: x.mandate_ref,
        ):
            if not Payment.objects.filter(
                mandate_ref=mandate_ref, due_date=due_date
            ).exists():
                amount = round(
                    sum(
                        map(
                            lambda x: get_total_price_for_sub_or_share_ownership(x),
                            subs,
                        )
                    ),
                    2,
                )

                payments.append(
                    Payment(
                        due_date=due_date,
                        amount=amount,
                        mandate_ref=mandate_ref,
                        status=Payment.PaymentStatus.DUE,
                    )
                )

        return payments

    due_date = datetime.today().replace(
        day=get_parameter_value(Parameter.PAYMENT_DUE_DAY)
    )

    existing_payments = list(
        Payment.objects.filter(transaction__isnull=True, due_date__lte=due_date)
    )
    payments = Payment.objects.bulk_create(generate_current_payments(due_date))

    payments.extend(existing_payments)

    site_name = get_parameter_value(Parameter.SITE_NAME)
    static_values = {
        KEY_SEPA_AG_NAME: site_name,
        KEY_SEPA_AG_IBAN: get_parameter_value(Parameter.PAYMENT_IBAN),
        KEY_SEPA_AG_BIC: get_parameter_value(Parameter.PAYMENT_BIC),
        KEY_SEPA_AG_GLA_ID: get_parameter_value(Parameter.PAYMENT_CREDITOR_ID),
        KEY_SEPA_CURRENCY: "EUR",
        KEY_SEPA_SEQUENCE: "RCUR",
        KEY_SEPA_ZAHLWEISE: "M",
        KEY_SEPA_ZAHLART: "SEPA",
    }

    # write header
    output, writer = begin_csv_string(
        [
            KEY_SEPA_ZAHLPFL_NAME,
            KEY_SEPA_ZAHLPFL_STREET,
            KEY_SEPA_ZAHLPFL_CITY,
            KEY_SEPA_ZAHLPFL_IBAN,
            KEY_SEPA_ZAHLPFL_BIC,
            KEY_SEPA_AMOUNT,
            KEY_SEPA_DUE_DATE,
            KEY_SEPA_VWZ1,
            KEY_SEPA_VWZ2,
            KEY_SEPA_MANDATE_REF,
            KEY_SEPA_MANDATE_DATE,
        ]
        + list(static_values.keys())
    )

    # write row
    for payment in payments:
        row = static_values.copy()

        row[
            KEY_SEPA_ZAHLPFL_NAME
        ] = f"{payment.mandate_ref.member.first_name} {payment.mandate_ref.member.last_name}"
        row[
            KEY_SEPA_ZAHLPFL_STREET
        ] = f"{payment.mandate_ref.member.street} {payment.mandate_ref.member.street_2}".strip()
        row[
            KEY_SEPA_ZAHLPFL_CITY
        ] = f"{payment.mandate_ref.member.postcode} {payment.mandate_ref.member.city}"
        row[KEY_SEPA_ZAHLPFL_IBAN] = payment.mandate_ref.member.iban
        row[KEY_SEPA_ZAHLPFL_BIC] = payment.mandate_ref.member.bic
        row[KEY_SEPA_AMOUNT] = payment.amount
        row[KEY_SEPA_DUE_DATE] = windata_date_format(due_date)
        row[KEY_SEPA_VWZ1] = (
            "Genossenschaftsanteile"
            if is_mandate_ref_for_coop_shares(payment.mandate_ref)
            else "Produktanteile"
        )
        row[KEY_SEPA_VWZ2] = payment.mandate_ref.ref
        row[KEY_SEPA_MANDATE_REF] = payment.mandate_ref.ref
        row[KEY_SEPA_MANDATE_DATE] = windata_date_format(
            payment.mandate_ref.member.sepa_consent
        )

        writer.writerow(row)

    # write file to db
    file = export_file(
        filename="SEPA-Payments",
        filetype=ExportedFile.FileType.CSV,
        content=bytes("windata CSV 1.1\n" + "".join(output.csv_string), "utf-8"),
        send_email=True,
    )

    transaction = PaymentTransaction.objects.create(file=file)
    for p in payments:
        p.transaction = transaction
        p.save()
