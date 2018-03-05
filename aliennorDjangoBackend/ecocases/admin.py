from django.contrib import admin
from .models import Ecocase, EcocaseRating, EcocaseComment, ESM, Ecocase2ESM, Category, Level, EcocaseImage, ESMEvaluation, Question
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

class ESMEvaluationInline(admin.TabularInline):
  model = ESMEvaluation
  extra = 0

class EcocaseAdmin(admin.ModelAdmin):
  inlines = [Ecocase2ESMInline, EcocaseImageInline]

class Ecocase2ESMAdmin(admin.ModelAdmin):
  inlines = [ESMEvaluationInline]

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