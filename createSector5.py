#创建扇区
#Author:  Chuckian
import os
import math
import arcpy
from arcpy import env

cameraName=arcpy.GetParameterAsText(0)
xcoord=arcpy.GetParameter(1)
ycoord=arcpy.GetParameter(2)
angleTemp=arcpy.GetParameter(3)
radiusTemp=arcpy.GetParameter(4)
outputSectorFeature=arcpy.GetParameterAsText(5)

#生成扇形方法
def create_sector2(x,y,radius,angle,SectorName):
	print "x,y,radius,angle,SectorName:" + str(x)+","+str(y)+","+str(radius)+","+str(angle)+","+str(SectorName)
        angle_sjx=90          #默认的扇形的角度        
        n = int(20);   #默认扇形上选取20个点
        angle_x=x+radius      #x旋转的开始位置		
        angle_y=y             #y旋转的开始位置
        #创建扇形上的点数组
	array_k = arcpy.Array()
        pnt = arcpy.Point()
        pnt.X = x
        pnt.Y = y
        array_k.add(pnt)
        angle1=(angle-angle_sjx/2)*math.pi/180.0000
        angle2=(angle+angle_sjx/2)*math.pi/180.0000
		#根据角度来计算扇形上的起始点坐标
	x1 =(angle_x - x)*math.cos(angle1) + (angle_y - y)*math.sin(angle1) + x
	y1 =-(angle_x - x)*math.sin(angle1) + (angle_y - y)*math.cos(angle1) + y
	x2 =(angle_x - x)*math.cos(angle2) + (angle_y - y)*math.sin(angle2) + x
	y2 =-(angle_x - x)*math.sin(angle2) + (angle_y - y)*math.cos(angle2) + y
        pnt1 = arcpy.Point(x1,y1)
        pnt2 = arcpy.Point(x2,y2)
		#扇形上的起始点为所有点的第二个点
	array_k.add(pnt1)	
        for k in range(n):   #计算angle_sjx个点的坐标
                anglek=(angle-angle_sjx/2+k*angle_sjx/n)*math.pi/180.0
                xk =(angle_x - x)*math.cos(anglek) + (angle_y - y)*math.sin(anglek) + x
                yk =-(angle_x - x)*math.sin(anglek) + (angle_y - y)*math.cos(anglek) + y
                pntk = arcpy.Point(xk,yk)
                array_k.add(pntk)
		#print "pntk:x"+str(k)+":"+str(xk)+",y"+str(k)+":"+str(yk)
        array_k.add(pnt2)
        array_k.add(array_k.getObject(0))         #这里又加了一次起始点
	print "array_k的长度为:"+str(len(array_k))	
        poly = arcpy.Polygon(array_k)
	array_k.removeAll()            #清空array_k
        #生成扇形图层
	outputSectorFeatureF = os.path.join(os.path.split(outputSectorFeature)[0], SectorName)
        arcpy.CopyFeatures_management(poly, outputSectorFeatureF)	
 	arcpy.DefineProjection_management(outputSectorFeatureF, arcpy.SpatialReference(2436))
	arcpy.SetParameterAsText(5, outputSectorFeatureF)
create_sector2(xcoord,ycoord,radiusTemp,angleTemp,cameraName)