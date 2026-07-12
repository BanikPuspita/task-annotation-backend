from rest_framework import serializers
from api.models import Image

class ImageSerializer(serializers.ModelSerializer):
    # Add a custom field for backward compatibility
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = Image
        fields = ['id', 'user', 'title', 'image_url', 'public_id', 'uploaded_at', 'image']
        read_only_fields = ["user", "public_id", "uploaded_at"]
    
    def get_image(self, obj):
        # Return image_url as 'image' for frontend compatibility
        return obj.image_url if obj.image_url else None