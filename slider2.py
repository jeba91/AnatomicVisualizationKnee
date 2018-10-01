import vtk
import sys

#change the 

def main():
	# Create the tail of the pipeline:
	# - Renderer
	# - RenderWindow
	# - RenderWindowInteractor
	colors = vtk.vtkNamedColors()
	colors.SetColor("SkinColor", [144, 125, 64, 255])
	colors.SetColor("BkgColor", [51, 77, 102, 255])


	# make renderer with a certain background
	ren1 = vtk.vtkRenderer()
	ren1.SetBackground(0.4, 0.4, 0.4)
	ren1.SetBackground2(0.9, 0.9, 0.9)
	ren1.GradientBackgroundOn()

	renWin = vtk.vtkRenderWindow()
	renWin.AddRenderer(ren1)
	renWin.SetSize(700, 700)

	iren = vtk.vtkRenderWindowInteractor()
	iren.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
	iren.SetRenderWindow(renWin)

	# create the main visualization pipeline:
	# source -> contour -> decimate -> smooth -> normals -> mapper -> actor

	source = vtk.vtkDataSetReader()
	source.SetFileName(sys.argv[1])
	source.Update()
	srange = source.ReadOutputType()

	# get the skin
	skinExtractor = vtk.vtkMarchingCubes()
	skinExtractor.SetInputConnection(source.GetOutputPort())
	skinExtractor.SetValue(1, 100)
	skinStripper = vtk.vtkStripper()
	skinStripper.SetInputConnection(skinExtractor.GetOutputPort())
	skinMapper = vtk.vtkPolyDataMapper()
	skinMapper.SetInputConnection(skinStripper.GetOutputPort())
	skinMapper.ScalarVisibilityOff()
	skin = vtk.vtkActor()

	skin.SetMapper(skinMapper)
	skin.GetProperty().SetDiffuseColor(colors.GetColor3d("SkinColor"))
	skin.GetProperty().SetSpecular(.3)
	skin.GetProperty().SetSpecularPower(40)
	skin.GetProperty().SetOpacity(.7)

	ren1.AddActor(skin)



	def showBones(obj, ev):
	    print("Before Event")
	    skinMapper.ScalarVisibilityOff()
	    print('ga nou uit')
	    renWin.Render()

	# Setup a slider widget for each varying parameter
	tubeWidth = 0.008
	sliderLength = 0.008
	titleHeight = 0.04
	labelHeight = 0.04

	sliderRepN1 = vtk.vtkSliderRepresentation2D()

	sliderRepN1.SetMinimumValue(0.0)
	sliderRepN1.SetMaximumValue(1000.0)
	sliderRepN1.SetValue(100.0)
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

	sliderWidgetN1.AddObserver(vtk.vtkCommand.InteractionEvent, SliderCallbackN1(skinExtractor))

	# Initialize and start the event handler
	iren.Initialize()
	iren.Start()


class SliderCallbackN1():
    def __init__(self, skinExtractor):
        self.skinExtractor = skinExtractor

    def __call__(self, caller, ev):
        sliderWidget = caller
        value = sliderWidget.GetRepresentation().GetValue()
        self.skinExtractor.SetValue(1, value)


if __name__ == '__main__':
    main()
