from django.contrib import admin

from .models import Game,Move



# Register your models here.

#admin.site.register(Game)  # to register the model with the admin site

@admin.register(Game)  #register your modeladmin class with your admin and couples it with your model
class GameAdmin(admin.ModelAdmin):  # ModelAdmin class to customize your model class
    list_display = ('id', 'first_player', 'second_player', 'status')  #tells  the admin site 
    #which fields i want to see from the list display for my model
    list_editable = ('status',) #makes the status field editable(adds a dropdown) from the game list

admin.site.register(Move)


