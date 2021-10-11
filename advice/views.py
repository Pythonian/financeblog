# from django.shortcuts import render
from django.contrib import messages
from django.views.generic import CreateView, DeleteView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.utils import formats

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .models import Advice, Question
from .serializers import AdviceCreateSerializer


class QuestionListView(ListView):
    model = Question
    paginate_by = 3
    ordering = ['-published']


class QuestionCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Question
    fields = ['title']
    success_message = "Question created successfully!"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class QuestionDetailView(DetailView):
    model = Question


class QuestionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Question
    success_message = "Question Deleted Successfully!"
    success_url = "/questions/"

    def test_func(self):
        question = self.get_object()
        if self.request.user == question.author:
            return True
        else:
            return False

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class AdviceListView(APIView):
    def get(self, request, pk=None):
        # Retrieve all instances of the Advice model that belongs to a question
        queryset = Advice.objects.all().filter(
            question_id=pk).order_by('-published')
        data_to_return = []

        for advice in queryset:
            username = advice.author.username
            user_url = request.build_absolute_uri(
                reverse('profile', args=[advice.author.pk]))
            user_image = request.build_absolute_uri(
                advice.author.profile.image.url)
            content = advice.content
            published = formats.date_format(
                advice.published, "SHORT_DATETIME_FORMAT")

            # Create instance of the Advice that'll be sent back to the URL
            instance = {
                'username': username,
                'user_url': user_url,
                'user_image': user_image,
                'content': content,
                'published': published
            }
            data_to_return.append(instance)
        # Returns data thro' the Response method after conversion to JSON obj
        return Response(data_to_return)


class AdviceCreateView(APIView):
    def post(self, request, pk=None):
        if request.user.is_authenticated:
            # pass in the user submitted data from the request
            serializer = AdviceCreateSerializer(data=request.data)
            if serializer.is_valid():
                user = request.user
                try:
                    question = Question.objects.get(pk=pk)
                except Question.DoesNotExist:
                    return Response({"error": "Question does not exist."},
                                    status=status.HTTP_400_BAD_REQUEST)
                advice = Advice.objects.create(
                    content=serializer.validated_data["content"],
                    author=user, question=question)
                advice.save()
                # returns a JSON/Dict object after save
                data_to_return = {
                    "username": advice.author.username,
                    "user_url": reverse("profile",
                                        args=[advice.author.pk],
                                        request=request),
                    "user_image": request.build_absolute_uri(
                        advice.author.profile.image.url),
                    "content": advice.content,
                    "published": formats.date_format(advice.published,
                                                     "SHORT_DATETIME_FORMAT")
                }
                return Response(data_to_return, status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status.HTTP_401_UNAUTHORIZED)
