from django import forms
from .models import ContactMessage, NewsletterSubscriber


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "subject", "message"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "framer-form-input",
                "placeholder": "Your Full Name",
                "required": True,
            }),
            "email": forms.EmailInput(attrs={
                "class": "framer-form-input",
                "placeholder": "Your Email Address",
                "required": True,
            }),
            "subject": forms.TextInput(attrs={
                "class": "framer-form-input",
                "placeholder": "Project Subject / Scope",
            }),
            "message": forms.Textarea(attrs={
                "class": "framer-form-textarea",
                "placeholder": "Tell me about your project, timeline, and budget...",
                "rows": 4,
                "required": True,
            }),
        }


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ["email"]
        widgets = {
            "email": forms.EmailInput(attrs={
                "class": "newsletter-input",
                "placeholder": "Enter your email address",
                "required": True,
            }),
        }
