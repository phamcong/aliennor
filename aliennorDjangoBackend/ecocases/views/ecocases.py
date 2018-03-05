from django.http import JsonResponse
from django.db.models import Avg, Count, Func
from django.shortcuts import render
from django.views.generic.edit import FormView
from rest_framework import viewsets

from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse

from ..forms import EcocaseForm
from ..models import Ecocase, EcocaseRating, ESM, Ecocase2ESM, Category, EcocaseComment, EcocaseImage, Level, ESMEvaluation, Question
from django.contrib.auth.models import User
from ..serializers import UserSerializer, EcocaseSerializer, EcocaseCommentSerializer
from ..mixins import FormUserNeededMixin, UserOwnerMixin
from django.db.models import Q

import json
import logging
from django.contrib import messages
from ecocases.utils import get_token_data
from django.utils.timezone import now

from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.core import serializers

from ecocases.variables import *

dirspot = os.getcwd()

def indexView(request):
    ecocases = Ecocase.objects.all()
    return render(request, 'ecocases/index.html', {'ecocases': ecocases})

def new_ecocase(request):
    if request.method != 'POST':
        pass

    # get ecocase title
    title = request.POST.get('title', '')

    # save new ecocase
    ecocase = Ecocase(title=title)
    try:
        ecocase.save()
    except Exception as e:
        return JsonResponse({
            'status': 'fail',
            'data': {
                'message': str(e) if type(e) == ValueError else 'Error while saving ecocase'
            }
        }, status=500)

    return JsonResponse({
        'status': 'success',
        'data': {
            'title': m.title
        }
    })

class EcocaseCreateView(FormUserNeededMixin, FormView):
    form_class = EcocaseForm
    template_name = 'ecocases/ecocase_create.html'
    success_url = reverse_lazy('ecocases:index')

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        # images = request.FILES.getlist('images')

        if form.is_valid():
            # image_url_list = []

            # for count, image in enumerate(images):
            #     uploaded_image = ecocase_image_fs.save(image.name, image)
            #     image_url_list.append(uploaded_image_path + uploaded_image)

            ecocase = Ecocase(title=form.cleaned_data['title'],                             
                              user=request.user,
                              )
            ecocase.save()
            
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

def get_ecocases(request):
    print("at ecocases view: get ecocases");
    if request.method != 'GET':
        pass

    esms_params = request.GET.get('esms', '').split(',')
    categories_params = request.GET.get('categories', '').split(',')
    selected_esms = [esm for esm in esms_params if esm != '']
    selected_categories = [ctg for ctg in categories_params if ctg != '']

    esms_values = ESM.objects.all().values()
    categories_values = Category.objects.all().values()
    ecocases = Ecocase.objects.filter(
        Q(first_esm__isnull = False) | Q(second_esm__isnull = False)
    )

    found_ecocases_array = []
    if len(selected_esms) == len(esms_values) and len(selected_categories) == len(categories_values):
        found_ecocases = ecocases
    else:
        # Apply cateogories filter
        ecocase_by_categories = []
        if len(selected_categories) == len(categories_values):
            ecocase_by_categories = ecocases
        else:
            for ecocase in ecocases:
                categories = [ctg['title'] for ctg in ecocase.categories.values()]
                if not set(categories).isdisjoint(selected_categories):
                    ecocase_by_categories.append(ecocase)

        # Apply esms filter
        ecocase_by_esms = []
        if len(selected_esms) == len(esms_values):
            ecocase_by_esms = ecocase_by_categories
        else:
            for ecocase in ecocase_by_categories:
                associated_esms_titles = []
                if (ecocase.first_esm != None):
                    associated_esms_titles.append(ecocase.first_esm.title)
                
                if (ecocase.second_esm != None):
                    associated_esms_titles.append(ecocase.second_esm.title)
                
                if not set(associated_esms_titles).isdisjoint(selected_esms):
                        ecocase_by_esms.append(ecocase)
        found_ecocases = ecocase_by_esms

    count_results = {}

    count_results['by_esms'] = {}
    count_results['by_ctgs'] = {}

    for esm in esms_values:
        count_results['by_esms'][esm['title']] = 0
    for ctg in categories_values:
        count_results['by_ctgs'][ctg['title']] = 0

    for ecocase in found_ecocases:
        if (ecocase.first_esm != None):
            count_results['by_esms'][ecocase.first_esm.title] += 1;
        if (ecocase.second_esm != None):
            count_results['by_esms'][ecocase.second_esm.title] += 1;
        if (ecocase.categories != None):
            ctgs = ecocase.categories.values()
            for ctg in ctgs:
                count_results['by_ctgs'][ctg['title']] += 1;

    return JsonResponse({
        'status': 'success',
        'data': {
            'count_results': count_results,
            'ecocases': ecocases_set_to_array(found_ecocases)
        }
    })

