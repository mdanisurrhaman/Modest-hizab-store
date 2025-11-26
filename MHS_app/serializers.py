from rest_framework import serializers
from MHS_app.models import *
from django.contrib.auth.models import User

from rest_framework.exceptions import AuthenticationFailed





class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','username','first_name','last_name','password','email']

class Customerserializers(serializers.ModelSerializer):
    user=UserSerializer()
    class Meta:
        model=Customer
        fields=['id','user','contact']

    # def create(self,validated_data):
    #         user=validated_data.pop("user")
    #         user_instance=User.objects.create_user(**user)
    #         customer=Customer.objects.create(user=user_instance,**validated_data)
    #         return customer

    def update(self,instance,validated_data):
            user_data=validated_data.pop('user',None)
            if user_data:
                user_instance=instance.user
                user_serializer=UserSerializer()
                user_serializer.update(user_instance,user_data)

            instance=super().update(instance,validated_data)
            return instance



class Prodserializers(serializers.ModelSerializer):
    Sub_category_id=serializers.PrimaryKeyRelatedField(queryset=SubCategory.objects.all())
    class Meta:
        model=Product
        fields=['id', 'Sub_category_id', 'Product_description', 'Availability', 'Stock', 'Price']

class Cartitemserilalizer(serializers.ModelSerializer):
    product=serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True)
    Product_id=Prodserializers(read_only=True)
    class Meta:
        model=Cartitem
        fields=['id','Product_id','Cart_id','Quantity','Cart_Total','product']  
 
     
        
class Cartserilalizer(serializers.ModelSerializer):
    cart_item=serializers.PrimaryKeyRelatedField(queryset=Cart.objects.all(), write_only=True)
    cartitem=Cartitemserilalizer(many=True,read_only=True)
    Customer_id=Customerserializers(read_only=True)
    
    # cartitem=serializers.StringRelatedField(many=True)
    class Meta:
        model=Cart
        fields=['cartitem','id','Customer_id','cart_item']


        
        
        
        
        
        
class EMPserializer(serializers.ModelSerializer):
    user_id=UserSerializer()
    class Meta:
        model=Employee
        fields=['id','user_id','salary','contact','address']

    def create(self,validated_data):
            user_id=validated_data.pop("user_id")
            user_instance=User.objects.create_user(**user_id)
            customer=Employee.objects.create(user_id=user_instance , **validated_data)
            return customer

    def update(self,instance,validated_data):
            user_data=validated_data.pop("user_id",None)
            if user_data:
                user_instance=instance.user_id
                user_serializer=UserSerializer()
                user_serializer.update(user_instance, user_data)

            instance=super().update(instance,validated_data)
            return instance




class Category_serializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields='__all__'



class sub_serializer(serializers.ModelSerializer):
    category=Category_serializer(read_only=True)
    Categoryy=serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), write_only=True , source='Category_id')
    class Meta:
        model=SubCategory
        fields=['id', 'Sub_Category_Name', 'category', 'Categoryy']               
        
        




class Product_variation_s(serializers.ModelSerializer):
    class Meta:
        model=Product_variation
        fields="__all__"




class Variation_option_serializers(serializers.ModelSerializer):
    class Meta:
        model=Variation_option
        fields='__all__'

        
class Variation_serializers(serializers.ModelSerializer):
    class Meta:
        model=Variation
        fields='__all__'



class Collection_serializers(serializers.ModelSerializer):
    class Meta:
        model=Collections
        fields='__all__'

class Quotation_serializers(serializers.ModelSerializer):
    class Meta:
        model=Quotation
        fields='__all__'
        
class Most_Popular_serializers(serializers.ModelSerializer):
    class Meta:
        model=Most_Popular
        fields='__all__'



class Adress_serializers(serializers.ModelSerializer):
    user_id=UserSerializer(read_only=True)
    user=serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True , source='user_id')

    class Meta:
        model=Address
        fields=['id','user_id','Address_type','Name','House_No','Area_Colony','Landmark','Pincode','City','State','Country','Contact','user']


class Wishlist_serializers(serializers.ModelSerializer):
    customer_id=Customerserializers(read_only=True)
    product_id=Prodserializers(read_only=True)
    class Meta:
        model=Wishlist
        fields='__all__'

class Payment_serializers(serializers.ModelSerializer):
    class Meta:
        model=Payment
        fields="__all__"



class Order_serializers(serializers.ModelSerializer):
    Cart_id=Cartserilalizer(read_only=True)
    Delivery_Address=Adress_serializers(read_only=True)
    Payment_id=Payment_serializers(read_only=True)
    Cart_idd=serializers.PrimaryKeyRelatedField(queryset=Cart.objects.all(), write_only=True ,source='Cart_id')
    Delivery_Addresss=serializers.PrimaryKeyRelatedField(queryset=Address.objects.all(), write_only=True,source='Delivery_Address' )
    Payment_idd=serializers.PrimaryKeyRelatedField(queryset=Payment.objects.all(), write_only=True ,source='Payment_id' )
    class Meta:
        model=Order
        fields=['id','Order_Date','Cart_id','Delivery_Address','Duration'
                ,'Payment_id','Payment_Confirmation','Cart_idd','Delivery_Addresss','Payment_idd']
        
    def create(self, validated_data):
        order = Order.objects.create(**validated_data)
        # Delete all cart items of the user after order is placed
        Cartitem.objects.filter(user=order.user).delete()
        return order        


class Order_satus_s(serializers.ModelSerializer):
    order_id=Order_serializers(read_only=True)
    class Meta:
        model=Order_Status
        fields="__all__"


class Review_serializers(serializers.ModelSerializer):
    Customer_id=Customerserializers(read_only=True)
    Product_id=Prodserializers(read_only=True)
    class Meta:
        model=Review
        fields="__all__"
# ============================================================================
class res(serializers.Serializer):
    email = serializers.EmailField()



class rs(serializers.Serializer):
    new_password = serializers.CharField(write_only=True,min_length=8)








