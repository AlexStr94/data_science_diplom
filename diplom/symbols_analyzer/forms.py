from django import forms
from django.core.files.base import ContentFile
from django.core.validators import FileExtensionValidator

from .models import Journal


class CreateJournalForm(forms.ModelForm):
    class Meta:
        model = Journal
        fields = ('students', 'lessons')


class UploadImage(forms.Form):
    CHOICES = (
        ('rotationNone', 'rotationNone'),
        ('rotationMinus90', 'rotationMinus90'),
        ('rotationPlus90', 'rotationPlus90'),
        ('rotation180', 'rotation180'),
    )
    file = forms.ImageField()
    rotation = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)


class UploadJournalForm(UploadImage):
    pass


class UploadBlankImageForm(UploadImage):
    pass


class SymbolAnalyzerForm(forms.Form):
    CHOICES = (
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('n', 'н'),
        ('empty', 'Пустая клетка'),
        ('error', 'Ошибка/нечитаемая клетка')
    )
    symbol = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    image_pk = forms.CharField(widget=forms.HiddenInput)