def get_all_ecocases(request):
    ecocases = Ecocase.objects.all()
    return JsonResponse({
        'status': 'success',
        'data': {
            'ecocases': ecocases_set_to_array(ecocases)
        }
    })

def get_esms_weights_tagged_ecocase(request, ecocase_id):
    ecocase = Ecocase.objects.get(id=ecocase_id)
    esms = ESM.objects.all()
    esms_weights_dict = {}
    for esm in esms:
        esms_weights_dict[esm.title] = {
            "esm": model_to_dict(esm),
            "weight": 15
        }
    if (ecocase.first_esm != None):
        esms_weights_dict[ecocase.first_esm.title]['weight'] = 30
    if (ecocase.second_esm != None):
        esms_weights_dict[ecocase.second_esm.title]['weight'] = 20
    return JsonResponse({
        'status': 'success',
        'data': {
            'esms_weights': esms_weights_dict
        }
    })
    
def get_untagged_ecocases(request):
    print("at ecocases view: get untagged ecocases");
    if request.method != 'GET':
        pass

    categories_params = request.GET.get('categories', '').split(',')
    selected_categories = [ctg for ctg in categories_params if ctg != '']

    esms_values = ESM.objects.all().values()
    categories_values = Category.objects.all().values()
    
    untagged_ecocases = Ecocase.objects.filter(
        Q(first_esm__exact = None),
        Q(second_esm__exact = None)
    )

    if len(selected_categories) == len(categories_values):
        found_untagged_ecocases = untagged_ecocases
    else:
        # Apply cateogories filter
        untagged_ecocase_by_categories = []
        for ecocase in untagged_ecocases:
            categories = [ctg['title'] for ctg in ecocase.categories.values()]
            if not set(categories).isdisjoint(selected_categories):
                untagged_ecocase_by_categories.append(ecocase)

        found_untagged_ecocases = untagged_ecocase_by_categories

    count_results_by_ctgs = {}

    for ctg in categories_values:
        count_results_by_ctgs[ctg['title']] = 0

    for ecocase in found_untagged_ecocases:
        if (ecocase.categories != None):
            ctgs = ecocase.categories.values()
            for ctg in ctgs:
                count_results_by_ctgs[ctg['title']] += 1;
    
    return JsonResponse({
        'status': 'success',
        'data': {
            'count_results_by_ctgs': count_results_by_ctgs,
            'untagged_ecocases': ecocases_set_to_array(found_untagged_ecocases)
        }
    })

