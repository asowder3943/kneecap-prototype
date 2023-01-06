from django.db import models, IntegrityError
from youtube.settings import api
from django.utils import timezone
from pytube import YouTube
from os import removedirs
from solo.models import SingletonModel

class FeedSettings(SingletonModel):
    CHRONOLOGICAL = 'CH'
    REVERSE_CHRONOLOGICAL = 'RC'
    FEED_ORDER_CHOICES = [
        (CHRONOLOGICAL, 'Chronological'),
        (REVERSE_CHRONOLOGICAL, 'Reverse Chronological'),
    ]

    feed_order = models.CharField(
        max_length=2,
        choices=FEED_ORDER_CHOICES,
        default=CHRONOLOGICAL,
    )

    hide_played = models.BooleanField(default=False)

    def reverse_feed_order(self):
        if self.feed_order == self.CHRONOLOGICAL:
            self.feed_order = self.REVERSE_CHRONOLOGICAL
            self.save()
        else:
            self.feed_order = self.CHRONOLOGICAL
            self.save()
    
    def __str__(self):
        return "Feed Settings"

    class Meta:
        verbose_name = "Feed Settings"


class Channel(models.Model):
    id = models.CharField(verbose_name="Youtube channel id", max_length=255, primary_key=True, unique=True)
    title = models.CharField(verbose_name="Youtube Channel Title", max_length=255, default = "")
    thumbnail = models.CharField(verbose_name="Youtube Channel Thumbnail", max_length=255, default="")
    plid = models.CharField(verbose_name="Youtube Channel Playlist id", max_length=255)
    initialized = models.BooleanField(verbose_name="Youtube Channel Initialized", default=False)
    
    def fetch(self):
        response = api.get_channel_info(channel_id=self.id).items[0]
        self.title = response.snippet.title
        self.thumbnail = response.snippet.thumbnails.default.url
        self.plid = response.contentDetails.relatedPlaylists.uploads
        if not self.initialized:
            self.initialized = True
        self.save()

    @classmethod
    def create_by_id(cls,id):
        channel = cls.objects.create(id=id)
        channel.fetch()
        
    class Meta:
        ordering = ['title']

# Viewable
class Video(models.Model):
    id = models.CharField(verbose_name="Youtube Video id", null=False, max_length=255, primary_key=True)
    date_posted = models.DateTimeField(blank=False, default=timezone.now)
    title = models.CharField(verbose_name="Youtube Video Title", max_length=255, default = "")
    thumbnail = models.CharField(verbose_name="Youtube Video Thumbnail", max_length=255, default="")
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, verbose_name="Youtube Channel Publisher")
    
    duration = models.CharField(max_length=255, verbose_name="Youtube Video Duration")

    # Downloads
    audio_downloaded = models.BooleanField(default=False, verbose_name="Youtube Audio Downloaded")
    hires_downloaded = models.BooleanField(default=False, verbose_name="Youtube High Resolution Downloaded")

    # Played Status
    played = models.BooleanField(default=False, verbose_name="Youtube Video Maked as played")

    # preform download and update download status
    def download(self, **kwargs):
        if kwargs.get('type_string') == 'audio_only':
            self.download(audio_only=True)
        if kwargs.get('type_string') == 'highest_resolution':
            self.download(highest_resolution=True)
        if kwargs.get('audio_only'):
            if not self.audio_downloaded:
                try:
                    YouTube(f'https://youtu.be/{self.id}').streams.filter(only_audio=True).first().download(output_path=f'media/{self.id}/audio/',  filename='audio.mp4')
                    self.audio_downloaded = True
                    self.save()
                except:
                    self.audio_downloaded = False
                    self.save()
                    pass
        if kwargs.get('highest_resolution'):
            if not self.hires_downloaded:
                try:
                    YouTube(f'https://youtu.be/{self.id}').streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(output_path=f'media/{self.id}/hires/', filename='video.mp4')
                    self.hires_downloaded = True
                    self.save()
                except:
                    self.hires_downloaded = False
                    self.save()
                    pass

    def remove_download(self):
        self.hires_downloaded = False
        self.audio_downloaded = False
        removedirs(f'media/{self.id}')

    def youtube_url(self):
        return f'https://youtu.be/{self.id}'

    def duration_string(self):
        return self.duration.replace('PT', '').replace('H', ' hr ').replace('M', ' min ').replace('S', ' s')
    

    @classmethod
    def fetch(cls):
        for chan in Channel.objects.all():
            playlist_videos = api.get_playlist_items(playlist_id=chan.plid).items
            for video in playlist_videos:
                video_response = api.get_video_by_id(video_id=video.contentDetails.videoId)
                try:
                    cls.objects.create(
                        id=video.contentDetails.videoId, 
                        date_posted=video.contentDetails.videoPublishedAt, 
                        title=video_response.items[0].snippet.title,
                        thumbnail=video_response.items[0].snippet.thumbnails.default.url,
                        duration=video_response.items[0].contentDetails.duration,
                        channel = chan)
                except IntegrityError:
                    existing_video = cls.objects.get(id=video.contentDetails.videoId)
                    existing_video.date_posted = video.contentDetails.videoPublishedAt
                    existing_video.title = video_response.items[0].snippet.title
                    existing_video.thumbnail = video_response.items[0].snippet.thumbnails.default.url
                    existing_video.save()
    
    @classmethod
    def feed(cls):
        if FeedSettings.get_solo().feed_order == FeedSettings.CHRONOLOGICAL:
            return  Video.objects.order_by('date_posted')
        else:
            return  Video.objects.order_by('date_posted').reverse()

    class Meta:
        ordering = ['date_posted']

