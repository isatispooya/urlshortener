from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Client
from .serailzers import ClientSerializer
import pandas as pd

class ClientListView(APIView):
    def get(self, request):
        params = request.query_params
        link_params = params.get('link',None)
        query = Client.objects.all()
        if link_params:
            query = query.filter(link__short_url=link_params)
        utm_params = params.get('utm',None)
        if utm_params:
            query = query.filter(utm_source=utm_params)
        browser_params = params.get('browser',None)
        if browser_params:
            query = query.filter(browser=browser_params)
        os_params = params.get('os',None)
        if os_params:
            query = query.filter(os=os_params)
        device_params = params.get('device',None)
        if device_params:
            query = query.filter(device=device_params)
        ip_params = params.get('ip',None)
        if ip_params:
            query = query.filter(ip_address=ip_params)
            
            




        serializer = ClientSerializer(query, many=True)
        
      
        df = pd.DataFrame(serializer.data) 
        count_link = df['link_short_url'].value_counts().to_dict()
        count_utm = df['utm_source'].value_counts().to_dict()
        count_utm_medium = df['utm_medium'].value_counts().to_dict()
        count_utm_campaign = df['utm_campaign'].value_counts().to_dict()
        count_utm_content = df['utm_content'].value_counts().to_dict()
        count_utm_term = df['utm_term'].value_counts().to_dict()
        count_browser = df['browser'].value_counts().to_dict()
        count_os = df['os'].value_counts().to_dict()
        count_device = df['device'].value_counts().to_dict()
        count_ip = df['ip_address'].value_counts().to_dict()


        print(df)
        
      
        
        
        result = {
            'count_link': count_link,
            'count_utm': count_utm,
            'count_utm_medium': count_utm_medium,
            'count_utm_campaign': count_utm_campaign,
            'count_utm_content': count_utm_content,
            'count_utm_term': count_utm_term,
            'count_browser': count_browser,
            'count_os': count_os,
            'count_device': count_device,   
            'count_ip': count_ip,
        }

        return Response(result)