def ecocases_set_to_array(ecocases):
    ecocases_array = []
    for ecocase in ecocases:
        ecocase_dict = model_to_dict(ecocase)
        ecocase_dict['levels'] = [item['title'] for item in ecocase.levels.values()]
        ecocase_dict['categories'] = [item['title'] for item in ecocase.categories.values()]
        if (ecocase.first_esm != None):
            ecocase_dict['first_esm'] = model_to_dict(ecocase.first_esm)
        if (ecocase.second_esm != None):
            ecocase_dict['second_esm'] = model_to_dict(ecocase.second_esm)
        # else:
        #     associated_esms_by_evals = ecocase.associated_esms_by_evals()
        #     if (associated_esms_by_evals['first_esm'] != '') and (associated_esms_by_evals['second_esm'] != ''):
        #         ecocase_dict['first_esm'] = model_to_dict(associated_esms_by_evals['first_esm'])
        #         ecocase_dict['second_esm'] = model_to_dict(associated_esms_by_evals['second_esm'])
        # ecocase_dict.update({'image_urls': ecocase.image_urls()})
        ecocase_dict['image_urls'] = ecocase.image_urls()
        ecocases_array.append(ecocase_dict)
    return ecocases_array
    # print('request GET all', request.GET)
    # esms = request.GET.get('esms')
    # ecocases = {}
    # if esms is not None:
    #     esms = request.GET.get('esms', '').split(',')
    #     categories = request.GET.get('categories', '').split(',')
    #     selected_esms = [esm for esm in esms if esm != '']
    #     selected_categories = [ctg for ctg in categories if ctg != '']

    #     all_ecocase2esms = Ecocase2ESM.objects.filter(
    #         Q(esm__title__in=selected_esms),
    #         Q(ecocase__category__title__in=selected_categories)
    #     )

    #     print('all_ecocase2esms filtered on categories: ', all_ecocase2esms)

    #     for ecocase2esm in all_ecocase2esms:
    #         ecocase = Ecocase.objects.get(id=ecocase2esm.ecocase.id)
    #         ecocase_dict = model_to_dict(ecocase)
    #         ecocase_dict['levels'] = [item['title'] for item in ecocase.levels.values()]
    #         ecocase_dict['categories'] = [item['title'] for item in ecocase.categories.values()]
    #         if (ecocase.first_esm != None) and (ecocase.second_esm != None):
    #             ecocase_dict['first_esm'] = model_to_dict(ecocase.first_esm)
    #             ecocase_dict['second_esm'] = model_to_dict(ecocase.second_esm)
    #         else:
    #             associated_esms_by_evals = ecocase.associated_esms_by_evals()
    #             if (associated_esms_by_evals['first_esm'] != '') and (associated_esms_by_evals['second_esm'] != ''):
    #             ecocase_dict['first_esm'] = model_to_dict(associated_esms_by_evals['first_esm'])
    #             ecocase_dict['second_esm'] = model_to_dict(associated_esms_by_evals['second_esm'])
    #         ecocase_dict['image_urls'] = ecocase.image_urls()
    #         ecocases[ecocase2esm.ecocase.id] = ecocase_dict
        
    # else:
    #     all_ecocases = Ecocase.objects.all()
    #     for ecocase in list(all_ecocases):
    #         ecocase_dict = model_to_dict(ecocase)
    #         ecocase_dict['levels'] = [item['title'] for item in ecocase.levels.values()]
    #         ecocase_dict['categories'] = [item['title'] for item in ecocase.categories.values()]
    #         if (ecocase.first_esm != None) and (ecocase.second_esm != None):
    #             ecocase_dict['first_esm'] = model_to_dict(ecocase.first_esm)
    #             ecocase_dict['second_esm'] = model_to_dict(ecocase.second_esm)
    #         else:
    #             associated_esms_by_evals = ecocase.associated_esms_by_evals()
    #             if (associated_esms_by_evals['first_esm'] != '') and (associated_esms_by_evals['second_esm'] != ''):
    #                 ecocase_dict['first_esm'] = model_to_dict(associated_esms_by_evals['first_esm'])
    #                 ecocase_dict['second_esm'] = model_to_dict(associated_esms_by_evals['second_esm'])
    #         # ecocase_dict.update({'image_urls': ecocase.image_urls()})
    #         ecocase_dict['image_urls'] = ecocase.image_urls()
    #         print('image_urls', ecocase_dict['image_urls'])
    #         ecocases[ecocase.id] = ecocase_dict
    
    # print('ecocases: ', ecocases[next(iter(ecocases))])

# check if an ecocase is associated with one of esm in seletec_esms
def is_associated(ecocase, selected_esms):
    is_associated = False
    print('selected_esms: ', selected_esms)
    esm_set = ecocase.esm_set.all().values()
    for esm in esm_set:
        if esm['display_name'] in selected_esms:
            is_associated = True
            break
    
    print('is_associated: ', is_associated)
    return is_associated

