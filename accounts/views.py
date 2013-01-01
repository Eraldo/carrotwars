# Create your views here.
from django.views.generic import RedirectView
from django.contrib import messages
from django.core.urlresolvers import reverse

class LoginErrorView(RedirectView):
    def get_redirect_url(self):        
        messages.add_message(self.request, messages.ERROR, 'Login failed.')
        return reverse('login')
