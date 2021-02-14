from django import forms


class InscriptionForm(forms.Form):
    """Inscription form"""

    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"placeholder": "Nom"}))
    email = forms.EmailField( widget=forms.TextInput(attrs={"placeholder": "Adresse e-mail"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Mot de passe"})
    )
    confirmation_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirmer le mot de passe"})
    )


class ConnexionForm(forms.Form):
    """Inscription form"""

    email = forms.EmailField(
        label="Adresse e-mail",
        widget=forms.TextInput(attrs={"placeholder": "Adresse e-mail"}),
    )
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={"placeholder": "Mot de passe"}),
    )


class SearchForm(forms.Form):
    """Search form"""

    search_input = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={"class": "col-12", "placeholder": "Recherche"}
        ),
    )


class InitializePasswordForm(forms.Form):
    """Inscription form"""

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Créer un mot de passe", "style": "width: 300px;"})
    )
    confirmation_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirmer le mot de passe", "style": "width: 300px;"})
    )


class LinkResetPasswordForm(forms.Form):
    """Inscription form"""

    email = forms.EmailField(
        label="Adresse e-mail",
        widget=forms.TextInput(attrs={"placeholder": "Entrez l'adresse e-mail du compte", "style": "width: 300px;"}),
    )



class ResetPasswordForm(forms.Form):
    """Search form"""

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Entrez le nouveau mot de passe", "style": "width: 300px;"})
    )
    confirmation_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirmer le mot de passe", "style": "width: 300px;"})
    )
