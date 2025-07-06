from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.template import TemplateDoesNotExist
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import SteelSheet, SteelSheetInspection
from django.views.decorators.http import require_POST
from django import forms
from django.forms import modelformset_factory
from django.contrib.auth import get_user_model
User = get_user_model()

@login_required
def root_page_view(request):
    try:
        return render(request, 'pages/index.html')
    except TemplateDoesNotExist:
        return render(request, 'pages/pages-404.html')

@login_required
def dynamic_pages_view(request, template_name):
    try:
        return render(request, f'pages/{template_name}.html')
    except TemplateDoesNotExist:
        return render(request, 'pages/pages-404.html')

class SteelSheetListView(ListView):
    model = SteelSheet
    template_name = 'pages/steel-sheets-list.html'
    context_object_name = 'sheets'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('search')
        if query:
            qs = qs.filter(
                Q(lot_number__icontains=query) |
                Q(part_name__icontains=query) |
                Q(category__icontains=query) |
                Q(location__icontains=query)
            )
        sort = self.request.GET.get('sort')
        allowed = [
            'lot_number', 'part_name', 'thickness', 'width', 'length', 'category',
            'quantity', 'location', 'created_at'
        ]
        if sort in allowed:
            qs = qs.order_by(sort)
        elif sort and sort.startswith('-') and sort[1:] in allowed:
            qs = qs.order_by(sort)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        return context

class SteelSheetCreateView(CreateView):
    model = SteelSheet
    fields = ['lot_number', 'part_name', 'thickness', 'width', 'length', 'category', 'quantity', 'location']
    template_name = 'pages/steel-sheets-add.html'
    success_url = reverse_lazy('pages:steel-sheet-list')


class SteelSheetUpdateView(UpdateView):
    model = SteelSheet
    fields = ['lot_number', 'part_name', 'thickness', 'width', 'length', 'category', 'quantity', 'location']
    template_name = 'pages/steel-sheets-add.html'
    success_url = reverse_lazy('pages:steel-sheet-list')

class SteelSheetDeleteView(DeleteView):
    model = SteelSheet
    template_name = 'pages/steel-sheet-confirm-delete.html'
    success_url = reverse_lazy('pages:steel-sheet-list')

class SteelSheetDetailView(DetailView):
    model = SteelSheet
    template_name = 'pages/steel-sheet-detail.html'

@require_POST
def steel_sheet_delete(request, pk):
    sheet = get_object_or_404(SteelSheet, pk=pk)
    sheet.delete()
    return redirect('pages:steel-sheet-list')

class SteelSheetInspectionForm(forms.ModelForm):
    class Meta:
        model = SteelSheetInspection
        fields = [
            'sheet', 'inspector', 'surface_deformation', 'scratches_percent', 'dent',
            'stain', 'other_remarks', 'conductivity_test', 'decision', 'notes'
        ]
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 2}),
        }

SteelSheetInspectionFormSet = modelformset_factory(
    SteelSheetInspection,
    form=SteelSheetInspectionForm,
    extra=0,
    can_delete=False,
)

@login_required
def batch_inspection_view(request):
    sheets = list(SteelSheet.objects.all().order_by('created_at'))
    initial = [{'sheet': sheet.id, 'inspector': request.user.id} for sheet in sheets]
    if request.method == 'POST':
        formset = SteelSheetInspectionFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('pages:steel-sheet-list')
    else:
        formset = SteelSheetInspectionFormSet(
            queryset=SteelSheetInspection.objects.none(),
            initial=initial
        )
    sheet_forms = zip(sheets, formset.forms)
    return render(request, 'pages/steel-sheet-batch-inspection.html', {
        'formset': formset,
        'sheet_forms': sheet_forms,
    })

@login_required
def steel_sheet_inspection_list(request):
    inspections = SteelSheetInspection.objects.select_related('sheet', 'inspector').order_by('-inspection_date')
    return render(request, 'pages/steel-sheet-inspection-list.html', {
        'inspections': inspections,
    })

@login_required
def steel_sheet_inspection_create(request):
    selected_sheet = None
    users = User.objects.all()  # You can filter for QC Inspectors later
    if request.method == 'POST':
        form = SteelSheetInspectionForm(request.POST)
        if form.is_valid():
            inspection = form.save(commit=False)
            inspector_id = form.cleaned_data.get('inspector') or request.POST.get('inspector')
            if inspector_id:
                inspection.inspector_id = inspector_id  # assign selected inspector
            inspection.save()
            return redirect('pages:steel-sheet-inspection-list')
        # Try to get sheet for preview on error redisplay
        sheet_id = request.POST.get('sheet')
        if sheet_id:
            from .models import SteelSheet
            try:
                selected_sheet = SteelSheet.objects.get(pk=sheet_id)
            except SteelSheet.DoesNotExist:
                selected_sheet = None
    else:
        sheet_id = request.GET.get('sheet')
        initial = {}
        if sheet_id:
            initial['sheet'] = sheet_id
            from .models import SteelSheet
            try:
                selected_sheet = SteelSheet.objects.get(pk=sheet_id)
            except SteelSheet.DoesNotExist:
                selected_sheet = None
        form = SteelSheetInspectionForm(initial=initial)
    return render(request, 'pages/steel-sheet-inspection-form.html', {
        'form': form,
        'selected_sheet': selected_sheet,
        'users': users,
    })

@login_required
def steel_sheet_inspection_edit(request, pk):
    inspection = get_object_or_404(SteelSheetInspection, pk=pk)
    selected_sheet = inspection.sheet  # The related sheet
    users = User.objects.all()  # List for inspector select
    if request.method == 'POST':
        form = SteelSheetInspectionForm(request.POST, instance=inspection)
        if form.is_valid():
            form.save()
            return redirect('pages:steel-sheet-inspection-list')
    else:
        form = SteelSheetInspectionForm(instance=inspection)
    return render(request, 'pages/steel-sheet-inspection-form.html', {
        'form': form,
        'selected_sheet': selected_sheet,
        'users': users,
    })

@require_POST
@login_required
def steel_sheet_inspection_delete(request, pk):
    inspection = get_object_or_404(SteelSheetInspection, pk=pk)
    inspection.delete()
    return redirect('pages:steel-sheet-inspection-list')
