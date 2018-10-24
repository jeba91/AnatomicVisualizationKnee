#!/usr/bin/env vtkpython

#
# This example reads a volume dataset and displays it via volume rendering.
#

# This is a modified version of Medical4.py:
# https://www.vtk.org/gitweb?p=VTK.git;a=blob_plain;f=Examples/Medical/Python/Medical4.py
# Modifications by Robert Belleman, University of Amsterdam.

# Althought this script accepts any VTK volume dataset (specified as the first argument
# on the command line), the transfer funtions are tuned to "headsq_masked.vtk".

import vtk
import sys

knee_list 	= ['knee1_1.vtk','knee1_2.vtk','knee1_3.vtk','knee1_4.vtk','knee1_5.vtk','knee1_6.vtk','knee1_7.vtk']
bone_list 	= ['knie1.vti','knie2.vti','knie3.vti','knie4.vti','knie5.vti','knie6.vti','knie7.vti']
muscle_list = ['spier1.vti','spier2.vti','spier3.vti','spier4.vti','spier5.vti','spier6.vti','spier7.vti']

def createVolumeRender(File, ScalarList, ColorList, OpacList, PieceList):
	volumeMapper = vtk.vtkGPUVolumeRayCastMapper()
	volumeMapper.SetInputConnection(File.GetOutputPort())
	volumeMapper.SetBlendModeToComposite()

	volumeCTF = vtk.vtkColorTransferFunction()
	volumeCTF.AddRGBPoint(ScalarList[0],  ColorList[0][0], ColorList[0][1], ColorList[0][2])
	volumeCTF.AddRGBPoint(ScalarList[1],  ColorList[1][0], ColorList[1][1], ColorList[1][2])
	volumeCTF.AddRGBPoint(ScalarList[2],  ColorList[2][0], ColorList[2][1], ColorList[2][2])
	volumeCTF.AddRGBPoint(ScalarList[3],  ColorList[3][0], ColorList[3][1], ColorList[3][2])

	volumeOTF = vtk.vtkPiecewiseFunction()
	volumeOTF.AddPoint(ScalarList[0],  OpacList[0])
	volumeOTF.AddPoint(ScalarList[1],  OpacList[1])
	volumeOTF.AddPoint(ScalarList[2],  OpacList[2])
	volumeOTF.AddPoint(ScalarList[3],  OpacList[3])

	volumeGOTF = vtk.vtkPiecewiseFunction()
	volumeGOTF.AddPoint(0,   PieceList[0])
	volumeGOTF.AddPoint(90,  PieceList[1])
	volumeGOTF.AddPoint(100, PieceList[2])

	volumeProperty = vtk.vtkVolumeProperty()
	volumeProperty.SetColor(volumeCTF)
	volumeProperty.SetScalarOpacity(volumeOTF)
	volumeProperty.SetGradientOpacity(volumeGOTF)
	volumeProperty.SetInterpolationTypeToLinear()
	volumeProperty.ShadeOn()
	volumeProperty.SetAmbient(0.3)
	volumeProperty.SetDiffuse(0.8)
	volumeProperty.SetSpecular(0.4)

	volume = vtk.vtkVolume()
	volume.SetMapper(volumeMapper)
	volume.SetProperty(volumeProperty)

	return volume

class SliderCallbackN1():
	def __init__(self, knee, bone, muscle):
	    self.knee = knee
	    self.bone = bone
	    self.muscle = muscle

	def __call__(self, caller, ev):
	    sliderWidget = caller
	    value = sliderWidget.GetRepresentation().GetValue()
	    if value >= 0 and value < 1:
	    	self.knee.SetFileName(knee_list[0])
	    	self.bone.SetFileName(bone_list[0])
	    	self.muscle.SetFileName(muscle_list[0])
	    elif value >= 1 and value < 2:
	    	self.knee.SetFileName(knee_list[1])
	    	self.bone.SetFileName(bone_list[1])
	    	self.muscle.SetFileName(muscle_list[1])
	    elif value >= 2 and value < 3:
	    	self.knee.SetFileName(knee_list[2])
	    	self.bone.SetFileName(bone_list[2])
	    	self.muscle.SetFileName(muscle_list[2])
	    elif value >= 3 and value < 4:
	    	self.knee.SetFileName(knee_list[3])
	    	self.bone.SetFileName(bone_list[3])
	    	self.muscle.SetFileName(muscle_list[3])
	    elif value >= 4 and value < 5:
	    	self.knee.SetFileName(knee_list[4])
	    	self.bone.SetFileName(bone_list[4])
	    	self.muscle.SetFileName(muscle_list[4])
	    elif value >= 5 and value < 6:
	    	self.knee.SetFileName(knee_list[5])
	    	self.bone.SetFileName(bone_list[5])
	    	self.muscle.SetFileName(muscle_list[5])
	    elif value >= 6 and value < 7:
	    	self.knee.SetFileName(knee_list[6])
	    	self.bone.SetFileName(bone_list[6])
	    	self.muscle.SetFileName(muscle_list[6])

