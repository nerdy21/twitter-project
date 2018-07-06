from django.shortcuts import render
from . import forms
from django.conf import settings
from django.http import HttpResponse
import json
from django.shortcuts import render

from . tweet_functions import extract_hashtags
from datetime import datetime
from . models import SearchLog

# Create your views here.
def home(request):

    # receive form input
    input_form = forms.InputForm(request.GET)

    # validate form input
    if not input_form.is_valid():
        # return home page
        return render(request, 'dashboard/charts_empty.html')

    # retrieve tweets from the user account
    statuses = settings.TWITTER_API.GetUserTimeline(screen_name=input_form.cleaned_data['user_id'], 
        count=settings.TWEET_CRAWL_COUNT, include_rts=False
    )

    # sort the tweets based on likes
    statuses = sorted(statuses, key=lambda k: k.favorite_count, reverse=True)

    # extract hashtags from tweets
    hashtags = extract_hashtags(statuses)

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
