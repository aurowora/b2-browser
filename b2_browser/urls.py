from django.urls import path
from browser.views import ls

urlpatterns = [
    path("<path:directory>", ls),
    path("", ls)
]
