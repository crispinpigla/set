from django import forms








class SearchForm(forms.Form):
    """Search form"""

    search_input = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={"class": "col-12", "placeholder": "Recherche"}
        ),
    )
##############################


class ProfilImageForm(forms.Form):
    """Set profil image form"""

    file = forms.FileField()


class SetNameForm(forms.Form):
    """set name form"""

    name = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={"class": "col-12", "placeholder": "Nouveau nom"}
        ),
    )

class SetMailForm(forms.Form):
    """set mail form"""

    mail = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={"class": "col-12", "placeholder": "Nouveau mail"}
        ),
    )
##############################

class CreateSetForm(forms.Form):
    """Create set form"""

    CHOICES = [('Entreprise', 'Entreprise'), ('Association', 'Association'),  ('Autres', 'Autres')]
    file = forms.FileField()
    name = forms.CharField(label="",widget=forms.TextInput(attrs={"class": "col-12", "placeholder": "Nom du set"}),)
    type_set = forms.ChoiceField(choices=CHOICES)
    description = forms.CharField(widget=forms.Textarea(attrs={"class": "col-12", "placeholder": "Description du set", 'size': '200'}))


##############################


class CreateEventForm(forms.Form):
    """Create event form"""

    name = forms.CharField(label="",widget=forms.TextInput(attrs={"class": "col-12", "placeholder": "Nom de l'évènement"}),)
    description = forms.CharField(widget=forms.Textarea(attrs={"class": "col-12", "placeholder": "Description de l'évènement", 'size': '200'}))


##############################


class MessageForm(forms.Form):
    """Message form"""

    message = forms.CharField(widget=forms.Textarea(attrs={"class": "col-12", "placeholder": "Ecrire ..."}))