#��������
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

#�������η���
def create_sector2(x,y,radius,angle,SectorName):
	print "x,y,radius,angle,SectorName:" + str(x)+","+str(y)+","+str(radius)+","+str(angle)+","+str(SectorName)
        angle_sjx=90          #Ĭ�ϵ����εĽǶ�        
        n = int(20);   #Ĭ��������ѡȡ20����
        angle_x=x+radius      #x��ת�Ŀ�ʼλ��		
        angle_y=y             #y��ת�Ŀ�ʼλ��
        #���������ϵĵ�����
	array_k = arcpy.Array()
        pnt = arcpy.Point()
        pnt.X = x
        pnt.Y = y
        array_k.add(pnt)
        angle1=(angle-angle_sjx/2)*math.pi/180.0000
        angle2=(angle+angle_sjx/2)*math.pi/180.0000
		#���ݽǶ������������ϵ���ʼ������
	x1 =(angle_x - x)*math.cos(angle1) + (angle_y - y)*math.sin(angle1) + x
	y1 =-(angle_x - x)*math.sin(angle1) + (angle_y - y)*math.cos(angle1) + y
	x2 =(angle_x - x)*math.cos(angle2) + (angle_y - y)*math.sin(angle2) + x
	y2 =-(angle_x - x)*math.sin(angle2) + (angle_y - y)*math.cos(angle2) + y
        pnt1 = arcpy.Point(x1,y1)
        pnt2 = arcpy.Point(x2,y2)
		#�����ϵ���ʼ��Ϊ���е�ĵڶ�����
	array_k.add(pnt1)	
        for k in range(n):   #����angle_sjx���������
                anglek=(angle-angle_sjx/2+k*angle_sjx/n)*math.pi/180.0
                xk =(angle_x - x)*math.cos(anglek) + (angle_y - y)*math.sin(anglek) + x
                yk =-(angle_x - x)*math.sin(anglek) + (angle_y - y)*math.cos(anglek) + y
                pntk = arcpy.Point(xk,yk)
                array_k.add(pntk)
		#print "pntk:x"+str(k)+":"+str(xk)+",y"+str(k)+":"+str(yk)
        array_k.add(pnt2)
        array_k.add(array_k.getObject(0))         #�����ּ���һ����ʼ��
	print "array_k�ĳ���Ϊ:"+str(len(array_k))	
        poly = arcpy.Polygon(array_k)
	array_k.removeAll()            #���array_k
        #��������ͼ��
	outputSectorFeatureF = os.path.join(os.path.split(outputSectorFeature)[0], SectorName)
        arcpy.CopyFeatures_management(poly, outputSectorFeatureF)	
 	arcpy.DefineProjection_management(outputSectorFeatureF, arcpy.SpatialReference(2436))
	arcpy.SetParameterAsText(5, outputSectorFeatureF)
create_sector2(xcoord,ycoord,radiusTemp,angleTemp,cameraName)