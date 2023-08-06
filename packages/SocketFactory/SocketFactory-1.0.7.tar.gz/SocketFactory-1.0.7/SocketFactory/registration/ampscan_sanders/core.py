# -*- coding: utf-8 -*-
"""
Package for defining the core AmpObject
Copyright: Joshua Steer 2020, Joshua.Steer@soton.ac.uk

"""

import numpy as np
import os
import struct

class AmpObject():
    r"""
    Base class for the ampscan project.
    Stores mesh data and extra information 
    Inherits methods via mixins
    Flexible class able to deal with surface data using 3 or 4 node faces and 
    visualise nodal data such as FEA outputs or shape deviations
    
    Parameters
    ----------
    data : str or dict
        Data input as either a string to import from an external file or a 
        dictionary to pull values directly
    stype : str, optional
        descriptor of the type of data the AmpObject is representing, e.g 
        'limb' or 'socket'. Default is 'limb'
    
    Returns
    -------
    AmpObject
        Initiation of the object
    
    Examples
    -------
    >>> amp = AmpObject(filename)

    """

    def __init__(self, data=None, stype='limb', unify=True, struc=True):
        self.stype = stype
        if isinstance(data, str):
            self.read_stl(data, unify, struc)
        elif isinstance(data, dict):
            for k, v in data.items():
                setattr(self, k, v)
            self.calcStruct()
        elif isinstance(data, bytes):
            self.read_bytes(data, unify, struc)

    def read_stl(self, filename, unify=True, struc=True):
        """
        Function to read .stl file from filename and import data into 
        the AmpObj 
        Parameters
        -----------
        filename: str 
            file path of the .stl file to read 
        unify: boolean, default True
            unify the coincident vertices of each face
        struc: boolean, default True
            Calculate the underlying structure of the mesh, such as edges

        """
        with open(filename, 'rb') as fh:
        # Defined no of bytes for header and no of faces
            HEADER_SIZE = 80
            COUNT_SIZE = 4
            # State the data type and length in bytes of the normals and vertices
            data_type = np.dtype([('normals', np.float32, (3, )),
                                  ('vertices', np.float32, (9, )),
                                  ('atttr', '<i2', (1, ))])
            # Read the header of the STL
            head = fh.read(HEADER_SIZE).lower()
            # Read the number of faces
            NFaces, = struct.unpack('@i', fh.read(COUNT_SIZE))
            # Read the remaining data and save as void, then close file
            data = np.fromfile(fh, data_type)
        # Test if the file is ascii
        if str(head[:5], 'utf-8') == 'solid':
            raise ValueError("ASCII files not supported")
        # Write the data to a numpy arrays in AmpObj
        tfcond = NFaces==data['vertices'].shape[0]			#assigns true or false to tfcond
        if not tfcond:							#if tfcond is false, raise error
            raise ValueError("File is corrupt")							#if true, move on
        vert = np.resize(np.array(data['vertices']), (NFaces*3, 3))
        norm = np.array(data['normals'])
        faces = np.reshape(range(NFaces*3), [NFaces,3])
        self.faces = faces
        self.vert = vert
        self.norm = norm
        
        # Call function to unify vertices of the array
        if unify is True:
            self.unifyVert()
        # Call function to calculate the edges array
#        self.fixNorm()
        if struc is True:
            self.calcStruct()
        self.values = np.zeros([len(self.vert)])

    def read_bytes(self, data, unify=True, struc=True):
        """
        Function to read .stl file from filename and import data into 
        the AmpObj 
        
        Parameters
        -----------
        filename: str 
            file path of the .stl file to read 
        unify: boolean, default True
            unify the coincident vertices of each face
        struc: boolean, default True
            Calculate the underlying structure of the mesh, such as edges

        """
        # Defined no of bytes for header and no of faces
        HEADER_SIZE = 80
        COUNT_SIZE = 4
        # State the data type and length in bytes of the normals and vertices
        data_type = np.dtype([('normals', np.float32, (3, )),
                                ('vertices', np.float32, (9, )),
                                ('atttr', '<i2', (1, ))])
        # Read the header of the STL
        head = data[:HEADER_SIZE].lower()
        # Read the number of faces
        NFaces, = struct.unpack('@i', data[HEADER_SIZE:HEADER_SIZE+COUNT_SIZE])
        # Read the remaining data and save as void, then close file
        data = np.frombuffer(data[COUNT_SIZE+HEADER_SIZE:], data_type)
        # Test if the file is ascii
        if str(head[:5], 'utf-8') == 'solid':
            raise ValueError("ASCII files not supported")
        # Write the data to a numpy arrays in AmpObj
        tfcond = NFaces==data['vertices'].shape[0]			#assigns true or false to tfcond
        if not tfcond:							#if tfcond is false, raise error
            raise ValueError("File is corrupt")							#if true, move on
        vert = np.resize(np.array(data['vertices']), (NFaces*3, 3))
        norm = np.array(data['normals'])
        faces = np.reshape(range(NFaces*3), [NFaces,3])
        self.faces = faces
        self.vert = vert
        self.norm = norm
        
        # Call function to unify vertices of the array
        if unify is True:
            self.unifyVert()
        # Call function to calculate the edges array
