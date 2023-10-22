from django.db import models

from vendor.models import Vendor


class Category(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=50, unique=True, error_messages={
        'unique': 'Category name already exist.'
    })
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=250, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    '''
        verbose_name: Thuộc tính này được sử dụng để đặt tên biểu đồ cho mô hình của bạn trong trường hợp đơn. 
        Ví dụ, nếu bạn có một mô hình có tên "Category", việc đặt verbose_name thành "category" sẽ khiến biểu đồ hiển thị "Category" khi đề cập đến mô hình này.

        verbose_name_plural: Thuộc tính này được sử dụng để đặt tên biểu đồ cho mô hình của bạn trong trường hợp số nhiều. 
        Ví dụ, nếu bạn đặt verbose_name_plural thành "categories", thì biểu đồ sẽ hiển thị "Categories" khi đề cập đến nhiều thể hiện của mô hình "Category".
    '''
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def clean(self) -> None:
        self.category_name = self.category_name.capitalize()

    def __str__(self) -> str:
        return self.category_name


class FoodItem(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    food_title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=250, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)     # max so thap phan la 10 va so thap phan sau dau phay la 2
    image = models.ImageField(upload_to='foodimages')
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.food_title
