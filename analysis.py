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
source.SetFileName(sys.argv[1])

# force the source to read the data set so that we can obtain its scalar range
source.Update()
srange = source.GetOutput().GetScalarRange()
print(srange)


vtk.vtkChartHistogram2D(source)

