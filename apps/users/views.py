from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CustomUserCreationForm
from signupcode.models import SignupCode


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

    def form_valid(self, form):
        code = self.request.POST.get('code')
        email = form.cleaned_data['email']

        try:
            signup_code = SignupCode.objects.get(email=email, authorization_code=code)
            form.instance.organization = signup_code.organization
            form.instance.save()
            SignupCode.objects.filter(email=email).delete()
            return super().form_valid(form)
        
        except SignupCode.DoesNotExist:
            form.add_error(None, 'E-mail e/ou código de registro inválido.')
            return self.form_invalid(form)
        
        except Exception as e:
            print(f'Erro ao salvar o usuário: {e}')
            form.add_error(None, 'Erro ao salvar o usuário. Por favor, tente novamente mais tarde.')
            return self.form_invalid(form)