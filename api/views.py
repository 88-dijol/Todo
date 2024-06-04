from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from api.serializers import Registration,User,todoserializer
from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework import authentication,permissions
from work.models import Taskmodel
from rest_framework import status
from api.permission import OwnerOnly



class Userregister(APIView):
    def post(self,request,*args,**kwargs):
        serializer=Registration(data=request.data)
        if serializer.is_valid():
            serializer.save() #create
        return Response(serializer.data)


# headers use cheyanel auth none aayirikynam
# authorization      Token xyz
class Todoviewsetview(ViewSet):

    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def list(self,request,*args,**kwargs):
        qs=Taskmodel.objects.all()
        serializer=todoserializer(qs,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    

    def create(slef,request,*args,**kwargs):
        serializer=todoserializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    

    # update,retrieve
    def put(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        qs=Taskmodel.objects.get(id=id)
        if qs.user==request.user:
            serializer=todoserializer(data=request.data,instance=qs)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response({"message":"can't update"})
        

    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        qs=Taskmodel.objects.get(id=id)
        if qs.user==request.user:
            serilaizer=todoserializer(qs)
            return Response(serilaizer.data,status=status.HTTP_202_ACCEPTED)
        else:
            return Response({"message":"there is no data found in this id  for this user"})
        
    
    def destroy(slef,request,*args,**kwargs):
        id=kwargs.get('pk')
        qs=Taskmodel.objects.get(id=id)
        if qs.user==request.user:
            qs.delete()
            return Response({"message":"todo object is destroyed"})
        else:
            return Response({"message":"not allowed"})

    

class Todomodelviewset(ModelViewSet):    #LCRUD
    queryset=Taskmodel.objects.all()
    serializer_class=todoserializer
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[OwnerOnly]



    # def get_queryset(self):
    #     return Taskmodel.objects.filter(user=self.request.user)  



        


