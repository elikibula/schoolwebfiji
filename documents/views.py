from django.shortcuts import render, redirect, get_object_or_404
from .models import Document, DocumentCategory, SubCategory
from .forms import DocumentForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, FileResponse, Http404
from django.contrib import messages
from django.db.models import Count, Prefetch
from django.views.decorators.http import require_POST


@login_required
def embedded_preview(request, pk):
    document = get_object_or_404(Document, pk=pk)
    file_url = request.build_absolute_uri(document.file.url)

    supported_formats = ['.pdf', '.doc', '.docx', '.ppt', '.pptx', '.xls', '.xlsx']
    if not any(file_url.lower().endswith(ext) for ext in supported_formats):
        return render(request, 'documents/unsupported_format.html', {'document': document})

    return render(request, 'documents/embedded_preview.html', {
        'document': document,
        'file_url': file_url
    })


@login_required
def category_detail(request, pk):
    user_groups = request.user.groups.all()

    # Use filter + distinct + first() instead of get() because of ManyToMany 'groups'
    category = DocumentCategory.objects.filter(pk=pk, groups__in=user_groups).distinct().first()
    if not category:
        raise Http404("Category not found or access denied")

    # Subcategories filtered by category and user groups
    subcategories = SubCategory.objects.filter(category=category, groups__in=user_groups).distinct()

    # Prefetch subcategories visible to user for sidebar
    subcategory_qs = SubCategory.objects.filter(groups__in=user_groups).distinct()
    categories = DocumentCategory.objects.filter(groups__in=user_groups).prefetch_related(
        Prefetch('subcategories', queryset=subcategory_qs)
    ).distinct()

    return render(request, 'documents/category_detail.html', {
        'category': category,
        'subcategories': subcategories,
        'categories': categories,
        'active_category_pk': category.pk,
        'active_subcategory_pk': None,
    })


@login_required
def subcategory_detail(request, pk):
    user_groups = request.user.groups.all()

    # Safer way to avoid MultipleObjectsReturned
    subcategory = SubCategory.objects.filter(pk=pk, groups__in=user_groups).distinct().first()
    if not subcategory:
        raise Http404("Subcategory not found or access denied")

    # Filter documents under subcategory, respecting user groups
    documents = Document.objects.filter(subcategory=subcategory, groups__in=user_groups).distinct()

    # Sidebar navigation categories with subcategories visible to user
    subcategory_qs = SubCategory.objects.filter(groups__in=user_groups).distinct()
    categories = DocumentCategory.objects.filter(groups__in=user_groups).prefetch_related(
        Prefetch('subcategories', queryset=subcategory_qs)
    ).distinct()

    return render(request, 'documents/subcategory_detail.html', {
        'subcategory': subcategory,
        'documents': documents,
        'categories': categories,
    })


@login_required
def document_list(request):
    user_groups = request.user.groups.all()
    categories = DocumentCategory.objects.filter(groups__in=user_groups).annotate(
        subcategory_count=Count('subcategories', distinct=True),
        document_count=Count('document', distinct=True)
    ).distinct()

    return render(request, 'documents/document_list.html', {
        'categories': categories
    })


@login_required
def upload_document(request):
    user_groups = request.user.groups.all()
    categories = DocumentCategory.objects.filter(groups__in=user_groups).distinct()

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.author = request.user
            document.owner = request.user
            document.save()
            form.save_m2m()
            messages.success(request, "Your document has been successfully uploaded.")
            return redirect('documents:subcategory_detail', pk=document.subcategory.pk)  # <-- Redirect here
    else:
        form = DocumentForm()

    return render(request, 'documents/upload_document.html', {
        'form': form,
        'categories': categories
    })


@login_required
def document_detail(request, pk):
    document = get_object_or_404(Document, pk=pk)
    return render(request, 'documents/document_detail.html', {'document': document})


@login_required
def view_document(request, pk):
    document = get_object_or_404(Document, pk=pk)
    return render(request, 'documents/view_document.html', {'document': document})


@login_required
def embedded_preview(request, pk):
    document = get_object_or_404(Document, pk=pk)
    file_url = request.build_absolute_uri(document.file.url)

    supported_formats = ['.pdf', '.doc', '.docx', '.ppt', '.pptx', '.xls', '.xlsx']
    if not any(file_url.lower().endswith(ext) for ext in supported_formats):
        return render(request, 'documents/unsupported_format.html', {'document': document})

    return render(request, 'documents/embedded_preview.html', {
        'document': document,
        'file_url': file_url
    })



@login_required
def download_document(request, pk):
    document = get_object_or_404(Document, pk=pk)
    return FileResponse(document.file.open(), as_attachment=True, filename=document.file.name)


@login_required
def update_document(request, pk):
    document = get_object_or_404(Document, pk=pk)
    form = DocumentForm(request.POST or None, request.FILES or None, instance=document)
    if form.is_valid():
        form.save()
        messages.success(request, "Document updated successfully.")
        return redirect('documents:subcategory_detail', pk=document.subcategory.pk)
    return render(request, 'documents/document_edit.html', {'form': form, 'document': document})


@login_required
@require_POST
def delete_document(request, pk):
    document = get_object_or_404(Document, pk=pk)
    document.delete()
    messages.success(request, "Document deleted successfully.")
    return redirect('documents:subcategory_detail', pk=document.subcategory.pk)


def get_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = SubCategory.objects.filter(category_id=category_id).values('id', 'name')
    return JsonResponse({'subcategories': list(subcategories)})


