from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.models import Group


@login_required
def subscribe(request):
    user = request.user
    subs = Group.objects.get(name='subscribers')
    if not request.user.groups.filter(name='subscribers').exists():
        subs.user_set.add(user)

    return redirect('/')
