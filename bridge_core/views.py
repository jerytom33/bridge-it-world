from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import CareerPath, Course, Mentor, MentorshipSession, Resource
from .serializers import CareerPathSerializer, CourseSerializer, MentorSerializer, MentorshipSessionSerializer, ResourceSerializer


class CareerPathListCreateView(generics.ListCreateAPIView):
    queryset = CareerPath.objects.all()
    serializer_class = CareerPathSerializer
    permission_classes = [IsAuthenticated]


class CareerPathDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CareerPath.objects.all()
    serializer_class = CareerPathSerializer
    permission_classes = [IsAuthenticated]


class CourseListCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]


class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]


class MentorListCreateView(generics.ListCreateAPIView):
    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer
    permission_classes = [IsAuthenticated]


class MentorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer
    permission_classes = [IsAuthenticated]


class MentorshipSessionListCreateView(generics.ListCreateAPIView):
    queryset = MentorshipSession.objects.all()
    serializer_class = MentorshipSessionSerializer
    permission_classes = [IsAuthenticated]


class MentorshipSessionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MentorshipSession.objects.all()
    serializer_class = MentorshipSessionSerializer
    permission_classes = [IsAuthenticated]


class ResourceListCreateView(generics.ListCreateAPIView):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    permission_classes = [IsAuthenticated]


class ResourceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    permission_classes = [IsAuthenticated]
