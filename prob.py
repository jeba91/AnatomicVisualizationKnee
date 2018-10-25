import vtk 
import sys








filename1 = 'pees1_6.vti'
filename2 = 'pees2_6.vti'
filename2 = 'ligament1_6.vti'
filename3 = 'ligament2_6.vti'
filename4  = 'kneecap_6.vti'
vessels = 'vessels_6.vti'
knee  = 'knee_6.vti'



def createKneeSkin(reader, value, smooth):

  isoValue = value
  mcubes = vtk.vtkMarchingCubes()
  mcubes.SetInputConnection(reader.GetOutputPort())
  mcubes.ComputeScalarsOff()
  mcubes.ComputeGradientsOff()
  mcubes.ComputeNormalsOff()
  mcubes.SetValue(0, isoValue)

  smoothingIterations = smooth
  passBand = 0.001
  featureAngle = 60.0
  smoother = vtk.vtkWindowedSincPolyDataFilter()
  smoother.SetInputConnection(mcubes.GetOutputPort())
  smoother.SetNumberOfIterations(smoothingIterations)
  smoother.BoundarySmoothingOff()
  smoother.FeatureEdgeSmoothingOff()
  smoother.SetFeatureAngle(featureAngle)
  smoother.SetPassBand(passBand)
  smoother.NonManifoldSmoothingOn()
  smoother.NormalizeCoordinatesOn()
  smoother.Update()

  normals = vtk.vtkPolyDataNormals()
  normals.SetInputConnection(smoother.GetOutputPort())
  normals.SetFeatureAngle(featureAngle)

  stripper = vtk.vtkStripper()
  stripper.SetInputConnection(normals.GetOutputPort())

  mapper = vtk.vtkPolyDataMapper()
  mapper.SetInputConnection(stripper.GetOutputPort())

  actor = vtk.vtkActor()
  actor.SetMapper(mapper)

  return actor




  #set the colors
colors = vtk.vtkNamedColors()
colors.SetColor("SkinColor", [255, 125, 64, 255])

# set the renderer
ren = vtk.vtkRenderer()
ren.SetBackground(0.2,0.2,0.2)

# set the renderWindow
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
renWin.SetSize(1000, 1000)

# Set the interactore
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

# Load the files
knee = vtk.vtkDataSetReader()
knee.SetFileName('knee1_6.vtk')


pees1 = vtk.vtkXMLImageDataReader()
pees2  = vtk.vtkXMLImageDataReader()

pees2.SetFileName("pees2_6.vti")
pees1.SetFileName("pees1_6.vti")

ligament1 = vtk.vtkXMLImageDataReader()
ligament2  = vtk.vtkXMLImageDataReader()

ligament1.SetFileName('ligament1_6.vti')
ligament2.SetFileName('ligament2_6.vti')


vessel = vtk.vtkXMLImageDataReader()
vessel.SetFileName('vessels_6.vti')


kniecap = vtk.vtkXMLImageDataReader()
kniecap.SetFileName('kneecap_6.vti')

# make the datasets
skinActor = createKneeSkin(knee,100, 20 )
skinActor.GetProperty().SetColor(colors.GetColor3d("SkinColor"))
skinActor.GetProperty().SetOpacity(0.2)

# make the bone actor:
boneActor  = createKneeSkin(kniecap, 50, 10 )
boneActor.GetProperty().SetColor(colors.GetColor3d("white"))
boneActor.GetProperty().SetOpacity(0.9)

# make the muscle actor:
pees1Actor  = createKneeSkin(pees1, 100,5 )
pees1Actor.GetProperty().SetColor(colors.GetColor3d("blue"))
pees1Actor.GetProperty().SetOpacity(0.9)

# make the muscle actor:
pees2Actor  = createKneeSkin(pees2, 100,5 )
pees2Actor.GetProperty().SetColor(colors.GetColor3d("blue"))
pees2Actor.GetProperty().SetOpacity(0.9)


# Add the actors to the renderer
ren.AddActor(boneActor)
ren.AddActor(pees1Actor)
ren.AddActor(pees2Actor)

# make the muscle actor:
ligament1Actor  = createKneeSkin(ligament1, 50,40 )
ligament1Actor.GetProperty().SetColor(colors.GetColor3d("green"))
ligament1Actor.GetProperty().SetOpacity(0.3)

# make the muscle actor:
ligament2Actor  = createKneeSkin(ligament2, 50,40 )
ligament2Actor.GetProperty().SetColor(colors.GetColor3d("green"))
ligament2Actor.GetProperty().SetOpacity(0.3)

# make the muscle actor:
vesselActor  = createKneeSkin(vessel, 100,5 )
vesselActor.GetProperty().SetColor(colors.GetColor3d("red"))
vesselActor.GetProperty().SetOpacity(0.1)

ren.AddActor(ligament1Actor)
ren.AddActor(ligament2Actor)
ren.AddActor(vesselActor)
ren.AddActor(skinActor)


renWin.Render()
iren.Initialize()
iren.Start()

print ("Cleanup time")

# Free up any objects we created (useless really, as we quit anyway)
contour = None
mapper = None
actor = None
ren1 = None
renWin = None



