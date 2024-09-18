from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView

from members.forms.member import MemberForm


class InfoPage(TemplateView):
    template_name = 'info/who.html'

class JoinInfoPage(TemplateView):
    template_name = 'info/join.html'

class JoinForm(CreateView):
    template_name = 'members/create.html'
    form_class = MemberForm
    success_url = reverse_lazy('members:success')

class JoinFormSuccess(TemplateView):
    template_name = 'members/success.html'

class BotInfo(TemplateView):
    template_name = 'info/bot.html'

