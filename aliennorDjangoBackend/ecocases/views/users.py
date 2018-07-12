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
from django.contrib.auth.models import Group, User
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
  
from .shared import *

def allocation_cas_users(request):
    print('At users: allocation cas users')
    if request.method != 'POST':
        pass
    post_data = json.loads(request.body)
    # get users to create
    user_infos = post_data['usersInfos']
    user_ids = []
    for item in user_infos:
        print(item)
        first_name = item['name'].split(' ')[0]
        last_name = item['name'].split(' ')[1]
        username = first_name + '.' + last_name
        username = username.lower()
        email, password = item['email'], item['password']
        user, created_ = User.objects.get_or_create(username=username)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.set_password(password)
        user.save()
        user_ids.append(user.id)
        g, created = Group.objects.get_or_create(name=item['group'])
        g.user_set.add(user)
        # yield user
    print(user_ids)

    ecocases = Ecocase.objects.all()
    ecocase_ids = [ecocase.id for ecocase in ecocases]
    print(ecocase_ids)

    _, userids_ecocaseid_dict = allocate_random(ecocase_ids, user_ids, m=15)

    for (ecocase_id, user_ids) in userids_ecocaseid_dict.items():
        ecocase = Ecocase.objects.get(id=ecocase_id)
        for user_id in user_ids:
            user = User.objects.get(id=user_id)
            ecocase.evaluate_by_users.add(user)
    
    return JsonResponse({
        'status': 'success'
    })

def allocate_random(papers, reviewers, m):
        '''
        Allocation X papers to Y reviewers. Each reviewer has to review m papers.
        Each paper is so reviewed by (y*m)/X reviewers.

        Arguments:
        papers -- python list, list of papers'ID to review,
        reviewers -- python list, list of reviewers' IDs,
        m -- interger, number of papers reviewed by a reviewer

        Returns:
        allocation -- two python dict, the allocation result.
                        papers_reviewer_dict -- (key, value) = (reviewerID, [allocated papers' IDs])
                        reviewers_paper_dict -- (key, value) = (paperID, [allocated reviewers' IDs])
        '''
        import random
        random.seed(1)

        n_papers, n_reviewers = len(papers), len(reviewers)
        n = int((n_reviewers * m) / n_papers)
        print('n: ', n)
        index_array = list(range(n_papers))  # create a list containing indexes of papers list

        papers_reviewer_dict = {}
        reviewers_paper_dict = {}

        for reviewer in reviewers:
            papers_reviewer_dict[reviewer] = []
        for paper in papers:
            reviewers_paper_dict[paper] = []

        papers_remain = papers[:]
        papers_all_taken = []

        for index, reviewer in enumerate(reviewers):
            papers_remain_copy_lens = [n - len(v) for _, v in reviewers_paper_dict.items()]

            while len(papers_remain) < m:
                pp_less_taken = min(reviewers_paper_dict, key=lambda k: len(reviewers_paper_dict[k]))

                # get all reviewers having m allocated papers. Reallocate the less allocated paper to the first one.
                sw_reviewer, sw_papers = \
                [(reviewer, papers) for reviewer, papers in papers_reviewer_dict.items() if pp_less_taken not in papers][0]
                pp_taken_to_sw = list(set(sw_papers) - set(papers_remain))[0]
                papers_reviewer_dict[sw_reviewer].append(pp_less_taken)
                papers_reviewer_dict[sw_reviewer].remove(pp_taken_to_sw)
                papers_remain.append(pp_taken_to_sw)
                reviewers_paper_dict[pp_taken_to_sw].remove(sw_reviewer)
                reviewers_paper_dict[pp_less_taken].append(sw_reviewer)

            papers_remain_copy = papers_remain[:]
            for i in range(m):
                if len(papers_remain_copy) != 0:
                    paper_ = random.choice(papers_remain_copy)
                    papers_reviewer_dict[reviewer].append(paper_)
                    reviewers_paper_dict[paper_].append(reviewer)
                    papers_remain_copy.remove(paper_)

                    if len(reviewers_paper_dict[paper_]) == n:
                        papers_remain.remove(paper_)
                        papers_all_taken.append(paper_)
        return papers_reviewer_dict, reviewers_paper_dict