def get_filtered_ecocases(request):
    print("at ecocases view: get ecocases");
    if request.method != 'GET':
        pass

    # get ecocases
    print('request GET all', request.GET)
    esms = request.GET.get('esms', '').split(',')
    categories = request.GET.get('categories', '').split(',')
    selected_esms = [esm for esm in esms if esm != '']
    selected_categories = [ctg for ctg in categories if ctg != '']

    print('selected_esms: ', selected_esms)
    print('selected_categories: ', selected_categories)
    
    ecocases = Ecocase.objects.all()
    ecocase_by_categories = []
    # Apply cateogories filter
    for ecocase in ecocases:
        categories = [ctg['title'] for ctg in ecocase.categories.values()]
        if not set(categories).isdisjoint(selected_categories):
            ecocase_by_categories.append(ecocase)
    
    print('len ecocase_by_categories ========> ', len(ecocase_by_categories))
    # Apply esms filter
    ecocase_by_esms_array = []
    for ecocase in ecocase_by_categories:
        if (ecocase.first_esm == None) or (ecocase.second_esm == None):
            associated_esms_by_evals = ecocase.associated_esms_by_evals()
            if (associated_esms_by_evals['first_esm'].title in selected_esms) or (associated_esms_by_evals['second_esm'].title in selected_esms):
                ecocase_by_esms_array.append(ecocase)
        else:
            associated_esms_titles = [ecocase.first_esm.title, ecocase.second_esm.title]
            if not set(associated_esms_titles).isdisjoint(selected_esms):
                ecocase_by_esms_array.append(ecocase)
            
    print('len ecocase_by_esms ========> ', len(ecocase_by_esms_array))
    found_ecocases_array = []
    for ecocase in ecocase_by_esms_array:
        ecocase_dict = model_to_dict(ecocase)
        ecocase_dict['levels'] = [item['title'] for item in ecocase.levels.values()]
        ecocase_dict['categories'] = [item['title'] for item in ecocase.categories.values()]
        if (ecocase.first_esm != None) and (ecocase.second_esm != None):
            ecocase_dict['first_esm'] = model_to_dict(ecocase.first_esm)
            ecocase_dict['second_esm'] = model_to_dict(ecocase.second_esm)
            ecocase_dict['image_urls'] = ecocase.image_urls()
            found_ecocases_array.append(ecocase_dict)
        else:
            print('associated_esms_by_evals: ', ecocase.associated_esms_by_evals())
            associated_esms_by_evals = ecocase.associated_esms_by_evals()
            if (associated_esms_by_evals['first_esm'] != '') and (associated_esms_by_evals['second_esm'] != ''):
                ecocase_dict['first_esm'] = model_to_dict(associated_esms_by_evals['first_esm'])
                ecocase_dict['second_esm'] = model_to_dict(associated_esms_by_evals['second_esm'])
                ecocase_dict['image_urls'] = ecocase.image_urls()
                found_ecocases_array.append(ecocase_dict)
        
    print('len found_ecocases_array ========> ', len(found_ecocases_array))
    return JsonResponse({
        'status': 'success',
        'data': {
            'ecocases': found_ecocases_array
        }
    })

def post_ecocase(request):
    print("at ecocase views: post ecocase")
    if request.method == 'POST':
        post_data = json.loads(request.body)
        title = post_data['title']

        try:
            username = post_data['username']
        except KeyError:
            token = get_token_data(request)
            username = token['username']

        # get ecocase object
        user = User.objects.get(username=username)
        # comment
        ecocase = Ecocase(title=title, user=user)
        try:
            ecocase.save()
        except:
            return JsonResponse({
                'status': 'fail',
                'data': {
                    'message': 'Error while saving ecocase'
                }
            }, status=500)

        return JsonResponse({
            'status': 'success',
            'data': {
                'id': ecocase.id
            }
        })
    elif request.method == 'DELETE':
        id = request.GET.get('id', '')
        # username = request.GET.get('u', '')

        try:
            ecocase = Ecocase.objects.get(id=id)
        except Ecocase.DoesNotExist:
            return JsonResponse({
                'status': 'fail',
                'data': {
                    'message': 'This ecocase does not exist'
                }
            }, status=500)

        try:
            ecocase.delete()
        except:
            return JsonResponse({
                'status': 'fail',
                'data': {
                    'message': 'Error while deleting ecocase'
                }
            }, status=500)

        return JsonResponse({
            'status': 'success'
        })

