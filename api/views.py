from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import WishModel
from .serializer import WishModelSerializer


@api_view(['GET'])
def api_overview(request):
    api_urls = {
        'List': '/wish-list/',
        'Detail View': '/wish-detail/<str:pk>/',
        'Create': '/wish-create/',
        'Update': '/wish-update/<str:pk>/',
        'Delete': '/wish-delete/<str:pk>/',
    }
    return Response(api_urls)


@api_view(['GET'])
def wish_list(request):

    wishes = WishModel.objects.all().filter(user=request.user).order_by('-id')
    serializer = WishModelSerializer(wishes, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def wish_detail(request, pk):
    wishes = WishModel.objects.get(id=pk)
    serializer = WishModelSerializer(wishes, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def wish_create(request):
    serializer = WishModelSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
    return Response(serializer.data)


@api_view(['POST'])
def wish_update(request, pk):
    wish = WishModel.objects.get(id=pk)
    serializer = WishModelSerializer(instance=wish, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['DELETE'])
def wish_delete(request, pk):
    wish = WishModel.objects.get(id=pk)
    wish.delete()
    return Response('Item successfully deleted!')

