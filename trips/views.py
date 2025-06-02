from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect,get_object_or_404
from .models import Trip
from .forms import TripForm
from django.db.models import Q
from django_filters.views import FilterView
import django_filters




def home(request):
    trips = Trip.objects.all()
    return render(request, 'home.html', {'trips': trips})


@login_required
def create_trip(request):
    if request.method == 'POST':
        form = TripForm(request.POST)
        if form.is_valid():
            trip = form.save(commit=False)
            trip.creator = request.user
            trip.save()
            return redirect('home')
    else:
        form = TripForm()
    return render(request, 'trips/create_trip.html', {'form': form})

@login_required
def delete_trip(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id, creator=request.user)
    trip.delete()
    return redirect('profile')  # Or wherever you want to redirect after deletion

@login_required
def edit_trip(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id, creator=request.user)

    if request.method == 'POST':
        form = TripForm(request.POST, instance=trip)
        if form.is_valid():
            form.save()
            return redirect('profile')  # or wherever you want to redirect after editing
    else:
        form = TripForm(instance=trip)

    return render(request, 'trips/edit_trip.html', {'form': form, 'trip': trip})


class TripFilter(django_filters.FilterSet):
    price_filter = django_filters.OrderingFilter(
        label='Sort by price',
        fields=(('price', 'price'),),
        field_labels={'price': 'Price'},
        choices=[
            ('price', 'Low to High'),
            ('-price', 'High to Low'),
        ]
    )

    class Meta:
        model = Trip
        fields = {
            'price': ['lte', 'gte'],
            'trip_date': ['exact', 'gte', 'lte'],
        }


def trip_search_view(request):
    queryset = Trip.objects.all()
    q = request.GET.get("q")

    if q:
        queryset = queryset.filter(title__icontains=q)

    trip_filter = TripFilter(request.GET, queryset=queryset)

    return render(request, "trips/search_results.html", {
        "filter": trip_filter
    })
