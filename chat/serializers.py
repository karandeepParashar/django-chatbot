from django.contrib.auth.models import User
from django.db.models import fields
from rest_framework import serializers
from chat.models import Game, Image, Message, Round
# 
# User Serializer
class UserSerializer(serializers.ModelSerializer):
    """For Serializing User"""
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
# Game Serializer
class GameSerializer(serializers.ModelSerializer):
    #round = serializers.SlugRelatedField(many = True, slug_field = 'id', queryset=Round.objects.all())
    user = serializers.SlugRelatedField(many=False, slug_field = 'id', queryset=User.objects.all())
    class Meta:
        model = Game
        fields = ['gameId', 'user']
# Image Serializer
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['imageId', 'imagePath']
# Round Serializer
class RoundSerializer(serializers.ModelSerializer):
    userImages = ImageSerializer(many = True)
    botImages = ImageSerializer(many = True)
    commonImages = ImageSerializer(many = True)
    userSelectedImages = ImageSerializer(many = True)
    botSelectedImages = ImageSerializer(many = True)
    #message = serializers.SlugRelatedField(many = True, slug_field = 'id', queryset=Message.objects.all())
    class Meta:
        model = Round
        fields = ['id', 'round', 'userImages', 'botImages', 'commonImages', 'userSelectedImages', 'botSelectedImages']

# Message Serializer
class MessageSerializer(serializers.ModelSerializer):
    """For Serializing Message"""
    #sender = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all())
    #receiver = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all())
    class Meta:
        model = Message
        fields = ['id','sender','roundId' ,'receiver','message','timestamp']