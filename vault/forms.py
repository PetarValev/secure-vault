from django import forms
from vault.models import PasswordEntry, Category


class PasswordEntryForm(forms.ModelForm):
    class Meta:
        model = PasswordEntry
        fields = ['title', 'username', 'email', 'password', 'website', 'category', 'notes']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Gmail, Facebook, Work Email'
            }),
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter password'
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Additional notes (optional)'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()
        self.fields['category'].empty_label = "Select category (optional)"

        self.fields['username'].required = False
        self.fields['email'].required = False
        self.fields['website'].required = False
        self.fields['category'].required = False
        self.fields['notes'].required = False

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')

        if not username and not email:
            raise forms.ValidationError("Please provide either a username or email address.")

        return cleaned_data