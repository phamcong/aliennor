from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Ecocase, EcocaseComment

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
      
class EcocaseSerializer(serializers.ModelSerializer):
  # author = UserSerializer(
  #   default=serializers.CurrentUserDefault(), read_only=True)
  class Meta:
    model = Ecocase
    fields = ('id', 'user', 'title')
  # def to_representation(self, obj):
  #   return super(EcocaseSerializer, self).to_representation(obj)

class EcocaseCommentSerializer(serializers.ModelSerializer):
  class Meta:
    model = EcocaseComment
    fields = ('id', 'ecocase', 'username', 'body')