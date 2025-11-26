from MHS_app.models import *
from MHS_app.serializers import *
from rest_framework.decorators import api_view , permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework import generics, filters
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.core.mail import send_mail
from django.conf import settings    
from rest_framework.views import APIView
from django.contrib.auth.tokens import default_token_generator

from django_filters.rest_framework import DjangoFilterBackend

from .filters import *
import random


# # User Views
@api_view(['POST'])
def Register(request, id=None):
    if request.method=='POST':
        username=request.data.get('username')
        first_name=request.data.get('first_name')
        last_name=request.data.get('last_name')
        password=request.data.get('password')
        email=request.data.get('email')
        contact=request.data.get('contact')
        # address=request.data.get('address')
        
    user=User.objects.create_user(
        username=username,
        first_name=first_name,
        last_name=last_name,
        password=password,
        email=email, 
        
    )
    
    
    customer=Customer.objects.create(user=user, contact=contact)

    Cart.objects.create(Customer_id=customer)
    return Response({"message": "User registered successfully, cart created"}, status=status.HTTP_201_CREATED)


# logout views
@api_view(['POST'])
def logout_view(request):
    refresh_token=request.data.get('refresh_token')
    if refresh_token:
        token=RefreshToken(refresh_token)
        token.blacklist()      #Blacklists (invalidates) the refresh token. token ko expire karna ya block karna     
        return Response('logout succesfull')
    else:
        return Response("provide refresh token")

# Product views
@api_view (['GET','POST','PUT','PATCH','DELETE'])
# @permission_classes([IsAuthenticated])
def product_view(request,id=None):
    if request.method=='GET':
        if id:
            try:
                pro=Product.objects.get(id=id)
                prod_serializers=Prodserializers(pro,many=True)
                return Response(prod_serializers.data)
            except Product.DoesNotExist:
                return Response("error found")
        else:
            pro=Product.objects.all()
            prod_serializers=Prodserializers(pro,many=True)
            return Response(prod_serializers.data)
    
            
            
    
    elif request.method=='POST':
        try:
            data=request.data
            prod_serializers=Prodserializers(data=data)
            if prod_serializers.is_valid():
                prod_serializers.save()
                return Response("message: data saved succesully")
        except prod_serializers.DoesNotExist:
                return Response('error')
    
    elif request.method=='PUT':
        try:
            data=request.data
            pro=Product.objects.get(id=id)
            prod_serializers=Prodserializers(pro,data=data,partial=True)
            if prod_serializers.is_valid():
                prod_serializers.save()
                return Response("message: data saved succesully")         
        except prod_serializers.DoesNotExist:
            return Response("error")
   
    elif request.method=='DELETE':
        d=Product.objects.get(id=id)
        d.delete()
        return Response("data deleted")

#Customer views
@api_view (['GET','POST','PUT','PATCH','DELETE'])
def customer_view(request,id=None):
    if request.method=='GET':
        cx=Customer.objects.all()
        cx_serializers=Customerserializers(cx,many=True)
        return Response(cx_serializers.data)
    
    elif request.method=='PUT':
        data=request.data
        cx=Customer.objects.get(id=id)
        cx_serializers=Customerserializers(cx,data=data,partial=True)
        if cx_serializers.is_valid():
            cx_serializers.save()
            return Response({"message: data saved succesully"})
        else:
            return Response(cx_serializers.errors)
   
    elif request.method=='DELETE':
        customer=Customer.objects.get(id=id)
        user=customer.user
        customer.delete()
        user.delete()
        return Response("data deleted")
        

# Cart views
@api_view (['GET','POST','PUT','PATCH','DELETE'])
def cart_view(request,id=None):
    if request.method=='GET':
        if id:
            try:
                cart=Cart.objects.get(id=id)
                cart_serializers=Cartserilalizer(cart,many=True) #(many=True)jab multiple object serialize karna ho
                return Response(cart_serializers.data)
            except Cart.DoesNotExist:
                return Response("cart not found ")
            
        else:
                cart=Cart.objects.all()
                cart_serializers=Cartserilalizer(cart,many=True)
                return Response(cart_serializers.data)

            
            
    
    
    elif request.method=='POST':
            try:
                cart_serializers=Cartserilalizer(data=request.data)
                if cart_serializers.is_valid():
                    cart_serializers.save()
                    return Response("message: data saved succesully")
                
            except Cart.DoesNotExist:
                return Response("error")
    
    

   
   