class SliderCallbackN2():
	def __init__(self, ren, volumebone):
			self.ren = ren

	def __call__(self, caller, ev):
	    sliderWidget = caller
	    value = sliderWidget.GetRepresentation().GetValue()
	    if value >= 0 and value < 1:
	    	self.ren.AddActor(volumeBone)
	    	self.ren.AddActor(volumeLnee)
	    	self.ren.AddActor(volumeMuscle)
	    elif value >= 1 and value < 2:
	    	self.ren.AddActor(volumeBone)
	    	self.ren.AddActor(volumeKnee)
	    	self.ren.RemoveActor(volumeMuscle)
	    elif value >= 2 and value < 3:
	    	self.ren.AddActor(volumeBone)
	    	self.ren.RemoveActor(volumeKnee)
	    	self.ren.AddActor(volumeMuscle)
	    elif value >= 3 and value < 4:
	    	self.ren.RemoveActor(volumeBone)
	    	self.ren.AddActor(volumeKnee)
	    	self.ren.AddActor(volumeMuscle)
	    elif value >= 4 and value < 5:
	    	self.ren.RemoveActor(volumeBone)
	    	self.ren.RemoveActor(volumeKnee)
	    	self.ren.AddActor(volumeMuscle)
	    elif value >= 5 and value < 6:
	    	self.ren.AddActor(volumeBone)
	    	self.ren.RemoveActor(volumeKnee)
	    	self.ren.RemoveActor(volumeMuscle)
	    elif value >= 6 and value < 7:
	    	self.ren.RemoveActor(volumeBone)
	    	self.ren.AddActor(volumeKnee)
	    	self.ren.RemoveActor(volumeMuscle)

# Create the renderer, the render window, and the interactor. The renderer
# draws into the render window, the interactor enables mouse- and
# keyboard-based interaction with the scene.
ren = vtk.vtkRenderer()
ren.SetBackground(0.2, 0.2, 0.2)
ren.SetBackground2(0.5, 0.5, 0.5)
ren.GradientBackgroundOn()

renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
renWin.SetSize(640, 480)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)


### Volume Rendering Skin ###
knee = vtk.vtkDataSetReader()
knee.SetFileName(knee_list[0])

scalarknee 	= [50,100,200,300]
colorlist 	= [[0.0, 0.0, 0.0],[1.0,0.5,0.3],[1.0,0.5,0.3],[0.0,0.0,0.0]]
opacknee 	= [0.00,0.10,0.25,0.00]
pieceknee 	= [0.0,0.1,0.2]

volumeKnee = createVolumeRender(knee,scalarknee,colorlist,opacknee,pieceknee)

### Volume Rendering Bone ###
bone = vtk.vtkXMLImageDataReader()
bone.SetFileName(bone_list[0])

scalarBone 	= [50,51,1100,1101]
colorBone 	= [[0.0, 0.0, 0.0],[1.0,1.0,0.9],[1.0,1.0,0.9],[0.0,0.0,0.0]]
opacBone 	= [0.00,1.00,1.00,0.00]
pieceBone 	= [0.0,1.0,1.0]

volumeBone = createVolumeRender(bone,scalarBone,colorBone,opacBone,pieceBone)

### Volume Rendering Muscle ###
muscle = vtk.vtkXMLImageDataReader()
muscle.SetFileName(muscle_list[0])

