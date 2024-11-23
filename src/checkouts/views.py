import helpers.billing
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from subscriptions.models import SubscriptionPrice

from django.conf import settings


BASE_URL = settings.BASE_URL 

# Create your views here.



def product_price_redirect_view(request, price_id=None, *args, **kwargs):
    request.session['checkout_subscription_price_id'] = price_id
    return redirect("stripe-checkout-start")

@login_required
def checkout_redirect_view(request):
    checkout_subscription_price_id = request.session.get("checkout_subscription_price_id")
    try:
        obj = SubscriptionPrice.objects.get(id=checkout_subscription_price_id)  
    except:
        obj = None 
    if checkout_subscription_price_id is None or obj is None:
        return redirect("/pricing")
    customer_stripe_id = request.user.customer.stripe_id
    success_url_base = BASE_URL
    success_url_path = reverse("stripe-checkout-end")
    pricing_url_path = reverse("price")
    success_url = f"{success_url_base}{success_url_path}"
    return_url = f"{success_url_base}{pricing_url_path}"
    price_stripe_id = obj.stripe_id
    url = helpers.billing.start_checkout_session(
        customer_stripe_id,
        success_url=success_url,
        return_url=return_url,
        price_stripe_id=price_stripe_id,
        raw=False,
    )
    return redirect(url)

def checkout_finalize_view(request):
    return      