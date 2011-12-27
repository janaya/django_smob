from django import forms
from django.forms.models import inlineformset_factory
#from datetime import datetime
from models import Person, Post, Location, Interest, Configuration

MAX_LOCATION = 1
MAX_INTEREST = 1

#LocationFormSet = inlineformset_factory(Post, 
#    Location, 
#    can_delete=True,
#    extra=MAX_LOCATION)

InterestFormSet = inlineformset_factory(Person, 
    Interest, 
    can_delete=True,
    extra=MAX_INTEREST)

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
