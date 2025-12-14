from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Car
from .forms import DriverCreationForm, DriverLicenseUpdateForm, CarForm

# ... Manufacturer and Car views from previous steps ...

class DriverCreateView(LoginRequiredMixin, generic.CreateView):
    model = get_user_model()
    form_class = DriverCreationForm
    success_url = reverse_lazy("taxi:driver-list")
    template_name = "taxi/driver_form.html"

class DriverDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = get_user_model()
    success_url = reverse_lazy("taxi:driver-list")
    template_name = "taxi/driver_confirm_delete.html"

class DriverLicenseUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = get_user_model()
    form_class = DriverLicenseUpdateForm
    template_name = "taxi/driver_license_form.html"
    
    def get_success_url(self):
        return reverse("taxi:driver-detail", kwargs={"pk": self.object.pk})

@login_required
def toggle_assign_to_car(request, pk):
    # Fix: Use request.user directly instead of querying database
    driver = request.user
    car = get_object_or_404(Car, id=pk)
    
    if car in driver.cars.all():
        driver.cars.remove(car)
    else:
        driver.cars.add(car)
        
    return HttpResponseRedirect(reverse_lazy("taxi:car-detail", args=[pk]))
