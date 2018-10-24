import vtk
import sys
import time

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

class MyInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):

    def __init__(self,parent=None):
        self.parent = iren
        self.bones = False
        self.muscles = False
        self.skin = False


        self.AddObserver("KeyPressEvent",self.keyPressEvent)

    def keyPressEvent(self,obj,event):
      key = self.parent.GetKeySym()
      if key == 'b':
        if self.bones == False:
          print("I want to see a bone")
          ren.AddActor(boneActor)
          iren.GetRenderWindow().Render()
          self.bones = True
        else:
          print("I want to unsee the bone")
          ren.RemoveActor(boneActor)
          iren.GetRenderWindow().Render()
          self.bones = False
      if key == 'p':
        print("let start this thing")
        for i in range(len(muscle_list)):
          knee.SetFileName(knee_list[i])
          bones.SetFileName(bone_list[i])
          muscle.SetFileName(muscle_list[i])
          iren.GetRenderWindow().Render()



class SliderCallbackN1():
    def __init__(self, knee, bones, muscle):
        self.knee = knee
        self.bones = bones
        self.muscle = muscle

    def __call__(self, caller, ev):
        sliderWidget = caller
        value = sliderWidget.GetRepresentation().GetValue()
        if value >= 0 and value < 1:
          self.knee.SetFileName(knee_list[0])
          self.bones.SetFileName(bone_list[0])
          self.muscle.SetFileName(muscle_list[0])
        elif value >= 1 and value < 2:
          self.knee.SetFileName(knee_list[1])
          self.bones.SetFileName(bone_list[1])
          self.muscle.SetFileName(muscle_list[1])
        elif value >= 2 and value < 3:
          self.knee.SetFileName(knee_list[2])
          self.bones.SetFileName(bone_list[2])
          self.muscle.SetFileName(muscle_list[2])
        elif value >= 3 and value < 4:
          self.knee.SetFileName(knee_list[3])
          self.bones.SetFileName(bone_list[3])
          self.muscle.SetFileName(muscle_list[3])
        elif value >= 4 and value < 5:
          self.knee.SetFileName(knee_list[4])
          self.bones.SetFileName(bone_list[4])
          self.muscle.SetFileName(muscle_list[4])
        elif value >= 5 and value < 6:
          self.knee.SetFileName(knee_list[5])
          self.bones.SetFileName(bone_list[5])
          self.muscle.SetFileName(muscle_list[5])
        elif value >= 6 and value < 7:
          self.knee.SetFileName(knee_list[6])
          self.bones.SetFileName(bone_list[6])
          self.muscle.SetFileName(muscle_list[6])

class SliderOpacity():
    def __init__(self, knee):
        self.knee = knee

    def __call__(self, caller, ev):
      sliderWidget = caller
      value = sliderWidget.GetRepresentation().GetValue()
      if value >= 0 and value < 100:

        print("i want to change this slide")
        skinActor.GetProperty().SetOpacity(value/100)

        # ren.AddActor(skinActor)
        renWin.Render()

class BoneOpacity():
    def __init__(self, knee):
        self.knee = knee

    def __call__(self, caller, ev):
      sliderWidget = caller
      value = sliderWidget.GetRepresentation().GetValue()
      if value >= 0 and value < 100:


        print("i want to change this slide")
        boneActor.GetProperty().SetOpacity(value/100)

        # ren.AddActor(skinActor)
        renWin.Render()

class MuscleOpacity():
    def __init__(self, muscle):
        self.muscle = muscle

    def __call__(self, caller, ev):
      sliderWidget = caller
      value = sliderWidget.GetRepresentation().GetValue()
      if value >= 0 and value < 100:
        muscleActor.GetProperty().SetOpacity(value/100)
        volumeGradientOpacity.AddPoint(100, 1/value)
        volumeProperty.SetScalarOpacity(volumeScalarOpacity)

        volume.SetProperty(volumeProperty)
        ren.AddViewProp(volume)

        # ren.AddActor(skinActor)
        renWin.Render()

