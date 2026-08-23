from django import forms

#I used it to create a form
class paste_data(forms.Form):
    paste = forms.CharField(
        label = "Paste your DNA sequence",
        widget = forms.Textarea)
