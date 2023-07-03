from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import Coupon
from .forms import CouponApplyForm
from accounts.models import UserProfile


@require_POST
def coupon_apply(request):
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']

        try:
            coupon = Coupon.objects.get(code__iexact=code,
                                        valid_from__lte=now,
                                        valid_to__gte=now,
                                        active=True)
            request.session['coupon_id'] = coupon.id


            try:
                user_profile = UserProfile.objects.get(id=request.session['user_profile_id'])
            except:
                user_profile = None

            if user_profile:
                user_profile.cart_code = code
                user_profile.save()


        except Exception as e:
            print(e)
            request.session['coupon_id'] = None
    return redirect('cart:cart_detail')