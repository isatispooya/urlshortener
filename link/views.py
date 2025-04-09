from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Link
from stats.models import Client
from user_agents import parse
from typing import Tuple
from urllib.parse import urlencode
import re

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

def clean_url(original_url: str) -> str:
    """این تابع برای تمیز کردن URL و اضافه کردن پروتکل https استفاده می‌شود."""
    if original_url.startswith('www.'):
        return 'https://' + original_url[4:]
    elif not original_url.startswith(('http://', 'https://')):
        return 'https://' + original_url
    return original_url

class LinkView(APIView):
    def get(self, request, short_url=None):
        """دریافت و ریدایرکت به URL مقصد"""
        if not short_url:
            return redirect('https://isatispooya.com')
            
        client_ip, is_routable = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        device, browser, os = get_device_info(user_agent)
        
        # دریافت تمام پارامترهای URL
        query_params = request.GET.dict()
        
        try:
            link = Link.objects.get(short_url=short_url)
            Client.objects.create(
                link=link,
                ip_address=client_ip,
                is_routable=is_routable,
                user_agent=user_agent,
                device=device,
                browser=browser,
                os=os
            )
            if 'utm_source' in query_params:
                link.utm_source = query_params['utm_source']
            if 'utm_medium' in query_params:
                link.utm_medium = query_params['utm_medium']
            if 'utm_campaign' in query_params:
                link.utm_campaign = query_params['utm_campaign']
            if 'utm_content' in query_params:
                link.utm_content = query_params['utm_content']
            if 'utm_term' in query_params:
                link.utm_term = query_params['utm_term']
            link.save()
            
            # اضافه کردن پارامترها به URL مقصد
            target_url = clean_url(link.original_url)
            if query_params:
                if '?' in target_url:
                    target_url += '&' + urlencode(query_params)
                else:
                    target_url += '?' + urlencode(query_params)
                    
            return redirect(target_url)
        except Link.DoesNotExist:
            return redirect('https://isatispooya.com')
        
    def post(self, request):
        """ایجاد لینک کوتاه از URL اصلی"""
        if 'original_url' not in request.data:
            return Response({'error': 'لینک صحیح وارد کنید'}, status=400)
        
        original_url = request.data['original_url']
        cleaned_url = clean_url(original_url)
        
        # اعتبارسنجی URL
        if not re.match(r'https?://[^\s/$.?#].[^\s]*$', cleaned_url):
            return Response({'error': 'لینک معتبر نیست'}, status=400)
        
        custom_url = request.data.get('custom')
        if not custom_url:
            link = Link.objects.create(original_url=cleaned_url)
        else:
            if Link.objects.filter(short_url=custom_url).exists():
                return Response({'error': 'این لینک قبلا استفاده شده است'}, status=400)
            link = Link.objects.create(original_url=cleaned_url, short_url=custom_url)
        
        return Response({'short_url': link.short_url})

    def patch(self, request, short_url=None):
        """به‌روزرسانی لینک با URL جدید"""
        if not short_url:
            return Response({'error': 'لینک صحیح وارد کنید'}, status=400)
        
        link = Link.objects.filter(short_url=short_url).first()
        if not link:
            return Response({'error': 'لینکی یافت نشد'}, status=404)
        
        original_url = request.data['original_url']
        cleaned_url = clean_url(original_url)
        
        # اعتبارسنجی URL
        if not re.match(r'https?://[^\s/$.?#].[^\s]*$', cleaned_url):
            return Response({'error': 'لینک معتبر نیست'}, status=400)
        
        link.original_url = cleaned_url
        link.save()
        return Response({'short_url': link.short_url})
