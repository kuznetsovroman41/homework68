from django import forms



class SearchForm(forms.Form):
    search = forms.CharField(label='Найти', max_length=100, required=False)