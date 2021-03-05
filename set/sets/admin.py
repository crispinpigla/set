from django.contrib import admin

from .models import Sets, Evenements, PublicationSet, PublicationEvenement

from user.models import Utilisateurs

# Register your models here.




# Les actions

def set_controlled(modeladmin, request, queryset):
	""""""
	queryset.update(control_admin='t')
set_controlled.short_description = "Marquer comme controllé"

def unset_controlled(modeladmin, request, queryset):
	""""""
	queryset.update(control_admin='f')
unset_controlled.short_description = "Marquer comme non-controllé"


def set_hide(modeladmin, request, queryset):
	""""""
	queryset.update(masquage_admin='t')
set_hide.short_description = "Masquer la(les) publication(s)"

def unset_hide(modeladmin, request, queryset):
	""""""
	queryset.update(masquage_admin='f')
unset_hide.short_description = "Démasquer la(les) publication(s)"


def close_set(modeladmin, request, queryset):
	""""""
	queryset.update(statut_fermeture_admin='t')
close_set.short_description = "Fermer le(s) set(s)"

def open_set(modeladmin, request, queryset):
	""""""
	queryset.update(statut_fermeture_admin='f')
open_set.short_description = "Ouvrir le(s) set(s)"


def close_event(modeladmin, request, queryset):
	""""""
	queryset.update(statut_fermeture_admin='t')
close_event.short_description = "Fermer les évènements"

def open_event(modeladmin, request, queryset):
	""""""
	queryset.update(statut_fermeture_admin='f')
open_event.short_description = "Ouvrir les évènements"

def lock_account(modeladmin, request, queryset):
	""""""
	queryset.update(statut_blocage_admin='t')
lock_account.short_description = "Bloquer les comptes"

def unlock_account(modeladmin, request, queryset):
	""""""
	queryset.update(statut_blocage_admin='f')
unlock_account.short_description = "Débloquer les comptes"






# Les sous-éléments

class PublicationSetInline(admin.TabularInline):
    model = PublicationSet   # the query goes through an intermediate table.
    extra = 0

class PublicationEvenementInline(admin.TabularInline):
    model = PublicationEvenement   # the query goes through an intermediate table.
    extra = 0















# Les tables

# PublicationsSets
class PublicationSetAdmin(admin.ModelAdmin):
	""""""
	readonly_fields = ('thumbnail_view1_detail', 'thumbnail_view2_detail')
	fields = ['contenu_text', 'auteur', 'thumbnail_view1_detail', 'thumbnail_view2_detail']
	list_display = ('contenu_text', 'view_media1', 'view_media2', 'date', 'control_admin', 'masquage_admin')
	list_filter = ['control_admin', 'masquage_admin']
	actions = [set_controlled, unset_controlled, set_hide, unset_hide]

	def thumbnail_view1(self, obj):
		return obj.view_media1
	thumbnail_view1.short_description = 'Image media1'
	thumbnail_view1.allow_tags = True

	def thumbnail_view2(self, obj):
		return obj.view_media2
	thumbnail_view2.short_description = 'Image media2'
	thumbnail_view2.allow_tags = True

	def thumbnail_view1_detail(self, obj):
		return obj.view_detail_media1
	thumbnail_view1_detail.short_description = 'Image detail media1'
	thumbnail_view1_detail.allow_tags = True

	def thumbnail_view2_detail(self, obj):
		return obj.view_detail_media2
	thumbnail_view2_detail.short_description = 'Image detail media2'
	thumbnail_view2_detail.allow_tags = True

admin.site.register(PublicationSet, PublicationSetAdmin)




# PublicationEvenement
class PublicationEvenementAdmin(admin.ModelAdmin):
	""""""
	readonly_fields = ('thumbnail_view1_detail', 'thumbnail_view2_detail')
	fields = ['contenu_text', 'auteur', 'thumbnail_view1_detail', 'thumbnail_view2_detail']
	list_display = ('contenu_text', 'view_media1', 'view_media2', 'date', 'control_admin', 'masquage_admin')
	list_filter = ['control_admin', 'masquage_admin']
	actions = [set_controlled, unset_controlled, set_hide, unset_hide]

	def thumbnail_view1(self, obj):
		return obj.view_media1
	thumbnail_view1.short_description = 'Image media1'
	thumbnail_view1.allow_tags = True

	def thumbnail_view2(self, obj):
		return obj.view_media2
	thumbnail_view2.short_description = 'Image media2'
	thumbnail_view2.allow_tags = True

	def thumbnail_view1_detail(self, obj):
		return obj.view_detail_media1
	thumbnail_view1_detail.short_description = 'Image detail media1'
	thumbnail_view1_detail.allow_tags = True

	def thumbnail_view2_detail(self, obj):
		return obj.view_detail_media2
	thumbnail_view2_detail.short_description = 'Image detail media2'
	thumbnail_view2_detail.allow_tags = True

admin.site.register(PublicationEvenement, PublicationEvenementAdmin)




# Utilisateurs
class UtilisateursAdmin(admin.ModelAdmin):
	""""""
	list_display = ('nom', 'adresse_mail', 'statut_blocage_admin')
	actions = [lock_account, unlock_account]
	inlines = [PublicationSetInline, PublicationEvenementInline, ]

admin.site.register(Utilisateurs, UtilisateursAdmin)


# Sets
class SetsAdmin(admin.ModelAdmin):
	""""""
	list_display = ('nom', 'type0', 'description', 'date', 'statut_fermeture_admin')
	actions = [close_set, open_set]
	inlines = [PublicationSetInline, ]

admin.site.register(Sets, SetsAdmin)


# Evenements
class EvenementsAdmin(admin.ModelAdmin):
	""""""
	list_display = ('set0', 'administrateur', 'nom', 'description', 'date', 'statut_fermeture_admin')
	actions = [close_event, open_event]
	inlines = [PublicationEvenementInline, ]

admin.site.register(Evenements, EvenementsAdmin)










