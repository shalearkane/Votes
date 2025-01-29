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
    vote_counts_data = (
        UserVote.objects.values("voted_option")
        .annotate(count=Count("voted_option"))
        .order_by("voted_option")
    )
    total_votes = UserVote.objects.exclude(voted_option__isnull=True).count()

    vote_counts_with_heights = []
    if total_votes > 0:
        for result in vote_counts_data:
            height_percentage = (
                (result["count"] / total_votes) * 250 if total_votes > 0 else 0
            )
            vote_counts_with_heights.append(
                {
                    "voted_option": result["voted_option"],
                    "count": result["count"],
                    "height_percentage": height_percentage,
                }
            )
    else:
        for (
            result
        ) in (
            vote_counts_data
        ):  # Still need to iterate to show options even with 0 votes
            vote_counts_with_heights.append(
                {
                    "voted_option": result["voted_option"],
                    "count": 0,
                    "height_percentage": 0,
                }
            )

    return render(
        request,
        "vote_results.html",
        {"vote_counts": vote_counts_with_heights, "total_votes": total_votes},
    )


@user_passes_test(lambda u: u.is_superuser)  # Admin access only
def clear_votes(request):
    UserVote.objects.all().update(
        voted_option=None
    )  # Clear all votes by setting voted_option to None
    return redirect("vote_results")  # Redirect back to results page after clearing
