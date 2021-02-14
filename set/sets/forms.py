from django import forms


class SearchForm(forms.Form):
    """Search form"""

    search_input = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={"class": "col-12", "placeholder": "Recherche"}),
    )


#############################


class SetCoverImageForm(forms.Form):
    """Set cover image form"""

    file = forms.FileField()


class SetDescriptionSetForm(forms.Form):
    """set description set form"""

    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "col-12",
                "placeholder": "Nouvelle description",
                "size": "200",
                "style": "width:700px; border-radius:5px; height: 100px; resize: none;",
            }
        )
    )


class PublicationSetForm(forms.Form):
    """publication set form"""

    publication_text = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "col-12",
                "placeholder": "Nouvelle publication",
                "size": "200",
                "style": "width:100%; border-radius:5px; height: 100px; resize: none;",
            }
        ),
    )
    file_1 = forms.FileField(required=False)
    file_2 = forms.FileField(required=False)


#############################


class SetDescriptionSetEvent(forms.Form):
    """set description set form"""

    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "col-12",
                "placeholder": "Nouvelle description",
                "size": "200",
                "style": "width:700px; border-radius:5px; height: 100px; resize: none;",
            }
        )
    )


class PublicationEventForm(forms.Form):
    """publication event form"""

    publication_text = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "col-12",
                "placeholder": "Nouvelle publication",
                "size": "200",
                "style": "width:100%; border-radius:5px; height: 100px; resize: none;",
            }
        ),
    )
    file_1 = forms.FileField(required=False)
    file_2 = forms.FileField(required=False)
