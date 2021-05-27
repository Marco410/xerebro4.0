from .forms import UserCreationFormWithEmail,ProfileForm,EmailForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django import forms
from django.views.generic.edit import UpdateView
from .models import Profile

# Create your views here.

class SignUpView(CreateView):
    form_class = UserCreationFormWithEmail
    template_name = 'registration/signup.html'

    def get_success_url(self):
        return reverse_lazy('profiles:list') + '?register'

    def get_form(self, form_class=None):
        form = super(SignUpView, self).get_form()
        form.fields['username'].widget = forms.TextInput(attrs={'class':'validate borde','placeholder':'Usuario'})
        form.fields['email'].widget = forms.EmailInput(attrs={'class':'validate borde','placeholder':'Correo Electronico'})
        form.fields['password1'].widget = forms.PasswordInput(attrs={'class':'validate borde','placeholder':'Contraseña'})
        form.fields['password2'].widget= forms.PasswordInput(attrs={'class':'validate borde','placeholder':'Repite la Contraseña'})
        
        return form

class ProfileUpdate(UpdateView):
    form_class = ProfileForm
    success_url = reverse_lazy('perfil')
    template_name = 'registration/profile_form.html'

    def get_object(self):
        #recuperar objeto a editar
        profile, create =  Profile.objects.get_or_create(user=self.request.user)
        return profile

class EmailUpdate(UpdateView):
    form_class = EmailForm
    success_url = reverse_lazy('perfil')
    template_name = 'registration/profile_email_form.html'

    def get_object(self):
        #recuperar objeto a editar
        return self.request.user

    def get_form(self, form_class=None):
        form = super(EmailUpdate, self).get_form()
        form.fields['email'].widget = forms.EmailInput(attrs={'class':'validate borde','placeholder':'Nuevo Correo'})
        return form

