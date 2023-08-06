from django.db.models import Max,Min
from .methods import *

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