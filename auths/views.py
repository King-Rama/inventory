from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import render, redirect

# Create your views here.
from auths.forms import ClientRegister


def client_register(request):
    if request.method == 'POST':  # checking if request is post
        form = ClientRegister(request.POST)     # instantiate the form
        if form.is_valid():
            new_client = form.save(commit=False)
            phone = form.cleaned_data['phone_number']
            password = form.cleaned_data['password1']
            new_client.save()
            login(request, new_client)
            # adding anything we want to send to our new registered client
            messages.add_message(request, messages.SUCCESS, 'Welcome now you can request for help!')
            return redirect('client:request-help')
    else:
        form = ClientRegister()
    return render(request, 'registration/register.html', {'form': form})

