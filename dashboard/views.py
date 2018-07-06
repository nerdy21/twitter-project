from datetime import datetime
import json

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from . tweet_functions import extract_hashtags, retrieve_tweets
from . models import SearchLog
from . import forms

# Create your views here.
def home(request):

    # receive form input
    input_form = forms.InputForm(request.GET)

    # validate form input
    if not input_form.is_valid():
        # return home page
        return render(request, 'dashboard/charts_empty.html', 
            {"message": "Please use the search bar to find the target twitter handle."}
        )

    # retrieve tweets from the user account
    statuses = retrieve_tweets(input_form.cleaned_data['user_id'])

    # sort the tweets based on likes
    statuses = sorted(statuses, key=lambda k: k.favorite_count, reverse=True)

    # extract hashtags from tweets
    hashtags = extract_hashtags(statuses)
    if hashtags == []:
        return render(request, 'dashboard/charts_empty.html', 
            {"message": "Please enter a valid Twitter User ID"}
        )

    # save query entry for reference
    SearchLog.objects.create(search_query=input_form.cleaned_data['user_id'],
        time=datetime.now()
    )

    # render and return the output
    return render(request, 'dashboard/charts.html', 
        {
            "user_name": input_form.cleaned_data['user_id'],
            "statuses": statuses, "hashtags": hashtags
        }
    )


def search_history(request):

    # retrieve logs
    history = SearchLog.objects.all().order_by('time')

    # render and return logs
    return render(request, 'dashboard/log.html', {"history": history})
