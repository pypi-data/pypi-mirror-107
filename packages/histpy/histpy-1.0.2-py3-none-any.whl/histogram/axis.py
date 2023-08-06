import logging
logger = logging.getLogger(__name__)

import numpy as np
from numpy import log2

class Axis:
    """
    Bin edges. Optionally labeled

    Args:
        edges (array-like): Bin edges
        label (str): Label for axis. If edges is an Axis object, this will 
            override its label
        scale (str): Bin center mode e.g. `"linear"` or `"log"`. 
            See `scale()`. If edges is an Axis 
            object, this will override its mode

    Attributes:
        edges (array-like): Bin edges
        label (str): Label for axis
    """

    def __init__(self, edges, label = None, scale = None):

        if isinstance(edges, Axis):
            self.edges = edges.edges

            #Override
            if label is None:
                self.label = edges.label
            else:
                self.label = label

            if scale is None:
                self._scale = edges._scale
            else:
                self._scale = scale
                
        else:
            
            self.edges = np.array(edges)

            if len(self.edges) < 2:
                raise ValueError("All edges need at least two edges")
        
            if any(np.diff(self.edges) <= 0):
                raise ValueError("All bin edges must be strictly monotonically"
                                 " increasing")

            self.label = label

            if scale is None:
                self._scale = 'linear'
            else:
                self._scale = scale                

    def scale(self, mode = None):
        """
        Control what is considered the center of the bin. This affects
        `centers()` and interpolations.

        Args:
            mode (str or None):
                - linear (default): The center is the midpoint between the bin edges
                - symmetric: same as linear, except for the first center, which
                  will correspond to the lower edge. This is, for example, useful 
                  when the histogram is filled with the absolute value of a 
                  variable.
                - log: The center is the logarithmic (or geometrical) midpoint between
                  the bin edges.
        
        Return:
            str: The new mode (or current if mode is `None`).
        """
        
        if mode is not None:

            if mode not in ['linear', 'symmetric', 'log']:
                raise ValueError("Bin center mode '{}' not supported".format(mode))

            if mode == 'log' and self.min <= 0:
                raise ArithmeticError("Bin center mode 'log' can only be assigned "
                                      "to axes starting at a positive number")
            
            self._scale = mode
            
        return self._scale
            
    def __array__(self):
        return np.array(self.edges)

    def __len__(self):
        return len(self.edges)

    def __eq__(self, other):
        return (np.array_equal(self.edges, other.edges)
                and
                self.label == other.label)

    def __getitem__(self, key):
        return self.edges[key]

    def find_bin(self, value):
        """
        Return the bin `value` corresponds to. 

        Return:
            int: Bin number. -1 for underflow, `nbins` for overflow
        """

        return np.digitize(value, self.edges)-1
    
    def interp_weights(self, value):
        """
        Get the two closest bins to `value`, together with the weights to 
        linearly interpolate between them. The bin contents are assigned to 
        the center of the bin.

        Values in the edges beyond the center of the first/last bin will 
        result in no interpolation.

        Return:
            [int, int]: Bins
            [float, float]: Weights
        """

        bin0 = self.find_bin(value)
        
        if bin0 < 0 or bin0 == self.nbins:
            raise ValueError("Value {} out of bounds [{} - {})"
                             .format(value,
                                     self.min,
                                     self.max))
    
        # Linear interpolation with two closest bins
        center0 = self.centers[bin0]

        if value > center0:
            bin1 = bin0 + 1
        else:
            bin1 = bin0 - 1

        # Handle histogram edges, beyond center of first/last pixel
        bin1 = min(self.nbins-1, max(0, bin1))

        if bin0 == bin1:
            # No interpolation at the very edge
            return ([bin0,bin1],[1,0])
        
        # Sort
        if bin0 > bin1:
            bin0, bin1 = bin1, bin0
            
        # Weights
        center0 = self.centers[bin0]
        center1 = self.centers[bin1]

        if self._scale == 'log':
            center0 = log2(center0)
            center1 = log2(center1)
            value = log2(value)
            
        norm = center1 - center0
        w0 = (center1 - value) / norm
        w1 = (value - center0) / norm

        return ([bin0,bin1], [w0,w1])
    
    @property
    def lower_bounds(self):
        '''
        Lower bound of each bin
        '''

        return self.edges[:-1]

    @property
    def upper_bounds(self):
        '''
        Upper bound of each bin
        '''

        return self.edges[1:]

    @property
    def bounds(self):
        '''
        Start of [lower_bound, upper_bound] values for each bin.
        '''

        return np.transpose([self.lower_bounds, self.upper_bounds])

    @property
    def min(self):
        """
        Overall lower bound
        """

        return self.edges[0]

    @property
    def max(self):
        """
        Overall upper bound of histogram
        """

        return self.edges[-1]

    @property
    def centers(self):
        '''
        Center of each bin.
        '''

        if self._scale == 'linear':
            centers = (self.edges[1:] + self.edges[:-1])/2
        elif self._scale == 'symmetric':
            centers = (self.edges[1:] + self.edges[:-1])/2
            centers[0] = self.min
        elif self._scale == 'log':
            log2_edges = log2(self.edges)
            centers = 2**((log2_edges[1:] + log2_edges[:-1])/2)
        else:
            raise AssertionError("This shouldn't happen, "
                                 "tell maintainers to fix it")
        
        return centers
        
    @property
    def widths(self):
        '''
        Width each bin.
        '''

        return np.diff(self.edges)

    @property
    def nbins(self):
        """
        Number of elements along each axis. Either an int (1D histogram) or an 
        array
        """
        
        return len(self.edges)-1
    
