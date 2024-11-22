
OVERVIEW
=======================

This is a modified version of ASE that introduces 2D lattices and cracks. The original library
was developed by Ask Hjorth Larsen et al 2017 J. Phys.: Condens. Matter 29 273002 and now newer
developers. All credit for base functionality goes to them.

The documentation for the base version of ASE can be found at http://wiki.fysik.dtu.dk/ase

REQUIREMENTS
-----------------------

Refer to https://github.com/hainm/ase

INSTALLATION
-----------------------
The library can be cloned like this::
    $ git clone https://github.com/svachher1/ase

ADDED FUNCTIONALITIES
-----------------------

In ase.build added the following functions:
    ase.build.hexagonal
    ase.build.square
    ase.build.rectangle
    ase.build.oblique

Added a new a new fracture module:
    ase.fracture
    current functions within ase.fracture
        ase.fracture.initialize_crack

LICENSE
-----------------------
This project is licensed under GNU General Lesser Public License used by ASE.
Modifications made in this version are also under the same license

ASE is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 2.1 of the License, or
(at your option) any later version.

ASE is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with ASE.  If not, see <http://www.gnu.org/licenses/>.

Example
-----------------------
Build a 2D hexagonal lattice with 60 atoms in the x direction and 15 in the y direction
The lattice spacing is 2 A, and a crack is initialized in the 100 direction halway at
the line y = 16 (2 A* 8 atoms)--i.e. midpoint of y atoms and halway through x atoms

>>> from ase.io import write
>>> from ase.build import hexagonal
>>> from ase.fracture import initialize_crack
>>> atoms = hexagonal('C', 2, size = (60, 15, 1), vacuum = 0.125)
>>> write('hexagonal_lattice.xyz', atoms, format = 'lammps-data')
>>> initialize_crack('hexagonal_lattice.xyz', 'hexagonal_lattice_fractured.xyz', stretch = 1.0, width = 1 , direction = 'x', format = 'lammps-data')

::
   $ ase gui hexagonal_lattice_fractured_POSCAR

.. image :: C:\Users\sahil\OneDrive\Desktop\PHY381C\cracked.png
  :width 800 

