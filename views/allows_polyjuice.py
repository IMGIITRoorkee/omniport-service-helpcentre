from rest_framework import generics, response, status, permissions

from helpcentre.serializers.allows_polyjuice import AllowsPolyjuiceSerializer


class AllowsPolyjuiceView(generics.GenericAPIView):
    """
    Set the ``allows_polyjuice`` field on the user model to ``true``
    """

    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = AllowsPolyjuiceSerializer

    def get(self, request, *args, **kwargs):
        """
        Return whether polyjuice is allowed or not for the logged in user
        """
        polyjuice_allowed = request.user.allows_polyjuice
        response_data = {
            'polyjuice_allowed': polyjuice_allowed
        }
        return response.Response(
            data=response_data,
            status=status.HTTP_200_OK
        )

    def post(self, request, *args, **kwargs):
        """
        View to serve POST requests
        :param request: the request that is to be responded to
        :param args: arguments
        :param kwargs: keyword arguments
        :return: the response for request
        """

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            user.allows_polyjuice = serializer.data['allows_polyjuice']
            user.save()
            response_data = {
                'polyjuice_allowed': user.allows_polyjuice
            }
            return response.Response(
                data=response_data,
                status=status.HTTP_200_OK
            )
        else:
            response_data = {
                'errors': serializer.errors
            }
            return response.Response(
                data=response_data,
                status=status.HTTP_400_BAD_REQUEST
            )
