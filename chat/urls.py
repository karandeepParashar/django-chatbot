from django.urls import path
from . import views
urlpatterns = [
    # New URLs
    # Basic implementation
    # URL form "/api/users/1"
    path('api/users/<int:pk>', views.user_list, name='user-detail'),      # GET request for user with id
    path('api/users/', views.user_list, name='user-list'),    # POST for new user and GET for all users list
    # Image GET and POST
    path('api/image', views.image_list, name='image_details'),
    
    # GAME
        #New Game
    path('api/game/new/<int:player>', views.game_list, name='create_game'),
        #Get All Game info
    path('api/game/<int:player>', views.game_details, name='game_details_all'),
    path('api/game/<int:gId>/<int:player>', views.game_details, name='game_details'),
        # Round Info
    path('api/rounds/<int:gId>', views.round_list, name='round_list'),
        #Add selected Images
    path('api/game/round/<int:rId>',views.round_selection, name='round_selection'),
    
    #MESSAGES
    #GET
    path('api/messages/<int:gId>/<int:round_num>', views.message_list, name='messages_all'),
    #POST
    path('api/messages', views.message_list, name='message_details'),

    #EVALUATION
    #GET
    path('api/evaluate/<int:gId>',views.evaluate_game, name='evaluate_game'),
    
]

'''
    # URL for begining the game api/game/
    path('api/game/', views.game_list, name='create_game'),
    # Get the whole game data
    path('api/game/<int:gameId>/', views.game_list, name='game_details'),
    # Processing a message for intent and everything
    path('api/message/<int:gameId>/<int:round>/<int:sender>/<int:receiver>/', views.message_list, name='message-process'),
    # Get all messages
    path('api/message/<int:gameId>/<int:round>/<int:sender>/<int:receiver>/', views.message_list, name='message-details'),

    # URL form : "/api/messages/1/2"
    path('api/messages/<int:sender>/<int:receiver>/<int:gameId>/<int:round>', views.message_list, name='message-detail'),  # For GET request.
    # URL form : "/api/messages/"
    #path('api/messages/<int:sender>/<int:receiver>/<int:gameId>/<int:round>', views.message_list, name='message-list'),   # For POST
    '''