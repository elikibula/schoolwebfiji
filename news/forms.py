from django import forms
from .models import News, Category, Comment
from tinymce.widgets import TinyMCE


class NewsForm(forms.ModelForm):
    content = forms.CharField(
        widget=TinyMCE(attrs={'cols': 80, 'rows': 20}),
        help_text="Write the full content of the news item."
    )

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Select a Category",
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text="Choose the relevant category for this news article."
    )

    class Meta:
        model = News
        fields = ['title', 'content', 'image', 'video', 'category', 'is_featured']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'video': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        help_texts = {
            'title': "Enter a descriptive and short title.",
            'image': "Upload an image for the news.",
            'video': "Optional: Upload a related video file.",
            'is_featured': "Check this box if you want this news to appear on the homepage.",
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

