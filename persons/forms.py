from django import forms
from django.core.exceptions import ValidationError
from main.models import Skill
import re


class ProfileEditForm(forms.Form):
    avatarInput = forms.ImageField(required=False)
    nameInput = forms.CharField(max_length=30)
    descriptionInput = forms.CharField(max_length=154, required=False, empty_value=None)
    # yearOfBornInput = forms.CharField(required=False, empty_value=None)
    # genderInput = forms.CharField(required=False, empty_value=None)
    skillsInput = forms.CharField(required=False, empty_value='')
    rezomeInput = forms.CharField(max_length=1000, required=False)
    githubInput = forms.CharField(required=False, empty_value=None)
    gitlabInput = forms.CharField(required=False, empty_value=None)
    stackoverflowInput = forms.CharField(required=False, empty_value=None)
    linkedinInput = forms.CharField(required=False, empty_value=None)
    devInput = forms.CharField(required=False, empty_value=None)
    facebookInput = forms.CharField(required=False, empty_value=None)
    instagramInput = forms.CharField(required=False, empty_value=None)
    twitterInput = forms.CharField(required=False, empty_value=None)
    virgoolInput = forms.CharField(required=False, empty_value=None)
    websiteInput = forms.URLField(required=False, empty_value=None)
    publicEmailInput = forms.EmailField(max_length=200, required=False, empty_value=None)
    mobileInput = forms.CharField(max_length=11, min_length=11, required=False, empty_value=None)
    telegramInput = forms.CharField(max_length=200, required=False, empty_value=None)
    matrixInput = forms.CharField(max_length=200, required=False, empty_value=None)


class RezomeForm(forms.Form):
    rezome = forms.CharField(widget = forms.Textarea(attrs = {'class': 'form-control'}), required = False, empty_value = "")
