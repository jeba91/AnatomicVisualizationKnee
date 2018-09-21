import vtk
import sys

# Create the tail of the pipeline:
# - Renderer
# - RenderWindow
# - RenderWindowInteractor
colors = vtk.vtkNamedColors()

colors.SetColor("SkinColor", [255, 125, 64, 255])
colors.SetColor("BkgColor", [51, 77, 102, 255])


# make renderer with a certain background
ren1 = vtk.vtkRenderer()
ren1.SetBackground(0.2, 0.2, 0.2)
ren1.SetBackground2(0.5, 0.5, 0.5)
ren1.GradientBackgroundOn()

renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren1)
renWin.SetSize(700, 700)

iren = vtk.vtkRenderWindowInteractor()
iren.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
iren.SetRenderWindow(renWin)

# iren.SetRenderWindow(renWin)


# create the main visualization pipeline:
# source -> contour -> decimate -> smooth -> normals -> mapper -> actor

source = vtk.vtkDataSetReader()
source.SetFileName(sys.argv[1])
source.Update()
srange = source.ReadOutputType()

#srange = source.GetOutput().GetScalarRange()
#print(srange)

# skin
# contour = vtk.vtkContourFilter()
# contour.SetInputConnection(source.GetOutputPort())
# contour.SetValue(0, 500)

# get the skin
skinExtractor = vtk.vtkMarchingCubes()
skinExtractor.SetInputConnection(source.GetOutputPort())
skinExtractor.SetValue(0, 100)
skinStripper = vtk.vtkStripper()
skinStripper.SetInputConnection(skinExtractor.GetOutputPort())
skinMapper = vtk.vtkPolyDataMapper()
skinMapper.SetInputConnection(skinStripper.GetOutputPort())
skinMapper.ScalarVisibilityOff()
skin = vtk.vtkActor()

skin.SetMapper(skinMapper)
skin.GetProperty().SetDiffuseColor(colors.GetColor3d("SkinColor"))
skin.GetProperty().SetSpecular(.3)
skin.GetProperty().SetSpecularPower(20)
skin.GetProperty().SetOpacity(.7)


# add the bones
# boneExtractor = vtk.vtkMarchingCubes()
# boneExtractor.SetInputConnection(source.GetOutputPort())
# boneExtractor.SetValue(100,150)

# boneStripper = vtk.vtkStripper()
# boneStripper.SetInputConnection(boneExtractor.GetOutputPort())

# boneMapper = vtk.vtkPolyDataMapper()
# boneMapper.SetInputConnection(boneStripper.GetOutputPort())
# boneMapper.ScalarVisibilityOff()

# bone = vtk.vtkActor()
# bone.SetMapper(boneMapper)
# bone.GetProperty().SetDiffuseColor(colors.GetColor3d("Ivory"))

# ren1.AddActor(bone)
ren1.AddActor(skin)


# Start by creating a black/white lookup table.
bwLut = vtk.vtkLookupTable()
bwLut.SetTableRange(0, 2000)
bwLut.SetSaturationRange(0, 0)
bwLut.SetHueRange(0, 0)
bwLut.SetValueRange(0, 1)
bwLut.Build()


sagittalColors = vtk.vtkImageMapToColors()
sagittalColors.SetInputConnection(source.GetOutputPort())
sagittalColors.SetLookupTable(bwLut)
sagittalColors.Update()

sagittal = vtk.vtkImageActor()
sagittal.GetMapper().SetInputConnection(sagittalColors.GetOutputPort())
sagittal.SetDisplayExtent(128, 128, 0, 255, 0, 92)

ren1.AddActor(sagittal)



outlineData = vtk.vtkOutlineFilter()
outlineData.SetInputConnection(source.GetOutputPort())

mapOutline = vtk.vtkPolyDataMapper()
mapOutline.SetInputConnection(outlineData.GetOutputPort())

outline = vtk.vtkActor()
outline.SetMapper(mapOutline)
outline.GetProperty().SetColor(colors.GetColor3d("Black"))


# contour2 = vtk.vtkContourFilter()
# contour2.SetInputConnection(source.GetOutputPort())
# contour2.SetValue(20, 100)

# decimate = vtk.vtkDecimatePro()
# decimate.SetInputConnection(contour.GetOutputPort())
# decimate.SetTargetReduction(0.9)
# decimate.PreserveTopologyOn()

# smooth = vtk.vtkSmoothPolyDataFilter()
# smooth.SetInputConnection(contour.GetOutputPort())
# smooth.SetNumberOfIterations(50)

# normals = vtk.vtkPolyDataNormals()
# normals.SetInputConnection(smooth.GetOutputPort())

# mapper = vtk.vtkPolyDataMapper()
# mapper.SetInputConnection(contour.GetOutputPort())
# # Do not use scalar values in colouring the contour
# mapper.ScalarVisibilityOff()

# mapper2 = vtk.vtkPolyDataMapper()
# mapper2.SetInputConnection(contour2.GetOutputPort())
# # Do not use scalar values in colouring the contour
# mapper2.ScalarVisibilityOff()



# actor = vtk.vtkActor()
# actor.SetMapper(mapper)
# actor.GetProperty().SetColor(100,0,0)
# ren1.AddActor(actor)


# actor2 = vtk.vtkActor()
# actor2.SetMapper(mapper2)
# actor2.GetProperty().SetColor(0,100,100)
# ren1.AddActor(actor2)


def showBones(obj, ev):
    print("Before Event")
    skinMapper.ScalarVisibilityOff()
    print('ga nou uit')
    renWin.Render()



# add a camera
aCamera = vtk.vtkCamera()
aCamera.SetViewUp(0, 0, -1)
aCamera.SetPosition(0, -1, 0)
aCamera.SetFocalPoint(0, 0, 0)
aCamera.ComputeViewPlaneNormal()
aCamera.Azimuth(30.0)
aCamera.Elevation(30.0)
ren1.SetActiveCamera(aCamera)



# Export to Alias Wavefront format (generates objexport.obj and .mtl files)
obj = vtk.vtkOBJExporter()
obj.SetInput(renWin)
obj.SetFilePrefix("objexport")
obj.Write()

# Initialize and start the event handler

#iren.RemoveObservers('LeftButtonPressEvent')
iren.AddObserver('LeftButtonPressEvent', showBones, 1.0)
iren.Initialize()
iren.Start()

# We won't reach this until the user has pressed 'q', 'e' or closed the
# RenderWindow
print( "Cleanup time")

# Free up any objects we created (useless really, as we quit anyway)
contour = None
mapper = None
actor = None
ren1 = None
renWin = None

