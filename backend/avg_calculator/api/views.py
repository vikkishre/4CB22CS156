from django.shortcuts import render
import requests
from collections import deque
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
import time

WINDOW_SIZE = 10
window = deque(maxlen=WINDOW_SIZE)

VALID_IDS = {
    'p': 'http://20.244.56.144/test/primes',
    'f': 'http://20.244.56.144/test/fibo',
    'e': 'http://20.244.56.144/test/even',
    'r': 'http://20.244.56.144/test/rand'
}

@api_view(['GET'])
def get_numbers(request, numberid):
    numbers = []

    if numberid not in VALID_IDS:
        return Response({'error': 'Invalid number ID'}, status=400)

    url = VALID_IDS[numberid]
    window_prev = list(window)

    try:
        start = time.time()
         headers={
             #Your access tokens
         }
        response = requests.get(url,headers=headers, timeout=0.5)
        end = time.time()

        # if response.status_code != 200 or (end - start) < 0.5:
        #     raise Exception("Slow or failed response")

        numbers = response.json().get('numbers', [])

        for num in numbers:
            if num not in window:
                window.append(num)

    except Exception as e:
        print("Exception:", e)

    window_curr = list(window)
    avg = round(sum(window) / len(window), 2) if window else 0

    return Response({
        'window_prev_state': window_prev,
        'window_current_state': window_curr,
        'numbers': numbers,
        'average': avg
    })
