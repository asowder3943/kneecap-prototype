from django.urls import path
from youtube.views import unsubscribe, youtube, subscribe, subscriptions, search_results, feed, refresh, download, player, reverse_feed, refresh_feed_item, blank, toggle_played, toggle_hide_played

urlpatterns = [
    path("", youtube),
    path("subscribe/<str:id>", subscribe),
    path("unsubscribe/<str:id>", unsubscribe),
    path("refresh", refresh),
    path("subscriptions", subscriptions),
    path("search/", blank),
    path("search/<str:query>", search_results),
    path("feed", feed),
    path("feed/<str:id>", refresh_feed_item),
    path("download/<str:video_id>/<str:download_type>", download),
    path("player/<str:video_id>", player),
    path("reverse", reverse_feed),
    path("toggle-played/<str:id>", toggle_played),
    path("toggle-hide-played", toggle_hide_played)
]