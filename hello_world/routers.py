from rest_framework.routers import DefaultRouter
from rest_framework.routers import Route
from django.urls import path
class DynamicJSONRouter(DefaultRouter):
    def get_urls(self):
        urls = super().get_urls()

        # Add a custom route for dynamic key lookup
        # urls += [
        #     Route(
        #         url=r'^{prefix}/{lookup}$',
        #         mapping={'get':'retrieve_by_key'},
        #         name='{basename}-detail',
        #         detail=False,
        #         initkwargs={'suffix':'Detail'}
        #     )
        # ]

        # Replace custom Route with path()
        dynamic_urls = [
            path('mbh/<str:lookup>/',
                 self.registry[0][1].as_view(
                     {
                         'get': 'retrieve_by_key',

                     }
                 ),
                 name=f'{self.registry[0][0]}-detail')
        ]
        return urls+dynamic_urls
