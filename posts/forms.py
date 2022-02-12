from django import forms


class PostForm(forms.Form):
    titleInput = forms.CharField(max_length=50)
    bodyInput = forms.CharField()
    coverInput = forms.URLField(required=False, empty_value=None)
    shortDescriptionInput = forms.CharField(required=False, empty_value=None, max_length=156)


class CommentForm(forms.Form):
    textInput = forms.CharField(max_length=1000)