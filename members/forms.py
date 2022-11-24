from django import forms
from members.models import CustomUser


class CustomUserRegisterForm(forms.ModelForm):
    email = forms.EmailField(max_length=128)
    password = forms.PasswordInput()

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'age', 'email', 'password')

    def save(self, commit=True):
        user = super().save(commit)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user
