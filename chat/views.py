from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User                                # Django Build in User Model
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from chat import serializers
from chat.NLP.bot import Bot
from rest_framework.parsers import JSONParser
from chat.models import Game, Image, Message, Round                                                   # Our Message model
from chat.serializers import MessageSerializer, UserSerializer,GameSerializer,ImageSerializer, RoundSerializer # Our Serializer Classes
import random
from collections import namedtuple

# Users View
@csrf_exempt                                                              # Decorator to make the view csrf excempt.
def user_list(request, pk=None):
    """
    List all required messages, or create a new message.
    """
    if request.method == 'GET':
        if pk:                                                                      # If PrimaryKey (id) of the user is specified in the url
            users = User.objects.filter(id=pk)              # Select only that particular user
        else:
            users = User.objects.all()                             # Else get all user list
        serializer = UserSerializer(users, many=True, context={'request': request}) 
        return JsonResponse(serializer.data, safe=False)               # Return serialized data
    elif request.method == 'POST':
        data = JSONParser().parse(request)           # On POST, parse the request object to obtain the data in json
        serializer = UserSerializer(data=data)        # Seraialize the data
        if serializer.is_valid():
            serializer.save()                                            # Save it if valid
            return JsonResponse(serializer.data, status=201)     # Return back the data on success
        return JsonResponse(serializer.errors, status=400)     # Return back the errors  if not valid
# Game View
@csrf_exempt
def game_list(request, player = None):
    if request.method == 'GET':
        #---- Game Table Code Starts -----
        game = Game(user_id = player)
        game.save()
        #---- Game Table Code Ends -----
        #---- Round Table Code Starts -----
        for i in range(0, 6):
            round = Round(game_id = game.gameId, round = i + 1)
            round.save()
            images = Image.objects.values_list('imageId', flat=True)
            n = random.randint(6,12)
            Images = random.sample(list(images), n)
            user_images = Images[0:6]
            bot_images = Images[(n-6):]
            common_images = Images[(n-6):6]
            round.userImages.add(*user_images)
            round.botImages.add(*bot_images)
            round.commonImages.add(*common_images)
            round.save()
        #---- Round Table Code Ends -----
        game = Game.objects.get(gameId = game.gameId)
        rounds = Round.objects.filter(game_id = game.gameId)
        serializer = GameSerializer(game, many = False, context={'request': request})
        roundSerializer = RoundSerializer(rounds, many = True, context={'request': request})
        data = {}
        data.update({'gameInfo': serializer.data})
        data.update({'roundInfo': roundSerializer.data})
        return JsonResponse(data, safe= False)

@csrf_exempt
def game_details(request, player, gId = None):
    if request.method == 'GET':
        if gId == None:
            games = Game.objects.filter(user_id = player)
            serializer = GameSerializer(games, many = True, context = {'request': request})
            data = serializer.data
        else:
            game = Game.objects.get(gameId = gId)
            rounds = Round.objects.filter(game_id = game.gameId)
            serializer = GameSerializer(game, many = False, context={'request': request})
            roundSerializer = RoundSerializer(rounds, many = True, context={'request': request})
            data = {}
            data.update({'gameInfo': serializer.data})
            data.update({'roundInfo': roundSerializer.data})
        return JsonResponse(data, safe= False)

@csrf_exempt
def round_list(request, gId):
    if request.method == 'GET':
        rounds = Round.objects.filter(game_id = gId)
        serializer = RoundSerializer(rounds, many = True, context={'request': request})
        return JsonResponse(serializer.data, safe= False)

@csrf_exempt
def round_selection(request, rId):
    if request.method == 'PUT':
        data = JSONParser().parse(request)
        round = Round.objects.get(id = rId)
        for selection in data['selectedImages']:
            round.userSelectedImages.add(selection['imageId'])
        round.save()
        serializer = RoundSerializer([round], many = True, context={'request': request})
        return JsonResponse(serializer.data, safe= False)


# Image View
@csrf_exempt
def image_list(request):
    if request.method == 'GET':
        images = Image.objects.all()
        serializer = ImageSerializer(images, many = True, context={'request': request})
        return JsonResponse(serializer.data, safe= False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        #print(request)
        serializer = ImageSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        else:
            return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def message_list(request, gId =None, round_num =None, sender=None, receiver=None):
    if request.method == 'GET':
        #game = Game.objects.get(gameId = gId)
        round = Round.objects.filter(game_id = gId, round = round_num)
        messages = Message.objects.filter(roundId_id = round.values_list()[0][0])
        serializer = MessageSerializer(messages, many = True,context={'request': request})
        return JsonResponse(serializer.data, safe= False,status=201)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            msg = serializer.data['message']
            reply = Bot.processText(msg)
            reply = Message(sender_id = serializer.data['receiver'], receiver_id = serializer.data['sender'], roundId_id = data['roundId'], message = reply)
            reply.save()
            serializer = MessageSerializer(reply, context={'request': request})
            return JsonResponse(serializer.data, safe = False ,status=201)
        return JsonResponse(serializer.errors, status=400)