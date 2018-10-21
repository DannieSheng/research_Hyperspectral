# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 13:24:25 2018

@author: hdysheng
"""

import numpy as np
import os

step = 5 # the step size of using images
#cubeNum = 458
flirFrmIdxPath = 'T:/Box2/Drone Data/CLMB 2018 drone data/Maria_Bradford_Switchgrass_Standplanting/100032_2018_08_06_18_19_57/FLIR'
imuPath        = 'T:/Box2/Drone Data/CLMB 2018 drone data/Maria_Bradford_Switchgrass_Standplanting/100032_2018_08_06_18_19_57'
imuName        = 'imu_gps.txt'
listCubeNum    = [0, 458, 939, 1440, 1943, 2463, 2946, 3447, 3948, 4448, 4930, 5419, 5892, 6422]
for cubeNum in listCubeNum:
    flirFrmIdxName = 'frameIndex_' + str(cubeNum) +'.txt'
    flirFrm = np.loadtxt(os.path.join(flirFrmIdxPath, flirFrmIdxName), skiprows = 1)
    frmIdxFlir = flirFrm[:, 0]
    frmGPS     = np.zeros([len(frmIdxFlir), 3])
    timestampFlir = flirFrm[:, 1]
    imu     = np.loadtxt(os.path.join(imuPath, imuName), skiprows = 1, usecols = (3,4,5,6))
    timestampImu  = imu[:, 3]
    laloal = imu[:, 0:3]
    count = 0
    listIndex = np.zeros(np.shape(timestampFlir))
    for ts in timestampFlir:
        listIndex[count] = np.argmin(abs(timestampImu-ts))
        count            = count + 1

# find those frames of flir with the same gps information based on the nearest theorem
    type, count = np.unique(listIndex, return_index = True)
#temp  = np.unique(listIndex)
#if len(temp) != len(listIndex):
#    temp2 = np.zeros(np.shape(listIndex)) 
#    count = 0
#    for li in listIndex:
#        temp2[count] = np.where(temp == li)[0][0]
#        count = count + 1
#idxNU = np.where(count!=1) # find the indexes of the not unique flir to imu 
    idxNU = np.flatnonzero(count!=1)
    aa = []
    for i in np.arange(0, len(idxNU)):
        temp = np.where(listIndex == type[idxNU[i]])
        for j in np.arange(0, len(temp)):
            aa.append(temp[j])
    
    count = 0
    for idx in listIndex:
        frmGPS[count, :] = laloal[int(idx),:]
        count = count + 1

    GPSfileName = 'T:/Results/Analysis CLMB 2018 drone data/correspondingRGB/CLMB 2018 drone data/Maria_Bradford_Switchgrass_Standplanting/100032_2018_08_06_18_19_57/FLIR/raw_' + str(cubeNum) + '/raw_' + str(cubeNum) + '.txt'
    with open(GPSfileName, 'w') as fileToWrite:
        for i in np.arange(0, len(frmIdxFlir), step):
            fileToWrite.write(str(i+cubeNum) + '.jpg, ' + str(frmGPS[i,0]) +', ' + str(frmGPS[i,1]) + ', '+ str(frmGPS[i,2]) + '\n')
    fileToWrite.close()