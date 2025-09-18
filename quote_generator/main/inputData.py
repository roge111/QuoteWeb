from django import forms


class InputQuote(forms.Form):
    quote_field = forms.CharField(
        label='Введите свою цитату:', 
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 50}), # Красивое большое поле
        max_length=10_000
    )

    source  = forms.CharField(
        label='Введите источник (книга, фильм и тд):',
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 50}),
        max_length=100
    )

    wieght  = forms.CharField(
        label='Введите вес цитаты',
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 50}),
        max_length=100
    )


class InputUser(forms.Form):
    login = forms.CharField(
        label = 'Введите свой логин:',
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 50}), # Красивое большое поле
        max_length=10_000
    )

    password = forms.CharField(
        label='Введите пароль:',
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 50}),
        max_length=1000
    )