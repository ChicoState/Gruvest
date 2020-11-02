from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from . import models


def must_be_unique(value):
    user = User.objects.filter(email=value)
    if len(user) > 0:
        raise forms.ValidationError("Email Already in Use")
    return value


class postForm(forms.Form):

    header = forms.CharField(
        label='Enter Title',
        required = True,
        max_length = 100,
    )

    post = forms.CharField(
        label='Enter Pitch',
        required = True,
        max_length = 1000,
    )

    def save(self):
        post_instance = models.PostModel()
        post_instance.post = self.cleaned_data["post"]
        post_instance.header = self.cleaned_data["header"]
        post_instance.save()
        return post_instance

# Class used by PitchCreator
class PostPitchForm(forms.ModelForm):

    # meta class
    class Meta:
        # model to be used
        model = models.PostModel
        # fields to be used
        fields = [
            "header",
            "post",
            "cost",
        ]

# Class used by CommentCreator
class PostCommentForm(forms.ModelForm):

    # meta class
    class Meta:
        # model to be used
        model = models.CommentModel
        # fields to be used
        fields = [
           "comment",
        ]

class AddFundsForm(forms.ModelForm):

    # meta class
    class Meta:
        # model to be used
        model = models.CatcherModel
        # fields to be used
        fields = [
           "funds",
        ]


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        label="Email",
        required=True,
        validators=[must_be_unique]
    )

    class Meta:
        model = User
        fields = ("username", "email",
                  "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user