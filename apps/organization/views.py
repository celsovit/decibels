from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden

from .models import Organization


@method_decorator(login_required, name='dispatch')
class OrganizationListView(UserPassesTestMixin, ListView):
    model = Organization
    template_name = 'organization_list.html'
    paginate_by = 10

    def get_queryset(self):
        return Organization.objects.order_by('name')

    def test_func(self):
        return is_super_user(self.request.user)

    def handle_no_permission(self):
        return HttpResponseForbidden("Página com acesso não autorizado.")


@method_decorator(login_required, name='dispatch')
class OrganizationCreateView(UserPassesTestMixin, CreateView):
    model = Organization
    fields = ('name', 'image_file', )
    template_name = 'organization_edit.html'
    success_url = reverse_lazy('organization_list')

    def test_func(self):
        return is_super_user(self.request.user)

    def handle_no_permission(self):
        return HttpResponseForbidden("Página com acesso não autorizado.")


@method_decorator(login_required, name='dispatch')
class OrganizationUpdateView(UserPassesTestMixin, UpdateView):
    model = Organization
    fields = ('name', 'image_file', )
    template_name = 'organization_edit.html'
    success_url = reverse_lazy('organization_list')

    def test_func(self):
        return is_super_user(self.request.user)

    def handle_no_permission(self):
        return HttpResponseForbidden("Página com acesso não autorizado.")


@method_decorator(login_required, name='dispatch')
class OrganizationDeleteView(UserPassesTestMixin, DeleteView):
    model = Organization
    template_name = 'organization_delete.html'
    success_url = reverse_lazy('organization_list')

    def test_func(self):
        return is_super_user(self.request.user)

    def handle_no_permission(self):
        return HttpResponseForbidden("Página com acesso não autorizado.")


def is_super_user(user):
    return user.is_authenticated and user.is_superuser