# cart item views
@api_view (['GET','POST','PUT','PATCH','DELETE'])
def cartt_item(request,id=None):
    if request.method=='GET':
        cart_item=Cartitem.objects.all()
        item_serializers=Cartitemserilalizer(cart_item,many=True)
        return Response(item_serializers.data)
    
    elif request.method=='POST':
        item_serializers=Cartitemserilalizer(data=request.data)
        if item_serializers.is_valid():
            item_serializers.save()
            return Response("message: data saved succesully")
        else:
            return Response(item_serializers.errors)
    
    elif request.method=='PUT':
        cart_item=Cartitem.objects.get(id=id)
        item_serializers=Cartitemserilalizer(cart_item,data=request.data,partial=True)
        if item_serializers.is_valid():
            item_serializers.save()
            return Response("message: data saved succesully")
        else:
            return Response(item_serializers.errors)
   
    elif request.method=='DELETE':
        cart_item=Cartitem.objects.get(id=id)
        cart_item.delete()
        return Response("data deleted")



# order views

    
    
    
# crud for employee 
@api_view (['GET','POST','PUT','DELETE'])
def Emp_view(request,id=None):
    if request.method=='GET':
        if id:
            try:
                emp=Employee.objects.get(id=id)
                emp_serializer=EMPserializer(emp,many=True)
                return Response(emp_serializer.data)
            except Employee.DoesNotExist:
                return Response("error found")
        else:
            emp=Employee.objects.all()
            emp_serializer=EMPserializer(emp,many=True)
            return Response(emp_serializer.data)
        
    elif request.method=='POST':
        emp_serializer=EMPserializer(data=request.data)
        if emp_serializer.is_valid():
            emp_serializer.save()
            return Response("messae saved succes") 
        else:
            return Response(emp_serializer.errors)


    elif request.method=='PUT':
        try:
            emp=Employee.objects.get(id=id)
            emp_serializer=EMPserializer(emp,data=request.data ,partial=True)
            if emp_serializer.is_valid():
                emp_serializer.save()
                return Response("data update succesully")
        except Employee.DoesNotExist:
                return Response('error found')

    elif request.method=='DELETE':
        try:
            
            emp=Employee.objects.get(id=id)
            emp.delete()
            return Response("Data delete succesully")
        except Employee.DoesNotExist:
            return Response("error foound")   



# Category views
@api_view (['GET','POST','PUT','DELETE'])
def category_view(request,id=None):
    if request.method=='GET':
        if id:
            try:
                category=Category.objects.get(id=id)
                cat_serializer=Category_serializer(category,many=True)
                return Response(Category_serializer.data)
            except Category.DoesNotExist:
                return Response("error found")
        else:
            category=Category.objects.all()
            cat_serializer=Category_serializer(category,many=True)
            return Response(cat_serializer.data)
        
    elif request.method=='POST':
        cat_serializer=Category_serializer(data=request.data)
        if cat_serializer.is_valid():
            cat_serializer.save()
            return Response("messae saved succes") 
        else:
            return Response(cat_serializer.errors)


    elif request.method=='PUT':
        try:
            category=Category.objects.get(id=id)
            cat_serializer=Category_serializer(category,data=request.data ,partial=True)
            if cat_serializer.is_valid():
                cat_serializer.save()
                return Response("data update succesully")
        except Category.DoesNotExist:
                return Response('error found')

    elif request.method=='DELETE':
        try:
            
            category=Category.objects.get(id=id)
            category.delete()
            return Response("Data delete succesully")
        except Category.DoesNotExist:
            return Response("error foound")   



