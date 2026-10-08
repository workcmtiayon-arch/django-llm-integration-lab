from django import forms

from .models import Comment, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("content", "visibility")
        labels = {"content": "Quoi de neuf ?", "visibility": "Qui peut voir cette publication ?"}
        widgets = {"content": forms.Textarea(attrs={"rows": 4, "placeholder": "Partagez une idée, une réussite ou une question…"})}

    def clean_content(self):
        content = self.cleaned_data["content"].strip()
        if not content:
            raise forms.ValidationError("Une publication ne peut pas être vide.")
        return content


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("content",)
        labels = {"content": "Commenter"}
        widgets = {"content": forms.TextInput(attrs={"placeholder": "Écrire un commentaire…"})}

