import requests
from django.conf import settings
from django.utils.dateparse import parse_datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Item
from .serializers import ItemSerializer

class LatestItemView(APIView):
    def get(self, request, item_id):
        try:
            item = Item.objects.get(id=item_id)
            serializer = ItemSerializer(item) 
            return Response(serializer.data)  
        except Item.DoesNotExist:
            return Response({"error": "Item not found"}, status=404)

class ReadWithQuorumView(APIView):
    def get(self, request, item_id):
        other_servers = settings.SERVERS
        responses = []

        for server_url in other_servers:
            try:
                response = requests.get(f"{server_url}/api/get_latest_item/{item_id}")
                if response.status_code == 200:
                    responses.append(response.json())
            except requests.RequestException:
                continue 

        latest_data = self._get_data_by_quorum(responses)
        if latest_data:
            serializer = ItemSerializer(data=latest_data)
            if serializer.is_valid():  
                return Response(serializer.data)
        return Response({"error": "Кворум не достигнут"}, status=503)

    def _get_data_by_quorum(self, responses):
        if len(responses) < 2:
            return None
    
        responses.sort(key=lambda x: parse_datetime(x["last_updated"]), reverse=True)
        latest_data = responses[0]
    
        quorum_count = sum(
            1 for response in responses
            if response["name"] == latest_data["name"] and
               response["value"] == latest_data["value"]
        )
    
        if quorum_count >= 2:
            return latest_data
        return None
    
class UpdateItemView(APIView):
    def post(self, request, item_id):
        item_data = request.data
        try:
            item = Item.objects.get(id=item_id)
            serializer = ItemSerializer(item, data=item_data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=200)
            return Response(serializer.errors, status=400)
        except Item.DoesNotExist:
            return Response({"error": "Item not found"}, status=404)

class UpdateWithQuorumView(APIView):
    def post(self, request, item_id):
        item_data = request.data
        responses = []
        quorum_count = 0

        try:
            item = Item.objects.get(id=item_id)
            serializer = ItemSerializer(item, data=item_data, partial=True)
            if serializer.is_valid():
                serializer.save()
                responses.append(True)  
                quorum_count += 1  

                for server_url in settings.SERVERS:
                    try:
                        response = requests.post(f"{server_url}/api/update_item/{item_id}/", json=item_data)
                        if response.status_code == 200:
                            responses.append(True)
                            quorum_count += 1
                        else:
                            responses.append(False) 
                    except requests.RequestException:
                        responses.append(False)  

                if quorum_count >= 2:
                    return Response(serializer.data, status=200)
                else:
                    return Response({"error": "Кворум не достигнут"}, status=503)

            return Response(serializer.errors, status=400)
        except Item.DoesNotExist:
            return Response({"error": "Item not found"}, status=404)