def get_associated_esms(request, ecocase_id):
    print('------- at get_associated_esms -------');
    errors = []
    try:
        ecocase = Ecocase.objects.get(id=ecocase_id)
    except Ecocase.DoesNotExist:
        errors.append("Ecocase doesn't exist")
        return JsonResponse({
            'status': 'success',
            'data': {                
                'errors': errors
            }
        })
    esmevaluations = ESMEvaluation.objects.filter((
                Q(ecocase2esm__ecocase__exact=ecocase)
            ))
    associated_esms_summary = {};
    esms = ESM.objects.all()
    for esm in esms:
        associated_esms_summary[esm.title] = {
            'esm': model_to_dict(esm),
            'title': esm.title,
            'first_esm_count': 0,
            'second_esm_count': 0
        }
    
    
    for esmevaluation in esmevaluations:
        if (esmevaluation.is_first_esm):
            associated_esms_summary[esmevaluation.ecocase2esm.esm.title]['first_esm_count'] += 1
        if (esmevaluation.is_second_esm):
            associated_esms_summary[esmevaluation.ecocase2esm.esm.title]['second_esm_count'] += 1

    return JsonResponse({
        'status': 'success',
        'data': {
            'associated_esms_summary': associated_esms_summary,
            'errors': errors
        }
    })
def ecocase_details(request, ecocase_id):
    print('at ecocase detail')
    errors = []
    if request.method != 'GET':
        pass

    # get ecocase
    try:
        ecocase = Ecocase.objects.get(id=ecocase_id)
    except Ecocase.DoesNotExist:
        errors.append("Ecocase doesn't exist")
        return JsonResponse({
            'status': 'success',
            'data': {
                'rating': {
                    'avg': None,
                    'comments': None
                },
                'errors': errors
            }
        })

    # get rating
    r = EcocaseRating.objects.filter(ecocase=ecocase)\
        .values('rating')\
        .aggregate(
            avg_rating=Avg('rating'),
            rating_count=Count('rating')
        )
    avg_rating = r['avg_rating']
    rating_count = r['rating_count']

    # get comments
    cmt = EcocaseComment.objects.filter(ecocase=ecocase).values('body', 'username')

    # print('ecocase:', ecocase);
    ecocase_dict = model_to_dict(ecocase)
    ecocase_dict['levels'] = [item['title'] for item in ecocase.levels.values()]
    ecocase_dict['categories'] = [item['title'] for item in ecocase.categories.values()]
    if (ecocase.first_esm != None):
        ecocase_dict['first_esm'] = model_to_dict(ecocase.first_esm)
    if (ecocase.second_esm != None):
        ecocase_dict['second_esm'] = model_to_dict(ecocase.second_esm)
    ecocase_dict['image_urls'] = ecocase.image_urls()
    # ecocase = serializers.serialize('json', [ecocase, ])
    # ecocase = json.loads(ecocase)


    
    # get esms by user
    esmevaluations_list = []
    username = request.GET.get('username')
    questions = Question.objects.all()
    print('usernameeeeeeee: ', username)
    try:
        user = User.objects.get(username=username)
        esmevaluations = ESMEvaluation.objects.filter(
                Q(ecocase2esm__ecocase__exact=ecocase),
                Q(user__username__exact=username)
            )
        if len(esmevaluations.values()) == 0: 
            # user view this ecocase for the first time
            # create all possible esmevaluations (for each esm and for each question)
            esms = ESM.objects.all()
            question = Question.objects.all()
            user = User.objects.get(username=username)
            for esm in esms:
                ecocase2esms = Ecocase2ESM.objects.filter(
                    ecocase=ecocase,
                    esm=esm
                )
                if len(ecocase2esms) == 0:
                    ecocase2esm = Ecocase2ESM(ecocase=ecocase,esm=esm)
                    ecocase2esm.save()
                else:
                    ecocase2esm = ecocase2esms[0]
                for question in questions:
                    if question.esm == esm:
                        new_esmevaluation = ESMEvaluation(
                            ecocase2esm=ecocase2esm,
                            question=question,
                            answer='',
                            user=user
                        )
                        new_esmevaluation.save()
            esmevaluations = ESMEvaluation.objects.filter(
                Q(ecocase2esm__ecocase__exact=ecocase),
                Q(user__username__exact=username)
            )
        else:
            for esmevaluation in esmevaluations:
                esmevaluation_dict = {}
                esmevaluation_dict['id'] = esmevaluation.id
                esmevaluation_dict['question'] = model_to_dict(esmevaluation.question)
                esmevaluation_dict['esm'] = model_to_dict(esmevaluation.ecocase2esm.esm)
                esmevaluation_dict['answer'] = esmevaluation.answer
                esmevaluations_list.append(esmevaluation_dict)

            print('Found esmevaluations: ', esmevaluations_list)
            # esmevaluations corresponding to this user exist.
            # return existing esmevaluations
    except User.DoesNotExist:
        errors.append('Not authenticated user. Please logged in to tag ecocase.')


    print('ecocase json: ', ecocase_dict);
    return JsonResponse({
        'status': 'success',
        'data': {
            'rating': {
                'avg': '{:.1f}'.format(avg_rating) if avg_rating is not None else None,
                'count': rating_count
            },
            'esmevaluations': esmevaluations_list,
            # 'ecocase': ecocase[0].get('fields'),
            'ecocase': ecocase_dict,
            'comments': list(cmt),
            'errors': errors
        }
    })

