# ***************************************************************************
# *                                                                         *
# *   Copyright (c) 2016 - Bernd Hahnebach <bernd@bimstatik.org>            *
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU Lesser General Public License (LGPL)    *
# *   as published by the Free Software Foundation; either version 2 of     *
# *   the License, or (at your option) any later version.                   *
# *   for detail see the LICENCE text file.                                 *
# *                                                                         *
# *   This program is distributed in the hope that it will be useful,       *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU Library General Public License for more details.                  *
# *                                                                         *
# *   You should have received a copy of the GNU Library General Public     *
# *   License along with this program; if not, write to the Free Software   *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# *   USA                                                                   *
# *                                                                         *
# ***************************************************************************

__title__ = "Command nonlinear mechanical material"
__author__ = "Bernd Hahnebach"
__url__ = "http://www.freecadweb.org"


import FreeCAD
from FemCommands import FemCommands

if FreeCAD.GuiUp:
    import FreeCADGui
    from PySide import QtCore


class _CommandMaterialMechanicalNonlinear(FemCommands):
    "The Fem_MaterialMechanicalNonlinear command definition"
    def __init__(self):
        super(_CommandMaterialMechanicalNonlinear, self).__init__()
        self.resources = {'Pixmap': 'fem-material',
                          'MenuText': QtCore.QT_TRANSLATE_NOOP("Fem_MaterialMechanicalNonlinear", "Nonlinear mechanical material"),
                          'Accel': "C, W",
                          'ToolTip': QtCore.QT_TRANSLATE_NOOP("Fem_MaterialMechanicalNonlinear", "Creates a nonlinear mechanical material")}
        self.is_active = 'with_material'

    def Activated(self):
        sel = FreeCADGui.Selection.getSelection()
        if len(sel) == 1 and sel[0].isDerivedFrom("App::MaterialObjectPython"):
            lin_mat_obj = sel[0]
            # check if an nonlinear material exists which is based on the selected material already
            allow_nonlinear_material = True
            for o in FreeCAD.ActiveDocument.Objects:
                if hasattr(o, "Proxy") and o.Proxy is not None and o.Proxy.Type == "FemMaterialMechanicalNonlinear" and o.LinearBaseMaterial == lin_mat_obj:
                    FreeCAD.Console.PrintError(o.Name + ' is based on the selected material: ' + lin_mat_obj.Name + '. Only one nonlinear object for each material allowed.\n')
                    allow_nonlinear_material = False
                    break
            if allow_nonlinear_material:
                string_lin_mat_obj = "App.ActiveDocument.getObject('" + lin_mat_obj.Name + "')"
                command_to_run = "FemGui.getActiveAnalysis().Member = FemGui.getActiveAnalysis().Member + [FemMaterialMechanicalNonlinear.makeFemMaterialMechanicalNonlinear(" + string_lin_mat_obj + ")]"
                FreeCAD.ActiveDocument.openTransaction("Create FemMaterialMechanicalNonlinear")
                FreeCADGui.addModule("FemMaterialMechanicalNonlinear")
                FreeCADGui.doCommand(command_to_run)

if FreeCAD.GuiUp:
    FreeCADGui.addCommand('Fem_MaterialMechanicalNonlinear', _CommandMaterialMechanicalNonlinear())
