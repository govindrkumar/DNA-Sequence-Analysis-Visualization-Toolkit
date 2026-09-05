from django import forms
from .models import SupportTicket

#I used it to create a form
class SupportTicketForm(forms.ModelForm):
    class Meta:
        model = SupportTicket
        fields = ['name', 'issue_type', 'issue_detail']

        #customizing widget
        widgets = {
            'name' : forms.TextInput(
                attrs = {
                    'placeholder' : 'Enter Your Name'
                }
            ),

            'issue_detail' : forms.Textarea(
                attrs = {
                    'placeholder' : 'Enter your issues....',
                    'rows' : 5,
                    'cols' : 40,
                }
            )
        }

from django import forms


class SequenceUploadForm(forms.Form):

    file = forms.FileField()

    def clean_file(self):
        uploaded_file = self.cleaned_data['file']

        max_size = 25 * 1024 * 1024  # 25 MB

        if uploaded_file.size > max_size:
            raise forms.ValidationError(
                "File is too large. Maximum allowed size is 25 MB."
            )

        return uploaded_file