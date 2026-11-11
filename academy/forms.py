from django import forms


class CodeSubmissionForm(forms.Form):
    submission = forms.CharField(
        label="Your code",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 14,
                "placeholder": "Write your solution here...",
            }
        ),
    )


class SupportChoiceForm(forms.Form):
    diagnosis = forms.ChoiceField(
        label="Choose the best next step",
        widget=forms.RadioSelect,
    )
