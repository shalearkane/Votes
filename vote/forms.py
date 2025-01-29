from django import forms


class VoteForm(forms.Form):
    option = forms.ChoiceField(
        choices=[
            ("A", "Option A"),
            ("B", "Option B"),
            ("C", "Option C"),
            ("D", "Option D"),
        ],
        widget=forms.RadioSelect,
        required=True,
    )
