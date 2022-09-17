from django.urls import path

from . import views

urlpatterns = [
    path('', views.loginRequest, name='login'),
    path('commandList', views.commandList, name='commandList'),
    path('device_list', views.deviceList, name='deviceList'),
    path('commands', views.commands, name='commands'),
    path('logout', views.logoutRequest, name='logout'),
    path('sshCommand', views.sshCommands, name='sshCommand'),
    path('editDevice/<int:pk>', views.editDevice, name='editDevice'),
    path('deleteDevice/<int:pk>', views.deleteDevice, name='deleteDevice'),
    path('editCommand/<int:pk>', views.editCommand, name='editCommand'),
    path('deleteCommand/<int:pk>', views.deleteCommand, name='deleteCommand'),
]
