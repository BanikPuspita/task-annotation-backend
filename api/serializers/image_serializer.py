from rest_framework import serializers
from api.models import Image

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"
        read_only_fields = ["user", "public_id"]
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Send the image_url as the image field to keep frontend compatibility
        data['image'] = instance.image_url
        return data