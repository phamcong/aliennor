from django.http import JsonResponse
import json

from ecocases.utils import get_token_data
from ..models import EcocaseRating, Ecocase, EcocaseComment


def ecocase_rate(request):

    # if POST, save or update rating
    if request.method == 'POST':
        body = json.loads(request.body)
        ecocase_id = body['id']
        rating = int(body['rating'])

        try:
            username = body['username']
        except KeyError:
            token = get_token_data(request)
            username = token['username']

        # get the ecocase object with id ecocase_id, or create it
        ecocase, created = Ecocase.objects.get_or_create(id=ecocase_id, defaults={'title': ''})
        # save or update rating
        try:
            r, created = EcocaseRating.objects.update_or_create(username=username, ecocase=m, defaults={'rating': rating})
        except Exception as e:
            print(e)
            return JsonResponse({
                'status': 'fail',
                'data': {
                    'message': 'Error while saving rating'
                }
            }, status=500)

        return JsonResponse({
            'status': 'success',
            'data': {
                'title': m.title,
                'rating': r.rating,
                'is_new': created
            }
        })
    elif request.method == 'DELETE':
        username = request.GET.get('u', '')
        ecocase_id = request.GET.get('m_id', '')

        # find ecocase object
        m = Ecocase.objects.filter(id=ecocase_id).first()
        r = EcocaseRating.objects.filter(ecocase=m, username=username)

        # delete rating
        try:
            r.delete()
        except:
            return JsonResponse({
                'status': 'fail',
                'data': {
                    'message': 'Error while deleting rating'
                }
            }, status=500)

        return JsonResponse({
            'status': 'success'
        })

def getRating(request, ecocase_id):
    if request.method != 'POST':
        pass

    body = json.loads(request.body)
    username = body['username']

    # get rating
    r = EcocaseRating.objects.filter(ecocase_id = ecocase_id, username = username).first()

    return JsonResponse({
        'result': 'success',
        'data': {
            'rating': r.rating if r else None
        }
    })