from django.http import JsonResponse
from django.db.models import Avg, Count, Func
from django.shortcuts import render
from django.views.generic.edit import FormView
from rest_framework import viewsets

from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse

from ..forms import EcocaseForm
from ..models import *
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

def submit_ecocaseevaluation(request, ecocase_id, username):
    print("at ecocase views: submit esmevaluations")
    errors = []
    if request.method == 'POST':
        post_data = json.loads(request.body)
        print('submit_esmevaluations - post_data', post_data)
        submit_esmevaluations = post_data['esmevaluations']
        nonESM = post_data['nonESM']
        updated_environ_gain_eval = post_data['environGainEval']
        updated_eco_effect_potential_eval_list = post_data['ecoEffectPotentialEvals']
        updated_ecoinnovation_status_eval= post_data['ecoinnovationStatusEval']

        ecocase = Ecocase.objects.get(id=ecocase_id)
        user = User.objects.get(username=username)

        for submit_esmevaluation in submit_esmevaluations:
            esmevaluation = ESMEvaluation.objects.get(id=submit_esmevaluation['id'])
            esmevaluation.answer = submit_esmevaluation['answer']
            esmevaluation.is_first_esm = submit_esmevaluation['isFirstESM']
            esmevaluation.is_second_esm = submit_esmevaluation['isSecondESM']
            if submit_esmevaluation['isFirstESM'] and username == 'admin':
                esm = ESM.objects.get(id=submit_esmevaluation['esm']['id'])
                ecocase.first_esm = esm
                ecocase.save()
            if submit_esmevaluation['isSecondESM'] and username == 'admin':
                esm = ESM.objects.get(id=submit_esmevaluation['esm']['id'])
                ecocase.second_esm = esm
                ecocase.save()
            esmevaluation.save()

        nonESMEvaluations = NonESMEvaluation.objects.filter(
          Q(ecocase=ecocase),
          Q(user=user)
        )

        if len(nonESMEvaluations) > 0:
          nonESMEvaluation = nonESMEvaluations[0]
          if nonESM['isNonESM']: 
            nonESMEvaluation.argumentation = nonESM['argumentation']
            nonESMEvaluation.save()
          else:
            nonESMEvaluation.delete()
        elif nonESM['isNonESM']:
          new_nonESMEvaluation = NonESMEvaluation(
                          ecocase=ecocase,
                          user=user,
                          argumentation=nonESM['argumentation']
                      )
          new_nonESMEvaluation.save()

        if user not in ecocase.evaluated_by_users.all():
            ecocase.evaluated_by_users.add(user)
            ecocase.save()

        # ----------------
        # update Environ Gain Eval
        # ----------------
        try:
            environ_gain = EnvironmentalGain.objects.get(level=updated_environ_gain_eval['environGain'])
            environ_gain_eval = EnvironGainEval.objects.get(id=updated_environ_gain_eval['id'])
            environ_gain_eval.environ_gain = environ_gain
            environ_gain_eval.comment = updated_environ_gain_eval['comment']
            environ_gain_eval.save()

        except EnvironmentalGain.DoesNotExist:
            errors.append('Environmental Gain does not exist.')
            return JsonResponse({
                'status': 'fail',
                'errors': errors
            })

        # ----------------
        # update Ecoinnovation Status Eval
        # ----------------
        try:
            ecoinnovation_status = EcoInnovationStatus.objects.get(title=updated_ecoinnovation_status_eval['ecoinnovationStatus'])
            eco_status_eval = EcoinnovationStatusEval.objects.get(id=updated_ecoinnovation_status_eval['id'])
            eco_status_eval.ecoinnovation_status = ecoinnovation_status
            eco_status_eval.comment = updated_environ_gain_eval['comment']
            eco_status_eval.save()

        except EcoInnovationStatus.DoesNotExist:
            errors.append('Ecoinnovation Status does not exist.')
            return JsonResponse({
                'status': 'fail',
                'errors': errors
            })
        # ----------------
        # update Eco Effect Potential Eval
        # ----------------
        for updated_eep_eval in updated_eco_effect_potential_eval_list:
            try:
                eep_eval = EcoEffectPotentialEval.objects.get(id=updated_eep_eval['id'])
                eep_eval.selected = updated_eep_eval['selected']
                eep_eval.comment = updated_eep_eval['comment']
                eep_eval.save()
            except EcoEffectPotentialEval.DoesNotExist:
                errors.append('Not authenticated user. Please logged in to tag ecocase.')
                return JsonResponse({
                    'status': 'fail',
                    'errors': errors
                })

        return JsonResponse({
            'status': 'sumit evaluations successfully'
        })
    else:
        errors.append('Not GET request')
        return JsonResponse({
            'status': 'fail',
            'errors': errors
        })