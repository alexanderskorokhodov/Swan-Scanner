from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
import django.conf.urls

from core.views import *
from startapp import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path('imageservice/', ImageServiceView.as_view(), name="some"),
    path('imageinfo/', ImageInfoView.as_view(), name="lolo"),
    path('deleteimage/', DeleteImageView.as_view(), name="lolo"),
    path('highlightimage/', HighlightImageView.as_view(), name="lolo"),
    path('rewritenote/', ReWriteNote.as_view(), name="lolo"),
    path('uploadimage/', ReWriteNote.as_view(), name="lolo")

]
