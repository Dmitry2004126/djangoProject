from crispy_forms.helper import FormHelper
from django import forms
from django.core.exceptions import ValidationError
from bootstrap_datepicker_plus.widgets import DatePickerInput
from Footballer.models import Project, Side

'''
class GameForm(forms.ModelForm):


    class Meta:
        model = Game
        fields = ('number', 'goals')
'''

class GameForm(forms.Form):
    number = forms.IntegerField(help_text="Input number", min_value=1, max_value=12)

    project_name = forms.CharField(help_text="Input the name of the project", max_length=200, min_length=0)
    date_start = forms.DateField(help_text="Input date", widget=DatePickerInput())
    def clean_goals(self):
        goals = self.cleaned_data['goals']

        if goals > 16:
            raise ValidationError("Are you sure? It is a world record!")

        return goals


class UserForm(forms.Form):
    side = forms.ModelMultipleChoiceField(queryset=Side.objects.all())

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

