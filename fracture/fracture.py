"""Functions to initialize a crack in a 2D lattice"""

import numpy as np
from ase.io import read, write

def _bulk_stretch(a, a_top, a_bot, midpoint, stretch = 1.0):
    """
    This function determines the new location of the atom after the lattice has been stretched


    Args:
       a (float): a coordinate of the atom (a can be x or y coord)
       a_top (float): 'a' coordinate of the top row
       a_bot (float): 'a' coordinate of the bot row
       midpoint (float): the point of symmetry in either x or y direction
       stretch (float): The amount the top row of the lattice was stretched.

    Return:
       scale (float): The amount that the row coordinate will be scaled by.
    """
    if a > midpoint:
        scale = stretch * (a - midpoint) / (a_top - midpoint)
    elif a < midpoint:
        scale = -1 * stretch * (a - midpoint) / (a_bot - midpoint)
    else:
        scale = 0
    return scale

def _crack_stretch(coor, xhi, yhi, xlo, ylo, stretch, width, horizontal_shift = None, vertical_shift = None, direction = 'x'):
    """
    This function generations the initial condition of the lattice with a crack

    Args:
        coor (array): The coordinate of the atom
        xhi (float): The coordinate of the top row of x_direction
        yhi (float): The coordinate of the top row of y_direction
        xlo (float): The coordinate of the bot row of x_direction
        ylo (float): The coordinate of the bot row of y_direction
        stretch (float): Distance that top row is to be moved
        width (float): determines the shape of the crack, crack width, higher the number, narrower the width, != 0
        horizontal_shift (float): How deep the crack should be
        vertical_shift (float) : Where the crack should be along the axis
        direction (string): 'x' or 'y'. Direction in which the crack should be initialzied
    Return:
        initial (array): Array of coordinates for the initial condition
    """

    if direction == "x":
        # check if vertical and horizontal shifts are provided
        if not horizontal_shift:
            horizontal_shift = xhi / 2
        if not vertical_shift:
            vertical_shift = yhi / 2

        new_coor = (_bulk_stretch(coor[1], yhi, ylo, vertical_shift, stretch) - np.sign(coor[1] - vertical_shift) * stretch) / 2.0 * np.tanh((coor[0] - horizontal_shift) / width) + \
                   (_bulk_stretch(coor[1], yhi, ylo, vertical_shift, stretch) + np.sign(coor[1] - vertical_shift) * stretch) / 2.0
        initial = np.array([coor[0], coor[1] + new_coor, coor[2]])
    elif direction == "y":
        # check if vertical and horizontal shifts are provided
        if not horizontal_shift:
            horizontal_shift = yhi / 2
        if not vertical_shift:
            vertical_shift = xhi / 2

        new_coor = (_bulk_stretch(coor[0], xhi, xlo, vertical_shift, stretch) - np.sign(coor[0] - vertical_shift) * stretch) / 2.0 * np.tanh((coor[1] - horizontal_shift) / width) + \
                   (_bulk_stretch(coor[0], xhi, xlo, vertical_shift, stretch) + np.sign(coor[0] - vertical_shift) * stretch) / 2.0
        initial = np.array([coor[0] + new_coor, coor[1], coor[2]])
    return initial

def _crack_positions(positions, stretch, width, horizontal_shift = None, vertical_shift = None, direction = 'x'):
    """
    This function takes in the positions and returns positions of an initialized crack

    Args:
        positions (ndarray of shape (N,3)): positions array for atoms in lattice
        stretch (float): Distance that top row is to be moved
        width (float): determines the shape of the crack, crack width, higher the number, narrower the width, != 0
        horizontal_shift (float): How deep the crack should be
        vertical_shift (float) : Where the crack should be along the axis
        direction (string): 'x' or 'y'. Direction in which the crack should be initialzied
    Return:
        new_coords (ndarray of shape (N,3)) : new positions with initialized crack
    """
    xhi = np.max(positions[:, 0])
    yhi = np.max(positions[:, 1])
    xlo = np.min(positions[:, 0])
    ylo = np.min(positions[:, 1])

    new_coords = np.empty(positions.shape)
    for i in range(positions.shape[0]):
        new_pos = _crack_stretch(positions[i], xhi, yhi, xlo, ylo, stretch, width, horizontal_shift, vertical_shift, direction)
        new_coords[i][0], new_coords[i][1], new_coords[i][2] = new_pos

    return new_coords

def initialize_crack(filename, new_filename, stretch, width = 1, horizontal_shift = None, vertical_shift = None, direction = 'x', format = "lammps-data"):
    """
    Reads in a file with coordinates of atoms and writes a new file with initialzed crack

    Args:
        filename (string or file): path to where the file is or file
        new_filename (string or file): path to where the new file should be written or new file
        width (float): determines the shape of the crack, crack width, higher the number, narrower the width, != 0
        stretch (float): Distance that top row is to be moved
        horizontal_shift (float): How deep the crack should be
        vertical_shift (float) : Where the crack should be along the axis
        direction (string): 'x' or 'y'. Direction in which the crack should be initialzied
        format (string): Used to specify the file-format. By default lammps-data
    Returns:
        None
    """
    atoms = read(filename)
    positions = atoms.get_positions()
    new_pos = _crack_positions(positions, stretch, width, horizontal_shift, vertical_shift, direction)
    atoms.set_positions(new_pos)

    write(new_filename, atoms, format = format)
