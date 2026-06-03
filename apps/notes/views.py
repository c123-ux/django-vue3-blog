from django.db.models import Q
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from .models import Note
from .serializers import NoteSerializer, NoteCreateSerializer
from .permissions import IsAuthorOrStaff


class NoteListView(generics.ListAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = None

    def get_queryset(self):
        qs = Note.objects.select_related('author')
        if self.request.user.is_authenticated:
            return qs.filter(Q(is_public=True) | Q(author=self.request.user)).distinct()
        return qs.filter(is_public=True)


class NoteDetailView(generics.RetrieveAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Note.objects.select_related('author')

    def get_object(self):
        obj = super().get_object()
        if not obj.is_public and self.request.user != obj.author and not self.request.user.is_staff:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('无权查看此笔记')
        return obj


class NoteCreateView(generics.CreateAPIView):
    serializer_class = NoteCreateSerializer
    permission_classes = [IsAuthenticated]
    queryset = Note.objects.all()


class NoteUpdateView(generics.UpdateAPIView):
    serializer_class = NoteCreateSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrStaff]
    queryset = Note.objects.all()


class NoteDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsAuthorOrStaff]
    queryset = Note.objects.all()
