from django.shortcuts import render, redirect, HttpResponse
from  app01 import models
# Create your views here.

def business(request):
	v1 = models.Business.objects.all()
	# 使用all或fiter方法queryset内是对象
	# [obj(id,caption,code),obj(id,caption,code)]
	v2 = models.Business.objects.all().values('id', 'caption')
	# 使用values取出指定字段的数据，queryset内是字典
	# [{'id':'1'}, {'caption': '运维部'}]
	v3 = models.Business.objects.all().values_list('id', 'caption')
	# 使用values取出指定字段的数据，queryset内是元组
	# [（'id':'1'）, （'caption': '运维部'）]
	return render(request, 'business.html', {'obj1': v1, 'obj2': v2, 'obj3': v3})

def host(request):
	if request.method == 'GET':
		# host_list 是对象类型
		host_list = models.Host.objects.all()
		# v2 queryset内是字典类型，前端使用key取值
		v2 = models.Host.objects.all().values('nid', 'hostname','bus_id',  'bus__caption')
		# v3 queryset内是元组类型，前端使用索引取值
		v3 = models.Host.objects.all().values_list('nid', 'hostname', 'bus_id', 'bus__caption')
		bus_list = models.Business.objects.all().values('id', 'caption')
		return render(request, 'host.html', {'host_list': host_list, 'v2': v2, 'v3': v3, 'bus_list': bus_list})
	elif request.method == 'POST':
		hostname = request.POST.get('hostname')
		ip = request.POST.get('ip')
		port = request.POST.get('port')
		bus = request.POST.get('bus')
		models.Host.objects.create(hostname=hostname, ip=ip, port=port, bus_id=bus)
		# host_list = models.Host.objects.all() # 获取最新数据，也可重新重定向get一下
		# v2 = models.Host.objects.all().values('nid', 'hostname','bus_id',  'bus__caption')
		# v3 = models.Host.objects.all().values_list('nid', 'hostname', 'bus_id', 'bus__caption')
		# bus_list = models.Business.objects.all().values('id', 'caption')
		# return render(request, 'host.html', {'host_list': host_list, 'v2': v2, 'v3': v3, 'bus_list': bus_list})
		return redirect('/host/')

def testajax(request):
	import json
	ret = {'status': True, 'error': None, 'data': None}
	if request.method == 'POST':
		try:
			hostname = request.POST.get('hostname')
			ip = request.POST.get('ip')
			port = request.POST.get('port')
			bus = request.POST.get('bus')
			if hostname and len(hostname) >= 5:
				models.Host.objects.create(hostname=hostname, ip=ip, port=port, bus_id=bus)
				# return HttpResponse("ok")
			else:
				ret['status'] = False
				ret['error'] = '主机名不足5个字符。'
		except Exception as e:
			ret['status'] = False
			ret['error'] = '请求错误'
		return HttpResponse(json.dumps(ret)) # 把字典转字符串返回，在前端再转回字典使用  注意：强烈建议让服务端返回一个字典