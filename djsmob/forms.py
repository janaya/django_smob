from django import forms
from django.forms.models import inlineformset_factory
#from datetime import datetime
from models import Person, Post, Location

MAX_LOCATION = 1

#LocationFormSet = inlineformset_factory(Post, 
#    Location, 
#    can_delete=True,
#    extra=MAX_LOCATION)

class PersonForm(forms.ModelForm):
   class Meta:
      model = Person

class PostForm(forms.ModelForm):
   class Meta:
      model = Post

#KnowsFormSet = inlineformset_factory(Person, Knows, fk_name="from_person")
