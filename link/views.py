from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Link, Stats
from django.shortcuts import redirect
from user_agents import parse
from typing import Tuple
from urllib.parse import urlencode

def get_client_ip(request) -> Tuple[str, bool]:
    """
    بهینه‌ترین روش برای دریافت IP کاربر با در نظر گرفتن امنیت
    returns: (ip, is_routable)
    """
    TRUSTED_PROXIES = {
        'HTTP_X_FORWARDED_FOR',
        'HTTP_X_REAL_IP',
        'HTTP_CLIENT_IP',
        'HTTP_X_FORWARDED',
        'HTTP_X_CLUSTER_CLIENT_IP',
        'HTTP_FORWARDED_FOR',
        'HTTP_FORWARDED',
        'HTTP_VIA',
    }
    
    remote_addr = request.META.get('REMOTE_ADDR', '0.0.0.0')
    
    client_ip = remote_addr
    is_routable = False
    
    for header in TRUSTED_PROXIES:
        forwarded_ips = request.META.get(header, '').split(',')
        if forwarded_ips and forwarded_ips[0].strip():
            client_ip = forwarded_ips[0].strip()
            if not (
                client_ip.startswith(('10.', '172.16.', '192.168.')) or
                client_ip == '127.0.0.1'
            ):
                is_routable = True
                break
    
    return client_ip or '0.0.0.0', is_routable

def get_device_info(user_agent_string):
    user_agent = parse(user_agent_string)
    device = user_agent.device.family
    browser = user_agent.browser.family
    os = user_agent.os.family
    return device, browser, os

class LinkView(APIView):
    def get(self, request, short_url=None):
        if not short_url:
            return redirect('https://isatispooya.com')
            
        client_ip, is_routable = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        device, browser, os = get_device_info(user_agent)
        
        # دریافت تمام پارامترهای URL
        query_params = request.GET.dict()
        
        try:
            link = Link.objects.get(short_url=short_url)
            Stats.objects.create(
                link=link,
                ip_address=client_ip,
                is_routable=is_routable,
                user_agent=user_agent,
                device=device,
                browser=browser,
                os=os
            )
            
            # اضافه کردن پارامترها به URL مقصد
            target_url = link.original_url
            if query_params:
                if '?' in target_url:
                    target_url += '&' + urlencode(query_params)
                else:
                    target_url += '?' + urlencode(query_params)
                    
            return redirect(target_url)
        except Link.DoesNotExist:
            return redirect('https://isatispooya.com')
        
    def post(self, request):
        if 'original_url' not in request.data:
            return Response({'error': 'لینک صحیح وارد کنید'}, status=400)
        link = Link.objects.create(original_url=request.data['original_url'])
        return Response({'short_url': link.short_url})

