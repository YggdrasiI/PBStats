# -*- coding: utf-8 -*-

from django.forms import ModelForm, Form
from django import forms
from pbspy.models import Game
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _


class ModelCommaSeparatedChoiceField(forms.ModelMultipleChoiceField):
    widget = forms.TextInput
    MAX_LIST_SIZE = 20
    def clean(self, value):
        if value is not None:
            users = []
            for item in value.split(",")[:self.MAX_LIST_SIZE]:
                try:
                    user = User.objects.get(username=item.strip())
                    users.append(user)
                except User.DoesNotExist:
                    pass
            value = [ user.pk for user in users]
            return value
        else:
            return []


class GameForm(ModelForm):
    password_dummy = "*****"
    adminsAsStr = ModelCommaSeparatedChoiceField(
        required = False,
        queryset = User.objects.filter().all(),
        label =  _("Admins"),
        help_text = _("Comma separated list. You can not remove yourself."),
    )
    class Meta:
        model = Game
        fields = ['name', 'description', 'hostname', 'port',
                  'manage_port', 'pb_remote_password', 'url',
                  'is_private', 'is_dynamic_ip', 'adminsAsStr',
                  ]
        labels = {
            'url' : _("Website"),
            'is_dynamic_ip': _("Dynamic hostname"),
        }
        help_texts = {
            'is_private' : _("Exclude game from public list."),
            'is_dynamic_ip': _('Update stored hostname/ip if Pitboss server'
                               + 'sends an update with a new address.'),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(GameForm, self).__init__(*args, **kwargs)

        # Fill list of admins into adminsAsStr field if game already exists.
        a = self.fields["adminsAsStr"]
        if self.instance.id != None:
            a.initial =  ",".join([str(u) for u in self.instance.admins.all()])
        else:
            a.initial = str(self.user.username)

    def save(self):
        # Todo
        #if self.fields['pb_remote_password']  == self.password_dummy:
        #    self.fields['pb_remote_password'] = game.pb_remote_password

        if self.instance.id != None and self.user != None:
            adminsNew = self.cleaned_data.get('adminsAsStr', [])
            game = self.instance
            user = self.user
            if game.can_manage(user) and not user.pk in adminsNew:
                self.fields['adminsAsStr'].initial += ","+str(user.username)
                adminsNew.append(user.pk)

            if len(adminsNew) > 0:
                game.admins.clear()
                for a in adminsNew:
                    game.admins.add(a)

        return super(GameForm, self).save()


class GameManagementCurrentTimerForm(Form):
    hours = forms.IntegerField(label=_('Remaining hours'), min_value=0, max_value=9999)
    minutes = forms.IntegerField(label=_('Remaining minutes'), min_value=0, max_value=9999)


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
        self.fields['log_turn_max'] = forms.IntegerField(label=_('Maximal turn'),
                min_value=0, max_value=9999)
        self.fields['log_turn_min'] = forms.IntegerField(label=_('Minimal turn'),
                min_value=0, max_value=9999)
        self.fields['log_player_ids'] = forms.MultipleChoiceField(
          label=_('Players'),
          required=False,
          #widget=forms.CheckboxSelectMultiple()
          )

class GameLogSaveFilterForm(forms.Form):
    MAX_SAVEABLE_NUMBER = 20
    def __init__(self, *args, **kwargs):
        super(GameLogSaveFilterForm, self).__init__(*args, **kwargs)
        self.fields['log_filter_name'] = forms.CharField(label=_('Filter name'),
                                                         required=False,
                                                         min_length=0, max_length=50)

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
