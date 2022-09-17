from django.contrib.auth.forms import AuthenticationForm
from django.forms import widgets
from django import forms

from DdosTool.models import Commands, Devices


class LoginUserForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget = widgets.TextInput(
            attrs={"class": "form-control form-control-lg", "placeholder": "Kullanıcı Adı"})
        self.fields["password"].widget = widgets.PasswordInput(
            attrs={"class": "form-control form-control-lg", "placeholder": "Şifre"})


class CommandForm(forms.ModelForm):
    class Meta:
        model = Commands
        fields = "__all__"
        labels = {
            'title': 'Komut Başlığı',
            'commandText': 'Komut Metni',
            'bandwidth': 'Bir cihaz için bant genişliği (mb)'
        }
        widgets = {
            'title': widgets.TextInput(attrs={"class": "form-control form-control mt-2"}),
            'commandText': widgets.Textarea(attrs={"class": "form-control form-control mt-2"}),
            'bandwidth': widgets.NumberInput(
                attrs={"class": "form-control mt-2", 'step': '0.1', 'min': '0.0', 'value': '0,0'})
        }


class DeviceForm(forms.ModelForm):
    class Meta:
        model = Devices
        fields = "__all__"
        labels = {
            'ip': 'ip',
            'username': 'Kullanıcı Adı',
            'password': 'Şifre'
        }
        widgets = {
            'ip': widgets.TextInput(attrs={"class": "form-control form-control mt-2"}),
            'username': widgets.TextInput(attrs={"class": "form-control form-control mt-2"}),
            'password': widgets.TextInput(attrs={"class": "form-control form-control mt-2"})
        }


"""class CommandForm(forms.Form):
    title = forms.CharField(label="Komut Başlığı")
    commandText = forms.CharField(label="Komut Metni", widget=forms.Textarea)
    bandwidth = forms.DecimalField(label="Bir cihaz için bant genişliği", min_value=0.0, initial=0.0)

    # widgets
    title.widget = widgets.TextInput(attrs={"class": "form-control form-control mt-2"})
    commandText.widget = widgets.Textarea(
        attrs={"class": "form-control form-control mt-2"})
    bandwidth.widget = widgets.NumberInput(attrs={"class": "form-control mt-2", 'step': '0.1', 'min': '0'})"""

"""class DeviceForm(forms.Form):
    ip = forms.CharField(label='IP Adresi', max_length=15)
    username = forms.CharField(label='Kullanıcı Adı', max_length=50)
    password = forms.CharField(label='Şifre')

    # widgets
    ip.widget = widgets.TextInput(attrs={"class": "form-control form-control mt-2"})
    username.widget = widgets.TextInput(
        attrs={"class": "form-control form-control mt-2"})
    password.widget = forms.PasswordInput(attrs={"class": "form-control form-control mt-2"})"""
