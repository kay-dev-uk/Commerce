from email.policy import default
from .models import Listing, Comment, Bid
from django import forms

class CreateListing(forms.Form):
    CATEGORY_CHOICES = [
        ("NO CATEGORY", "NO CATEGORY"),
        ("MISC", "MISC"),
        ("ELECTRONICS", "ELECTRONICS"),
        ("TOYS", "TOYS"),
        ("FASHION", "FASHION"),
        ("HOME", "HOME"),
    ]
    title = forms.CharField()
    url = forms.URLField(required=False)
    category = forms.ChoiceField(choices=CATEGORY_CHOICES)
    description = forms.CharField(widget=forms.Textarea)
    price = forms.IntegerField(min_value=0)

    class Meta():
        model = Listing
        fields = ["title", "url", "category", "description", "price"]


class CommentForm(forms.Form):
    comment = forms.CharField()

    class Meta():
        model = Comment
        fields = ["comment"]


class BiddingForm(forms.Form):
    bid = forms.IntegerField()

    class Meta():
        model = Bid
        fields = ["bid"]

