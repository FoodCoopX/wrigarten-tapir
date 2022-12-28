from django.urls import path

from tapir.wirgarten.views import (
    RegistrationWizardView,
    RegistrationWizardConfirmView,
    exported_files,
)
from tapir.wirgarten.views.admin_dashboard import AdminDashboardView
from tapir.wirgarten.views.member import (
    MemberListView,
    MemberDetailView,
    MemberPaymentsView,
    MemberDeliveriesView,
    get_payment_amount_edit_form,
    get_coop_share_transfer_form,
    get_member_personal_data_create_form,
    get_harvest_shares_waiting_list_form,
    WaitingListView,
    export_waitinglist,
    get_add_harvest_shares_form,
    get_member_personal_data_edit_form,
    get_member_payment_data_edit_form,
    get_coop_shares_waiting_list_form,
    get_pickup_location_choice_form,
    get_add_chicken_shares_form,
    get_add_bestellcoop_form,
    get_add_coop_shares_form,
    cancel_contract_at_period_end,
    renew_contract_same_conditions,
    SubscriptionListView,
)
from tapir.wirgarten.views.payments import PaymentTransactionListView
from tapir.wirgarten.views.pickup_location_config import (
    PickupLocationCfgView,
    get_pickup_location_add_form,
    get_pickup_location_edit_form,
    delete_pickup_location,
)
from tapir.wirgarten.views.product_cfg import (
    ProductCfgView,
    delete_period,
    get_period_copy_form,
    get_period_add_form,
    delete_product_handler,
    get_product_edit_form,
    get_product_add_form,
    get_product_type_capacity_edit_form,
    get_product_type_capacity_add_form,
    delete_product_type,
)

urlpatterns = [
    path(
        "product",
        ProductCfgView.as_view(),
        name="product",
    ),
    path(
        "product/<str:periodId>/<str:capacityId>/typeedit",
        get_product_type_capacity_edit_form,
        name="product_type_edit",
    ),
    path(
        "product/<str:periodId>/typeadd",
        get_product_type_capacity_add_form,
        name="product_type_add",
    ),
    path(
        "product/<str:periodId>/<str:capacityId>/typedelete",
        delete_product_type,
        name="product_type_delete",
    ),
    path(
        "product/<str:periodId>/<str:capacityId>/add",
        get_product_add_form,
        name="product_add",
    ),
    path(
        "product/<str:periodId>/<str:capacityId>/<str:prodId>/edit",
        get_product_edit_form,
        name="product_edit",
    ),
    path(
        "product/<str:periodId>/<str:capacityId>/<str:prodId>/delete",
        delete_product_handler,
        name="product_delete",
    ),
    path("product/periodadd", get_period_add_form, name="period_add"),
    path("product/<str:periodId>/periodcopy", get_period_copy_form, name="period_copy"),
    path("product/<str:periodId>/perioddelete", delete_period, name="period_delete"),
    path(
        "register",
        RegistrationWizardView.as_view(),
        name="draftuser_register",
    ),
    path(
        "register/confirm",
        RegistrationWizardConfirmView.as_view(),
        name="draftuser_confirm_registration",
    ),
    path(
        "admin/dashboard",
        AdminDashboardView.as_view(),
        name="admin_dashboard",
    ),
    path(
        "admin/exportedfiles",
        exported_files.ExportedFilesListView.as_view(),
        name="exported_files_list",
    ),
    path(
        "admin/exportedfiles/<str:pk>/download",
        exported_files.download,
        name="exported_files_download",
    ),
    path(
        "admin/pickuplocations",
        PickupLocationCfgView.as_view(),
        name="pickup_locations",
    ),
    path(
        "admin/pickuplocations/add",
        get_pickup_location_add_form,
        name="pickup_locations_add",
    ),
    path(
        "admin/pickuplocations/edit/<str:id>",
        get_pickup_location_edit_form,
        name="pickup_locations_edit",
    ),
    path(
        "admin/pickuplocations/delete/<str:id>",
        delete_pickup_location,
        name="pickup_locations_delete",
    ),
    path(
        "admin/waitinglist",
        WaitingListView.as_view(),
        name="waitinglist",
    ),
    path("admin/waitinglist/export", export_waitinglist, name="export_waitlist"),
    path(
        "register/waitlist/hs",
        get_harvest_shares_waiting_list_form,
        name="waitlist_harvestshares",
    ),
    path(
        "register/waitlist/cs",
        get_coop_shares_waiting_list_form,
        name="waitlist_coopshares",
    ),
    path("members", MemberListView.as_view(), name="member_list"),
    path("members/create", get_member_personal_data_create_form, name="member_create"),
    path(
        "members/<int:pk>/edit", get_member_personal_data_edit_form, name="member_edit"
    ),
    path(
        "members/<int:pk>/editpaymentdetails",
        get_member_payment_data_edit_form,
        name="member_edit_payment_details",
    ),
    path(
        "members/<int:pk>/editpickuplocation",
        get_pickup_location_choice_form,
        name="member_pickup_location_choice",
    ),
    path(
        "members/<int:pk>/cancelcontract",
        cancel_contract_at_period_end,
        name="member_cancel_contract",
    ),
    path(
        "members/<int:pk>/renewcontract",
        renew_contract_same_conditions,
        name="member_renew_same_conditions",
    ),
    path(
        "members/<int:pk>/addharvestshares",
        get_add_harvest_shares_form,
        name="member_add_harvest_shares",
    ),
    path(
        "members/<int:pk>/addchickenshares",
        get_add_chicken_shares_form,
        name="member_add_chicken_shares",
    ),
    path(
        "members/<int:pk>/addbestellcoop",
        get_add_bestellcoop_form,
        name="member_add_bestellcoop",
    ),
    path(
        "members/<int:pk>/addcoopshares",
        get_add_coop_shares_form,
        name="member_add_coop_shares",
    ),
    path("members/<int:pk>", MemberDetailView.as_view(), name="member_detail"),
    path(
        "members/<int:pk>/coopsharestransfer",
        get_coop_share_transfer_form,
        name="member_coopshare_transfer",
    ),
    path("contracts", SubscriptionListView.as_view(), name="subscription_list"),
    path("payments/<int:pk>", MemberPaymentsView.as_view(), name="member_payments"),
    path(
        "payments/<int:member_id>/edit/<str:mandate_ref_id>/<str:payment_due_date>",
        get_payment_amount_edit_form,
        name="member_payments_edit",
    ),
    path("sepa", PaymentTransactionListView.as_view(), name="payment_transactions"),
    path(
        "deliveries/<int:pk>", MemberDeliveriesView.as_view(), name="member_deliveries"
    ),
]
app_name = "wirgarten"
