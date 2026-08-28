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

class SequenceUploadForm(forms.Form):
    file = forms.FileField()