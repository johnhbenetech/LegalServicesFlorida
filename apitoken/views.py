from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.authtoken.models import Token


class TokenGetView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'apitoken/get.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        token = Token.objects.get_or_create(user=self.request.user)[0]
        context['token'] = token
        return self.render_to_response(context)