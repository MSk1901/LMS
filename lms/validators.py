import re

from rest_framework import serializers


def is_youtube_link(link):
    youtube_regex = r"(https?://)?(www\.)?(youtube\.com|youtu\.?be)/.+$"
    return re.match(youtube_regex, link)


class LessonURLValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        link = value.get(self.field)
        result = is_youtube_link(link)
        if not result:
            raise serializers.ValidationError("Можно прикреплять ссылки только на Youtube")