# SubCategory views
@api_view (['GET','POST','PUT','DELETE'])
def sub_view(request,id=None):
    if request.method=='GET':
        if id:
            try:
                sub=SubCategory.objects.get(id=id)
                sub_seri=sub_serializer(sub,many=True)
                return Response(sub_seri.data)
            except SubCategory.DoesNotExist:
                return Response("error found")
        else:
            sub=SubCategory.objects.all()
            sub_seri=sub_serializer(sub,many=True)
            return Response(sub_seri.data)
        
    elif request.method=='POST':
        sub_seri=sub_serializer(data=request.data)
        if sub_seri.is_valid():
            sub_seri.save()
            return Response("messae saved succes") 
        else:
            return Response(sub_seri.errors)


    elif request.method=='PUT':
        try:
            sub=SubCategory.objects.get(id=id)
            sub_seri=sub_serializer(sub,data=request.data ,partial=True)
            if sub_seri.is_valid():
                sub_seri.save()
                return Response("data update succesully")
        except SubCategory.DoesNotExist:
                return Response('error found')

    elif request.method=='DELETE':
        try:
            
            sub=SubCategory.objects.get(id=id)
            sub.delete()
            return Response("Data delete succesully")
        except SubCategory.DoesNotExist:
            return Response("error foound")   






# Product_variation views
@api_view (['GET','POST','PUT','DELETE'])
def Pro_variation(request,id=None):
    if request.method=='GET':
        if id:
            try:
                Pro_variation=Product_variation.objects.get(id=id)
                Pro_variation_serializers=Product_variation_s(Pro_variation,many=True)
                return Response(Pro_variation_serializers.data)
            except Product_variation.DoesNotExist:
                return Response("error found")
        else:
            Pro_variation=Product_variation.objects.all()
            Pro_variation_serializers=Product_variation_s(Pro_variation,many=True)
            return Response(Pro_variation_serializers.data)
        
    elif request.method=='POST':
        Pro_variation_serializers=Product_variation_s(data=request.data)
        if Pro_variation_serializers.is_valid():
            Pro_variation_serializers.save()
            return Response("messae saved succes") 
        else:
            return Response(Product_variation_s.errors)


    elif request.method=='PUT':
        try:
            Pro_variation=Product_variation.objects.get(id=id)
            Pro_variation_serializers=Product_variation_s(Pro_variation,data=request.data ,partial=True)
            if Pro_variation_serializers.is_valid():
                Pro_variation_serializers.save()
                return Response("data update succesully")
        except Product_variation.DoesNotExist:
                return Response('error found')

    elif request.method=='DELETE':
        try:
            
            Pro_variation=Product_variation.objects.get(id=id)
            Pro_variation.delete()
            return Response("Data delete succesully")
        except Product_variation.DoesNotExist:
            return Response("error foound") 



# Variation Crud views      
@api_view (['GET','POST','PUT','DELETE'])
def variation_views(request,id=None):
    if request.method=='GET':
        if id:
            try:
                variation=Variation.objects.get(id=id)
                variation_serializers=Variation_serializers(variation,many=True)
                return Response(variation_serializers.data)
            except Variation.DoesNotExist:
                return Response("error found")
        else:
            variation=Variation.objects.all()
            variation_serializers=Variation_serializers(variation,many=True)
            return Response(variation_serializers.data)
        
    elif request.method=='POST':
        variation_serializers=Variation_serializers(data=request.data)
        if variation_serializers.is_valid():
            variation_serializers.save()
            return Response("messae saved succes") 
        else:
            return Response(variation_serializers.errors)


    elif request.method=='PUT':
        try:
            variation=Variation.objects.get(id=id)
            variation_serializers=Variation_serializers(variation,data=request.data ,partial=True)
            if variation_serializers.is_valid():
                variation_serializers.save()
                return Response("data update succesully")
        except Variation.DoesNotExist:
                return Response('error found')

    elif request.method=='DELETE':
        try:
            
            variation=Variation.objects.get(id=id)
            variation.delete()
            return Response("Data delete succesully")
        except Variation.DoesNotExist:
            return Response("error foound")   





