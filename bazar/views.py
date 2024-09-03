from .serializers import sandoghSerializer
from .models import Sandogh, Asset
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.http import JsonResponse

class CalculateProfitView(CreateAPIView):
    serializer_class = sandoghSerializer
    permission_class = [AllowAny]
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        initial_amount = serializer.validated_data['initial_amount']
        start_month = serializer.validated_data['start_month']
        end_month = serializer.validated_data['end_month']

        results = []

        for asset in Asset.objects.all():
            current_assest = asset.name
            prices = asset.monthly_prices

            start_price = prices.get(start_month)
            end_price = prices.get(end_month)

            if start_price and end_price :
                profit = ((end_price - start_price) / start_price) * 100
                final_amount = initial_amount * (1 + profit / 100)

                results.append({
                    'assest': current_assest,
                    'profit_percentage': profit,
                    'final_amount': final_amount,
                })
                max_profit = max(results, key=lambda x: x['profit_percentage'])

        return Response({'results': results,
                         'max_profit' : max_profit})
    

def find_best_investment_period(request,name):
    best_profit = 0
    obj = Asset.objects.get(name=name)
    prices = obj.monthly_prices
    mounth_list = list(prices.keys())
    for start in range(len(mounth_list)):
        for end in range(start+1, len(mounth_list)):
            start_price = prices.get(mounth_list[start])
            end_price = prices.get(mounth_list[end])
            if start_price and end_price:
                profit = ((end_price - start_price) / start_price) * 100
                if profit > best_profit:
                    best_profit = profit
                    best_start_month = mounth_list[start]
                    best_end_month = mounth_list[end]
    return JsonResponse({
        'name': name,
        'best_profit': best_profit,
        'best_start_month': best_start_month,
        'best_end_month': best_end_month,
    })  