opacmuscle = [50,51,1100,1101]

scalarMuscle	= [50,51,1100,1101]
colorMuscle		= [[0.0, 0.0, 0.0],[1.0,0.0,0.0],[1.0,0.0,0.0],[0.0,0.0,0.0]]
opacMuscle 		= [0.00,0.05,0.05,0.00]
pieceMuscle 		= [0.0,1.0,1.0]

volumeMuscle = createVolumeRender(muscle,scalarMuscle,colorMuscle,opacMuscle,pieceMuscle)

#ADD THEM
# Finally, add the volume to the renderer
ren.AddActor(volumeBone)

# Finally, add the volume to the renderer
ren.AddActor(volumeKnee)

# Finally, add the volume to the renderer
ren.AddActor(volumeMuscle)


# Set up an initial view of the volume.  The focal point will be the
# center of the volume, and the camera position will be 400mm to the
# patient's left (which is our right).
camera =  ren.GetActiveCamera()
c = volumeKnee.GetCenter()
camera.SetFocalPoint(c[0], c[1], c[2])
camera.SetPosition(c[0] + 400, c[1], c[2])
camera.SetViewUp(0, 0, -1)


# Setup a slider widget for each varying parameter
tubeWidth = 0.008
sliderLength = 0.008
titleHeight = 0.04
labelHeight = 0.04

sliderRepN1 = vtk.vtkSliderRepresentation2D()

sliderRepN1.SetMinimumValue(0)
sliderRepN1.SetMaximumValue(7)
sliderRepN1.SetValue(0)
sliderRepN1.SetTitleText("Skin extractor value")

sliderRepN1.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
sliderRepN1.GetPoint1Coordinate().SetValue(.9, .9)
sliderRepN1.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
sliderRepN1.GetPoint2Coordinate().SetValue(.9, .1)

sliderRepN1.SetTubeWidth(tubeWidth)
sliderRepN1.SetSliderLength(sliderLength)
sliderRepN1.SetTitleHeight(titleHeight)
sliderRepN1.SetLabelHeight(labelHeight)

sliderWidgetN1 = vtk.vtkSliderWidget()
sliderWidgetN1.SetInteractor(iren)
sliderWidgetN1.SetRepresentation(sliderRepN1)
sliderWidgetN1.SetAnimationModeToAnimate()
sliderWidgetN1.EnabledOn()

sliderWidgetN1.AddObserver(vtk.vtkCommand.InteractionEvent, SliderCallbackN1(knee, bone, muscle))

# Setup a slider widget for each varying parameter
tubeWidth = 0.008
sliderLength = 0.008
titleHeight = 0.04
labelHeight = 0.04

sliderRepN2 = vtk.vtkSliderRepresentation2D()

sliderRepN2.SetMinimumValue(0)
sliderRepN2.SetMaximumValue(7)
sliderRepN2.SetValue(0)
sliderRepN2.SetTitleText("Skin extractor value")

sliderRepN2.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
sliderRepN2.GetPoint1Coordinate().SetValue(0.95, 0.95)
sliderRepN2.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
sliderRepN2.GetPoint2Coordinate().SetValue(0.95, .1)

sliderRepN2.SetTubeWidth(tubeWidth)
sliderRepN2.SetSliderLength(sliderLength)
sliderRepN2.SetTitleHeight(titleHeight)
sliderRepN2.SetLabelHeight(labelHeight)

sliderWidgetN2 = vtk.vtkSliderWidget()
sliderWidgetN2.SetInteractor(iren)
sliderWidgetN2.SetRepresentation(sliderRepN2)
sliderWidgetN2.SetAnimationModeToAnimate()
sliderWidgetN2.EnabledOn()

sliderWidgetN2.AddObserver(vtk.vtkCommand.InteractionEvent, SliderCallbackN2(ren,volumeBone))

# Interact with the data.
iren.Initialize()
iren.Start()

# We won't reach this until the user has pressed 'q', 'e' or closed the
# RenderWindow
print "Cleanup time"

# Free up any objects we created (useless really, as we quit anyway)
contour = None
mapper = None
actor = None
ren1 = None
renWin = None