#        self.fixNorm()
        if struc is True:
            self.calcStruct()
        self.values = np.zeros([len(self.vert)])
        
    def calcStruct(self, norm=True, edges=True, 
                   edgeFaces=True, faceEdges=True, vNorm=False):
        r"""
        Top level function to calculate the underlying structure of the 
        AmpObject
        
        Parameters
        ----------
        norm: boolean, default True
            If true, the normals of each face in the mesh will be calculated
        edges: boolean, default True
            If true, the edges of the mesh will be calculated, the refers to
            the vertex index that make up any edge
        edgeFaces: boolean, default True
            If true, the edgeFaces array of the mesh will be calculated, this 
            refers to the index of the three edges that make up each face
        faceEdges: boolean, default True
            If true, the faceEdges array will be calculated, this refers to 
            index of the faces that are coincident to each edge. Normally, 
            there are two faces per edge, if there is only one, then -99999 
            will be used to indicate this 
        vNorm: boolean, default False
            If true, the normals of each vertex in the mesh will be calculated

        """
        if norm is True:
            self.calcNorm()
        if edges is True:
            self.calcEdges()
        if edgeFaces is True:
            self.calcEdgeFaces()
        if faceEdges is True:
            self.calcFaceEdges()
        if vNorm is True:
            self.calcVNorm()

    def unifyVert(self):
        r"""
        Function to unify coincident vertices of the mesh to reduce
        size of the vertices array enabling speed increases when performing
        calculations using the vertex array
        
        Examples
        --------
        >>> amp = AmpObject(filename, unify=False)
        >>> amp.vert.shape
        (44832, 3)
        >>> amp.unifyVert()
        >>> amp.vert.shape
        (7530, 3)

        """
        # Requires numpy 1.13
        self.vert, indC = np.unique(self.vert, return_inverse=True, axis=0)
        # Maps the new vertices index to the face array
        self.faces = np.resize(indC[self.faces], 
                               (len(self.norm), 3)).astype(np.int32)

    def calcEdges(self):
        """
        Function to compute the edges array ie the index of the two vertices
        that make up each edge
        
        Returns
        -------
        edges: ndarray
            Denoting the indicies of two vertices on each edge

        """
        # Get edges array
        self.edges = np.reshape(self.faces[:, [0, 1, 0, 2, 1, 2]], [-1, 2])
        self.edges = np.sort(self.edges, 1)
        # Unify the edges
        self.edges, indC = np.unique(self.edges, return_inverse=True, axis=0)

    def calcEdgeFaces(self):
        r"""
        Function that calculates the indicies of the three edges that make up
        each face 
        
        Returns
        -------
        edgesFace: ndarray
            Denoting the indicies of the three edges on each face
        
        """
        edges = np.reshape(self.faces[:, [0, 1, 0, 2, 1, 2]], [-1, 2])
        edges = np.sort(edges, 1)
        # Unify the edges
        edges, indC = np.unique(edges, return_inverse=True, axis=0)
        # Get edges on each face 
        self.edgesFace = np.reshape(range(len(self.faces)*3), [-1,3])
        #Remap the edgesFace array 
        self.edgesFace = indC[self.edgesFace].astype(np.int32)

    def calcFaceEdges(self):
        r"""
        Function that calculates the indicies of the faces on each edge
        
        Returns
        -------
        faceEdges: ndarray
            The indicies of the faces in each edge, edges may have either 
            1 or 2 faces, if 1 then the second index will be NaN

        """
        #Initiate the faceEdges array
        self.faceEdges = np.empty([len(self.edges), 2], dtype=np.int32)
        self.faceEdges.fill(-99999)
        # Denote the face index for flattened edge array
        fInd = np.repeat(np.array(range(len(self.faces))), 3)
        # Flatten edge array
        eF = np.reshape(self.edgesFace, [-1])
        eFInd = np.unique(eF, return_index=True)[1]
        logic = np.zeros([len(eF)], dtype=bool)
        logic[eFInd] = True
        self.faceEdges[eF[logic], 0] = fInd[logic]
        self.faceEdges[eF[~logic], 1] = fInd[~logic]        
        

    def calcNorm(self):
        r"""
        Calculate the normal of each face of the AmpObj
        
        Returns
        -------
        
        norm: ndarray
            normal of each face

        """
        norms = np.cross(self.vert[self.faces[:,1]] -
                         self.vert[self.faces[:,0]],
                         self.vert[self.faces[:,2]] -
                         self.vert[self.faces[:,0]])
        mag = np.linalg.norm(norms, axis=1)
        self.norm = np.divide(norms, mag[:,None])
    
    def fixNorm(self):
        r"""
        Fix normals of faces so they all face outwards 
        """
        fC = self.vert[self.faces].mean(axis=1)
        cent = self.vert.mean(axis=0)
        # polarity = np.sum(self.norm * (fC-cent), axis=1) < 0
        # if polarity.mean() > 0.5:
        #     self.faces[:, [1,2]] = self.faces[:, [2,1]]
        #     self.calcNorm()
        #     if hasattr(self, 'vNorm'): self.calcVNorm()
        polarity  = np.einsum('ij, ij->i', fC - cent, self.norm) < 0
        # self.faces[polarity, [1,2]] = self.faces[polarity, [2,1]]
        for i, f in enumerate(self.faces):
            if polarity[i] == True:
                self.faces[i, :] = [f[0], f[2], f[1]]

        self.calcNorm()
        if hasattr(self, 'vNorm'): self.calcVNorm()
        
    def calcVNorm(self):
        """
        Function to compute the vertex normals based upon the mean of the
        connected face normals 
        
        Returns
        -------
        vNorm: ndarray
            normal of each vertex

        """
        f = self.faces.flatten()
        o_idx = f.argsort()
        row, col = np.unravel_index(o_idx, self.faces.shape)
        ndx = np.searchsorted(f[o_idx], range(self.vert.shape[0]), side='right')
        ndx = np.r_[0, ndx]
        norms = self.norm[row, :]
        self.vNorm = np.zeros(self.vert.shape)
        for i in range(self.vert.shape[0]):
            self.vNorm[i, :] = np.nanmean(norms[ndx[i]:ndx[i+1], :], axis=0)
            
    def save(self, filename):
        r"""
        Function to save the AmpObj as a binary .stl file 
        
        Parameters
        -----------
        filename: str
            file path of the .stl file to save to

        """
        self.calcNorm()
        fv = self.vert[np.reshape(self.faces, len(self.faces)*3)]
        with open(filename, 'wb') as fh:
            header = '%s' % (filename)
            header = header.split('/')[-1].encode('utf-8')
            header = header[:80].ljust(80, b' ')
            packed = struct.pack('@i', len(self.faces))
            fh.write(header)
            fh.write(packed)
            data_type = np.dtype([('normals', np.float32, (3, )),
                                  ('vertices', np.float32, (9, )),
                                  ('atttr', '<i2', (1, ))])
            data_write = np.zeros(len(self.faces), dtype=data_type)
            data_write['normals'] = self.norm
            data_write['vertices'] = np.reshape(fv, (len(self.faces), 9))
            data_write.tofile(fh)

    def translate(self, trans):
        r"""
        Translate the AmpObj in 3D space

        Parameters
        -----------
        trans: array_like
            Translation in [x, y, z]

        """

        # Check that trans is array like
        if isinstance(trans, (list, np.ndarray, tuple)):
            # Check that trans has exactly 3 dimensions
            if len(trans) == 3:
                self.vert[:] += trans
            else:
                raise ValueError("Translation has incorrect dimensions. Expected 3 but found: " + str(len(trans)))
        else:
            raise TypeError("Translation is not array_like: " + trans)


    def rotateAng(self, rot, ang='rad', norms=True):
        r"""
        Rotate the AmpObj in 3D space according to three angles

        Parameters
        -----------
        rot: array_like
            Rotation around [x, y, z]
        ang: str, default 'rad'
            Specify if the euler angles are in degrees or radians. 
            Default is radians
        
        Examples
        --------
        >>> amp = AmpObject(filename)
        >>> ang = [np.pi/2, -np.pi/4, np.pi/3]
        >>> amp.rotateAng(ang, ang='rad')
        """

        # Check that ang is valid
        if ang not in ('rad', 'deg'):
            raise ValueError("Ang expected 'rad' or 'deg' but {} was found".format(ang))

        if isinstance(rot, (tuple, list, np.ndarray)):
            R = self.rotMatrix(rot, ang)
            self.rotate(R, norms)
        else:
            raise TypeError("rotateAng requires a list")

            
    def rotate(self, R, norms=True):
        r"""
        Rotate the AmpObject using a rotation matrix 
        
        Parameters
        ----------
        R: array_like
            A 3x3 array specifying the rotation matrix
        norms: boolean, default True
            
        """
        if isinstance(R, (list, tuple)):
            # Make R a np array if its a list or tuple
            R = np.array(R, np.float)
        elif not isinstance(R, np.ndarray):
            # If
            raise TypeError("Expected R to be array-like but found: " + str(type(R)))
        if len(R) != 3 or len(R[0]) != 3:
            # Incorrect dimensions
            if isinstance(R, np.ndarray):
                raise ValueError("Expected 3x3 array, but found: {}".format(R.shape))
            else:
                raise ValueError("Expected 3x3 array, but found: 3x"+str(len(R)))
        self.vert[:, :] = np.dot(self.vert, R.T)
        if norms is True:
            self.norm[:, :] = np.dot(self.norm, R.T)
            if hasattr(self, 'vNorm'):
                self.vNorm[:, :] = np.dot(self.vNorm, R.T)
            
            
    def rigidTransform(self, R=None, T=None):
        r"""
        Perform a rigid transformation on the AmpObject, first the rotation, 
        then the translation 
        
        Parameters
        ----------
        R: array_like, default None
            A 3x3 array specifying the rotation matrix
        T: array_like, defauly None
            An array of the form [x, y, z] which specifies the translation
            
        """
        if R is not None:
            if isinstance(R, (tuple, list, np.ndarray)):
                self.rotate(R, True)
            else:
                raise TypeError("Expecting array-like rotation, but found: "+type(R))
        if T is not None:
            if isinstance(T, (tuple, list, np.ndarray)):
                self.translate(T)
            else:
                raise TypeError("Expecting array-like translation, but found: "+type(T))
        

    @staticmethod
    def rotMatrix(rot, ang='rad'):
        r"""
        Calculate the rotation matrix from three angles, the order is assumed 
        as around the x, then y, then z axis
        
        Parameters
        ----------
        rot: array_like
            Rotation around [x, y, z]
        ang: str, default 'rad'
            Specify if the Euler angles are in degrees or radians
        
        Returns
        -------
        R: array_like
            The calculated 3x3 rotation matrix 
    
        """

        # Check that rot is valid
        if not isinstance(rot, (tuple, list, np.ndarray)):
            raise TypeError("Expecting array-like rotation, but found: "+type(rot))
        elif len(rot) != 3:
            raise ValueError("Expecting 3 arguments but found: {}".format(len(rot)))

        # Check that ang is valid
        if ang not in ('rad', 'deg'):
            raise ValueError("Ang expected 'rad' or 'deg' but {} was found".format(ang))

        if ang == 'deg':
            rot = np.deg2rad(rot)

        [angx, angy, angz] = rot
        Rx = np.array([[1, 0, 0],
                       [0, np.cos(angx), -np.sin(angx)],
                       [0, np.sin(angx), np.cos(angx)]])
        Ry = np.array([[np.cos(angy), 0, np.sin(angy)],
                       [0, 1, 0],
                       [-np.sin(angy), 0, np.cos(angy)]])
        Rz = np.array([[np.cos(angz), -np.sin(angz), 0],
                       [np.sin(angz), np.cos(angz), 0],
                       [0, 0, 1]])
        R = np.dot(np.dot(Rz, Ry), Rx)
        return R
   