#!/usr/bin/python
# This file is part of MSMBuilder.
#
# Copyright 2011 Stanford University
#
# MSMBuilder is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import sys
import numpy as np

import ArgLib

from msmbuilder import Serializer

def run(assignments, ass_rmsd, rmsdcutoff, output):
    ArgLib.CheckPath(output)
    assignments[ np.where(ass_rmsd > rmsdcutoff) ] = -1
    Serializer.SaveData(output, assignments)
    print "Wrote:", output
    return


if __name__ == "__main__":
    print """
\nTrims assignments based on the distance to their generator. Useful for
eliminating bad assignments from a coase clustering. Note that this
discards (expensive!) data, so should only be used if an optimal
clustering is not available.

Note: Check your cluster sized with CalculateClusterRadii.py to get
a handle on how big they are before you trim. Recall the radius is the
*average* distance to the generator, here you are enforcing the
*maximum* distance.

Output: A trimmed assignments file (Assignments.Trimmed.h5).\n"""

    arglist=["assignments", "assrmsd", "rmsdcutoff","outdir"]
    options=ArgLib.parse(arglist, Custom=[("rmsdcutoff", 
        "RMSD value at which to trim, in nm. Data further than this value in RMSD from its generator will be discarded.", None), 
        ("assignments", "Path to assignments file. Default: Data/Assignments.Fixed.h5", "Data/Assignments.Fixed.h5") ])
    print sys.argv

    assignments = Serializer.LoadData(options.assignments)
    ass_rmsd    = Serializer.LoadData(options.assrmsd)
    output      = options.outdir+'/Assignments.Trimmed.h5'
    rmsdcutoff  = float(options.rmsdcutoff)

    run(assignments, ass_rmsd, rmsdcutoff, output)