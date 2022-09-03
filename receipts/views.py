from django.shortcuts import render
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView, RetrieveAPIView
# from .serializers import ReceiptListSerializer, ReceiptCreateSerializer
from .serializers import ReceiptSerializer
from rest_framework.response import Response
from rest_framework import status
from posts.models import Post
from posts.models import Post
from receipts.models import Receipt
from datetime import datetime
import boto3
import base64
from django.conf import settings
from consumptions.utils import delete_image

class ReceiptCreateAPIView(CreateAPIView):
  # LOGIC : 해당 탭에 들어왔을 때 이미 post_id값과 date값을 가지고 있어야 함
  # 두 가지 값을 가지고 새로운 receipt 객체 생성
  # queryset = Post.objects.all()
  queryset = Receipt.objects.all() # 차이? **
  # serializer_class = ReceiptCreateSerializer
  serializer_class = ReceiptSerializer

  def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

  def create(self, request, *args, **kwargs):
        # request.data에 담겨야할 정보 : "created_at"(str, unix timestamp), "image"(str, base64)
        # TODO: request.data에서 입력받은 날짜를 post_id로 변환 / image S3객체 후 image_url 반환
        # 1)POST_ID 추출
        author = request.user
        date = request.data['created_at']
        formatted_date = datetime.fromtimestamp(int(date)/1000)
        try:
          post = Post.objects.get(author=author, created_at=formatted_date)
        except Post.DoesNotExist:
          data = {
            "err_msg" : "해당 날짜에 존재하는 포스트가 없습니다(또는 2개 이상입니다.)"
          }
          return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        
        # 2)IMAGE s3객체 생성 후 image_url 추출
        image_string = request.data['image']
        year = formatted_date.strftime('%Y')
        month = formatted_date.strftime('%m')
        day = formatted_date.strftime('%d')
        header, data = image_string.split(';base64,')
        if Receipt.objects.last() == None:
          receipt_id = 1
        else:
          receipt_id = int(Receipt.objects.last().id) + 1
        # header, data = image_string[num].split(';base64,') # 리스트째로 들어옴!
        data_format, ext = header.split('/')
        try:
          image_data = base64.b64decode(data) # 이미지 파일 생성
          s3r = boto3.resource('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
          key = "%s"%(f'{year}/{month}/{day}')
          s3r.Bucket(settings.AWS_STORAGE_BUCKET_NAME).put_object(Key=key+'/%s'%(f'{post.id}_receipt_{receipt_id}.{ext}'), Body=image_data, ContentType='jpg')
          aws_url = f'{settings.IMAGE_URL}/{year}/{month}/{day}/{post.id}_receipt_{receipt_id}.{ext}'
        except TypeError:
          self.fail('invalid_image')

        receipt_data = {
          'post' : post.id,
          'image' : aws_url,
        }
        serializer = self.get_serializer(data=receipt_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# 해당 날짜와 해당 유저의 영수증을 불러오는 APIView(ListAPIView)
class ReceiptListAPIView(ListAPIView):

  # serializer_class = ReceiptListSerializer
  serializer_class = ReceiptSerializer

  def get_queryset(self):
    author = self.request.user
    date = self.request.query_params.get('date')
    formatted_date = datetime.fromtimestamp(int(date)/1000)
    # print(author, formatted_date)
    try:
      post = Post.objects.get(author=author, created_at=formatted_date)
    except Post.DoesNotExist:
      data = {
        "err_msg" : "해당 날짜에 존재하는 포스트가 없습니다(또는 2개 이상입니다.)"
      }
      # return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
      return # 임시 예외처리(해당 날짜에 포스트 존재하지 않으면 빈 리스트 리턴)
    queryset = Receipt.objects.filter(post=post)
    return queryset

class ReceiptDetailAPIView(RetrieveAPIView):
  queryset = Receipt.objects.all()
  serializer_class = ReceiptSerializer

# 영수증 객체 삭제 APIView(DestroyAPIView)
class ReceiptDeleteAPIView(DestroyAPIView):
  queryset = Receipt.objects.all()
  serializer_class = ReceiptSerializer

  def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

  def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

  def perform_destroy(self, instance):
      # print(instance)
      # print(instance.image) # https://s3.ap-northeast-2.amazonaws.com/jinhyung.test.aws/2022/12/01/11_receipt_5.jpeg
      # s3 이미지 삭제
      delete_image(instance.image)
      instance.delete()