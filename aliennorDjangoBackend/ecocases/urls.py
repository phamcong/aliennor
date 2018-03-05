from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'ecocases'

ecocases_routes = [
    url(r'^get-all$', views.ecocases_summary, name='ecocases summary'),
    url(r'^$', views.get_all_ecocases, name='get all ecocases'),
    url(r'^ecocase/index$', views.indexView, name='index'),
    url(r'^ecocase/new$', views.EcocaseCreateView.as_view(), name='new ecocase'),
    url(r'^ecocase/post$', views.post_ecocase, name='post ecocase'),
    url(r'^upload/json/$', views.upload_json, name='upload_json'),
    url(r'^ecocase/(?P<ecocase_id>[a-zA-Z0-9]+)/$', views.ecocase_details, name='ecocase details'),
    url(r'^ecocase/(?P<ecocase_id>[a-zA-Z0-9]+)/rating/$', views.getRating, name='get ecocase rating'),
    url(r'^ecocase/(?P<ecocase_id>[0-9]+)/comments/$', views.get_comments, name='get ecocase comments'),
    # url(r'^ecocase/(?P<ecocase_id>[0-9]+)/esms/$', views.get_ecocase_esm_by_user, name='get ecocase esms by user'),
    url(r'^ecocase/(?P<ecocase_id>[0-9]+)/esms/(?P<username>[a-zA-Z0-9]+)/submit/$', views.submit_esmevaluations, name='sumbit esmevaluations'),
    url(r'^ecocase/(?P<ecocase_id>[0-9]+)/esms/summary/$', views.get_associated_esms, name='get associated esms summary'),
    url(r'^ecocase/tagged/(?P<ecocase_id>[0-9]+)/esms-weights/$', views.get_esms_weights_tagged_ecocase, name='get esms weight of tagged ecocase'),
    url(r'^filters$', views.get_filter_criteria, name='get filter criteria'),
    url(r'^search/$', views.get_ecocases, name='filter ecocases'),
    url(r'^untagged/search/$', views.get_untagged_ecocases, name='get untagged ecocases'),
]

ecocase_rate_routes = [
    url(r'^rate$', views.ecocase_rate, name='ecocase rate'),
]

ecocase_comment_routes = [
    url(r'^comments$', views.EcocaseCommentViewSet, name='get all comments'),
    url(r'^comment$', views.comment, name='comment'),
    url(r'^comment/(?P<id>[0-9]+)/$', views.update_comment, name='update comment')
]

urlpatterns = ecocases_routes + ecocase_rate_routes + ecocase_comment_routes