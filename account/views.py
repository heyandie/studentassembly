from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist

from .models import User, VerificationToken, ResetPasswordToken


# Create your views here.
def ActivateAccountView(request, token):

    try:
        token = VerificationToken.objects.get(token=token)
        user = User.objects.get(id=token.user_id)
        if not user.is_verified:
            user.is_verified = True
            user.save()
            token.delete()
            return HttpResponseRedirect('/login?s=verified')
        else:
            return render(request, 'index.html', {'message':'Account has been already verified.'})
    except ObjectDoesNotExist:
        return render(request, 'index.html', {'message':'Invalid activation key'})


def ResetPasswordView(request):

    try:
        username = request.GET.get('username')
        user = User.objects.get(username='username')

        token = request.GET.get('token')
        reset_token = ResetPasswordToken.objects.get(token=token, user_id=user.id)

        return render(request, 'index.html')

    except ObjectDoesNotExist:
        return render(request, 'index.html', {'message':'Invalid reset password link'})
