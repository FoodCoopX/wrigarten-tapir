from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import transaction
from django.urls import reverse_lazy
from django.views import generic

from tapir.configuration.forms import ParameterForm
from tapir.configuration.models import Parameter


class ParameterView(PermissionRequiredMixin, generic.FormView):
    template_name = "configuration/parameter_view.html"
    permission_required = "coop.admin"
    form_class = ParameterForm
    success_url = reverse_lazy("configuration:parameters")

    @transaction.atomic
    def form_valid(self, form):
        response = super().form_valid(form)

        for field in form.visible_fields():
            Parameter.objects.filter(pk=field.name).update(
                value=str(form.data[field.name])
            )

        return response