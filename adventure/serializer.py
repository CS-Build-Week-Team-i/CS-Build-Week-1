from rest_framework import serializers


class RoomSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=50, default="DEFAULT TITLE")
    description = serializers.CharField(max_length=500, default="DEFAULT DESCRIPTION")
    n_to = serializers.IntegerField(default=0)
    s_to = serializers.IntegerField(default=0)
    e_to = serializers.IntegerField(default=0)
    w_to = serializers.IntegerField(default=0)
    x = serializers.IntegerField(default=0)
    y = serializers.IntegerField(default=0)