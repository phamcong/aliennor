from django.http import JsonResponse
from django.db.models import Avg, Count, Func
from django.shortcuts import render
from django.views.generic.edit import FormView
from rest_framework import viewsets

from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse

from ..forms import EcocaseForm
from ..models import Ecocase, EcocaseRating, ESM, Ecocase2ESM, Category, EcocaseComment, EcocaseImage, Level, ESMEvaluation, Question, NonESMEvaluation
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

def submit_esmevaluations(request, ecocase_id, username):
    print("at ecocase views: submit esmevaluations")
    if request.method == 'POST':
        post_data = json.loads(request.body)
        print('submit_esmevaluations - post_data', post_data)
        submit_esmevaluations = post_data['esmevaluations']
        nonESM = post_data['nonESM']

        for submit_esmevaluation in submit_esmevaluations:
            esmevaluation = ESMEvaluation.objects.get(id=submit_esmevaluation['id'])
            esmevaluation.answer = submit_esmevaluation['answer']
            esmevaluation.is_first_esm = submit_esmevaluation['isFirstESM']
            esmevaluation.is_second_esm = submit_esmevaluation['isSecondESM']
            esmevaluation.save()
        
        ecocase = Ecocase.objects.get(id=ecocase_id)
        user = User.objects.get(username=username)

        
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
            
        return JsonResponse({
            'status': 'success'
        })
    else:
        pass