class Round(Func):
    function = 'ROUND'
    template='%(function)s(%(expressions)s, 1)'

def ecocases_summary(request):
    if request.method != 'GET':
        pass

    # get all requested ecocase ids
    ecocase_ids = request.GET.get('ids', '').split(',')

    ecocase = Ecocase.objects.filter(id__in=ecocase_ids).annotate(
        avg_rating=Round(Avg('rating__rating')), # avg on rating column of rating table
        comment_count=Count('comment', distinct=True)
    ).values()

    ecocases = {}
    for ecocase in list(ecocase):
        ecocases[ecocase.get('id')] = ecocase

    return JsonResponse({
        'status': 'success',
        'data': {
            'ecocases': ecocases
        }
    })

def get_filter_criteria(request):
    print("at esms view: get esm");
    if request.method != 'GET':
        pass
    filter_criteria = {}
    # get esms
    esms = ESM.objects.all()
    categories = Category.objects.all()
    
    filter_criteria['esms'] = [model_to_dict(esm) for esm in esms]
    filter_criteria['categories'] = [model_to_dict(category) for category in categories]

    return JsonResponse({
        'status': 'success',
        'data': {
            'filter_criteria': filter_criteria
        }
    })

''' API '''

class EcocaseViewSet(viewsets.ModelViewSet):  
    serializer_class = EcocaseSerializer
    queryset = Ecocase.objects.all()


class EcocaseCommentViewSet(viewsets.ModelViewSet):
    serializer_class = EcocaseCommentSerializer
    queryset = EcocaseComment.objects.all()
    print('ecocase comments:', queryset)


def submit_esmevaluations(request, ecocase_id, username):
    print("at ecocase views: submit esmevaluations")
    if request.method == 'POST':
        post_data = json.loads(request.body)
        print('submit_esmevaluations - post_data', post_data)
        submit_esmevaluations = post_data['esmevaluations']

        for submit_esmevaluation in submit_esmevaluations:
            esmevaluation = ESMEvaluation.objects.get(id=submit_esmevaluation['id'])
            esmevaluation.answer = submit_esmevaluation['answer']
            esmevaluation.is_first_esm = submit_esmevaluation['isFirstESM']
            esmevaluation.is_second_esm = submit_esmevaluation['isSecondESM']
            esmevaluation.save()
        
        return JsonResponse({
            'status': 'success'
        })
    else:
        pass

