from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.shortcuts import resolve_url as r

from app.core.forms import SignInForm


def _login(request, form):
    form.is_valid()

    user = authenticate(
        request,
        username=form.cleaned_data["username"],
        password=form.cleaned_data["password"],
    )

    if not user:
        return

    login(request, user)

    # Expiry is set to 0 seconds.
    # So it will automatically close the session after the browser is closed.
    request.session.set_expiry(0)

    return user


# Views
def signin(request):
    if request.method == "POST":
        form = SignInForm(request.POST)
        if not _login(request, form):
            messages.error(request, "Verifique seus dados.")
            return render(request, "sign-in.html", {"form": form})

        return redirect("report")

    return render(request, "sign-in.html", {"form": SignInForm()})


def signout(request):
    logout(request)
    return HttpResponseRedirect(r("sign-in"))


@login_required
def report(request):
    return render(request, "report.html")
