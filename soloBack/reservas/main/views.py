from django.shortcuts import render
from main import models
# Create your views here.


def catalogo():
    vehicles = models.Vehicles.objects.all()
    context = {"vehicles": vehicles}
    return render("catalogo.html", context)


@login_required
def reserva():
    if request.method == "GET":
        reserva = eval(request.request)
        redirect success
    if request.method == "POST":
        crear_reserva()


def admin():
    if request.method == "GET":
        if request.user.isAdmin:
            return render("accept.html")
        return render("noadmin.html")
    if request.method == "POST":
        accept_reserva()
