from django import forms
from django.forms import BooleanField

from mailings.models import Client, Message, Mailings


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class ClientForm(StyleFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Client
        fields = ('email', 'full_name', 'comment',)


class MessageForm(StyleFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Message
        fields = ('title', 'body',)


class MailingsForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Mailings
        fields = '__all__'
        widgets = {
            'date_first_dispatch': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }
