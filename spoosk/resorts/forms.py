from django.forms import ModelForm
from .models import SkiReview
from django import forms


class ReviewForm(forms.ModelForm):

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['riding_level'].empty_label = "Категория не выбрана"

    class Meta:
        model = SkiReview
        # fields = ['author', 'text']
        fields = ['text']
        widgets = {
            # 'author': forms.TextInput(attrs={'class': 'form__input', 'placeholder': 'Введите ваше имя'}),
            'text': forms.Textarea(attrs={'class': 'form__text',  'placeholder': 'Введите свой отзыв здесь', 'rows': "10", 'cols': "90"}),
            # 'riding_level': forms.Select(attrs={'class': 'form__text'}),
        }
