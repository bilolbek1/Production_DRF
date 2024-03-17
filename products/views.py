from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Warehouse, Product
from .serializers import WarehouseSerializer


#Bu API omborxonada qanchadan xomashyolar borligi ro'yxati chiqariladi
class HomeApiView(APIView):
    def get(self, request):
        warehouses = Warehouse.objects.all()
        serializer = WarehouseSerializer(warehouses, many=True)
        return Response(serializer.data)




#Bu API post request orqali json formatda ma'lumot yani Mahsulot nomi [Ko'ylak yoki Shim]
#kirtiladi va shunga ko'ra qanchadan xomashyo kerakligi responseda chiqadi
class ResultApiView(APIView):
    def post(self, request):
        data = request.data
        product = data.get('product')
        materials_item = 0# Kiritilgan productning nomi belgilab olish uchun
        tshirt_material = {'Mato': 24, 'Tugma': 150, 'Ip': 300}# 30ta Ko'ylak uchun ketadigan xomashyolar
        shim_material = {'Mato': 28, 'Ip': 300, "Zamok": 20}# 20ta Shim uchun ketadigan xomashyolar
        if product == "Ko'ylak":# Kiritilgan product yani mahsulotni belgilab olish uchun
            materials_item = tshirt_material
        elif product == 'Shim':
            materials_item = shim_material
        result = [

        ]
        for key, value in materials_item.items():# Mahsulot belgilab olingandan so'ng
            # unga ketadigan xomashyolarni topish uchun
            overall = value # Overallni valuega tenglab olamiz
            warehouses = Warehouse.objects.filter(material_id__name=key).order_by('remainder')
            consumables = 0 #Agar kerakli material omborxonada bor yo'qligin hisoblash uchun
            for j in warehouses:
                if value == 0:
                    break
                if j.remainder <= value and j.remainder > 0: #Agar remainder yani xomashyoning
                    # qiymati  kerak bo'ladigan qiymatdan kichik yoki teng bo'lsa va remainder
                    # qiymati 0dan katta bo'lsa, biz hammasini olishimiz kerak
                    value = j.remainder
                    j.remainder -= value
                    j.save()
                    consumables += value
                    data = {
                            "warehouse_id": j.id,
                            "material_name": key,
                            "qty": value,
                            "price": j.price
                            }
                    result.append(data)
                elif j.remainder > value and warehouses.count() == 1 or j.remainder > value and value == overall:
                #Agar omborxonada qaysidir xomashyo 1ta kelgan bolsa va uning qiymati
                # kerak boladigan xomashyo qimatidan ko'proq bolsa, keraklichasini olsih kerak
                    value = value
                    j.remainder -= value
                    j.save()
                    consumables += value
                    data = {
                        "warehouse_id": j.id,
                        "material_name": key,
                        "qty": value,
                        "price": j.price
                    }
                    result.append(data)
                elif j.remainder > value:
                    #Agar xomashyo omborxonaga 1necha partiya kelgan bolsa va oldingisi
                    # yetmagan taqdirda, olinishi kerak bolgan xomashyo qiymatidan, bungacha
                    # olingan qiymatdan ayirib olsihimiz kerak, bu degani 300m ip kerak bo'lganida
                    # 1-sida 40m bor va 40m olinadi, keyin 2-sida 300m bor, 260 olish kerak degani
                    value = overall - value
                    j.remainder -= value
                    j.save()
                    consumables += value
                    data = {
                            "warehouse_id": j.id,
                            "material_name": key,
                            "qty": value,
                            "price": j.price
                            }
                    result.append(data)
            if overall != consumables:
                #Agar xomashyo omborda qolmasa null tariqasida bolsa ham qancha olish kerakligi
                # ko'rsatilishi uchun
                value = overall - value
                data = {
                    "warehouse_id": None,
                    "material_name": key,
                    "qty": value,
                    "price": None
                }
                result.append(data)

        data = {
            'products': product,
            'product_materials': result
        }
        return Response(data)







