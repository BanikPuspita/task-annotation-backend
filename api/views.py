from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics
from .models import Task
from .serializers.task_serializer import TaskSerializer
from .models import Image
from .serializers.image_serializer import ImageSerializer
from .models import Annotation
from .serializers.annotation_serializer import AnnotationSerializer
from rest_framework.exceptions import PermissionDenied
from .serializers.auth_serializer import EmailLoginSerializer
import cloudinary.uploader
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Image
from .serializers.image_serializer import ImageSerializer

@api_view(["POST"])
def login(request):
    serializer = EmailLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response(serializer.validated_data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def profile(request):
    user = request.user

    return Response({
        "id": user.id,
        "username": user.username,
        "email": user.email,
    })
    
    
class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user)

        selected_date = self.request.query_params.get("date")

        if selected_date:
            queryset = queryset.filter(task_date=selected_date)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
    


class ImageListCreateView(generics.ListCreateAPIView):
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Image.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            # Get the uploaded file from request
            uploaded_file = request.FILES.get('image')
            
            if not uploaded_file:
                return Response(
                    {'error': 'No image file provided'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Upload to Cloudinary
            upload_result = cloudinary.uploader.upload(
                uploaded_file,
                folder='taskflow_images/',
                resource_type='image'
            )
            
            # Create the image record
            image = Image.objects.create(
                user=request.user,
                title=request.data.get('title', uploaded_file.name),
                image_url=upload_result['secure_url'],
                public_id=upload_result['public_id']
            )
            
            serializer = self.get_serializer(image)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            print(f"Upload error: {str(e)}")  # This will show in Render logs
            return Response(
                {'error': f'Upload failed: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )    

   
class AnnotationListCreateView(generics.ListCreateAPIView):
    serializer_class = AnnotationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Annotation.objects.filter(
            image__user=self.request.user
        )

        image = self.request.query_params.get("image")

        if image:
            queryset = queryset.filter(image=image)

        return queryset

    def perform_create(self, serializer):
        image = serializer.validated_data["image"]

        if image.user != self.request.user:
            raise PermissionDenied(
                "You do not own this image."
            )

        serializer.save()

class AnnotationDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AnnotationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Annotation.objects.filter(
            image__user=self.request.user
        )