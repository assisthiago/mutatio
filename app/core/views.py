from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from app.core.form import SignInForm


def _login(request, form):
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
        if not form.is_valid():
            return render(request, "sign-in.html", {"form": form})

        if not _login(request, form):
            messages.error(request, "Verifique seus dados")
            return render(request, "sign-in.html", {"form": form})

        return redirect("home")

    return render(request, "sign-in.html", {"form": SignInForm()})
