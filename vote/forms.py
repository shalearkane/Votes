from django import forms


class VoteForm(forms.Form):
    option = forms.ChoiceField(
        choices=[
            ("A", "🅰 Option A"),
            ("B", "🅱 Option B"),
            ("C", "🅲 Option C"),
            ("D", "🅳 Option D"),
            ("E", "🚫 None of these"),
            ("F", "🤔 Explain every option in more detail"),
        ],
        widget=forms.RadioSelect,
        required=True,
    )
