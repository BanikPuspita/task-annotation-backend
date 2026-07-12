from rest_framework import serializers
from api.models import Image

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"
        read_only_fields = ["user"]
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Cloudinary already returns the full URL
        if instance.image:
            data['image'] = instance.image.url
        return data