from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist

from .models import User, VerificationToken


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
