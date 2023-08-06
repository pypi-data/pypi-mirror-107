from .config import FILTER_TYPES
import json
import inspect
from rest_framework import serializers
class Validation:



	def __init__(self,function):
		self.function = function


	def __call__(self,request,queryset,view):
		filters = []
		if request.query_params.get('filters[]'):
			filters = self.optimize_parameters(filters=json.loads(request.query_params.get('filters[]')))
			self.validate_types(filters)
			self.validate_fields(filters,queryset)
		return self.function(self,request,queryset,view)


	def validate_types(self,filters):
		for filter in filters:
			if not filter['type'] in FILTER_TYPES.keys():
				raise serializers.ValidationError({'no_exist':
					{'message':'نوع فیلتر غیر مجاز است لطفا از لیست انتخاب کنید.',
					'fields':FILTER_TYPES.keys()
					}})
		return filters

	def validate_fields(self,filters,queryset):
		model_fields = [field.name for field in queryset.model._meta.fields]
		for filter in filters:
			if not filter['key'] in model_fields:
				raise serializers.ValidationError({'invalid_key':
					{'message':f"{filter['key']} this field does not exist in {queryset.model.__name__}"
					}})
		return filters


	def optimize_parameters(self,filters):
		for filter in filters:
			if FILTER_TYPES[filter['type']]['extra_keys']:
				temp_key = filter['key']
				filter['key'] = []
				extra_keys = FILTER_TYPES[filter['type']]['extra_keys']
				if len(extra_keys) == 1 :
					filter['key'] = f'{temp_key}__{extra_keys[0]}'
				else:
					for extra_key in extra_keys:
						filter['key'].append(f'{temp_key}__{extra_key}')
		return filters