def upload_json(request):
    data = {}
    if "GET" == request.method:
        return render(request, "ecocases/upload_json.html", data)
    # if not GET, then proceed
    try:
        json_file = request.FILES["json_file"]
        if not json_file.name.endswith('.json'):
            messages.error(request, 'File is not json type')
            return HttpResponseRedirect(reverse("ecocases:upload_json"))

        # if file is too large, return
        if json_file.multiple_chunks():
            messages.error(request, "Uploaded file is too big (%.2f MB)." % (
                json_file.size / (1000 * 1000),))
            return HttpResponseRedirect(reverse("ecocases:upload_json"))

        file_data = json.load(json_file)

        for obj in file_data:
            data_dict = {}
            data_dict["title"] = obj["title"]
            data_dict["promise"] = obj["promise"]
            data_dict["description"] = obj["description"] 
            data_dict["timestamp"] = now
            data_dict["image_urls"] = obj["image_urls"].split(', ')
            # data_dict["categories"] = obj["categories"]
            # data_dict["levels"] = obj["levels"]
            # data_dict["first_esm"] = obj["first_esm"]
            # data_dict["second_esm"] = obj["second_esm"]

            try:
                new_ecocase = Ecocase(
                    title=obj["title"],
                    promise=obj["promise"],
                    description=obj["description"],
                    user = request.user
                )
                new_ecocase.save()
                if "categories" in obj:
                    if obj["categories"] == 'All':
                        categories = Category.objects.all()
                        for ctg in categories:
                            new_ecocase.categories.add(ctg)
                    else:
                        data_dict["categories"] = obj["categories"]
                        for ctg in data_dict['categories'].split(', '): 
                        # print('ctg: ', ctg)                   
                            try:
                                new_ecocase.categories.add(Category.objects.get(title=ctg))
                            except Exception as e:
                                print('category', ctg)
                                print('error categories', e)
                if "levels" in obj:
                    if obj["levels"] == 'All':
                        levels = Level.objects.all()
                        for level in levels:
                            new_ecocase.levels.add(level)
                    else:
                        data_dict["levels"] = obj["levels"]
                        for level in data_dict['levels'].split(', '):
                        # print('level: ', level)                     
                            try:
                                new_ecocase.levels.add(Level.objects.get(title=level))
                            except Exception as e:
                                print('level', level)
                                print('error levels', e)
                if "first_esm" in obj:
                    data_dict["first_esm"] = obj["first_esm"]
                    try:
                        new_ecocase.first_esm = ESM.objects.get(label=data_dict['first_esm'])
                    except Exception as e:
                        print("error:", e)
                if "second_esm" in obj:
                    data_dict["second_esm"] = obj["second_esm"]
                    try: 
                        new_ecocase.second_esm = ESM.objects.get(label=data_dict['second_esm'])
                    except Exception as e:
                        print("error:", e)
                
                # for associated_esm in data_dict['associated_esms'].split(', '):
                #     try:
                #         new_ecocase.associated_esms.add(ESM.objects.get(label=associated_esm))
                #     except Exception as e:
                #         print('associated_esm', associated_esm)
                #         print('error associated esms', e)
                new_ecocase.save()

                print('Ecocase saveeeedddddd: ', new_ecocase)

                for image_url in data_dict["image_urls"]:
                    # print(dirspot)
                    # print('uuuuuuuuurrrrrrllllll: ' + image_url)
                    try:
                        local_image_path = 'ecocases/static/ecocases/images/' + image_url
                        open_file = open(local_image_path, "rb")
                        image_file = File(open_file)
                        m = EcocaseImage(prefix='prefix', ecocase=new_ecocase)
                        m.image.save(image_url.split(
                            '/')[-1], image_file, save=True)
                        m.save()
                    except Exception as e:
                        print("error:", e)
            except Exception as e:
                print('error: ', e)
                pass

    except Exception as e:
        logging.getLogger("error_logger").error(
            "Unable to upload file. " + repr(e))
        messages.error(request, "Unable to upload file. " + repr(e))

    return HttpResponseRedirect(reverse("ecocases:index"))