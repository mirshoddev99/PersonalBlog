from django import forms
from members.models import CustomUser


class CustomUserRegisterForm(forms.ModelForm):
    email = forms.EmailField(max_length=128)
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())


    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email')


    def save(self, commit=True):
        user = super().save(commit)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user

    
    def clean_password2(self):
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password and password2 and password2 != password:
            raise forms.ValidationError("Password does not match")
        return password2
    
    
