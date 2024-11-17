from .models import SkiReview, ReviewImage, User
from django import forms


class SkiReviewForm(forms.ModelForm):
    resort = forms.IntegerField(widget=forms.HiddenInput)
    author = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput)

    class Meta:
        model = SkiReview
        fields = ['resort', 'author', 'text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form__text', 'autocomplete': 'off', 'placeholder': 'Напишите свой отзыв здесь', 'rows': "8", 'cols': "114", 'maxlength': "2000"})
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.fields['author'].initial = self.get_current_user()

    def get_current_user(self):
        if self.request.user.is_authenticated:
            return self.request.user
        return None


class ReviewImageForm(forms.ModelForm):
    photo = forms.FileField(label='Фото')

    class Meta:
        model = ReviewImage
        fields = ['photo']
