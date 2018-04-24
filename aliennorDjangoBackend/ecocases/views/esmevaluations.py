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

def submit_esmevaluations(request, ecocase_id, username):
    print("at ecocase views: submit esmevaluations")
    if request.method == 'POST':
        post_data = json.loads(request.body)
        print('submit_esmevaluations - post_data', post_data)
        submit_esmevaluations = post_data['esmevaluations']
        nonESM = post_data['nonESM']
        updated_environ_gain_eval = post_data['environGainEval']
        updated_eco_effect_potential_eval = post_data['ecoEffectPotentialEval']
        updated_ecoinnovation_status_eval = post_data['ecoinnovationStatusEval']

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
        environ_gain_evals = EnvironGainEval.objects.filter(
            Q(ecocase=ecocase),
            Q(user__username=username)
        )

        if len(environ_gain_evals) == 0:
            EnvironGainEval(ecocase=ecocase, user=user, environ_gain=updated_environ_gain_eval.environ_gain, comment=updated_environ_gain_eval.comment)
        else:
            environ_gain_evals[0].environ_gain = updated_environ_gain_eval.environ_gain
            environ_gain_evals[0].comment = updated_environ_gain_eval.comment

        # ----------------
        # update Eco Effect Potential Eval
        # ----------------
        try:
            eco_effect_potential_eval = EnvironGainEval.objects.get(
                Q(ecocase=ecocase),
                Q(user__username=username)
            )
            eco_effect_potential_eval.comment = eco_effect_potential_eval.comment
            for eep in eco_effect_potential_eval.eco_effect_potentials.all():
                for updated_eep in updated_eco_effect_potential_eval.eco_effect_potentials:
                    if eep.title == updated_eep.title:
                        eep.selected = updated_eep.selected
                        eep.save()
            eco_effect_potential_eval.save()
        except Exception as e:
            print(e)

        if len(environ_gain_evals) == 0:
            EnvironGainEval(ecocase=ecocase, user=user, environ_gain=updated_environ_gain_eval.environ_gain,
                            comment=updated_environ_gain_eval.comment)
        else:
            environ_gain_evals[0].environ_gain = updated_environ_gain_eval.environ_gain
            environ_gain_evals[0].comment = updated_environ_gain_eval.comment
            environ_gain_evals[0].save()

        # ----------------
        # update Ecoinnovation Status Eval
        # ----------------

        return JsonResponse({
            'status': 'success'
        })
    else:
        pass