# Variation option crud views 
@api_view (['GET','POST','PUT','DELETE'])
def variation_option(request,id=None):
    if request.method=='GET':
        if id:
            try:
                variation_option=Variation_option.objects.get(id=id)
                variation_option_serializers=Variation_option_serializers(variation_option,many=True)
                return Response(variation_option_serializers.data)
            except Variation_option.DoesNotExist:
                return Response("error found")
        else:
            variation_option=Variation_option.objects.all()
            variation_option_serializers=Product_variation_s(variation_option,many=True)
            return Response(variation_option_serializers.data)
        
    elif request.method=='POST':
        variation_option_serializers=Product_variation_s(data=request.data)
        if variation_option_serializers.is_valid():
            variation_option_serializers.save()
            return Response("messae saved succes") 
        else:
            return Response(variation_option_serializers.errors)


    elif request.method=='PUT':
        try:
            variation_option=Variation_option.objects.get(id=id)
            variation_option_serializers=Product_variation_s(variation_option,data=request.data ,partial=True)
            if variation_option_serializers.is_valid():
                variation_option_serializers.save()
                return Response("data update succesully")
        except Variation_option.DoesNotExist:
                return Response('error found')

    elif request.method=='DELETE':
        try:
            
            variation_option=Variation_option.objects.get(id=id)
            variation_option.delete()
            return Response("Data delete succesully")
        except Variation_option.DoesNotExist:
            return Response("error foound")   

# crud for address

@api_view (['GET','POST','PUT','DELETE'])
def Addresss(request,id=None):
    if request.method=='GET':
        if id:
            try:
                address=Address.objects.get(id=id)
                address_serializer=Adress_serializers(address,many=True)
                return Response(address_serializer.data)
            except Address.DoesNotExist:
                return Response("error found")
        else:
            address=Address.objects.all()
            address_serializer=Adress_serializers(address,many=True)
            return Response(address_serializer.data)
        
    elif request.method=='POST':
        address_serializer=Adress_serializers(data=request.data)
        if address_serializer.is_valid():
            address_serializer.save()
            return Response("messae saved succes") 
        else:
            return Response(address_serializer.errors)


    elif request.method=='PUT':
        try:
            address=Address.objects.get(id=id)
            address_serializer=Adress_serializers(address,data=request.data ,partial=True)
            if address_serializer.is_valid():
                address_serializer.save()
                return Response("data update succesully")
        except Address.DoesNotExist:
                return Response('error found')

    elif request.method=='DELETE':
        try:
            
            address=Address.objects.get(id=id)
            address.delete()
            return Response("Data delete succesully")
        except Address.DoesNotExist:
            return Response("error foound")   




# crud for order
@api_view (['GET','POST','PUT','DELETE'])
def Order_view(request,id=None):
    if request.method=='GET':
        if id:
            try:
                order=Order.objects.get(id=id)
                order_serializers=Order_serializers(order,many=True)
                return Response(order_serializers.data)
            except Order.DoesNotExist:
                return Response("error found")
        else:
            order=Order.objects.all()
            order_serializers=Order_serializers(order,many=True)
            return Response(order_serializers.data)
        
    elif request.method=='POST':
        order_serializers=Order_serializers(data=request.data)
        if order_serializers.is_valid():
            order_serializers.save()
            return Response("messae saved succes") 
        else:
            return Response(order_serializers.errors)


    elif request.method=='PUT':
        try:
            order=Order.objects.get(id=id)
            order_serializers=Order_serializers(order,data=request.data ,partial=True)
            if order_serializers.is_valid():
                order_serializers.save()
                return Response("data update succesully")
        except Order.DoesNotExist:
                return Response('error found')

    elif request.method=='DELETE':
        try:
            
            order=Order.objects.get(id=id)
            order.delete()
            return Response("Data delete succesully")
        except Order.DoesNotExist:
            return Response("error foound")   



@api_view (['GET','POST','PUT','DELETE'])
def Wishlist_view(request,id=None):
    if request.method=='GET':
        if id:
            try:
                wishlist=Wishlist.objects.get(id=id)
                wishlist_serializer=Wishlist_serializers(wishlist,many=True)
                return Response(wishlist_serializer.data)
            except Wishlist.DoesNotExist:
                return Response("error found")
        else:
            wishlist=Wishlist.objects.all()
            wishlist_serializer=Wishlist_serializers(wishlist,many=True)
            return Response(wishlist_serializer.data)
        
    elif request.method=='POST':
        wishlist_serializer=Wishlist_serializers(data=request.data)
        if wishlist_serializer.is_valid():
            wishlist_serializer.save()
            return Response("messae saved succes") 
        else:
            return Response(wishlist_serializer.errors)


    elif request.method=='PUT':
        try:
            wishlist=Wishlist.objects.get(id=id)
            wishlist_serializer=Wishlist_serializers(wishlist,data=request.data ,partial=True)
            if wishlist_serializer.is_valid():
                wishlist_serializer.save()
                return Response("data update succesully")
        except Wishlist.DoesNotExist:
                return Response('error found')

    elif request.method=='DELETE':
        try:
            
            wishlist=Wishlist.objects.get(id=id)
            wishlist.delete()
            return Response("Data delete succesully")
        except Wishlist.DoesNotExist:
            return Response("error foound")  






         
