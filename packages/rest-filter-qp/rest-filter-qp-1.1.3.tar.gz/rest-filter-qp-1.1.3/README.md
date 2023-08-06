A package for filter all models in django based on query parameters.


<h1>Installation:</h1>
```
pip3 install django_rest_framework
pip3 install rest_filter_qp
```
if you use jalali date:
```
pip3 install jalali_date
```
query parameters:
https://example.com/[URL]/?filters[]=[{"key":"KEY1","value":"VALUE1","type":"TYPE"},{"key":"KEY2","value":"VALUE2",,"type":"TYPE"},...]
```
key : model field name

type : type of filters, you should write a type from these :
```
FILTER_TYPES = {
		'max':{ # max of a field
			'type' : 'int',
			'len' : 1,
			'extra_keys':[],
			'method' : Max,
			'is_aggregate':True
		},
		'min':{ # min of a field
			'type' : 'int',
			'len' : 1,
			'extra_keys':[],
			'method' : Min,
			'is_aggregate':True
		},
		'bwn':{ # field between 2 value
			'type' : 'list',
			'len' : 2,
			'extra_keys':['gte','lte'],
			'method' : None,
			'is_aggregate':False
		},
		'normal':{ # field equal a value 
			'type' : None,
			'len' : 1,
			'extra_keys':[],
			'method' : None,
			'is_aggregate':False
		},
		'today':{ # objects that created today
			'type' : 'list',
			'len'  : 1,
			'extra_keys' : ['year','month','day'],
			'method' : this_day,
			'is_aggregate':False
		},
		'toweek' : { # objects that created current week (based jalali date)
			'type':'rang',
			'len' : 1,
			'extra_keys' : ['range'],
			'method' : this_week,
			'is_aggregate':False
		},
		'tomonth' : { # objects that created current month
			'type' : 'list',
			'len' : 1,
			'extra_keys' : ['year','month'],
			'method' : this_month,
			'is_aggregate':False
		},
		'asc' : { # order asc
			'type' : 'sort',
			'len' : 1,
			'extra_keys' : [],
			'method' : None,
			'is_aggregate' : False
		},
		'desc' : { # order desc
			'type' : 'sort',
			'len' : 1,
			'extra_keys' : [],
			'method' : None,
			'is_aggregate' : False
		}
	}
``` 


for example, you have a model like this :
```
class Product(models.Model):
    title = models.CharField(max_length=255)
    by_count = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)
    slug = models.SlugField(max_length=255,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

```
you should add <b>FilterParams</b> class from <b>rest_filter_qp</b> to your <b>filter_backends[]</b>: 
```
from rest_filter_qp import FilterParams
class ProductView(generics.ListAPIView):
	queryset = Product.objects.all()
	serializer_class = ProductSerializer
	filter_backends = [FilterParams]
```

now, you want filter product model by <b>title</b> field that value is <i>"Foo" and created today :</i>:
```
[YOUR_DOMAIN]/products/?filters[]=[{"key":"title","value":"Foo","type":"normal"},{"key":"created_at","value":"","type":"today"}]
```
if you want a objects with maximum value :
```
[YOUR_DOMAIN]/products/?filters[]=[{"key":"view_count","value":"","type":"max"}]
```