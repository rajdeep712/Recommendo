from django import forms

class CommentForm(forms.Form):
    name = forms.CharField(max_length=100)
    comment = forms.CharField(max_length=1500)