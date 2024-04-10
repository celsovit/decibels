from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import SignupCode
from .forms import SignupCodeForm, SignupCodeUpdateForm


@method_decorator(login_required, name='dispatch')
class SignupCodeListView(ListView):
    model = SignupCode
    template_name = 'signupcode_list.html'
    paginate_by = 3


@method_decorator(login_required, name='dispatch')
class SignupCodeCreateView(CreateView):
    model = SignupCode
    form_class = SignupCodeForm
    template_name = 'signupcode_edit.html'
    success_url = reverse_lazy('signupcode_list')

    def form_valid(self, form):
        form.instance.organization = self.request.user.organization
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class SignupCodeUpdateView(UpdateView):
    model = SignupCode
    form_class = SignupCodeUpdateForm
    template_name = 'signupcode_edit.html'
    success_url = reverse_lazy('signupcode_list')


@method_decorator(login_required, name='dispatch')
class SignupCodeDeleteView(DeleteView):
    model = SignupCode
    template_name = 'signupcode_delete.html'
    success_url = reverse_lazy('signupcode_list')

