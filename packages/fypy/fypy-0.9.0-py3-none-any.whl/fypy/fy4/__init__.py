#coding:utf-8
'''

'''
import os

import sys
import numpy as np
import datetime

dirpath = os.path.dirname(__file__)
sys.path.append(dirpath)
from .FY4ASearchTable import *

#
# def IJ2LatLon(row, col, subpoint=104.7):
#
#     row = np.array(row)
#     col = np.array(col)
#
#     x = deg2rad * (col - coff) / (2**-16 * cfac)
#     y = deg2rad * (row - loff) / (2**-16 * lfac)
#
#     sd = (H * np.cos(x) * np.cos(y)) * (H * np.cos(x) * np.cos(y)) - \
#          (np.cos(y) * np.cos(y) + (ea * ea) / (eb * eb) * np.sin(y) * np.sin(y)) * ((H * H) - ea * ea)
#
#     flag = sd < 0
#
#     sd[sd>=0] = np.sqrt(sd[sd>=0])
#
#     sn = (H * np.cos(x) * np.cos(y) - sd) / \
#          (np.cos(y) * np.cos(y) + (ea * ea) / (eb * eb) * np.sin(y) * np.sin(y))
#
#     S1 = H - (sn * np.cos(x) * np.cos(y))
#     S2 = sn * np.sin(x) * np.cos(y)
#     S3 = -sn * np.sin(y)
#     Sxy = np.sqrt(S1 * S1 + S2 * S2)
#
#     lon = rad2deg * np.arctan(S2 / S1) + subpoint
#     lat = rad2deg * np.arctan((ea * ea) / (eb * eb) * S3 / Sxy)
#
#     lon[flag] = FILLVALUE
#     lat[flag] = FILLVALUE
#
#     return  lat, lon
#
#
# def CalSatZenith(lat, lon, subpoint = 104.7) :
#     lat = np.array(lat, dtype=np.float32)
#     lon = np.array(lon, dtype=np.float32)
#     fillflag = (lat < -90) | (lat > 90) | (lon < -180) | (lon > 180)
#
#     c_lat = np.arctan(0.993243 * np.tan(lat * deg2rad))
#     rl = 6356.7523 / np.sqrt(1 - 0.00675701 * np.cos(c_lat) * np.cos(c_lat))
#     r1 = H - rl * np.cos(c_lat) * np.cos(lon * deg2rad - subpoint * deg2rad)
#     r2 = -rl * np.cos(c_lat) * np.sin(lon * deg2rad - subpoint * deg2rad)
#
#     r3 = rl * np.sin(c_lat)
#     rn = np.sqrt(r1 * r1 + r2 * r2 + r3 * r3)
#
#     r4 = np.arccos((rn * rn + H * H - rl * rl) / (2 * rn * H))
#
#     r5 = np.arcsin(np.sin(r4) * H / 6356.7523) * rad2deg
#
#     r5[fillflag] = FILLVALUE
#
#     return r5
#
# def CalSatAzimuth(lat, lon, subpoint = 104.7):
#     '''
#     计算卫星方位角
#     :param lat: array_like,
#                 unit: degree
#     :param lon: array_like,
#                 unit: degree
#     :param subpoint: float,
#                 unit: degree
#     :return: satellite azimuth , array_like:
#                 unit:degree
#     '''
#     lat = np.array(lat, dtype=np.float32)
#     lon = np.array(lon, dtype=np.float32)
#     fillflag = (lat < -90) | (lat > 90) | (lon < -180) | (lon > 180)
#
#     heigh = H * 1.0E3
#
#
#     RX = Zocgef(lat, lon, heigh)
#
#     RSat = Zocgef(0.0, subpoint, heigh)
#
#     Azi = ICGSSAT(lat, lon, RSat, RX)
#
#     sata = Azi * rad2deg
#
#     flag = sata >= 180
#     sata[flag] -= 180.0
#     sata[~flag] += 180.0
#
#     sata[fillflag] = FILLVALUE
#
#     return sata
#
#
# def CalSunZenith(lat, lon, nowtime):
#     lat = np.array(lat, dtype=np.float32)
#     lon = np.array(lon, dtype=np.float32)
#     fillflag = (lat < -90) | (lat > 90) | (lon < -180) | (lon > 180)
#
#     sttime = (nowtime - datetime.datetime.strptime('%s-01-01' % (nowtime.strftime('%Y')), '%Y-%m-%d')).total_seconds()
#
#     PHIG,  DPHIDT, CHISUN,  EPSLON = EARTH(sttime)
#
#     RSOL = 149600881.0
#     COSX = np.cos(CHISUN)
#     SINX = np.sin(CHISUN)
#     COSE = np.cos(EPSLON)
#     SINE = np.sin(EPSLON)
#
#     RX = [RSOL*COSX,  RSOL*(SINX*COSE),  RSOL*(SINX*SINE)]
#
#     TH = np.fmod(lon * deg2rad + PHIG, TWOPI)
#     cTH = np.cos(TH)
#     sTH = np.sin(TH)
#
#     Azgs, Elgs = ICGS(RX, sTH, cTH, lat)
#
#     SunAzi = Azgs * rad2deg
#     SunZen = ((np.pi / 2.0) - Elgs) * rad2deg
#
#     SunZen[fillflag] = FILLVALUE
#
#     return SunZen
#
# def CalSunAzimuth(lat, lon, nowtime):
#     lat = np.array(lat, dtype=np.float32)
#     lon = np.array(lon, dtype=np.float32)
#     fillflag = (lat < -90) | (lat > 90) | (lon < -180) | (lon > 180)
#
#     sttime = (nowtime - datetime.datetime.strptime('%s-01-01' % (nowtime.strftime('%Y')), '%Y-%m-%d')).total_seconds()
#
#     PHIG,  DPHIDT, CHISUN,  EPSLON = EARTH(sttime)
#
#     RSOL = 149600881.0
#     COSX = np.cos(CHISUN)
#     SINX = np.sin(CHISUN)
#     COSE = np.cos(EPSLON)
#     SINE = np.sin(EPSLON)
#
#     RX = [RSOL*COSX,  RSOL*(SINX*COSE),  RSOL*(SINX*SINE)]
#
#     TH = np.fmod(lon * deg2rad + PHIG, TWOPI)
#     cTH = np.cos(TH)
#     sTH = np.sin(TH)
#
#     Azgs, Elgs = ICGS(RX, sTH, cTH, lat)
#
#     SunAzi = Azgs * rad2deg
#     SunZen = ((np.pi / 2.0) - Elgs) * rad2deg
#
#     SunAzi[fillflag] = FILLVALUE
#
#     return SunAzi
#
#
# def CalSunGL(satz, sunz, rela):
#     '''
#
#     :param satz:
#     :param sunz:
#     :param rela:
#     :return:
#     '''
#     fillflag = (satz < -360) | (satz > 360) | (sunz < -360) | (sunz > 360) | (rela < -360) | (rela > 360)
#
#     data = np.cos(satz * deg2rad) * np.cos(sunz * deg2rad) \
#            + np.sin(satz * deg2rad) * np.sin(sunz * deg2rad) * np.cos(rela * deg2rad)
#     # cos_solzen * cos_satzen + sin_solzen * sin_satzen * cos_relaz
#
#     data[data > 1.0] = 0.0
#     SunGL = np.arccos(data) * rad2deg
#     SunGL[fillflag] = -999.0
#
#     return SunGL
#
#
# def CalRelativeAzimuth(sata, suna):
#     fillflag = (sata > 360) | (sata < 0) | (suna > 360) | (suna < 0)
#
#     RelativeAzi = np.fabs(sata - suna) + 180.0 # ???? + 180
#
#     RelativeAzi[fillflag] = -999.0
#
#     return RelativeAzi
#



