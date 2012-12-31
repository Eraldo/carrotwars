# Create your views here.
from django.views.generic import RedirectView
from django.contrib import messages

class LoginErrorView(RedirectView):
    def get_redirect_url(self, pk):        
        messages.add_message(self.request, messages.ERROR, 'Login failed.')
        return reverse('login')
