# taxi/views.py
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Driver, Car
from .forms import DriverCreationForm, DriverLicenseUpdateForm, CarForm

# ... Existing Manufacturer views ...

# --- Car Views (Updated to use CarForm) ---

class CarCreateView(LoginRequiredMixin, generic.CreateView):
    model = Car
    form_class = CarForm
    success_url = reverse_lazy("taxi:car-list")
    template_name = "taxi/car_form.html"

class CarUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Car
    form_class = CarForm
    success_url = reverse_lazy("taxi:car-list")
    template_name = "taxi/car_form.html"

# ... Car Delete/Detail/List views ...

# --- Driver Views ---

class DriverCreateView(LoginRequiredMixin, generic.CreateView):
    model = Driver
    form_class = DriverCreationForm
    success_url = reverse_lazy("taxi:driver-list")
    template_name = "taxi/driver_form.html"

class DriverDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Driver
    success_url = reverse_lazy("taxi:driver-list")
    template_name = "taxi/driver_confirm_delete.html"

class DriverLicenseUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Driver
    form_class = DriverLicenseUpdateForm
    template_name = "taxi/driver_license_form.html"
    
    def get_success_url(self):
        return reverse("taxi:driver-detail", kwargs={"pk": self.object.pk})

# --- Custom Action ---

@login_required
def toggle_assign_to_car(request, pk):
    driver = Driver.objects.get(id=request.user.id)
    car = get_object_or_404(Car, id=pk)
    
    if car in driver.cars.all():
        driver.cars.remove(car)
    else:
        driver.cars.add(car)
        
    return HttpResponseRedirect(reverse_lazy("taxi:car-detail", args=[pk]))
