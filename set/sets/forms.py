from django import forms








class CreateSetForm(forms.Form):
    """Create set form"""

    CHOICES = [
        ("Entreprise", "Entreprise"),
        ("Association", "Association"),
        ("Autres", "Autres"),
    ]
    file = forms.FileField()
    name = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={"class": "col-12", "placeholder": "Nom du set"}),
    )
    type_set = forms.ChoiceField(choices=CHOICES)
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "col-12",
                "placeholder": "Description du set",
                "size": "200",
                "style": "width:100%; border-radius:5px; height: 90%; resize: none; border: solid silver 1px;",
            }
        )
    )


##############################


class CreateEventForm(forms.Form):
    """Create event form"""

    name = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={"class": "col-12", "placeholder": "Nom de l'évènement"}
        ),
    )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "col-12",
                "placeholder": "Description de l'évènement",
                "size": "200",
                "style": "width:100%; border-radius:5px; height: 90%; resize: none; border: solid silver 1px;",
            }
        )
    )


##############################


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
