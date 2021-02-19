from django import forms


class SearchForm(forms.Form):
    """Search form"""

    search_input = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={"class": "col-12", "placeholder": "Recherche"}),
    )


##############################


class ProfilImageForm(forms.Form):
    """Set profil image form"""

    file = forms.FileField(
        widget=forms.FileInput(attrs={ "style": "display:none;"})
    )


class SetNameForm(forms.Form):
    """set name form"""

    name = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={"class": "col-12", "placeholder": "Nouveau nom",  "style": "display:none;"}),
    )


class SetMailForm(forms.Form):
    """set mail form"""

    mail = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={"class": "col-12", "placeholder": "Nouveau mail",  "style": "display:none;"}
        ),
    )




##############################


class MessageForm(forms.Form):
    """Message form"""

    message = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "placeholder": "Ecrire un message ...",
                "style": "width:90%; border-radius:5px; height: 90%; resize: none; border: solid silver 1px;",
            }
        ),
    )
