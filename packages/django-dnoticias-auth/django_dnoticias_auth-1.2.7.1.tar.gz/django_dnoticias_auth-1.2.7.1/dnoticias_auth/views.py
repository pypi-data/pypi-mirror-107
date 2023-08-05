from django.shortcuts import render
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.clickjacking import xframe_options_exempt
from mozilla_django_oidc.views import OIDCLogoutView

class SilentCheckSSOView(View):
    @method_decorator(xframe_options_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
        
    def get(self, request, *args, **kwargs):
        return render(request, "authentication/silent-check-sso.html", locals())

class DnoticiasOIDCLogoutView(OIDCLogoutView):
    http_method_names = ['get', 'post']

    @property
    def redirect_url(self):
        return self.request.POST.get("next", self.get_settings('LOGOUT_REDIRECT_URL', '/'))