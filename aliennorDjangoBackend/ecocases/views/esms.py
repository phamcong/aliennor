from django.http import JsonResponse
from django.db.models import Avg, Count, Func
from django.shortcuts import render
from django.views.generic.edit import FormView
from rest_framework import viewsets

from django.urls import reverse_lazy

from ..forms import EcocaseForm
from ..models import Ecocase, EcocaseRating, ESM, ESMEvaluation
from django.contrib.auth.models import User
from ..serializers import UserSerializer, EcocaseSerializer
from ..mixins import FormUserNeededMixin, UserOwnerMixin

import json
from ecocases.utils import get_token_data

from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.core import serializers

from django.db.models import Q

def get_esms(request):
    print("at get_esms view: get esms");
    if request.method != 'GET':
        pass
    
    # get esms
    esms = ESM.objects.all()
    esms_array = []
    for esm in esms:
        esms_array.append(model_to_dict(esm))
    # esms = {}
    # for esm in list(all_esms):
    #     esms[esm.get('id')] = esm

    return JsonResponse({
        'status': 'success',
        'data': {
            'esms': esms_array
        }
    })

def get_ecocases_by_esm(request, esm_id):
    esm = ESM.objects.get(id=esm_id)
    ecocases = Ecocase.objects.all()
    ecocases_array = []
    for ecocase in ecocases:
        if (ecocase.first_esm == esm) or (ecocase.second_esm == esm):
            ecocase_dict = model_to_dict(ecocase)
            ecocase_dict['levels'] = [item['title'] for item in ecocase.levels.values()]
            ecocase_dict['categories'] = [item['title'] for item in ecocase.categories.values()]
            if (ecocase_dict['first_esm'] != None):
                ecocase_dict['first_esm'] = model_to_dict(ecocase.first_esm)
            if (ecocase_dict['second_esm'] != None):
                ecocase_dict['second_esm'] = model_to_dict(ecocase.second_esm)   
            ecocase_dict['is_first_esm'] = True if ecocase.first_esm == esm else False
            ecocase_dict['image_urls'] = ecocase.image_urls()
            ecocases_array.append(ecocase_dict)
        # elif (ecocase.first_esm == None) or (ecocase.first_esm == None):
        #     associated_esms_by_evals = ecocase.associated_esms_by_evals()
        #     if (associated_esms_by_evals['first_esm'] != '') and (associated_esms_by_evals['second_esm'] != ''):
        #         ecocase_dict = model_to_dict(ecocase)
        #         ecocase_dict['levels'] = [item['title'] for item in ecocase.levels.values()]
        #         ecocase_dict['categories'] = [item['title'] for item in ecocase.categories.values()]
        #         ecocase_dict['first_esm'] = model_to_dict(associated_esms_by_evals['first_esm'])
        #         ecocase_dict['second_esm'] = model_to_dict(associated_esms_by_evals['second_esm'])
        #         ecocase_dict['image_urls'] = ecocase.image_urls()
        #         ecocases_array.append(ecocase_dict)

    # esmevaluations = ESMEvaluation.objects.filter(
    #     Q(ecocase2esm__esm=esm),
    #     Q(is_first_esm__exact=True) |  Q(is_second_esm=True)
    # )

    # esms_array = []
    # for esmevaluation in esmevaluations:
    #     ecocase = esmevaluation.ecocase2esm.ecocase
    #     ecocase_dict = model_to_dict(ecocase)
    #     ecocase_dict['levels'] = [item['title'] for item in ecocase.levels.values()]
    #     ecocase_dict['categories'] = [item['title'] for item in ecocase.categories.values()]
    #     if (ecocase.first_esm != None) and (ecocase.second_esm != None):
    #             ecocase_dict['first_esm'] = model_to_dict(ecocase.first_esm)
    #             ecocase_dict['second_esm'] = model_to_dict(ecocase.second_esm)
    #     else:
    #         associated_esms_by_evals = ecocase.associated_esms_by_evals()
    #         ecocase_dict['first_esm'] = model_to_dict(associated_esms_by_evals['first_esm'])
    #         ecocase_dict['second_esm'] = model_to_dict(associated_esms_by_evals['second_esm'])
    #     ecocase_dict['image_urls'] = ecocase.image_urls()
    #     esms_array.append(ecocase_dict)

    return JsonResponse({
        'status': 'success',
        'data': {
            'ecocases': ecocases_array
        }
    })

def get_esm_by_id(request, esm_id):
    esm = ESM.objects.get(id=esm_id);

    return JsonResponse({
        'status': 'success',
        'data': {
            'esm': model_to_dict(esm)
        }
    })