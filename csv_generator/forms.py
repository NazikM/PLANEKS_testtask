from django import forms
from .models import Schema


class SchemaForm(forms.ModelForm):
    SEPARATOR_CHOICES = (
        (',', 'Comma (,)'),
        (';', 'Semicolon (;)'),
        ('|', 'Pipe (|)'),
    )
    STRING_CHARACTER_CHOICES = (
        ('"', 'Double quote (")'),
        ("'", "Single quote (')"),
    )
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    separator = forms.ChoiceField(choices=SEPARATOR_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    string_character = forms.ChoiceField(choices=STRING_CHARACTER_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = Schema
        fields = ('name', 'separator', 'string_character', 'columns')
        widgets = {
            'columns': forms.Textarea(attrs={'rows': 4}),
        }
