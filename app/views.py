import os
from decimal import *
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from app.models import WifiPoint
from app.utils import StaticUtils
from django.contrib.admin.views.decorators import staff_member_required
from access_tokens import scope, tokens

# Create your views here.
@staff_member_required
def index(request):
    _application   = request.GET['app']
    _scope         = request.GET['scope']

    # Generate an access token for a scope permission on a given app.
    publish_app_token = tokens.generate(
    scope.access_app(_application, _scope),
    )

    return HttpResponse( 'Your token is:' + publish_app_token)

def addNewWifi(request):  
    _key         = request.GET['key']
    _wifi_name   = request.GET['name']
    _password    = request.GET['pwd']
    _loc_lat     = Decimal(request.GET['lat'])
    _loc_long    = Decimal(request.GET['long'])

    # validate the key first
    bValidated = tokens.validate(
        _key,
        scope.access_app(os.environ['APP_NAME'], os.environ['SCOPE']),
    )

    if bValidated == False:
        # return an error response
        result = dict(Reason='Permission denied!')
        response = dict(Status='failure', Response=result)
        return JsonResponse(response)

    # validate the supplied params
    latitudeCheck = StaticUtils.isLatitudeValid(_loc_lat)
    if latitudeCheck == False:
        # return an error response
        result = dict(Reason='Lattitude is invalid!')
        response = dict(Status='failure', Response=result)
        return JsonResponse(response)
    
    longitudeCheck = StaticUtils.isLongitudeValid(_loc_long)
    if longitudeCheck == False:
        # return an error response
        result = dict(Reason='Longitude is invalid!')
        response = dict(Status='failure', Response=result)
        return JsonResponse(response)

    # get the distance from the origin
    _dest_to_orig = StaticUtils.getDistanceToOrigin(_loc_lat, _loc_long)

    # get all of the nearby wifi data points
    objs = StaticUtils.getWifiPointsNearLocation(_loc_lat, _loc_long, _dest_to_orig)

    # decide if a duplicate wifi point exists in the area
    bWifiPointExists = False
    if objs:
        for wifiPoint in objs:
            if (wifiPoint.wifiName == _wifi_name) and (wifiPoint.password == _password):
                bWifiPointExists = True

    if bWifiPointExists == True:
        result = dict(Reason='WifiPoint already exits!')
        response = dict(Status='failure', Response=result)

        #response = 'Wifi ' + _wifi_name + ' with password ' + _password + ' at location (' + str(_loc_lat) + ',' + str(_loc_long) + ') and dist ' + str(_dest_to_orig) + ' already exists!'
    else:
        obj = WifiPoint(wifiName=_wifi_name, 
                        password=_password, 
                        loc_lat=_loc_lat,
                        loc_long=_loc_long,
                        dest_to_orig =_dest_to_orig)
        obj.save()
        result = dict(Reason='WifiPoint added')
        response = dict(Status='success', Response=result)
        #response = 'Wifi ' + _wifi_name + ' with password ' + _password + ' at location (' + str(_loc_lat) + ',' + str(_loc_long) + ') and dist ' + str(_dest_to_orig) + ' was added!'   
    
    return JsonResponse(response)

def findWifiPoints(request):
    _key         = request.GET['key']
    _loc_lat  = Decimal(request.GET['lat'])
    _loc_long = Decimal(request.GET['long'])

    # validate the key first
    bValidated = tokens.validate(
        _key,
        scope.access_app(os.environ['APP_NAME'], os.environ['SCOPE']),
    )

    if bValidated == False:
        # return an error response
        result = dict(Reason='Permission denied!')
        response = dict(Status='failure', Response=result)
        return JsonResponse(response)

    # validate the supplied params
    latitudeCheck = StaticUtils.isLatitudeValid(_loc_lat)
    if latitudeCheck == False:
        # return an error response
        result = dict(Reason='Lattitude is invalid!')
        response = dict(Status='Failure', Response=result)
        return JsonResponse(response)
    
    longitudeCheck = StaticUtils.isLongitudeValid(_loc_long)
    if longitudeCheck == False:
        # return an error response
        result = dict(Reason='Longitude is invalid!')
        response = dict(Status='Failure', Response=result)
        return JsonResponse(response)

    # get the distance from the origin
    _dest_to_orig = StaticUtils.getDistanceToOrigin(_loc_lat, _loc_long)

    # get all of the nearby wifi data points
    objs = StaticUtils.getWifiPointsNearLocation(_loc_lat, _loc_long, _dest_to_orig)

    # prepare the response
    result = dict(Length=len(objs), WifiPoints=list(objs.values('wifiName','password','loc_lat','loc_long')))
    response = dict(Staus='success', Response=result)
             
    return JsonResponse(response)
