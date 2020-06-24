from allauth.account.views import *
from allauth.account.app_settings import *


class JointLoginSignupView(LoginView):
    form_class = LoginForm
    signup_form = SignupForm
    template_name = 'account/login.html'

    def __init__(self, **kwargs):
        super(JointLoginSignupView, self).__init__(*kwargs)

    def get_context_data(self, **kwargs):
        ret = super(JointLoginSignupView, self).get_context_data(**kwargs)

        ret['signup_form'] = get_form_class(app_settings.FORMS, 'signup', self.signup_form)
        return ret


login = JointLoginSignupView.as_view()