@api_view (['GET','POST','PUT','DELETE'])
def order_status(request,id=None):
    if request.method=='GET':
        if id:
            try:
                status=Order_Status.objects.get(id=id)
                status_serializer=Order_satus_s(status,many=True)
                return Response(status_serializer.data)
            except Order_Status.DoesNotExist:
                return Response("error found")
        else:
            status=Order_Status.objects.all()
            status_serializer=Order_satus_s(status,many=True)
            return Response(status_serializer.data)
        
    elif request.method=='POST':
        status_serializer=Order_satus_s(data=request.data)
        if status_serializer.is_valid():
            status_serializer.save()
            return Response("messae saved succes") 
        else:
            return Response(status_serializer.errors)


    elif request.method=='PUT':
        try:
            status=Order_Status.objects.get(id=id)
            status_serializer=Order_satus_s(status,data=request.data ,partial=True)
            if status_serializer.is_valid():
                status_serializer.save()
                return Response("data update succesully")
        except Order_Status.DoesNotExist:
                return Response('error found')

    elif request.method=='DELETE':
        try:
            
            status=Order_Status.objects.get(id=id)
            status.delete()
            return Response("Data delete succesully")
        except Order_Status.DoesNotExist:
           return Response("error foound")   



       
@api_view (['GET','POST','PUT','DELETE'])
def payment_view(request,id=None):
    if request.method=='GET':
        if id:
            try:
                payment=Payment.objects.get(id=id)
                payment_serializers=Payment_serializers(payment,many=True)
                return Response(payment_serializers.data)
            except Payment.DoesNotExist:
                return Response("error found")
        else:
            payment=Payment.objects.all()
            payment_serializers=Payment_serializers(payment,many=True)
            return Response(payment_serializers.data)
        
    elif request.method=='POST':
        payment_serializers=Payment_serializers(data=request.data)
        if payment_serializers.is_valid():
            payment_serializers.save()
            return Response("messae saved succes") 
        else:
            return Response(payment_serializers.errors)


    elif request.method=='PUT':
        try:
            payment=Payment.objects.get(id=id)
            payment_serializers=Payment_serializers(payment,data=request.data ,partial=True)
            if payment_serializers.is_valid():
                payment_serializers.save()
                return Response("data update succesully")
        except Payment.DoesNotExist:
                return Response('error found')

    elif request.method=='DELETE':
        try:
            
            payment=Payment.objects.get(id=id)
            payment.delete()
            return Response("Data delete succesully")
        except Payment.DoesNotExist:
            return Response("error foound")   




     
@api_view(['GET','POST','PUT','DELETE'])
def review_view(request,id=None):
    if request.method=='GET':
        if id:
            try:
                review=Review.objects.get(id=id)
                review_serializers=Review_serializers(review,many=True)
                return Response(review_serializers.data)
            except Review.DoesNotExist:
                return Response('error ')
        else:
            review=Review.objects.all()
            review_serializers=Payment_serializers(review,many=True)
            return Response(review_serializers.data)

    elif request.method == 'POST':
        review_serializers=Review_serializers(data=request.data)
        if review_serializers.is_valid():
            review_serializers.save()
            return Response('data saved succesfully')
        else:
            return Response(review_serializers.errors)
        


    elif request.method == 'PUT':
        try:
            review=Review.objects.get(id=id)
            review_seri=Review_serializers(review , data=request.data ,partial=True)
            if review_seri.is_valid():
                review_seri.save()
                return Response('data updated succesfully')
        except Review.DoesNotExist:
            return Response("error while updatingg the data ")

    elif request.method == 'DELETE':
        try:
            revir=Review.objects.get(id=id)
            revir.save()
        except Review.DoesNotExist:
                return Response('error while deleting the data')


