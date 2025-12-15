from django.shortcuts import render,redirect, get_object_or_404
from .models import MedicineDetail, OfferedRates
from django.http import JsonResponse

# Create your views here.
def home(request):
    query = request.GET.get('q')
    medicine = MedicineDetail.objects.all()

    if query:
        try:
            # Try to find the medicine by name (case-insensitive)
            medicine = MedicineDetail.objects.get(name__iexact=query)
            return redirect('detail', pk=medicine.pk)
        except MedicineDetail.DoesNotExist:
            medicines = MedicineDetail.objects.filter(name__icontains=query)
            

    return render(request,'catalogue/home.html', {'medicine': medicine})

def detail(request,pk):
    # medicine = MedicineDetail.objects.get(pk=pk)
    medicine = get_object_or_404(MedicineDetail, pk=pk)
    return render(request,'catalogue/detail.html', {'medicine': medicine})

def contact(request):
    return render(request,'catalogue/contact.html')

def autocomplete(request):
    if 'term' in request.GET:
        qs = MedicineDetail.objects.filter(name__icontains=request.GET.get('term'))
        # names = list(qs.values_list('name', flat=True))
        results = list(qs.values('id', 'name'))
        return JsonResponse(results, safe=False)
    return JsonResponse([], safe=False)



def offered_rates(request):
    rate = OfferedRates.objects.first()
    return render(request, 'catalogue/offered_rates.html', {'rate': rate})


