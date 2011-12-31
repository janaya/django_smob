from django import forms
from django.forms.models import inlineformset_factory
#from datetime import datetime
from models import *

import logging

MAX_LOCATION = 1
MAX_INTEREST = 1

#LocationFormSet = inlineformset_factory(Post, 
#    Location, 
#    can_delete=True,
#    extra=MAX_LOCATION)

# http://stackoverflow.com/questions/2581049/filter-queryset-in-django-inlineformset-factory
class InterestForm(forms.ModelForm):
    person = forms.ModelChoiceField(queryset=Person.objects.all())
    class Meta:
        model = Interest
    #def __init__(self, *args, **kwargs):
    #    person = kwards.pop('person')
    #    super(InterestForm, self).__init__(*args, **kwargs)
    #    logging.debug("InterestForm.__init__() fields[person]")
    #    self.fields["person"].queryset = Person.objects.get()
        

InterestFormSet = inlineformset_factory(Person, 
    Interest, 
    can_delete=True,
    extra=MAX_INTEREST,
    form=InterestForm)

class PersonForm(forms.ModelForm):
   class Meta:
      model = Person

class PostForm(forms.ModelForm):
   class Meta:
      model = Post
      #widgets = {
      #    'location_uri': forms.HiddenInput(),
      #}
#KnowsFormSet = inlineformset_factory(Person, Knows, fk_name="from_person")

class ConfigurationForm(forms.ModelForm):
   class Meta:
      model = Configuration
