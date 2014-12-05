# -*- coding: utf-8 -*-

from django.forms import ModelForm, Form
from django import forms
from pbspy.models import Game
from django.utils.translation import ugettext as _

class GameForm(ModelForm):
    class Meta:
        model = Game
        fields = ['name', 'description', 'hostname', 'port',
                  'manage_port', 'pb_remote_password', 'url', 'is_private']


class GameManagementTimerForm(Form):
    timer = forms.IntegerField(label=_('New timer (h)'), min_value=0, max_value=9999)


class GameManagementChatForm(Form):
    message = forms.CharField(label=_('Text message'))


class GameManagementMotDForm(Form):
    message = forms.CharField(label=_('Text message'))


class GameManagementShortNamesForm(Form):
    iShortNameLen = forms.IntegerField(label=_('New max. length of leader name'),
            min_value=0, max_value=9999, initial=2 )
    iShortDescLen = forms.IntegerField(label=_('New max. length of civ description'),
            min_value=0, max_value=9999, initial=3 )


class GameManagementSaveForm(Form):
    filename = forms.CharField(label=_('Filename (without extension)'), max_length=20)


class GameManagementLoadForm(Form):
    def __init__(self, savegames, *args, **kwargs):
        super(GameManagementLoadForm, self).__init__(*args, **kwargs)
        self.fields['filename'] = forms.ChoiceField(choices=savegames, label=_('Savegame'))


class GameManagementSetPlayerPasswordForm(Form):
    def __init__(self, players, *args, **kwargs):
        super(GameManagementSetPlayerPasswordForm, self).__init__(*args, **kwargs)
        self.fields['player'] = forms.ModelChoiceField(players, label=_('Player'))

    password = forms.CharField(label=_('New password'), min_length=1)

class GameLogTypesForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(GameLogTypesForm, self).__init__(*args, **kwargs)
        self.fields['log_type_filter'] = forms.MultipleChoiceField(
          label=_('Log entry filter'),
          required=False,
          widget=forms.CheckboxSelectMultiple()
          )
        self.fields['log_turn_max'] = forms.IntegerField(label=_('Maximal Round'),
                min_value=0, max_value=9999)
        self.fields['log_turn_min'] = forms.IntegerField(label=_('Minimal Round'),
                min_value=0, max_value=9999)
        self.fields['log_player_ids'] = forms.MultipleChoiceField(
          label=_('Players'),
          required=False,
          )

class GameManagementSetPlayerColorForm(Form):
    def __init__(self, players, num_colors, *args, **kwargs):
        super(GameManagementSetPlayerColorForm, self).__init__(*args, **kwargs)
        self.fields['player'] = forms.ModelChoiceField(players, label=_('Player'))
        self.fields['num_colors'] = forms.CharField(
            required=False,
            widget=forms.HiddenInput()
            )
        self.fields['num_colors'].initial = num_colors
        col_choices = []
        for col_id in range(num_colors):
            col_choices.append( (col_id,"Colorset "+str(col_id)) )
        self.fields['color'] = forms.ChoiceField(
                choices=col_choices,
                label=_('New color'),
                required=False
                )