class ChangeRenderStyle():
    def __init__(self, muscle):
      self.muscle = muscle

    def __call__(self, caller, ev):
      sliderWidget = caller
      value = sliderWidget.GetRepresentation().GetValue()
      if value >= 0.5:
        ren.RemoveActor(boneActor)
        ren.RemoveActor(skinActor)
        ren.RemoveActor(muscleActor)
        ren.AddActor(volumeBone)
        ren.AddActor(volumeKnee)
        ren.AddActor(volumeMuscle)
      elif value < 0.5:
        ren.RemoveActor(volumeBone)
        ren.RemoveActor(volumeKnee)
        ren.RemoveActor(volumeMuscle)
        ren.AddActor(boneActor)
        ren.AddActor(skinActor)
        ren.AddActor(muscleActor)

def createSliderStyle(min,max,value,point1,point2,title,dim):
  SliderStyle = vtk.vtkSliderRepresentation2D()
  SliderStyle.SetMinimumValue(min)
  SliderStyle.SetMaximumValue(max)
  SliderStyle.SetValue(value)
  SliderStyle.SetTitleText(title)
  SliderStyle.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
  SliderStyle.GetPoint1Coordinate().SetValue(point1[0], point1[1])
  SliderStyle.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
  SliderStyle.GetPoint2Coordinate().SetValue(point2[0], point2[1])
  SliderStyle.SetTubeWidth(dim[0])
  SliderStyle.SetSliderLength(dim[1])
  SliderStyle.SetTitleHeight(dim[2])
  SliderStyle.SetLabelHeight(dim[3])
  return SliderStyle


knee_list   = ['knee1_1.vtk','knee1_2.vtk','knee1_3.vtk','knee1_4.vtk','knee1_5.vtk','knee1_6.vtk','knee1_7.vtk']
bone_list   = ['knie1.vti','knie2.vti','knie3.vti','knie4.vti','knie5.vti','knie6.vti','knie7.vti']
muscle_list = ['spier1.vti','spier2.vti','spier3.vti','spier4.vti','spier5.vti','spier6.vti','spier7.vti']

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
iren.SetInteractorStyle(MyInteractorStyle())
iren.SetRenderWindow(renWin)


# Load the files
knee = vtk.vtkDataSetReader()
knee.SetFileName(knee_list[0])

bones = vtk.vtkXMLImageDataReader()
bones.SetFileName(bone_list[0])

muscle = vtk.vtkXMLImageDataReader()
muscle.SetFileName(muscle_list[0])


### Volume Rendering Skin ###
scalarKnee  = [50,100,200,300]
colorKnee   = [[0.0, 0.0, 0.0],[1.0,0.5,0.3],[1.0,0.5,0.3],[0.0,0.0,0.0]]
opacKnee    = [0.00,0.10,0.25,0.00]
pieceKnee   = [0.0,0.1,0.2]
volumeKnee  = createVolumeRender(knee,scalarKnee,colorKnee,opacKnee,pieceKnee)

### Volume Rendering Bone ###
scalarBone  = [50,51,1100,1101]
colorBone   = [[0.0, 0.0, 0.0],[1.0,1.0,0.9],[1.0,1.0,0.9],[0.0,0.0,0.0]]
opacBone    = [0.00,1.00,1.00,0.00]
pieceBone   = [0.0,1.0,1.0]
volumeBone  = createVolumeRender(bones,scalarBone,colorBone,opacBone,pieceBone)

### Volume Rendering Muscle ###
scalarMuscle    = [50,51,1100,1101]
colorMuscle     = [[0.0, 0.0, 0.0],[1.0,0.0,0.0],[1.0,0.0,0.0],[0.0,0.0,0.0]]
opacMuscle      = [0.00,0.05,0.1,0.00]
pieceMuscle     = [0.0,1.0,1.0]
volumeMuscle    = createVolumeRender(muscle,scalarMuscle,colorMuscle,opacMuscle,pieceMuscle)

