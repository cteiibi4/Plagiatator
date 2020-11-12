import json
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from .plagiatator import check_plagiat
from .common import FILE_DICT


class PlagiatatorView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        files = request.FILES['file']
        text_file = files.read().decode('utf-8')
        answer = check_plagiat(text_file)
        if answer is True:
            FILE_DICT.update({files.name: text_file})
            return Response({'answer': "OK"}, status=204)
        elif answer is False:
            return Response({'answer': "this file have low length"}, status=400)
        else:
            response = json.dumps(answer, ensure_ascii=False)
            return Response(response, status=501)
