from django import forms
from . import models

class postForm(forms.Form):

    header = forms.CharField(
        label='Enter Title',
        required = True,
        max_length = 100,
    )

    post = forms.CharField(
        label='Enter Pitch',
        required = True,
        max_length = 240,
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