# make the datasets
skinActor = createKneeSkin(knee,35, 20 )
skinActor.GetProperty().SetColor(colors.GetColor3d("SkinColor"))
skinActor.GetProperty().SetOpacity(0.2)

# make the bone actor:
boneActor  = createKneeSkin(bones, 50, 10 )
boneActor.GetProperty().SetColor(colors.GetColor3d("white"))
boneActor.GetProperty().SetOpacity(0.9)

# make the muscle actor:
muscleActor  = createKneeSkin(muscle, 50,40 )
muscleActor.GetProperty().SetColor(colors.GetColor3d("red"))
muscleActor.GetProperty().SetOpacity(0.9)

# Add the actors to the renderer
ren.AddActor(boneActor)
ren.AddActor(skinActor)
ren.AddActor(muscleActor)


# make slider
StyleDim = [0.008,0.008,0.03,0.02]
StyleN1 = createSliderStyle(0,7,0,[0.1,0.1],[0.9,0.1], "Knee flexion", StyleDim)

sliderWidgetN1 = vtk.vtkSliderWidget()
sliderWidgetN1.SetInteractor(iren)
sliderWidgetN1.SetRepresentation(StyleN1)
sliderWidgetN1.SetAnimationModeToAnimate()
sliderWidgetN1.EnabledOn()

sliderWidgetN1.AddObserver(vtk.vtkCommand.InteractionEvent, SliderCallbackN1(knee, bones, muscle))

### Skin Opacity Slider ###
StyleDim = [0.008,0.008,0.015,0.015]
StyleSkin = createSliderStyle(0,100,20,[0.7,0.9],[0.9,0.9], "Skin opacity", StyleDim)

sliderSkinWidget = vtk.vtkSliderWidget()
sliderSkinWidget.SetInteractor(iren)
sliderSkinWidget.SetRepresentation(StyleSkin)
sliderSkinWidget.SetAnimationModeToAnimate()
sliderSkinWidget.EnabledOn()

sliderSkinWidget.AddObserver(vtk.vtkCommand.InteractionEvent, SliderOpacity(knee))

### Bone Opacity Slider ###
StyleDim = [0.008,0.008,0.015,0.015]
styleBone = createSliderStyle(0,100,20,[0.7,0.8],[0.9,0.8], "Bone opacity", StyleDim)

sliderBoneWidget = vtk.vtkSliderWidget()
sliderBoneWidget.SetInteractor(iren)
sliderBoneWidget.SetRepresentation(styleBone)
sliderBoneWidget.SetAnimationModeToAnimate()
sliderBoneWidget.EnabledOn()

sliderBoneWidget.AddObserver(vtk.vtkCommand.InteractionEvent, BoneOpacity(knee))

### Muscle Opacity Slider ###
StyleDim = [0.008,0.008,0.015,0.015]
styleMuscle = createSliderStyle(0,100,20,[0.7,0.7],[0.9,0.7], "Muscle opacity", StyleDim)

sliderMuscleWidget = vtk.vtkSliderWidget()
sliderMuscleWidget.SetInteractor(iren)
sliderMuscleWidget.SetRepresentation(styleMuscle)
sliderMuscleWidget.SetAnimationModeToAnimate()
sliderMuscleWidget.EnabledOn()

sliderMuscleWidget.AddObserver(vtk.vtkCommand.InteractionEvent, MuscleOpacity(muscle))

### Render Style Slider ###
StyleDim = [0.008,0.008,0.015,0.015]
styleStyle = createSliderStyle(0,1,0,[0.7,0.6],[0.9,0.6], "Render Style", StyleDim)

SliderStyleWidget = vtk.vtkSliderWidget()
SliderStyleWidget.SetInteractor(iren)
SliderStyleWidget.SetRepresentation(styleStyle)
SliderStyleWidget.SetAnimationModeToAnimate()
SliderStyleWidget.EnabledOn()
SliderStyleWidget.AddObserver(vtk.vtkCommand.InteractionEvent, ChangeRenderStyle(muscle))

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


















