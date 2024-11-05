from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Application, Subscription, Category
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

@login_required(login_url='signup')
def subscription_page(request):
    # Get all categories to display in the filter menu
    categories = Category.objects.all()

    # Get the category ID from the request parameters (if any)
    category_id = request.GET.get('category')

    # Filter applications based on the selected category, if any
    if category_id:
        all_applications = Application.objects.filter(category_id=category_id)
    else:
        all_applications = Application.objects.all()

    # Get the subscriptions for the logged-in user
    user_subscriptions = Subscription.objects.filter(user=request.user)
    subscribed_applications = [sub.application for sub in user_subscriptions]

    context = {
        'all_applications': all_applications,
        'subscribed_applications': subscribed_applications,
        'categories': categories,           # Pass categories to the template
        'selected_category': category_id    # Pass the selected category ID
    }
    return render(request, 'subscriptions/subscription_page.html', context)

@login_required
def subscribe(request, app_id):
    application = get_object_or_404(Application, id=app_id)
    Subscription.objects.get_or_create(user=request.user, application=application)
    return redirect('subscription_page')

@login_required
def unsubscribe(request, app_id):
    subscription = Subscription.objects.filter(user=request.user, application_id=app_id)
    if subscription.exists():
        subscription.delete()
    return redirect('subscription_page')

def signup(request):
    if request.user.is_authenticated:
        # Redirect logged-in users directly to the subscription page
        return redirect('subscription_page')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user after signup
            return redirect('subscription_page')  # Redirect to subscription page
    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})
