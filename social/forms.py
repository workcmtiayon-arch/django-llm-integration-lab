from django import forms

from .models import Comment, Post, PostReport


class PostForm(forms.ModelForm):
    remove_image = forms.BooleanField(
        label="Supprimer l’image actuelle",
        required=False,
    )

    class Meta:
        model = Post
        fields = ("content", "image", "visibility")
        labels = {"content": "Quoi de neuf ?", "image": "Ajouter une image", "visibility": "Qui peut voir cette publication ?"}
        widgets = {
            "content": forms.Textarea(attrs={"rows": 4, "placeholder": "Partagez une idée, une réussite ou une question…"}),
            "image": forms.FileInput,
        }

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


class PostReportForm(forms.ModelForm):
    class Meta:
        model = PostReport
        fields = ("reason", "details")
        labels = {"reason": "Motif", "details": "Détails supplémentaires"}
        widgets = {"details": forms.Textarea(attrs={"rows": 3, "maxlength": 500})}
