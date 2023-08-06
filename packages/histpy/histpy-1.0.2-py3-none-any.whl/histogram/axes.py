import logging
logger = logging.getLogger(__name__)

import numpy as np

from copy import copy,deepcopy

from .axis import Axis

class Axes:
    """
    Holds a list of axes. 

    The operator Axes[key] return a subset of these. Key can be either the
    index or the label. If the key is a single index, a single Axis object
    will be returned

    Args:
        edges (array or list of arrays or Axis): Definition of bin edges.
        labels (array of str): Optionally label the axes for easier indexing.
            Will override the labels of edges, if they are Axis objects
        scale (str or array): Bin center mode e.g. `"linear"` or `"log"`. 
            See Axis.scale. If not an array, all axes will have this mode.

    """

    def __init__(self, edges, labels=None, scale = None):

        # Standarize axes as list of Axis
        if isinstance(edges, Axes):
            # From another Axes object
            
            self._axes = copy(edges._axes)
            
        elif np.ndim(edges) == 0:

            if np.isscalar(edges):
                raise TypeError("'edges' can't be a scalar")

        elif np.ndim(edges) == 1:

            if len(edges) == 0:
                raise ValueError("'edges' can't be an empty array")

            if all(np.ndim(a) == 0 for a in edges):
                #1D histogram
                self._axes = [Axis(edges)]
            else:
                #Multi-dimensional histogram.
                self._axes = [Axis(axis) for axis in edges]

        elif np.ndim(edges) == 2:

            #Multi-dimensional histogram
            self._axes = [Axis(axis) for axis in edges]

        else:
            raise ValueError("'edges' can have at most two dimensions")
            

        #Override labels if nedeed
        if labels is not None:
            
            if np.isscalar(labels):
                labels = [labels]

            if len(labels) != self.ndim:
                raise ValueError("Edges - labels size mismatch")

            for n,label in enumerate(labels):
                self._axes[n] = Axis(self._axes[n], label)

        #Maps labels to axes indices. Only keep non-None
        labels = np.array([a.label for a in self._axes])

        non_none_labels = labels[labels != None]
        if len(np.unique(non_none_labels)) != len(non_none_labels):
                    raise ValueError("Labels can't repeat")

        self._labels = {}
        
        for n,label in enumerate(labels):
            if label is not None:
                self._labels[label] = n

        #Override scale if nedeed
        if scale is not None:
            
            if np.isscalar(scale):
                scale = self.ndim*[scale]

            if len(scale) != self.ndim:
                raise ValueError("Edges - scale size mismatch")

            for mode,ax in zip(scale, self._axes):
                ax.scale(mode)

                
    def __len__(self):
        return self.ndim

    def __iter__(self):
        return iter(self._axes)
    
    @property
    def labels(self):
        """
        Label of axes. 

        Return:
            Either a string or a tuple of string. None if
            they are not defined
        """
        return [a.label for a in self._axes]
        
    @property
    def ndim(self):
        """
        Number of axes
        """
        return len(self._axes)

    def key_to_index(self, key):
        """
        Turn a key or list of keys, either indices or labels, into indices

        Args:
            key (int or str): Index or label
        
        Return:
            int: Index
        """
        
        if isinstance(key, int):
            return key
        if (isinstance(key, (np.ndarray, list, tuple, range))
            and
            not isinstance(key, str)):
            return tuple(self.key_to_index(k) for k in key)
        else:
            #Label
            try:
                return self._labels[key]
            except KeyError:
                logger.error("Axis with label {} not found".format(key))
                raise

    def __getitem__(self, key):

        indices = self.key_to_index(key)

        if np.isscalar(indices):
            return self._axes[indices]
        else:
            return Axes([self._axes[i] for i in indices])

    def __eq__(self, other):
        return all([a1 == a2 for a1,a2 in zip(self._axes,other._axes)])

    def __array__(self):
        return np.array(self._axes)

    def interp_weights(self, *values):
        """
        Get the bins and weights to linearly interpolate between bins.
        The bin contents are assigned to the center of the bin.

        Args:
            values (float or array): Coordinates within the axes to interpolate.
                Must have the same size as `ndims`. Input values as
                ``(1,2,3)`` or ``([1,2,3])``.
        
        Returns:
            array of tuples of int, array of floats: Bins  and weights to use. Size=2^ndim. Each bin is specified by a tuple containing `ndim` integers

        """
        
        #Standarize
        if (len(values) == 1 and
            isinstance(values[0], (list, np.ndarray, range, tuple))):
               # Got a sequence
               values = values[0]

        if len(values) != self.ndim:
            raise ValueError("Number of values different than number of dimensions")
           
        # Get the bin/weights for each individual axis
        dim_bins = []
        dim_weights = []
        
        for dim,value in enumerate(values):

            bins,weights = self._axes[dim].interp_weights(value)

            dim_bins += [bins]
            dim_weights += [weights]

        bins = []
        weights = []

        # Combine them. e.g. for 2D this results in
        # weights = [dim_weights[0][0]*dim_weights[1][0],
        #            dim_weights[0][1]*dim_weights[1][0],
        #            dim_weights[0][0]*dim_weights[1][1],
        #            dim_weights[0][1]*dim_weights[1][1]]
        # bins = [(dim_bins[0][0], dim_bins[1][0]),
        #         (dim_bins[0][1], dim_bins[1][0]),
        #         (dim_bins[0][0], dim_bins[1][1]),
        #         (dim_bins[0][1], dim_bins[1][1])]
        # bit_masks = [0b001, 0b010, 0b100, ...]
        bit_masks = 2**np.array(range(self.ndim))
        for n in range(2**self.ndim):

            weight = 1
            bin_list = [] 

            # Since there are two weights per axis, we use bit
            # masking to loop between them instead of recursion
            for dim,bit_mask in enumerate(bit_masks):

                index = int(bool(n & bit_mask)) # Either 0 or 1

                weight *= dim_weights[dim][index]
                bin_list += [dim_bins[dim][index]]
                
            bins += [tuple(bin_list)]
            weights += [weight]
            
        return bins,weights
            
    def _get_axis_property(f):
        """
        Decorator to retrieve a property for an axis based on an index. 
        This allows to specify the axis or axes as (x), (x,y), ([x,y])
        or even (x,[z,[x,y]]).
        
        The methods need to be reclared as:
        @_get_axis_property
        def property_name(self, axis):
            return self[axis]

        This decorator will automatically get the corresponding property based
        on the name of the methods
        """
        def wrapper(self, *axis):
            
            if len(axis) == 0:
                #Default to first axis, useful for 1D histograms
                return wrapper(self, 0)
            elif len(axis) == 1:
                if np.isscalar(axis[0]):
                    #Standard way, single axis. Do other types recursively
                    return getattr(f(self, axis[0]), f.__name__)
                else:
                    return [wrapper(self, a) for a in axis[0]]    
            else:
                return [wrapper(self, a) for a in axis]
                
        return wrapper

    @_get_axis_property
    def edges(self, axis):
        """
        Edges for a given axis

        Args:
            axis (int, str or list): Axis or axes indices or labels

        Return:
            array or list of arrays
        """

        return self[axis]

    @_get_axis_property
    def lower_bounds(self, axis=0):
        '''
        Lower bound of each bin

        Args:
            axis (int, str or list): Axis or axes indices or labels

        Return:
            array or list of arrays
        '''

        return self[axis]

    @_get_axis_property
    def upper_bounds(self, axis=0):
        '''
        Upper bound of each bin

        Args:
            axis (int, str or list): Axis or axes indices or labels

        Return:
            array or list of arrays
        '''

        return self[axis]

    @_get_axis_property
    def bounds(self, axis=0):
        '''
        Start of [lower_bound, upper_bound] values for each bin.

        Args:
            axis (int, str or list): Axis or axes indices or labels

        Return:
            array or list of arrays
        '''

        return self[axis]

    @_get_axis_property
    def min(self, axis=0):
        """
        Overall lower bound

        Args:
            axis (int, str or list): Axis or axes indices or labels

        Return:
            float or array
        """

        return self[axis]

    @_get_axis_property
    def max(self, axis=0):
        """
        Overall upper bound of histogram

        Args:
            axis (int, str or list): Axis or axes indices or labels

        Return:
            float or array
        """

        return self[axis]

    @_get_axis_property
    def centers(self, axis=0):
        '''
        Center of each bin.

        Args:
            axis (int, str or list): Axis or axes indices or labels

        Return:
            array or list of arrays
        '''

        return self[axis]

    @_get_axis_property
    def widths(self, axis=0):
        '''
        Width each bin.

        Args:
            axis (int, str or list): Axis or axes indices or labels

        Return:
            array or list of arrays
        '''

        return self[axis]

    @_get_axis_property
    def nbins(self, axis=0):
        """
        Number of elements along each axis. Either an int (1D histogram) or an 
        array

        Args:
            axis (int, str or list): Axis or axes indices or labels

        Return:
            float or array
        """

        return self[axis]
    
