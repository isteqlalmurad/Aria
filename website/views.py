from django.shortcuts import render, redirect

from django.http import HttpResponse


def homepage(request):
    return render(request, "website/home.html")


def subscribe(request):
    if request.method == "POST":
        email = request.POST.get("email")
        # Save the email to waitingList.txt
        with open("waitingList.txt", "a") as file:
            file.write(email + "\n")
        # return HttpResponse("Thank you for subscribing!")
    return render(request, "website/thanks.html")
