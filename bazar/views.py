from .serializers import SandoghSerializer, AssetSerializer, ProfitCalculationHistorySerializer
from .models import Sandogh, Asset, ProfitCalculationHistory
from rest_framework.generics import CreateAPIView, ListCreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.response import Response
from django.http import JsonResponse
from django.views import View

class Login(TokenObtainPairView):
    pass


class Refresh(TokenRefreshView):
    pass


class CalculateProfitView(CreateAPIView):
    serializer_class = SandoghSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        sandogh = Sandogh.objects.filter(user=request.user).first()

        if not sandogh:
            return Response({"error": "This user does not have any sandogh"}, status=400)

        initial_amount = sandogh.initial_amount
        start_month = sandogh.start_month
        end_month = sandogh.end_month

        results = []

        for asset in sandogh.assets.all():
            current_asset = asset.name
            prices = asset.monthly_prices

            start_price = prices.get(start_month)
            end_price = prices.get(end_month)

            if start_price and end_price:
                profit = ((end_price - start_price) / start_price) * 100
                final_amount = initial_amount * (1 + profit / 100)

                results.append({
                    'asset': current_asset,
                    'profit_percentage': profit,
                    'final_amount': final_amount,
                })

        if results:
            max_profit = max(results, key=lambda x: x['profit_percentage'])

            ProfitCalculationHistory.objects.create(
                user=request.user,
                initial_amount=initial_amount,
                start_month=start_month,
                end_month=end_month,
                results=results
            )

            return Response({'results': results, 'max_profit': max_profit})
        else:
            return Response({"error": "There is no data to calculate"}, status=400)
    

class FindBestInvestmentPeriodView(View):
    def get(self, request, name):
        best_profit = 0
        best_start_month = ''
        best_end_month = ''
        
        try:
            obj = Asset.objects.get(name=name)
        except Asset.DoesNotExist:
            return JsonResponse({'error': 'Asset not found'}, status=404)

        prices = obj.monthly_prices
        month_list = list(prices.keys())
        
        for start in range(len(month_list)):
            for end in range(start + 1, len(month_list)):
                start_price = prices.get(month_list[start])
                end_price = prices.get(month_list[end])
                
                if start_price and end_price:
                    profit = ((end_price - start_price) / start_price) * 100
                    if profit > best_profit:
                        best_profit = profit
                        best_start_month = month_list[start]
                        best_end_month = month_list[end]
        
        return JsonResponse({
            'name': name,
            'best_profit': f'{best_profit}%',
            'best_start_month': best_start_month,
            'best_end_month': best_end_month,
        })

class ListCreateAsset(ListCreateAPIView):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    permission_classes = [IsAuthenticated]

class ListCreateSandogh(ListCreateAPIView):
    queryset = Sandogh.objects.all()
    serializer_class = SandoghSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Sandogh.objects.filter(user = self.request.user)
    

class ProfitCalculationHistoryView(ListAPIView):
    serializer_class = ProfitCalculationHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ProfitCalculationHistory.objects.filter(user=self.request.user)