from django import forms
#from datetime import datetime
from models import Person, Post

class PersonForm(forms.ModelForm):
   class Meta:
      model = Person

class PostForm(forms.ModelForm):
   class Meta:
      model = Post