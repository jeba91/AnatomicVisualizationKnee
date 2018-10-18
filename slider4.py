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

knee_list = ['knee1_1.vtk','knee1_2.vtk','knee1_3.vtk','knee1_4.vtk','knee1_5.vtk','knee1_6.vtk','knee1_7.vtk']

def main():
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

	# create the main visualization pipeline:
	#
	#             volumeCTF  volumeOTF  volumeGOTF
	#                     |       |     |
	#                     \       |     /
	#                      volumeProperty
	#                             |
	#                             v
	# source -> volumeMapper -> volume

	source = vtk.vtkDataSetReader()
	source.SetFileName(knee_list[0])

	# force the source to read the data set so that we can obtain its scalar range
	source.Update()
	srange = source.GetOutput().GetScalarRange()
	print(srange)


	# The volume will be displayed by ray-cast alpha compositing.
	# A ray-cast mapper is needed to do the ray-casting, and a
	# compositing function is needed to do the compositing along the ray.
	volumeMapper = vtk.vtkGPUVolumeRayCastMapper()
	volumeMapper.SetInputConnection(source.GetOutputPort())
	volumeMapper.SetBlendModeToComposite()

	# The color transfer function (CTF) maps voxel intensities to colors.
	# It is modality-specific, and often anatomy-specific as well.
	# The goal is to one color for flesh (between 500 and 1000)
	# and another color for bone (1150 and over).
	volumeCTF = vtk.vtkColorTransferFunction()
	volumeCTF.AddRGBPoint(0,    0.0, 0.0, 0.0)
	volumeCTF.AddRGBPoint(50,  1.0, 0.5, 0.3)
	volumeCTF.AddRGBPoint(300, 1.0, 0.5, 0.3)
	volumeCTF.AddRGBPoint(900, 1.0, 1.0, 0.9)

	# The opacity transfer function (OTF) is used to control the opacity
	# of different tissue types.
	volumeOTF = vtk.vtkPiecewiseFunction()
	volumeOTF.AddPoint(0,    0.00)
	volumeOTF.AddPoint(50,  0.05)
	volumeOTF.AddPoint(300, 0.05)
	volumeOTF.AddPoint(900, 0.85)

	# The gradient opacity transfer function (GOTF) is used to decrease the opacity
	# in the "flat" regions of the volume while maintaining the opacity
	# at the boundaries between tissue types.  The gradient is measured
	# as the amount by which the intensity changes over unit distance.
	# For most medical data, the unit distance is 1mm.
	volumeGOTF = vtk.vtkPiecewiseFunction()
	volumeGOTF.AddPoint(0,   0.0)
	volumeGOTF.AddPoint(90,  0.5)
	volumeGOTF.AddPoint(100, 1.0)

	# The VolumeProperty attaches the color and opacity functions to the
	# volume, and sets other volume properties.  The interpolation should
	# be set to linear to do a high-quality rendering.  The ShadeOn option
	# turns on directional lighting, which will usually enhance the
	# appearance of the volume and make it look more "3D".  However,
	# the quality of the shading depends on how accurately the gradient
	# of the volume can be calculated, and for noisy data the gradient
	# estimation will be very poor.  The impact of the shading can be
	# decreased by increasing the Ambient coefficient while decreasing
	# the Diffuse and Specular coefficient.  To increase the impact
	# of shading, decrease the Ambient and increase the Diffuse and Specular.
	volumeProperty = vtk.vtkVolumeProperty()
	volumeProperty.SetColor(volumeCTF)
	volumeProperty.SetScalarOpacity(volumeOTF)
	volumeProperty.SetGradientOpacity(volumeGOTF)
	volumeProperty.SetInterpolationTypeToLinear()
	volumeProperty.ShadeOn()
	volumeProperty.SetAmbient(0.4)
	volumeProperty.SetDiffuse(0.6)
	volumeProperty.SetSpecular(0.2)

	# The vtkVolume is a vtkProp3D (like a vtkActor) and controls the position
	# and orientation of the volume in world coordinates.
	volume = vtk.vtkVolume()
	volume.SetMapper(volumeMapper)
	volume.SetProperty(volumeProperty)

	# Finally, add the volume to the renderer
	ren.AddViewProp(volume)

	# Set up an initial view of the volume.  The focal point will be the
	# center of the volume, and the camera position will be 400mm to the
	# patient's left (which is our right).
	camera =  ren.GetActiveCamera()
	c = volume.GetCenter()
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
	sliderRepN1.GetPoint1Coordinate().SetValue(.1, .1)
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

	sliderWidgetN1.AddObserver(vtk.vtkCommand.InteractionEvent, SliderCallbackN1(source))

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

class SliderCallbackN1():
    def __init__(self, source):
        self.source = source

    def __call__(self, caller, ev):
        sliderWidget = caller
        value = sliderWidget.GetRepresentation().GetValue()
        if value >= 0 and value < 1:
        	self.source.SetFileName(knee_list[0])
        elif value >= 1 and value < 2:
        	self.source.SetFileName(knee_list[1])
        elif value >= 2 and value < 3:
        	self.source.SetFileName(knee_list[2])
        elif value >= 3 and value < 4:
        	self.source.SetFileName(knee_list[3])
        elif value >= 4 and value < 5:
        	self.source.SetFileName(knee_list[4])
        elif value >= 5 and value < 6:
        	self.source.SetFileName(knee_list[5])
        elif value >= 6 and value < 7:
        	self.source.SetFileName(knee_list[6])

if __name__ == '__main__':
    main()