#=============================only collection======================================
# @api_view(['GET','POST','PUT','DELETE'])       
# def Collection_view(request , id=None):
#     if request.method == 'GET':
#         if id:
#             try:
#                 collection=Collections.objects.get(id=id)
#                 collection_serializers=Collection_serializers(collection ,data=request.data)
#                 return Response(collection_serializers.data)
#             except Collections.DoesNotExist:
#                 return Response('unable to view data')

#         else :
#             collection=Collections.objects.all()
#             collection_serializers=Collection_serializers(collection ,many=True)
#             return Response(collection_serializers.data)


#     elif request.method == 'POST':
#         collection_serializers=Collection_serializers(data=request.data)
#         if collection_serializers.is_valid():
#             collection_serializers.save()
#             return Response('data saved succesfully')
#         else:
#             return Response(collection_serializers.errors)
        


#     elif request.method == 'PUT':
#         try:
#             collection=Collections.objects.get(id=id)
#             collection_serializers=Collection_serializers(collection , data=request.data ,partial=True)
#             if collection_serializers.is_valid():
#                 collection_serializers.save()
#                 return Response('data updated succesfully')
#         except Collections.DoesNotExist:
#             return Response("error while updatingg the data ")

#     elif request.method == 'DELETE':
#         try:
#             collection=Collections.objects.get(id=id)
#             collection.save()
#         except Collections.DoesNotExist:
#             return Response('error while deleting the data')
# ========================HTTP Collection=============================
@api_view(['GET','POST','PUT','PATCH','DELETE'])
def Collections_View(request,id=None):
    if request.method=='GET':
        col=Collections.objects.all()
        colserializer=Collection_serializers(col,many=True  , context={'request':request})
        return Response(colserializer.data)
    

    elif request.method=='POST':
        data=request.data
        colserializer=Collection_serializers(data=data ,context={'request':request})
        if colserializer.is_valid():
            colserializer.save()
            return Response("Collections added")
        else:
            return Response(colserializer.errors)

        
    elif request.method=='PUT':
        data=request.data
        col=Collections.objects.get(id=id)
        col_serializer=Collection_serializers(col,data=data,partial=True)
        if col_serializer.is_valid():
            col_serializer.save()
            return Response("collections Updated")
        else:
            return Response(col_serializer.errors)

    elif request.method=='DELETE':
        col=Collections.objects.get(id=id)
        col.delete()
        return Response("collections Deleted") 



# =========================All data =============================================================
# @api_view(['GET','POST','PUT','DELETE'])       
# def Quotation_view(request , id=None):
#     if request.method == 'GET':
#         if id:
#             try:
#                 quotation=Quotation.objects.get(id=id)
#                 quotation_serializers=Quotation_serializers(quotation ,data=request.data)
#                 return Response(quotation_serializers.data)
#             except Quotation.DoesNotExist:
#                 return Response('unable to view data')

#         else :
#             quotation=Quotation.objects.all()
#             quotation_serializers=Quotation_serializers(quotation ,many=True)
#             return Response(quotation_serializers.data)


#     elif request.method == 'POST':
#         quotation_serializers=Quotation_serializers(data=request.data)
#         if quotation_serializers.is_valid():
#             quotation_serializers.save()
#             return Response('data saved succesfully')
#         else:
#             return Response(quotation_serializers.errors)
        


#     elif request.method == 'PUT':
#         try:
#             quotation=Quotation.objects.get(id=id)
#             quotation_serializers=Quotation_serializers(quotation , data=request.data ,partial=True)
#             if quotation_serializers.is_valid():
#                 quotation_serializers.save()
#                 return Response('data updated succesfully')
#         except Quotation.DoesNotExist:
#             return Response("error while updatingg the data ")

