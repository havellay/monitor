from django import forms

from monitor.models.Symbol import Symbol
from monitor.attribute import Attribute

class UserForm(forms.Form):
  # TODO: sign up form for user
  pass

class SymbolForm(forms.Form):
  name        = forms.CharField()
  y_symbol    = forms.CharField(required=False)
  g_symbol    = forms.CharField(required=False)
  nse_symbol  = forms.CharField(required=False)
  # Javascript validation : atleast one of the
  # above picker symbols should be valid


class TriggerForm(forms.Form):
  # the reminder should be auto assigned;
  symbol_choices  = tuple([sym.name for sym in Symbol.objects.all()])
  symbol          = forms.ChoiceField(choices=[symbol_choices])
  attribute_choices = tuple([x for x in Attribute.directory.keys()])
  attribute         = forms.ChoiceField(choices=[attribute_choices])
  # form for attribute is attribute_forms.get(attribute)


class ReminderForm(forms.Form):
  # when inserting a new Reminder, only the user name would
  # be needed; once the reminder has been created, iterate
  # over the following formset and create the necessary number
  # of triggers with the associated Reminder.id

  # the following line creates a formset of 3 forms
  triggerFormSet  = forms.formsets.formset_factory(TriggerForm, extra=2)
