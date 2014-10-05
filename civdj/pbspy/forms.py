from django.forms import ModelForm
from pbspy.models import Game


class GameForm(ModelForm):
    class Meta:
        model = Game
        fields = ['name', 'description', 'hostname', 'port',
                  'manage_port', 'pb_remote_password', 'url']