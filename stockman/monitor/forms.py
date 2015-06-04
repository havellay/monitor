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
  symbol_choices  = [(sym.name,sym.name) for sym in Symbol.objects.all()]
  symbol          = forms.ChoiceField(choices=symbol_choices)

  attribute_choices = [(x,x) for x in Attribute.directory.keys()]
  default_attribute = '---'
  attribute_choices.insert(0, (default_attribute, default_attribute))
  # changing the names of attribute1 and attribute2 variables
  # below will need changing the javascript in insert_trigger.html
  attribute1        = forms.ChoiceField(
      choices=attribute_choices,
      initial=default_attribute,
    )
  attribute1_hidden = forms.CharField(required=False,widget=forms.HiddenInput())
  attribute2        = forms.ChoiceField(
      choices=attribute_choices,
      initial=default_attribute,
    )
  attribute2_hidden = forms.CharField(required=False,widget=forms.HiddenInput())
  # for attribute1 and attribute2, make sure that the default
  # choice is '---' or something; when the user selects a valid
  # option, the form for the appropriate attribute is fetched;
  # form for attribute is attribute_forms.get(attribute)


class ReminderForm(forms.Form):
  # when inserting a new Reminder, only the user name would
  # be needed; once the reminder has been created, iterate
  # over the following formset and create the necessary number
  # of triggers with the associated Reminder.id

  # the following line creates a formset of 3 forms
  triggerFormSet  = forms.formsets.formset_factory(TriggerForm, extra=2)
