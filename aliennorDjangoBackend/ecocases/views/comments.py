from django.http import JsonResponse
import math
import json

from ..models import Ecocase, EcocaseComment
from django.contrib.auth.models import User
from ecocases.utils import get_token_data

# @csrf_exempt # temporary decorator to remove csrf, just to test with postman
def comment(request):
    print("at comment views")
    if request.method == 'POST':
        post_data = json.loads(request.body)
        ecocase_id = post_data['ecocaseId']
        body = post_data['body']

        try:
            username = post_data['username']
        except KeyError:
            token = get_token_data(request)
            username = token['username']

        # get ecocase object
        ecocase, created = Ecocase.objects.get_or_create(id=ecocase_id, defaults={'title': ''})
        user = User.objects.get(username=username)
        # comment
        cmt = EcocaseComment(ecocase=ecocase, username=username, body=body)
        try:
            cmt.save()
        except:
            return JsonResponse({
                'status': 'fail',
                'data': {
                    'message': 'Error while saving comment'
                }
            }, status=500)

        return JsonResponse({
            'status': 'success',
            'data': {
                'id': cmt.id
            }
        })
    elif request.method == 'DELETE':
        id = request.GET.get('id', '')
        username = request.GET.get('u', '')

        try:
            cmt = EcocaseComment.objects.get(id=id, username=username)
        except EcocaseComment.DoesNotExist:
            return JsonResponse({
                'status': 'fail',
                'data': {
                    'message': 'This comment does not exist'
                }
            }, status=500)

        try:
            cmt.delete()
        except:
            return JsonResponse({
                'status': 'fail',
                'data': {
                    'message': 'Error while deleting comment'
                }
            }, status=500)

        return JsonResponse({
            'status': 'success'
        })

def get_comments(request, ecocase_id):
    if request.method != 'GET':
        pass

    items_per_page = 7
    page = int(request.GET.get('p', 1))

    cmt = EcocaseComment.objects.filter(ecocase_id=ecocase_id).order_by('-date')
    total_pages = math.ceil(cmt.count() / items_per_page)

    page = page-1 if page <=total_pages or total_pages==0 else total_pages-1
    limits = {
        'from': items_per_page * page,
        'to': (items_per_page * page) + items_per_page
    }

    comments = cmt[limits['from']: limits['to']].values()
    print('comments: ', list(comments))
    return JsonResponse({
        'status': 'success',
        'data': {
            'comments': list(comments),
            'total_pages': total_pages,
            'current_page': page+1,
            'items_per_page': items_per_page
        }
    })

# not currently used
def update_comment(request, id):
    if request.method != 'POST':
        pass

    username = request.POST.get('username', '')
    body = request.POST.get('body', '')

    try:
        cmt = EcocaseComment.objects.get(id=id, username=username)
    except EcocaseComment.DoesNotExist:
        return JsonResponse({
            'status': 'fail',
            'data': {
                'message': 'This comment does not exist'
            }
        }, status=500)

    cmt.body = body
    try:
        cmt.save()
    except:
        return JsonResponse({
            'status': 'fail',
            'data': {
                'message': 'Error while updating comment'
            }
        })

    return JsonResponse({
        'status': 'success'
    })