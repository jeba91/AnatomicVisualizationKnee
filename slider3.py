import vtk
import sys
# from vtk import *	

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
	
	reader = vtk.vtkStructuredPointsReader()
	reader.SetFileName("Liver.vtk")

	MIP = vtk.vtkVolumeRayCastMIPFunction()
	volumeMapper = vtkVolumeRayCastMapper()
	volumeMapper.SetVolumeRayCastFunction(MIP)
	volumeMapper.SetInputConnection(source.GetOutputPort())

	volume = vtkVolume()
	volume.SetMapper(volumeMapper)

	ren = vtkRenderer()
	ren.AddVolume(volume)
	ren.SetBackground(0.1, 0.1, 0.2)

	renWin = vtkRenderWindow()
	renWin.AddRenderer(ren)
	renWin.SetWindowName("Volume rendering of Liver data");
	renWin.SetSize(500, 500)

	iren = vtkRenderWindowInteractor()
	iren.SetRenderWindow(renWin)
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
