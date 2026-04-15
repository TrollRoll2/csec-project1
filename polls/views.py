from django.db import connection
from django.db.models import F
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone

from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )

    selected_choice.votes = F("votes") + 1
    selected_choice.save()
    return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

class CreateView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "polls/create.html")

    def post(self, request):
        question_text = request.POST["question_text"]

        if not question_text:
            return render(request, "polls/create.html", {
                "error_message": "Question can not be empty",
            })

        q = Question(
            question_text=question_text,
            pub_date=timezone.now(),
            author=request.user,
        )
        q.save()

        return redirect("polls:detail", q.id)

class AddChoiceView(LoginRequiredMixin, View):
    def post(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)

        if question.author != request.user:
            return HttpResponseForbidden("Only the author may add choices.")

        choice_text = request.POST.get("choice_text")
        cursor = connection.cursor() #Remove this line
        query = "SELECT id, question_text FROM polls_question WHERE question_text = '%s'" % choice_text #Remove this line

# A05:2025, Injection is possible here due to the user input not being filtered. The cursor and query functionality should be removed, as well as the try-except block.

        try: #Remove this line
            cursor.execute(query) #Remove this line
            results = cursor.fetchall() #Remove this line
        except Exception as e:  #Remove this line
            return render(request, "polls/detail.html", { #Remove this line
                "question": question, #Remove this line
                "error_message": str(e), #Remove this line
            }) #Remove this line
        
# A10:2025, Mishandling of exceptional conditions is prevalent here, as the error message provides information about the SQL query and error, which could be
# used in refining an SQL-injection. The error message should be more general and not reveal information.

        if not choice_text:
            return render(request, "polls/detail.html", {
                "question": question,
                "error_message": "Choice cannot be empty.",
            })

        question.choice_set.create(choice_text=choice_text, votes=0)

        return redirect("polls:detail", question.id)

class DeleteView(LoginRequiredMixin, View):
    def post(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)

#        if question.author != request.user:
#            return HttpResponseForbidden("You are not allowed to delete this poll.")

# A01:2025, Broken access control gives logged in users the option to delete any poll, even ones that they are not the author of,
# by manually entering the delete address. The above commented out code would fix this problem.

        question.delete()
        return redirect("account:profile")
