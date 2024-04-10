from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Location


@method_decorator(login_required, name='dispatch')
class LocationListView(ListView):
    model = Location
    template_name = 'location_list.html'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        return Location.objects.filter(organization=user.organization).order_by('name')


@method_decorator(login_required, name='dispatch')
class LocationCreateView(CreateView):
    model = Location
    fields = ('name', 'threshold')
    template_name = 'location_edit.html'
    success_url = reverse_lazy('location_list')

    def form_valid(self, form):
        # Define a organização do usuário atual para a localização criada
        form.instance.organization = self.request.user.organization
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class LocationUpdateView(UpdateView):
    model = Location
    fields = ('name', 'threshold')
    template_name = 'location_edit.html'
    success_url = reverse_lazy('location_list')

    def get_queryset(self):
        user = self.request.user
        return Location.objects.filter(organization=user.organization)


@method_decorator(login_required, name='dispatch')
class LocationDeleteView(DeleteView):
    model = Location
    template_name = 'location_delete.html'
    success_url = reverse_lazy('location_list')

    def get_queryset(self):
        user = self.request.user
        return Location.objects.filter(organization=user.organization)