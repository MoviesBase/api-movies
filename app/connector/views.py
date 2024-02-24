from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import permissions, status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from connector.operations import MoviesOperations
from connector.serializers import (
    MovieParameterSizeSerializer,
    MovieRequestSerializer,
    MoviesSerializer,
)


@extend_schema(tags=['movies'])
class MoviesView(viewsets.ViewSet):
    """
    Movies operations
    """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    serializer_class = MoviesSerializer
    serializer_class_request = MovieRequestSerializer
    serializer_class_parameters = MovieParameterSizeSerializer

    pagination_class = PageNumberPagination

    @extend_schema(
        responses={
            201: OpenApiResponse(
                description='Request success',
            ),
            400: OpenApiResponse(
                description='Invalid value',
            ),
            403: OpenApiResponse(
                description='Permission Denied',
            ),
            500: OpenApiResponse(
                description='Internal server error',
            ),
        },
        request=serializer_class_request,
    )
    def create(self, request):
        """
        Receives movies data for processing
        """
        serializer = self.serializer_class_request(request.data)
        serializer.is_valid(raise_exception=True)

        MoviesOperations().create_movie_record(
            movie_title=serializer.validated_data,
            context={'request': request},
        )

        return Response(
            data='Movie record created successfully',
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(
        responses={
            201: OpenApiResponse(
                description='Request success',
            ),
            400: OpenApiResponse(
                description='Invalid value',
            ),
            403: OpenApiResponse(
                description='Permission Denied',
            ),
            500: OpenApiResponse(
                description='Internal server error',
            ),
        },
        request=serializer_class,
    )
    def update(self, request):
        """
        Receives Movie data for processing
        """
        movie_id = request.data.get('id')

        movie_instance = MoviesOperations().get_movie_instance(movie_id)

        MoviesOperations().update_movie_record(
            movie_data=request.data,
            context={'request': request},
            movie_instance=movie_instance,
        )

        return Response(
            data='Movie record updated successfully',
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(
        responses={
            200: OpenApiResponse(
                description='Request success',
                response=serializer_class,
            ),
            404: OpenApiResponse(
                description='Resource not available',
            ),
            400: OpenApiResponse(
                description='Invalid value',
            ),
            403: OpenApiResponse(
                description='Permission Denied',
            ),
            500: OpenApiResponse(
                description='Internal server error',
            ),
        },
    )
    def retrieve(self, request, movie_id):
        """
        Returns the Movie data on given ID
        """
        movie_instance = MoviesOperations().get_movie_instance(movie_id)

        # Check if the authenticated user
        # has permission to retrieve this Movie data
        self.check_object_permissions(request, movie_instance)
        serializer = self.serializer_class(movie_instance)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        parameters=[serializer_class_parameters],
        responses={
            200: OpenApiResponse(
                description='Request success',
                response=serializer_class,
            ),
            404: OpenApiResponse(
                description='Resource not available',
            ),
            400: OpenApiResponse(
                description='Invalid value',
            ),
            403: OpenApiResponse(
                description='Permission Denied',
            ),
            500: OpenApiResponse(
                description='Internal server error',
            ),
        },
    )
    def list(self, request):
        """
        Returns all the movies from the database,
        ordered by title
        """
        # Get the title filter from query parameters, if provided
        title_filter = request.query_params.get('title')

        paginator = self.pagination_class()

        # Get the limit from query parameters, if provided
        # default=10
        page_size = request.query_params.get('limit', 10)

        paginator.page_size = page_size

        movies = MoviesOperations().get_all_movies(
            page_size=page_size, title_filter=title_filter
        )
        page = paginator.paginate_queryset(movies, request)

        serializer = self.serializer_class(page, many=True)

        return paginator.get_paginated_response(serializer.data)

    @extend_schema(
        responses={
            201: OpenApiResponse(
                description='Request success',
            ),
            404: OpenApiResponse(
                description='Resource not available',
            ),
            400: OpenApiResponse(
                description='Invalid value',
            ),
            403: OpenApiResponse(
                description='Permission Denied',
            ),
            500: OpenApiResponse(
                description='Internal server error',
            ),
        },
    )
    def delete(self, request, movie_id):
        """
        Deletes Movie data on given id
        """
        movie_instance = MoviesOperations().get_movie_instance(movie_id)

        MoviesOperations().delete_movie_record(movie_instance)

        return Response(
            {f'Movie data on id {movie_id} was successfully deleted'},
            status=status.HTTP_200_OK,
        )
