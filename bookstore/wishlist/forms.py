from django import forms

class AddToCartForm(forms.Form):
    # The form for entering the amount of a book
    # to add.

    # choices is an option that defines what values
    # the user can populate the field with; in this
    # case I've set it to be 1-99, i.e. a user can't
    # add less than one copy of a
    # book or more than 99 to his
    # cart at once
    amount = 1

    # This field allows us to specify whether we want
    # to change the number of books in a cart to a specific
    # number (in the case of True) or simply add the amount we specified to the
    # existing total (in the case of False). This is specified by us,
    # so we hide it from the user with the forms.HiddenInput widget
    change_amount = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

