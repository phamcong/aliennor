from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
from tinymce import models as tinymce_models

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

from ecocases.variables import *
from operator import itemgetter
from django.db.models import Q

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=50, default='')

    def __str__(self):
        return self.title

class Level(models.Model):
    title = models.CharField(max_length=50, default='')

    def __str__(self):
        return self.title

class ESM(models.Model):    
    label = models.CharField(max_length=50, default='')
    title = models.CharField(max_length=100, default='')
    description = models.CharField(max_length=500, default='')
    logo_url = models.CharField(max_length=500, default='', null=True)
    image_url = models.CharField(max_length=500, default='', null=True)
    pdf_url = models.CharField(max_length=500, default='', null=True)

    def __str__(self):
        return self.label
   
class Question(models.Model):
    title = models.CharField(max_length=500)
    esm = models.ForeignKey(ESM, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title
    
class Ecocase(models.Model):    
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    promise = tinymce_models.HTMLField(default='')
    description = tinymce_models.HTMLField(default='')
    levels = models.ManyToManyField(Level)
    categories = models.ManyToManyField(Category)
    first_esm = models.ForeignKey(ESM, null=True, blank=True, on_delete=models.CASCADE, related_name='first_esm')
    second_esm = models.ForeignKey(ESM, null=True, blank=True, on_delete=models.CASCADE, related_name='second_esm')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # ecocase ID has to be unique (should probably make it a primary key)
        self.title = self.title.title()
        if Ecocase.objects.filter(title=self.title).exists():
            super(Ecocase, self).save(*args, **kwargs)
            # raise ValueError('The ecocase with title %s is already present' % self.title)
        else:
            # save
            super(Ecocase, self).save(*args, **kwargs)

    def image_urls(self):
        ecocase_images = EcocaseImage.objects.filter(ecocase__id = self.id).values()
        image_urls = [aws_s3_ecocase_image_url + ecocase_image['image'] for ecocase_image in ecocase_images ]
        return image_urls

    def associated_esms_by_evals(self):
        ecocase = Ecocase.objects.get(id=self.id)
        esms = ESM.objects.all()
        esms_array = []
        for esm in esms:
            esm_dict = {}
            esm_dict['title'] = esm.title
            esm_dict['esm'] = esm
            esm_dict['first_esm_count'] = 0
            esm_dict['second_esm_count'] = 0
            esms_array.append(esm_dict)

        esmevaluations = ESMEvaluation.objects.filter(
            Q(ecocase2esm__ecocase=ecocase)
        )
        for esmevaluation in esmevaluations:
            esm = next(item for item in esms_array if item["title"] == esmevaluation.ecocase2esm.esm.title)
            if (esmevaluation.is_first_esm):
                esm['first_esm_count'] += 1
            if (esmevaluation.is_second_esm):
                esm['second_esm_count'] += 1

        sorted_by_first_esm = sorted(esms_array, key=itemgetter('first_esm_count'), reverse=True)
        sorted_by_second_esm = sorted(esms_array, key=itemgetter('second_esm_count'), reverse=True)

        if (sorted_by_first_esm[0]['title'] != sorted_by_second_esm[0]['title']):
            return {
                'first_esm': '' if sorted_by_first_esm[0]['first_esm_count'] == 0 else sorted_by_first_esm[0]['esm'],
                'second_esm': '' if sorted_by_second_esm[0]['first_esm_count'] == 0 else sorted_by_second_esm[0]['esm']
            }
        else:
            return {
                'first_esm': '' if sorted_by_first_esm[0]['first_esm_count'] == 0 else sorted_by_first_esm[0]['esm'],
                'second_esm': '' if sorted_by_second_esm[1]['first_esm_count'] == 0 else sorted_by_second_esm[1]['esm']
            }
class EcocaseImage(models.Model):
    prefix = models.CharField(max_length=200, default='')
    ecocase = models.ForeignKey(Ecocase, on_delete=models.CASCADE, null=True)
    image = models.ImageField(
        upload_to='ecocases/images/', default='ecocases/images/no-image.jpg')

    def __str__(self):
        return "../media/" + str(self.image)

class EcocaseComment(models.Model):
    ecocase = models.ForeignKey(Ecocase, on_delete=models.CASCADE)    
    username = models.CharField(max_length=100, validators=[MinLengthValidator(1)])
    body = models.TextField()
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.body

    def save(self, *args, **kwargs):
        self.full_clean()
        super(EcocaseComment, self).save(*args, **kwargs)

class EcocaseRating(models.Model):
    ecocase = models.ForeignKey(Ecocase, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    username = models.CharField(max_length=100, validators=[MinLengthValidator(1)])

    def __str__(self):
        return 'Title: %s | Vote: %s' % (self.ecocase, self.rating)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(EcocaseRating, self).save(*args, **kwargs)

    # def _get_vote_point_total(self):
    #     vote_point_total = 0
    #     for vote in self.vote_set.all():
    #         vote_point_total += vote.vote_point
    #     return vote_point_total
    # vote_point_total = property(_get_vote_point_total)

    # def vote_point_options(self):
    #     return vote_point_options

class Ecocase2ESM(models.Model):
    ecocase = models.ForeignKey(Ecocase, on_delete=models.CASCADE)
    esm = models.ForeignKey(ESM, on_delete=models.CASCADE)
    weight = models.IntegerField(default=0)

    def __str__(self):
        return self.ecocase.title + ' - ' + self.esm.title

class ESMEvaluation(models.Model):
    ecocase2esm = models.ForeignKey(Ecocase2ESM, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE)
    answer = tinymce_models.HTMLField(default='')
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    is_first_esm = models.NullBooleanField(null=True, default=False)
    is_second_esm = models.NullBooleanField(null=True, default=False)

    def clean(self):
        ecocase2esm = self.ecocase2esm
        question = self.question

        # validate piece 
        if question.esm.title != ecocase2esm.esm.title:
            raise ValidationError({'question': _("Selected question is not belong to the ecocase2esm's esm.")})
            # if you detect errors in multiple fields during Model.clean(), you can also pass a dictionary mapping field names to errors:
            # raise ValidationError({
            #     'title': ValidationError(_('Missing title.'), code='required'),
            #     'pub_date': ValidationError(_('Invalid date.'), code='invalid'),
            # })
        if (self.is_first_esm and self.is_second_esm):
            raise ValidationError({'associated_esms': _("A mechanism could not be both the most and the second most associated mechanims of an ecocase.")})
    def __str__(self):
        return self.ecocase2esm.ecocase.title + ' - ' + self.ecocase2esm.esm.title + ': ' + self.question.title + ' _by_ ' + self.user.username