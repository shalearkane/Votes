from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count
from .forms import VoteForm
from .models import UserVote


@login_required
def vote_page(request):
    user_vote_profile, created = UserVote.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = VoteForm(request.POST)
        if form.is_valid():
            user_vote_profile.voted_option = form.cleaned_data["option"]
            user_vote_profile.save()
            return redirect("vote_results")  # Redirect to results page after voting
    else:
        form = VoteForm(
            initial={"option": user_vote_profile.voted_option}
        )  # pre-select if already voted

    return render(request, "vote_page.html", {"form": form})


def vote_results(request):
    vote_counts = (
        UserVote.objects.values("voted_option")
        .annotate(count=Count("voted_option"))
        .order_by("voted_option")
    )
    total_votes = UserVote.objects.exclude(voted_option__isnull=True).count()
    return render(
        request,
        "vote_results.html",
        {"vote_counts": vote_counts, "total_votes": total_votes},
    )


@user_passes_test(lambda u: u.is_superuser)  # Admin access only
def clear_votes(request):
    UserVote.objects.all().update(
        voted_option=None
    )  # Clear all votes by setting voted_option to None
    return redirect("vote_results")  # Redirect back to results page after clearing
