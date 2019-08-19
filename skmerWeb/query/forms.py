from django import forms
from django.forms import ModelForm
from .models import *



class queryFileCreateForm(ModelForm):

    class Meta:
        model = inputQueryFile
        fields = ('collectionName', 'fastQ')


class inputQueryForm(queryFileCreateForm):

    addToRef = forms.TypedChoiceField(coerce=lambda x: x == 'True',
                                      choices=((False, 'No'), (True, 'Yes')), label="Add to Reference ?")
    class Meta(queryFileCreateForm.Meta):
        fields = queryFileCreateForm.Meta.fields + ('addToRef',)
        labels = {
            "collectionName": "Collection Name",
            "fastQ": "Fast Q files batch upload",
        }
        widgets = {
            "fastQ": forms.ClearableFileInput(attrs={'multiple' : True})
        }

