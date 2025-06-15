from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect,get_object_or_404
from .models import Trip
from .forms import TripForm
import django_filters
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from django.forms import DateInput




def home(request):
    form = TripForm()
    trips = Trip.objects.all()
    trip_filter = TripFilter(request.GET, queryset=trips)
    return render(request, 'home.html', {
        'form': form,
        'trips': trip_filter.qs,
        'filter': trip_filter  # 👈 This makes filter.form available in the template
    })

@login_required
def create_trip(request):
    trips = Trip.objects.all()

    if request.method == 'POST':
        form = TripForm(request.POST, request.FILES)
        if form.is_valid():
            trip = form.save(commit=False)

            # Resize image if there is one
            image = form.cleaned_data.get('trip_picture')
            if image:
                img = Image.open(image)
                img = img.resize((1000, 400), Image.LANCZOS)
                img.thumbnail((1000, 400), Image.LANCZOS)

                buffer = BytesIO()
                img.save(buffer, format='JPEG')
                buffer.seek(0)

                trip.trip_picture.save(image.name, ContentFile(buffer.read()), save=False)

            trip.creator = request.user
            trip.save()
            return redirect('home')  # Redirect after success to clear form data and errors
        # if invalid POST, render with errors and trips (modal stays open)
        return render(request, 'home.html', {'form': form, 'trips': trips})

    # On GET, render home with blank form and trips (modal closed)
    form = TripForm()
    return render(request, 'home.html', {'form': form, 'trips': trips})


@login_required
def delete_trip(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id, creator=request.user)
    trip.delete()
    return redirect('profile')  # Or wherever you want to redirect after deletion

@login_required
def edit_trip(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id, creator=request.user)

    if request.method == 'POST':
        form = TripForm(request.POST, request.FILES , instance=trip) #changed
        if form.is_valid():
            form.save()
            return redirect('profile')  # or wherever you want to redirect after editing
    else:
        form = TripForm(instance=trip)

    return render(request, 'trips/edit_trip.html', {'form': form, 'trip': trip})


class TripFilter(django_filters.FilterSet):
    # Min and Max Price
    price_min = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='gte',
        label='Min Price'
    )
    price_max = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='lte',
        label='Max Price'
    )

    # Date range (2 fields only)
    date_start = django_filters.DateFilter(
        field_name='trip_date_start',
        lookup_expr='gte',
        label='Start After',
        widget=DateInput(attrs={'type': 'date'})
    )
    date_end = django_filters.DateFilter(
        field_name='trip_date_start',
        lookup_expr='lte',
        label='End Before',
        widget=DateInput(attrs={'type': 'date'})
    )

    # Combined sorting filter
    ordering = django_filters.OrderingFilter(
        label='Sort by',
        fields=(
            ('price', 'price'),
            ('trip_date_start', 'trip_date_start'),
        ),
        field_labels={
            'price': 'Price',
            'trip_date_start': 'Trip Date',
        },
        choices=[
            ('price', 'Price: Low to High'),
            ('-price', 'Price: High to Low'),
            ('trip_date_start', 'Date: Close to Far'),
            ('-trip_date_start', 'Date: Far to Close'),
        ]
    )

    class Meta:
        model = Trip
        fields = []


def trip_search_view(request):
    queryset = Trip.objects.all()
    q = request.GET.get("q")

    if q:
        queryset = queryset.filter(title__icontains=q)

    trip_filter = TripFilter(request.GET, queryset=queryset)

    return render(request, "trips/search_results.html", {
        "filter": trip_filter
    })

@login_required
@require_POST
def toggle_favorite(request, trip_id):
    profile = request.user.profile
    trip = get_object_or_404(Trip, id=trip_id)

    if trip in profile.favorites.all():
        profile.favorites.remove(trip)
        favorited = False
    else:
        profile.favorites.add(trip)
        favorited = True

    return JsonResponse({'success': True, 'favorited': favorited})


def trip_details(request,trip_id):
    trip = get_object_or_404(Trip, id=trip_id)

    return render(request, 'trip_details.html', {'trip': trip})
