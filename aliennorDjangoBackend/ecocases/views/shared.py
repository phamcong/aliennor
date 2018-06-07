from django.db.models import Avg, Count, Func
from django.shortcuts import render
from django.views.generic.edit import FormView
from rest_framework import viewsets

from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.urls import reverse

from ..forms import EcocaseForm
from ..models import *
from django.contrib.auth.models import User
from ..serializers import EcocaseSerializer, EcocaseCommentSerializer
from ..mixins import FormUserNeededMixin
from django.db.models import Q

import json
import logging
from django.contrib import messages
from ecocases.utils import get_token_data
from django.utils.timezone import now

from django.http import JsonResponse
from django.forms.models import model_to_dict

import boto3

from django.core.files.base import ContentFile
import base64

from ecocases.variables import *

def model_to_dict_ecocase(ecocase):
    ecocase_dict = model_to_dict(ecocase)
    ecocase_dict['levels'] = [item['title'] for item in ecocase.levels.values()]
    ecocase_dict['categories'] = [item['title'] for item in ecocase.categories.values()]
    ecocase_dict['evaluated_by_users'] = [item['username'] for item in ecocase.evaluated_by_users.values()]
    ecocase_dict['evaluate_by_users'] = [item['username'] for item in ecocase.evaluate_by_users.values()]
    if (ecocase.first_esm != None):
        ecocase_dict['first_esm'] = model_to_dict(ecocase.first_esm)
    if (ecocase.second_esm != None):
        ecocase_dict['second_esm'] = model_to_dict(ecocase.second_esm)
    ecocase_dict['image_urls'] = ecocase.image_urls()
    return ecocase_dict

def ecocases_set_to_array(ecocases):
    ecocases_array = []
    for ecocase in ecocases:
        ecocase_dict = model_to_dict_ecocase(ecocase)
        ecocases_array.append(ecocase_dict)
    return ecocases_array
    # print('ecocases: ', ecocases[next(iter(ecocases))])