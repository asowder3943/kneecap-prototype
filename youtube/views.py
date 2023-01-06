from django.shortcuts import render
from youtube.settings import api
from youtube.models import Channel, Video, FeedSettings
from django.http import HttpResponse
from youtube.utill import get_size_gb
from kneecap_backend.settings import MEDIA_ROOT


def blank(request): 
    return HttpResponse(status=200)


def youtube(request): 
    context_wrapper = {
        "context": {
            "library_size": get_size_gb(MEDIA_ROOT),
            "feed_settings": FeedSettings.get_solo(),
            "channels": Channel.objects.all(),
            "videos": Video.feed()
        }
    }
    
    return  render(request, 'youtube.html', context_wrapper)

def subscribe(request, id):
    Channel.create_by_id(id=id)
    return HttpResponse(status=200)

def unsubscribe(request, id):
    Channel.objects.filter(id=id).delete()
    return HttpResponse(status=200)

def refresh(request):
    Video.fetch()
    return HttpResponse(status=200)

def subscriptions(request):
    context_wrapper = {
        "context": {
            "channels": Channel.objects.all()
        }
    }
    return render(request, 'subscriptions.html', context_wrapper)

def search(request):
    return render(request, 'search.html')

def search_results(request, query):
    results = api.search(q=query,count=5,search_type="channel").items
    context_wrapper = {
        "context":{
            "results": [
                {
                "title": result.snippet.title,
                "thumbnail": result.snippet.thumbnails.default.url,
                "id": result.snippet.channelId
                }
                for result in results
            ]
        }
    }
    return render(request, 'search-results.html', context_wrapper)


def feed(request):
    context_wrapper = {
        "context":{
            "library_size": get_size_gb(MEDIA_ROOT),
            "feed_settings": FeedSettings.get_solo(),
            "videos": Video.feed()
        }
    }
    return render(request, 'feed.html', context_wrapper)

def download(request, video_id, download_type):
    Video.objects.get(id=video_id).download(type_string=download_type)
    return HttpResponse(status=200)

def player(request, video_id):
    context_wrapper = {
        "context":{
            "playing_video": video_id
        }
    }
    return render(request, 'player.html', context_wrapper)

def reverse_feed(request):
    FeedSettings.get_solo().reverse_feed_order()
    return HttpResponse(status=200)

def refresh_feed_item(request, id):
    context_wrapper = {
        "video": Video.objects.get(id=id)
    }
    return render(request, 'feed-item.html', context_wrapper)
