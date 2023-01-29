#1)Say you have 10 million rows in a db table represented by a django model. How do you efficiently load all of these, run a function on them and then write some changes back to the db.

#Approach 01: 
# One way to efficiently load and update a large number of rows in a Django model is
# to use the "update()" method in combination with the "values()" method. This allows 
# you to update multiple rows at once, without having to load them into memory all at 
# once.
# Here's an example of how you might use this method to update all 
# rows in a table, run a function on them, and then write some changes 
# back to the database:
from django.db.models import F

# My function
def my_function(row):
    # Do something with the row
    row.column1 = row.column1 + 1
    return row

# Load the rows in chunks
for chunk in range(0, 1000000, 10000):  #range(start, stop, step)
    rows = MyModel.objects.all()[chunk:chunk+10000]
    # Apply the function to the rows
    rows = [my_function(row) for row in rows]
    # Update the rows in the database
    MyModel.objects.filter(id__in=[row.id for row in rows]).update(column1="updated")



# In this example, the rows are loaded in 10,000-row chunks, and the function is then
# applied to each chunk before the database rows are updated. By using this method, 
# the amount of memory needed can be decreased and the application can avoid crashing 
# due to memory issues.

# Approach 02:
#     Another approach is to use the bulk_update method. This method updates multiple 
#     rows at once and allows you to pass a callable function as argument to update the
#     values of certain fields.

from django.db import transaction
from django.db.models import F

def my_function(row):
    # Do something with the row
    return {'column1': row.column1 + 1}

with transaction.atomic():
    MyModel.objects.all().bulk_update(update_fields=['column1'], column1=my_function)

# This method is faster than the previous one and it will also take care of the database 
# transaction.    

# Approach 02: 
#           When you have large databases, it's pretty normal to index your database. That way, retrieving data, should be pretty quick.

# Approach 03:
#           we can also use Pagenation in django when we have to show data to user whaile when we have large amount of data in our database
def myfunc(rewuest):
    products=Product.objects.all().order_by('id')
    paginator=Paginator(products,3,orphans=1)
    page_number= request.GET.get('page')
    product_page = paginator.get_page(page_number)
                
    return render(request,'store/dashboard.html',{'products':product_page,'total':order}) 
        
    
