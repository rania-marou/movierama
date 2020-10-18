from django.urls import path, include

from drf_yasg2.views import get_schema_view
from drf_yasg2 import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Movierama API",
        default_version='v1',
        contact=openapi.Contact(email="rania.marou@gmail.com")
    ),
    public=True,
)

urlpatterns = [
    # MovieRama API
    path('api/', include('api.urls')),

    # MovieRama Documentation
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
