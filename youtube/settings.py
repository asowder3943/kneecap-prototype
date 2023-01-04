from pyyoutube import Api
from os import getenv

api_key = getenv("YOUTUBE_API")
api  = Api(api_key=api_key)

