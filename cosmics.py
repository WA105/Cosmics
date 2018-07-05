"""
Functions to create CR tables importing information from the CORSIKA database at /eos/experiment/wa105/offline/LArSoft/MC/CORSIKADB/
Return a TH2 of cosmic muons that can be used for the particle gun.
The output is saved on .rootfile whose name is passed as argument to the main function
"""

import sqlite3
import os, sys
import numpy as np
import ROOT

def cos2( x ):
    cos=np.cos(x)
    return cos*cos

def get_theta( dir, mag2 ):
    """
    direction cosine of an array along a direction.
    mag2 is the squared mag of the vector
    """

    theta = np.arccos(dir/np.sqrt(mag2))
    return theta

def get_phi( y, z ):
    """
    get the horizontal angle in a 3D sperical coordinates system.
    """

    if z != 0:
        if z > 0:
            phi=np.arctan(y/z)
        elif y/z < 0:
            phi= np.arctan(y/z) + np.pi
        else:
            phi= np.arctan(y/z) - np.pi
    elif y > 0:
        phi=np.pi/2
    else:
        phi=-np.pi/2

    return phi

def extract_values(row): #already done by fetchall (keep the function for future usese)
    """
    Parse the db database raw to an array
    """
    dummy_row = str(row).replace('(', '').replace(')', '')
    row_array = dummy_row.split(',')
    return map(float, row_array) #to parse string to float

def fill_hist1D(hist, x):
    for  i in range(0, len(x)):
        hist.Fill( x[i] )

    return


def fill_hist2D(hist, x, y):
    """
    Filling a TH2 from a numpy array
    """
    
    if len(x) != len(y):
        print "Error!! X and Y array must have the same size"

    for  i in range(0, len(x)):
        hist.Fill( x[i], y[i] )
        
    return

def readdb(directory, statement):
    
    """
    Execute the statement on the selected db.
    Return a numpy array with the query arguments
    """

    lst = []

    for dbname in os.listdir(directory):

        if not dbname.endswith(".db"):
            print "Skip file without *.db extention"
            continue

        print "Reading file: "+dbname

        db=sqlite3.connect(directory+'/'+dbname) #connecting to the database
        c = db.cursor() #made pointer to the database
        c.execute(statement) #exectute the statement on the connector

        for row in c.fetchall():

            dummy_row = ( row[0], row[1], get_theta(row[3], row[5]), get_phi(row[4], row[2]) ) #dummy_row(pdg,enegy,theta,phi)
            lst.append(dummy_row)

        db.close()

    return np.array(lst)
