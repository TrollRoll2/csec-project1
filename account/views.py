from django.shortcuts import render, redirect
from django.views import View, generic
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

# import logging

from polls.models import Question

# logger = logging.getLogger(__name__)

class ProfileView(LoginRequiredMixin, generic.ListView):
    template_name = "account/profile.html"
    context_object_name = "latest_poll_list"

    def get_queryset(self):
        return Question.objects.filter(author=self.request.user).order_by("-pub_date")

class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("account:profile")
        return render(request, "account/login.html")

    def post(self, request):
        if request.user.is_authenticated:
            return redirect("account:profile")

        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is None:
#            logger.warning(f"Failed login attempt for {username}")
            return render(request, "account/login.html", {
                "error_message": "Username or password invalid",
            })

#        logger.info(f"User {username} logged in")
        login(request, user)
        return redirect("account:profile")
    
# A09:2025, Security Logging and Alerting Failures is present here, as no logging is done what-so-ever. Uncommenting the logger import
# and the loggers provide logging for successful and unsuccessful login attempts, which could be stored in a database for admins to see.
# Further logging and functionality could and should be derived from the logger, such as lockout for too many failed login attempts.

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("account:login")

class SignupView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("account:profile")
        return render(request, "account/signup.html")

    def post(self, request):
        if request.user.is_authenticated:
            return redirect("account:profile")

        username = request.POST["username"]
        password = request.POST["password"]

        if not username or not password:
            return render(request, "account/signup.html", {
                "error_message": "Username and password are both required.",
            })

#        if User.objects.filter(username=username).exists():
#            return render(request, "account/signup.html", {
#                "error_message": "Username already exists.",
#            })

# A10:2025, Instead of telling the user that the username is already taken and allowing them to try with another name, the whole app breaks.
# The above commented code would give the user an error message telling them that the name is already taken.

#        try:
#            validate_password(password)
#        except:
#            return render(request, "account/signup.html", {
#                "error_message": "The password must contain at least 8 characters and not be too common"
#            })

# A07:2025, The user is allowed to choose any password as long as it is not empty. Using the above commented out check forces
# the user to choose one that adheres to Django's default validation, although more checks could be added.

        User.objects.create_user(username=username, password=password)

        return redirect("account:login")