#     elif request.method == 'DELETE':
#         try:
#             quotation=Quotation.objects.get(id=id)
#             quotation.save()
#         except Quotation.DoesNotExist:
#                 return Response('error while deleting the data')
# =======================Random quotes======================================================
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def Quotation_view(request, id=None):
    if request.method == 'GET':
        if id:
            try:
                quotation = Quotation.objects.get(id=id)
                quotation_serializers = Quotation_serializers(quotation)
                return Response(quotation_serializers.data)
            except Quotation.DoesNotExist:
                return Response({'error': 'Unable to view data'}, status=404)
        else:
            quotations = list(Quotation.objects.all())  # Convert to list for random selection
            if quotations:
                random_quotation = random.choice(quotations)  # Get a random quote
                quotation_serializers = Quotation_serializers(random_quotation)
                return Response(quotation_serializers.data)
            else:
                return Response({'message': 'No quotations available'}, status=404)

    elif request.method == 'POST':
        quotation_serializers = Quotation_serializers(data=request.data)
        if quotation_serializers.is_valid():
            quotation_serializers.save()
            return Response({'message': 'Data saved successfully'})
        else:
            return Response(quotation_serializers.errors, status=400)

    elif request.method == 'PUT':
        try:
            quotation = Quotation.objects.get(id=id)
            quotation_serializers = Quotation_serializers(quotation, data=request.data, partial=True)
            if quotation_serializers.is_valid():
                quotation_serializers.save()
                return Response({'message': 'Data updated successfully'})
            else:
                return Response(quotation_serializers.errors, status=400)
        except Quotation.DoesNotExist:
            return Response({'error': 'Error while updating the data'}, status=404)

    elif request.method == 'DELETE':
        try:
            quotation = Quotation.objects.get(id=id)
            quotation.delete()
            return Response({'message': 'Data deleted successfully'})
        except Quotation.DoesNotExist:
            return Response({'error': 'Error while deleting the data'}, status=404)                
                
#=============================password reset========================================


class ResetRequestView(APIView):
    def post(self, request):
        serializer = res(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get the user and generate a token
        email = serializer.validated_data['email']
        user = User.objects.filter(email=email).first()


        if not user:
            return Response({"error": "No user found with this email."}, status=status.HTTP_400_BAD_REQUEST)

        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)

        # Construct the reset link (example: "http://example.com/reset/<uid>/<token>/")
        reset_link = f"http://127.0.0.1:8000/reset/{token}/"

        # Send the email
        send_mail(
            subject="Password Reset Request",
            message=f"Click the link to reset your password: {reset_link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )

        return Response({"message": "Password reset link sent to your email."})




class PasswordResetConfirmView(APIView):
    def post(self, request,user_id , token):
        serializer = rs(data=request.data)
        serializer.is_valid(raise_exception=True)

        # user = request.data.get("user_id")  # Expecting user ID directly from request body
        # if not user:
        #     return Response({"error": "User ID is required."}, status=status.HTTP_400_BAD_REQUEST)


        try:
            user = User.objects.get(id=user_id)
        except (User.DoesNotExist, ValueError, TypeError):
            return Response({"error": "Invalid token or user."}, status=status.HTTP_400_BAD_REQUEST)

        token_generator = PasswordResetTokenGenerator()
        if token_generator.check_token(user, token):
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"message": "Password reset successful."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)



# ==============================================check user========================================================
@api_view(['GET'])
def U_view(request):
    if request.method=='GET':
        p=User.objects.all()
        ps=UserSerializer(p,many=True)
        return Response(ps.data)



# ================================filter search============================================


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = Prodserializers
    filter_backends = [DjangoFilterBackend]  # Enables filtering
    filterset_class = Product_filter  # Links the filter class


class Sub_ListView(generics.ListAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = sub_serializer
    filter_backends = [DjangoFilterBackend]  # Enables filtering
    filterset_class = Subcategory_filter  # Links the filter class


class Category_ListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = Category_serializer
    filter_backends = [DjangoFilterBackend]  # Enables filtering
    filterset_class = Category_filter  # Links the filter class    

class SubCategoryViewSet(generics.ListAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = sub_serializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SubCategoryFilter    

# =======================Cartitems get deleted as soon as order is placed==================
class OrderCreateView(generics.CreateAPIView):
    serializer_class = Order_serializers

    def perform_create(self, serializer):
        order= serializer.save(user=self.request.user)
        # Cart items will be deleted automatically from serializer
        return Response({"message": "Order placed successfully!"}, status=status.HTTP_201_CREATED)