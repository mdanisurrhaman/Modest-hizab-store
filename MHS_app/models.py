from django.db import models
from django.contrib.auth.models import User
# from phonenumber_field.modelfields import PhoneNumberField





# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)#(CASCADE MEANS)on_delete behavior (Agar parent object delete ho jaye, toh uske saare related child objects bhi automatically delete ho jayein.)
    contact = models.BigIntegerField()


    def _str_(self):
            return self.user.username



class Employee(models.Model):
        user_id = models.OneToOneField(User,on_delete=models.CASCADE)
        salary=models.BigIntegerField()
        contact = models.BigIntegerField()
        address = models.CharField(max_length=100)

        def _str_(self):
            return self.user_id.username    



class Product (models.Model):
    Product_description=models.CharField(max_length=9000)
    Sub_category_id = models.ForeignKey('SubCategory', related_name="products", on_delete=models.CASCADE)
    Availability=models.CharField(max_length=500)
    Stock=models.IntegerField()
    Price=models.BigIntegerField()
    
    

class SubCategory(models.Model):
    Sub_Category_Name=models.CharField(max_length=200,null=True)
    Category_id=models.ForeignKey('Category' ,on_delete=models.CASCADE ,related_name='category')


# class SubCategory(models.Model):
#     sub_category_name = models.CharField(max_length=200, null=True)  # Use lowercase with underscores
#     category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='subcategories')  
#     # 'related_name' allows reverse access from Category -> SubCategory

#     def __str__(self):
#         return self.sub_category_name


class Category(models.Model):
    Category_name=models.CharField(max_length=100)
    Category_image=models.ImageField(upload_to="category")





class Product_variation(models.Model):
    Product_id=models.ForeignKey(Product ,on_delete=models.CASCADE )
    option_id=models.ForeignKey("Variation_option" ,on_delete=models.CASCADE )




class Variation_option(models.Model):
    variation_id=models.ForeignKey('Variation' ,on_delete=models.CASCADE)
    value=models.CharField(max_length=200)
    


class Variation(models.Model):
    variation_name=models.CharField(max_length=200)

    # def _str_(self):
    #         return self
        
class Image(models.Model):
    img_path=models.ImageField(upload_to='Image')
    product_variation_id=models.ForeignKey(Product_variation, on_delete=models.CASCADE)
        
        
        
class Cart(models.Model):
    Customer_id=models.ForeignKey(Customer,on_delete=models.CASCADE)
    
    
class Cartitem(models.Model):
    Cart_id=models.ForeignKey(Cart , on_delete=models.CASCADE, related_name='cartitem')
    Product_id=models.ForeignKey(Product , on_delete=models.CASCADE )
    Quantity=models.IntegerField()
    Cart_Total=models.BigIntegerField()
    
    
    
    # def _str_(self):
    #      return self.product.product_name
     



class Collections(models.Model):
    Collection_image=models.ImageField(upload_to='Collection')



class Quotation(models.Model):
    Quote=models.CharField(max_length=50)



class Most_Popular(models.Model):
    popular_image=models.ImageField(upload_to='Popular')



        

class Address(models.Model):
    user_id=models.ForeignKey(User, on_delete=models.CASCADE)
    Address_type=models.CharField(max_length=50)
    Name=models.CharField(max_length=50)
    House_No=models.CharField(max_length=50)
    Area_Colony=models.CharField(max_length=50)
    Landmark=models.CharField(max_length=50)
    Pincode=models.BigIntegerField()
    City=models.CharField(max_length=50)
    State=models.CharField(max_length=50)
    Country=models.CharField(max_length=50)
    Contact=models.BigIntegerField()


    def _str_(self):
        return f"{self.House_No}, {self.City}, {self.State}, {self.Pincode}, {self.Country}"




class Wishlist(models.Model):
    customer_id=models.ForeignKey(Customer , on_delete=models.CASCADE)
    product_id=models.ForeignKey(Product, on_delete=models.CASCADE)
    addTime=models.DateTimeField()




class Order(models.Model):
    Order_Date=models.DateField()
    Cart_id=models.ForeignKey(Cart ,on_delete=models.CASCADE)
    Delivery_Address=models.OneToOneField(Address , on_delete=models.CASCADE)
    Duration=models.IntegerField()
    Payment_id=models.OneToOneField("Payment", on_delete=models.CASCADE)
    Payment_Confirmation=models.IntegerField()




class Order_Status(models.Model):
    order_id=models.ForeignKey(Order, on_delete=models.CASCADE)
    order_status=models.CharField(max_length=50)


class Payment(models.Model):
    Payment_mode=models.CharField(max_length=50)






class Review(models.Model):
    Customer_id=models.ForeignKey(Customer, on_delete=models.CASCADE)
    Product_id=models.ForeignKey(Product ,on_delete=models.CASCADE)

    Review=models.CharField(max_length=50)
    Ratings=models.IntegerField()



    # =========================password reset no models=================================


