from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import *
# Register your models here.

class Ecocase2ESMInline(admin.TabularInline):
  model = Ecocase2ESM
  extra = 0

class EcocaseImageInline(admin.TabularInline):
  model = EcocaseImage
  extra = 0

class EcocaseInline(admin.TabularInline):
  model = Ecocase
  extra = 0

# class GroupInline(admin.TabularInline):
#   model = Group
#   extra = 0

# class UserAdmin(admin.ModelAdmin):
#   inlines = [GroupInline]

class ESMEvaluationInline(admin.TabularInline):
  model = ESMEvaluation
  extra = 0

class EcocaseAdmin(admin.ModelAdmin):
  inlines = [Ecocase2ESMInline, EcocaseImageInline]

class Ecocase2ESMAdmin(admin.ModelAdmin):
  inlines = [ESMEvaluationInline]

# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)
admin.site.register(Ecocase, EcocaseAdmin)
admin.site.register(EcocaseRating)
admin.site.register(EcocaseComment)
admin.site.register(ESM)
admin.site.register(Ecocase2ESM, Ecocase2ESMAdmin)
admin.site.register(Category)
admin.site.register(Level)
admin.site.register(EcocaseImage)
admin.site.register(ESMEvaluation)
admin.site.register(Question)
admin.site.register(NonESMEvaluation)
admin.site.register(EnvironmentalGain)
admin.site.register(EnvironGainEval)
admin.site.register(EcoEffectPotential)
admin.site.register(EcoEffectPotentialEval)
admin.site.register(EcoInnovationStatus)
admin.site.register(EcoinnovationStatusEval)
admin.site.register(MassEffectPotential)
admin.site.register(MassEffectPotentialEval)
admin.site.register(ReboundPotential)
admin.site.register(ReboundPotentialEval)