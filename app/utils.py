from decimal import *
from app.models import WifiPoint
from geopy.distance import vincenty

class StaticUtils(object):
    @staticmethod
    def getWifiPointsNearLocation(lattitude, longitude, distance):
        """
        Finds all the wifi points in the database that are
        within a zone around the specified point. 
        """
        _dest_to_orig = distance

        # check to make sure a duplicate object doesn't exist. If doesn't, add the new point
        lower_limit_dist = _dest_to_orig - 0.1
        upper_limit_dist = _dest_to_orig + 0.1
        lower_limit_long = longitude - 10
        upper_limit_long = longitude + 10
        lower_limit_lat  = lattitude  - 10
        upper_limit_lat  = lattitude  + 10

        # filter out the available data points
        objs = WifiPoint.objects.filter(
            dest_to_orig__gte=lower_limit_dist).filter(
            dest_to_orig__lte=upper_limit_dist).filter(
            loc_long__gte=lower_limit_long).filter(
            loc_long__lte=upper_limit_long).filter(
            loc_lat__gte=lower_limit_lat).filter(
            loc_lat__lte=upper_limit_lat)

        # DEBUG ONLY
        # for one_obj in objs:
        #     print(one_obj.dest_to_orig)
        #     print(one_obj.loc_lat)
        #     print(one_obj.loc_long)
        #     print(one_obj.wifiName)
        #     print(one_obj.password)
        #     print(" EMPTY ")

        return objs

    @staticmethod
    def getDistanceToOrigin(lattitude, longitude):
        """
        Calculates the distance from the origin to the specified point.
        Returns distance in miles. 
        """
        # use (0,0) as reference for calculating the absolute distance
        origin = ( 0.0, 0.0)
        location = (lattitude, longitude)
        dest_to_orig = vincenty(origin, location).miles

        return dest_to_orig

    @staticmethod
    def isLatitudeValid(lattitude):
        """
        This method checks if the lattitude value is within the range (-90.00,90.00) 
        Returns True if valid, False otherwise
        """
        if ((lattitude > Decimal('90.000000')) == True) or ((lattitude < Decimal('-90.000000')) == True):
            return False
        return True

    @staticmethod
    def isLongitudeValid(longitude):
        """
        This method checks if the longitude value is within the range (-180.00,180.00) 
        Returns True if valid, False otherwise
        """
        if ((longitude > Decimal('180.000000')) == True) or ((longitude < Decimal('-180.000000')) == True):
            return False
        return True