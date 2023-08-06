import logging
logger = logging.getLogger(__name__)

import numpy as np

import operator

from copy import copy,deepcopy

import matplotlib.pyplot as plt

from scipy.optimize import curve_fit

from .axes import Axes

class Histogram(object):
    """
    This is a wrapper of a numpy array with axes and a fill method.
    
    Like an array, the histogram can have an arbitrary number of dimensions.

    Standard numpy array indexing is supported to get the contents 
    --i.e. :code:`h[:]`, :code:`h[4]`, :code:`h[[1,3,4]]`, :code:`h[:,5:50:2]]`,
    etc.--. However, the meaning of the :code:`-1` index is different. Instead of 
    counting from the end, :code:`-1` corresponds to the underflow bin. Similarly,
    an index equal to the number of bins corresponds to the overflow bin. 

    You can however give relative position with respect to :code:`h.NBINS` 
    --e.g. :code:`h[0:h.NBINS]` result in all regular bins, :code:`h[-1:h.NBINS+1]` 
    includes also the underflow/overflow bins and :code:`h[h.NBINS]` gives you the 
    contents of the overflow bin. 
    
    You can also use an Ellipsis object (...) at the end to specify that the
    contents from the rest of the dimension are to have the under and overflow
    bins included. e.g. for a 3D histogram :code:`h[1,-1:h.NBINS+1,-1:h.NBINS+1]
    = h[1,...]`. h[:] returns all contents without under/overflow bins and
    h[...] returns everything, including those special bins.

    Additionally, you can specify with a dictionary the indices for specific 
    axes, with all the rest being the default. e.g. 
    :code:`h[:,:,1:,:,6] <==> h[{2:slice(1,None), 4:6}]`. If you also use the
    axes id if you labeled them, e.g. :code:`h[{'x':slice(0,h.NBINS+1)}]`

    If :code:`sumw2` is not :code:`None`, then the histogram will keep track of 
    the sum of the weights squared --i.e. you better use this if you are using 
    weighted data and are concern about error bars--. You can access these with
    `h.sumw2[item]`, where `item` is interpreted the same was a in `h[item]`.
    `h.bin_error[item]` return the `sqrt(sumw2)` (or `sqrt(contents)` is `sumw2
    was not specified`).

    You can use the :code:`*=` operator to weight by a number or an array of 
    weights with the shape of :code:`h.nbins+2` (to include under/overflow bins).

    The operators :code:`+`, :code:`-`, :code:`+=` and :code:`-=` are available.
    Both operands need to be histograms. An exception will be raised if the axes
    are not the same. Note that :code:`h += h0` is more efficient than 
    :code:`h = h + h0` since latter involves the instantiation of a new histogram.

    Args:
        edges (Axes or array): Definition of bin edges, Anything that can
            be processes by Axes. Lower edge value is included in the bin, 
            upper edge value is excluded.
        contents (array): Initialization of histogram contents. Might or might
            not include under/overflow bins. Initialize to 0 by default.
        sumw2 (None, bool or array): If True, it will keep track of the sum of
            the weights squared. You can also initialize them with an array
        labels (array of str): Optionally label the axes for easier indexing
        scale (str or array): Bin center mode e.g. `"linear"` or `"log"`. 
            See ``Axis.scale()``. Not to be confused with the 
            ``Histogram`'s `method ``scale()``, which `scales` the bin contents, 
            rather than defining what the scale mode of an axis is.

    """
            
    def __init__(self, edges, contents = None, sumw2 = None,
                 labels=None, scale = None):

        self._axes = Axes(edges, labels=labels, scale = scale)
        self._nbins = np.array([a.nbins for a in self._axes])

        # Standarize contents (with under/overflow) or initialize them to zero.
        if contents is not None:
            if np.array_equal(self._nbins+2, np.shape(contents)):
                # Includes under and overflow
                self._contents = np.array(contents) 
            elif np.array_equal(self._nbins, np.shape(contents)):
                # Missing under and overflow, but right shape.
                # Adding empty under/overflow bins
                self._contents = np.pad(contents, 1)
            else:
                raise ValueError("Edges-contents size mismatch")
        else:
            self._contents = np.zeros([n+2 for n in self._nbins])

        #Check if we'll keep track of the sum of the weights 
        if sumw2 is None or sumw2 is False:
            self._sumw2 = None
        elif sumw2 is True:
            self._sumw2 = Histogram(self._axes)
        elif isinstance(sumw2, Histogram):
            if self.axes != sumw2.axes:
                raise ValueError("Is sumw2 is a Histogram is needs to have "
                                 "consistent axes")

            self._sumw2 = sumw2
        
        else:
            self._sumw2 = Histogram(self._axes, sumw2)

        # Special access methods
        self.sumw2 = self._get_sumw2(self)
        self.bin_error = self._get_bin_error(self)
            
    @classmethod
    def concatenate(cls, edges, histograms, label = None):
        """
        Generate a Histogram from a list os histograms. The axes of all input
        histograms must be equal, and the new histogram will have one more
        dimension than the input. The new axis has index 0.

        Args:
            edges (Axes or array): Definition of bin edges of the new dimension
            histograms (list of Histogram): List of histogram to fill contents. 
                Might or might not include under/overflow bins.
            labels (str): Label the new dimension

        Return:
            Histogram
        """

        # Check new axis matches number of histograms,
        # with or without under/overflow
        new_axis = Axis(edges, label = label)

        if len(histograms) == new_axis.nbins:
            underflow_bin_shift = 1
        elif len(histograms) == new_axis.nbins + 2:
            underflow_bin_shift = 0
        else:
            raise ValueError("Mismatch between number of bins and "
                             "number of histograms")

        # Create new axes and new contents
        old_axes = histograms[0].axes

        new_axes = Axes([new_axis] + [ax for ax in old_axes])
        
        contents = np.zeros([ax.nbins+2 for ax in new_axes])

        sumw2 = np.zeros([ax.nbins+2 for ax in new_axes])

        for bin,hist in enumerate(histograms):

            if hist.axes != old_axes:
                raise ValueError("The axes of all input histogram must equal")
            
            bin += underflow_bin_shift # Account for under/overflow bins

            contents[bin] = hist[...]

            if sumw2 is not None:
                if hist._sumw2 is not None:
                    sumw2[bin] = hist.sumw2[...]
                else:
                    logger.warning("Not all input histogram have sum of weights "
                                   "squared. sumw2 will be dropped")
                    sumw2 = None
            
        return Histogram(new_axes, contents, sumw2)
            
    @property
    def ndim(self):
        return self._axes.ndim
            
    def clear(self):
        """
        Set all counts to 0
        """

        self._contents[:] = 0

        if self._sumw2 is not None:
            self._sumw2.clear()
                    
    def __eq__(self, other):
        # Histogram is completely defined by axes and contents
        return (self._axes == other._axes
                and
                np.array_equal(self._contents, other._contents)
                and
                self._sumw2 == other._sumw2)
            
    class _NBINS():        
        '''
        Convenience class that will expand to the number of bins of a 
        given dimension. 

        The trick is to overload the -/+ operators such than 
        h.NBINS +/- offset (h being an instance of Histogram and NBINS an 
        static instance of Histogram._NBINS) returns an instance of _NBINS 
        itself, which stores the offset. The [] operator can then detect that
        the input is an instance of _NBINS and convert it into an integer with
        respect to the size of the appropiate axis.
        '''
        
        def __init__(self, offset = 0):
            self.offset = offset
    
        def __add__(self, offset):
            return self.__class__(offset)
    
        def __sub__(self, offset):
            return self + (-offset)
        
    NBINS = _NBINS()

    def _prepare_indices(self, indices):
        '''
        Prepare indices for it use in __getitem__ and __setitem__ 
        --i.e. [] overloading --
        
        See class help.
        '''
        
        def _prepare_index(index, dim):
            '''
            Modify index for a single axis to account for under/overflow, 
            as well as to catch instances of _NBINS (see description above)
            This depend on the number of bins in the axis of a given 
            dimension (dim)
            '''

            if isinstance(index,slice):

                # Both start and stop can be either None, an instance of
                # _NBINS or an integer
                index = slice(1
                              if index.start is None
                              else
                              self._nbins[dim] + index.start.offset + 1
                              if isinstance(index.start, self._NBINS)
                              else
                              index.start+1,
                              
                              self._nbins[dim]+1
                              if index.stop is None
                              else
                              self._nbins[dim] + index.stop.offset + 1
                              if isinstance(index.stop, self._NBINS)
                              else
                              index.stop+1,
                              
                              index.step)
                
                # Check bounds. Note index is the _contents index at this point
                if index.start < 0 or index.stop > self._nbins[dim] + 2:
                    raise IndexError("Bin index out of bounds")
                
                return index
            
            elif isinstance(index, (np.integer, int)):
                if index < -1 or index > self._nbins[dim]:
                    raise IndexError("Bin index out of bounds")

                return index+1

            elif isinstance(index, self._NBINS):

                # Referece with respect to nbins
                return _prepare_index(self._nbins[dim] + index.offset, dim)
            
            elif isinstance(index, (np.ndarray, list, tuple, range)):

                # Note: this will return a copy, not a view

                # Handle references with respecto to nbins
                index =  [self._nbins[dim] + i.offset + 1
                          if isinstance(i,self._NBINS) else
                          i + 1
                          for i in index]

                # Check bounds. Note index is the _contents index at this point/
                for ind in index:
                    if ind < 0 or ind > self._nbins[dim] + 1:
                        raise IndexError("Bin index out of bounds")

                return index
                    
            else:
                raise TypeError("Index can only be an int, slice, list or array")
        
        if isinstance(indices, tuple):

            # Get the rest of the dimensions with under/overflow user used ...
            if indices[-1] is Ellipsis:
                extra_indices = tuple(slice(-1, self._nbins[dim]+1)
                                      for dim in range(len(indices)-1, self.ndim))

                indices = self._prepare_indices(indices[:-1] + extra_indices)

                return indices
            
            # Standard way. All other ways end up here after recursion
            indices = tuple(_prepare_index(index, dim)
                            for dim,index in enumerate(indices))

            # Remove under/overflow of the rest of the dimensions
            indices += tuple(_prepare_index(slice(None), dim) for dim in
                             range(len(indices), self.ndim))
                        
            return indices

        if isinstance(indices, dict):

            # Indices for specified axes. Default to all other axes
            new_indices = [slice(None)] * self.ndim

            for axis,index in indices.items():

                axis = self.axes.key_to_index(axis)
                
                new_indices[axis] = index

            return self._prepare_indices(tuple(new_indices))
                
        else:
            # Single axis
            return self._prepare_indices(tuple([indices]))

    def __getitem__(self, indices):

        return self._contents[self._prepare_indices(indices)]

    def __setitem__(self, indices, new_contents):

        self._contents[self._prepare_indices(indices)] = new_contents
    
    class _special_getitem:
        """
        This allows to use regular indexing for special access methods. 
        e.g. h.sumw2[] and h.bin_error[]
        """
        
        def __init__(self, hist):
            self._hist = hist

        def __getitem__(self, item):
            raise NotImplmentedError

        def __array__(self):
            return self[...]

        @property
        def contents(self):
            return self[:]
    
    class _get_sumw2(_special_getitem):
        """
        Return the sum fo the weights squares. If sumw2 is not stored, then
        it assumed all the weights of all entries equal 1.
        """
        
        def __getitem__(self, item):

            if self._hist._sumw2 is not None:
                return self._hist._sumw2[item]
            else:
                return np.abs(self._hist[item])

        def __setitem__(self, indices, new_sumw2):

            if self._sumw2 is None:
                raise ValueError("Histogram does not have sumw2")

            self._hist._contents[self._prepare_indices(indices)] = new_sumw2
            
    class _get_bin_error(_special_getitem):
        """
        Return the sqrt of sumw2
        """
        
        def __getitem__(self, item):
            return np.sqrt(self._hist.sumw2[item])
                        
        def __setitem__(self, indices, new_bin_error):

            if self._sumw2 is None:
                raise ValueError("Histogram does not have sumw2")

            self._hist._contents[self._prepare_indices(indices)] = \
                                                     np.pow(new_bin_error, 2)

        def __array__(self):

            return self._contents

    @property
    def contents(self):
        """
        Equivalent to `h[:]`. Use `h[...]` or `np.array(h)`
        to get under/overflow bins.
        """
        return self[:]
        
    @property
    def axes(self):
        """
        Underlaying axes object
        """
        return self._axes

    @property
    def axis(self):
        """
        Equivalent to `self.axes[0]`, but fails if `ndim > 1`
        """

        if self.ndim > 1:
            raise ValueError("Property 'axis' can only be used with 1D "
                            "histograms. Use `axes` for multidimensional "
                            "histograms")

        return self.axes[0]

    @property
    def nbins(self):

        if self.ndim == 1:
            return self._nbins[0]
        else:
            return self._nbins
    
    @property
    def shape(self):
        '''
        Tuple with number of bins along each dimensions
        '''

        return tuple(self._nbins)
        
    def find_bin(self, *values, axis = None):
        """
        Return one or more indices corresponding to the bin this value or 
        set of values correspond to.

        You can pass either an array, or specified the values as different 
        arguments. i.e. :code:`h.find_bin(x,y,z)` = :code:`h.find_bin([x,y,z])`

        Args:
            values (float or array): Vaule or list of values. Either shape N or
               ndim x N, where N is the number of entries.
            axis (int or str or list): If set, values correspond to the\
                subset of axes listed here

        Return:
            int or tuple: Bin index
        """

        
        # Get axes
        if axis is None:
            axes = self._axes
        else:
            axes = Axes(self._axes[axis])

        # Handle 1D vs N-D case
        if axes.ndim == 1:

            # 1D hist, any shape of values works. The output has the same shape
            
            if len(values) != 1:
                raise ValueError("Mismatch between values shape and number of axes")

            return axes[0].find_bin(values[0])

        else:

            # >=2D case
            
            if len(values) == 1:
                # e.g. ([x,y]) or ([[x0,x1], [y0,y1]]), NOT (x,y,z), [[x0,x1], [y0,y1]]
                values = values[0]
              
            elif len(values) != axes.ndim:
                raise ValueError("Mismatch between values shape and number of axes")
                
            values = np.array(values)

            if values.shape[0] != axes.ndim:
                # NOTE: Not redundant
                raise ValueError("Mismatch between values shape and number of axes")

            return tuple(axis.find_bin(val)
                         for val,axis in zip(values, axes))

    def interp(self, *values):
        """
        Get a linearly interpolated content for a given set of values
        along each axes. The bin contents are assigned to the center of the bin.
        
        Args:
            values (float or array): Coordinates within the axes to interpolate.
                 Must have the same size as `ndims`. Input values as
                 `(1,2,3)` or `([1,2,3])`

        Return:
            float
        """

        content = 0

        bins,weights = self._axes.interp_weights(*values)
        
        for bin,weight in zip(bins, weights):

            content += weight*self[bin]

        return content
        
    def fill(self, *values, weight=1):
        '''
        And an entry to the histogram. Can be weighted.

        Follow same convention as find_bin()

        Args:
            values (float or array): Value of entry
            weight (float): Value weight in histogram. 
        
        Note:
            Note that weight needs to be specified explicitely by key, otherwise
            it will be considered a value an a IndexError will be thrown.
        '''

        indices = self._prepare_indices(self.find_bin(*values))

        for i,w in np.broadcast(indices, weight):
            self._contents[i] += w

        if self._sumw2 is not None:
            for i,w in np.broadcast(indices, weight):
                self._sumw2._contents[i] += w*w

    def project(self, *axis):
        """
        Return a histogram consisting on a projection of the current one

        Args:
            axis (int or str or list): axis or axes onto which the
                histogram will be projected --i.e. will sum up over the
                other dimensiones--. The axes of the new histogram will
                have the same order --i.e. you can transpose axes--

        Return:
            Histogram: Projected histogram
        """
        if self.ndim == 1:
            raise ValueError("Can't project a 1D histogram. "
                             "Consider using np.sum(h[...])")

        #Standarize
        if len(axis) == 1 and \
           isinstance(axis[0], (list, np.ndarray, range, tuple)):
            # Got a sequence
            axis = axis[0]
        
        axis = self._axes.key_to_index(axis)
        
        if len(np.unique(axis)) != len(axis):
            raise ValueError("An axis can't repeat")

        sum_axes = tuple(dim for dim in range(0, self.ndim) if dim not in axis)
        new_contents = self._contents.sum(axis = sum_axes)

        # Transpose the contents to match the order of the axis provided by the
        # the user, which are currently sorted
        new_contents = np.transpose(new_contents,
                                    axes = np.argsort(np.argsort(axis)))

        new_sumw2 = None
        if self._sumw2 is not None:
            new_sumw2 = self._sumw2.project(axis)._contents
                
        return Histogram(edges = self._axes[axis],
                         contents = new_contents,
                         sumw2 = new_sumw2)

    def slice(self, axis, start = None, stop = None,
              underflow = True, overflow = True):
        """
        Return a histogram which is a slice of the current one, along a given
        dimension. 

        Follows same indexing convention as [] operator 
        
        Args:
            axis (int or str): Dimension that will be sliced
            start (None or int): Start bin (inclusive)
            stop (None or int): Stop bin (exclusive). Must be greater than start
            underflow (bool): If True, the contents before the start bin will be
                summed up and kept in the underflow bins, otherwise they'll
                be discarded
            overflow (overflow): same as underflow

        Return:
            Histogram: Sliced histogram
        """

        # If it's a label, turn it into an integer
        axis = self._axes.key_to_index(axis)
        
        # Standarize start/stop and checks. These are the indices of the bins,
        # without taking into account under/overflow
        if isinstance(start, self._NBINS):
            start = self._nbins[axis] + start.offset
        elif start is None:
            start = 0

        if start < 0 or not (start < self._nbins[axis]):
            raise IndexError("'start' out of bounds")
            
        if isinstance(stop, self._NBINS):
            stop = self._nbins[axis] + stop.offset
        elif stop is None:
            stop = self._nbins[axis]

        if not (stop > start):
            raise ValueError("'stop' must be greater than 'start'")

        if stop > self._nbins[axis]:
            raise IndexError("'stop' out of bounds")

        # Redefine axis. Include upper bound of last bin in slice
        new_axes = [Axis(a.edges[start:stop+1], a.label) if adim == axis
                    else a
                    for adim,a in enumerate(self._axes)]

        # This is to select every bin from the dimensions we are not cutting on
        axis_pre = tuple(slice(None) for i in range(0,axis))
        axis_post = tuple(slice(None) for i in range(axis+1, self.ndim)) 

        # Slice, keeping all entries not in the slice in the under/overflow bins
        # if needed
        new_contents = self._contents[axis_pre +
                                      tuple([slice(start+1,stop+1)]) +
                                      axis_post]

        if underflow:

            underflow_contents = np.sum(self._contents[axis_pre +
                                                       tuple([slice(0,start+1)]) +
                                                       axis_post],
                                        axis = axis, keepdims = True)

        else:

            underflow_contents = np.zeros([1 if d == axis
                                           else self._nbins[d] + 2
                                           for d in range(self.ndim)])
            
        new_contents = np.append(underflow_contents, new_contents, axis = axis)

        if overflow:
            
            overflow_contents = np.sum(self._contents[axis_pre +
                                                      tuple([slice(stop+1,
                                                                   self._nbins[axis]+2)]) +
                                                      axis_post],
                                       axis = axis, keepdims = True)

        else:

            overflow_contents = np.zeros([1 if d == axis
                                           else self._nbins[d] + 2
                                           for d in range(self.ndim)])
            
        new_contents = np.append(new_contents, overflow_contents, axis = axis)

        new_sumw2 = None
        if self._sumw2 is not None:
            new_sumw2 = self._sumw2.slice(axis, start, stop)._contents
        
        # Create new histogram
        return Histogram(edges = new_axes,
                         contents = new_contents,
                         sumw2 = new_sumw2)

    def _ioperation(self, other, operation):

        sum_operation = operation in [operator.isub, operator.iadd,
                                      operator.sub,  operator.add]

        product_operation = operation in [operator.imul, operator.itruediv,
                                          operator.mul, operator.truediv]
        
        if isinstance(other, Histogram):
            
            # Another histogram, same axes
            
            if self.axes != other.axes:
                raise ValueError("Axes mismatch")
            
            new_contents = operation(self._contents, other._contents)

            if self._sumw2 is not None or other._sumw2 is not None:

                if self._sumw2 is None or other._sumw2 is None:
                    logger.warning("Operation between histograms with and "
                                   "without sumw2. Using default.")
                
                if sum_operation:

                    self._sumw2._contents = self.sumw2[...] + other.sumw2[...]

                elif product_operation:

                    # Error of either f = A*B or f = A/B is
                    # f_err^2 = f^2 * ((A_err/A)^2 + (B_err/B)^2)
                    
                    relvar = self.sumw2[...]/(self._contents*self._contents)

                    other_relvar = other.sumw2[...]/(other._contents*other._contents)
                    
                    self._sumw2._contents = (new_contents*new_contents*
                                             (relvar + other_relvar))

                else:
                    
                    raise ValueError("Operation not supported")
                
            self._contents = new_contents
                
        else:

            # By scalar or array. Can be broadcasted

            if not np.isscalar(other):

                # Array. With or without under/overflow bins
                other = np.array(other)
                
                if all(np.logical_or(self._nbins == other.shape,
                                     other.shape == 1)):
                    # Missing under and overflow, but right shape.
                    # Adding empty under/overflow bins, exept for axes
                    # with length one that will be broadcasted
                    pad = [(0,) if s==1 else (1,) for s in other.shape]
                    
                    other = np.pad(other, pad)
                    
                elif not all(np.logical_or(self._nbins+2 == other.shape,
                                           other.shape == 1)):
                    raise ValueError("Size mismatch")
                
            self._contents = operation(self._contents, other)

            if self._sumw2 is not None:

                if sum_operation:

                    # sumw2 remains constant if summing/substracting a constant
                    pass
                    
                elif product_operation:
                    
                    self._sumw2 = operation(operation(self._sumw2, other), other)
                    
                else:
                    
                    raise ValueError("Operation not supported")
                    
        return self

    def _operation(self, other, operation):

        new = deepcopy(self)

        new._ioperation(other, operation)

        return new
    
    def __imul__(self, other):

        return self._ioperation(other, operator.imul)
                
    def __mul__(self, other):

        return self._operation(other, operator.mul)

    def __rmul__(self, other):

        return self*other

    def __itruediv__(self, other):

        return self._ioperation(other, operator.itruediv)

    def __truediv__(self, other):

        return self._operation(other, operator.truediv)

    def __rtruediv__(self, other):
        """
        Divide a scalar by the histogram
        """

        if not np.isscalar(other):
            raise ValueError("Inverse operation can only occur between "
                             "histograms or a histogram and a scalar")

        new = deepcopy(self)

        # Error propagtion of f = b/A (where b is constant, no error) is:
        # f_err^2 = f^2 (A_err/A)^2
        
        if new._sumw2 is not None:
            new._sumw2._contents *= other*other/np.power(new._contents, 4)

        new._contents = other/new._contents
        
        return new
    
    def __iadd__(self, other):

        return self._ioperation(other, operator.iadd)
            
    def __add__(self, other):

        return self._operation(other, operator.add)

    def __radd__(self, other):

        return self + other

    def __neg__(self):

        new = deepcopy(self)

        new._contents *= -1

        # No change to sumw2

        return new
    
    def __isub__(self, other):

        return self._ioperation(other, operator.isub)
            
    def __sub__(self, other):

        return self._operation(other, operator.sub)

    def __rsub__(self, other):

        return -self + other
    
    def scale(self, weight, indices = Ellipsis, axis = None):
        """
        Scale the histogram contents.

        By default, :code:`h.scale(weight) <==> h *= weight`

        The parameter :code:`indices` can be used to specify the slice that will
        be multiplied by the weights. Follow the same index convention as in []. 

        If axis is specified, then weights and indices correspond to a single 
        axis.
        
        Args:
            weights (array-like): Weights
            indices (int or tuple): Bin indices
            axis (int or str): Axis index 

        """
        
        if axis is None:

            indices = self._prepare_indices(indices)
            
            self._contents[indices] *= weight

            if self._sumw2 is not None:
                self._sumw2._contents[indices] *= weight*weight

        else:

            # Scale along a dimension
            # We just need to reshape weights and indices

            axis = self._axes.key_to_index(axis)
            
            if axis < 0 or not (axis < self.ndim):
                raise ValueError("Axis out of bounds")
            
            if indices is Ellipsis:
                # In this context Ellipsis means all bins inclusing overflow
                indices = slice(-1,self.NBINS+1)

            # Select all bins from the other dimensions
            indices = tuple(axis*[slice(-1,self.NBINS)]
                            + [indices]
                            + [Ellipsis])

            # Change axis shape to be compatible if needed
            if not np.isscalar(weight):

                weight = np.array(weight)

                if weight.ndim != 1:
                    raise ValueError("When using 'axis', weight can either be "
                                     "scalar or a 1D array")

                newaxis = tuple(axis*[np.newaxis]
                                      + [slice(None,None)]
                                      + (self.ndim-axis-1)*[np.newaxis]) 

                weight = weight[newaxis]

            self.scale(weight,
                       indices = indices)

    def rebin(self, ngroup = 2):

        """
        Need to implement multidiemnsional
        
        sumw2
        
        ngroup negative starts from the last one
        """

        # === Contents ===

        # New number of bins. We'll need both floor and ceil

        ngroup = abs(ngroup)
        ngroup_sign = np.sign(ngroup)
        
        new_nbins = self._nbins[0] / ngroup
        
        # Add padding do under/overflow bins match ngroup including "leftover bins"
        padding =  (ngroup - 1,
                    ngroup - (1 + self._nbins[0] - int(np.floor(new_nbins) * ngroup)))

        padding = padding[::ngroup_sign]
        
        new_contents = np.pad(self._contents, padding)

        # Sum every ngroup elements by reshaping first
        new_nbins = int(abs(np.floor(new_nbins)))

        new_contents = np.sum(new_contents.reshape((new_nbins+2, ngroup)),
                                axis = 1)
    
        # === Adjust edges ===
        new_axes = []
        for n,axis in enumerate(self._axes):

            # Very ngroup-th edge
            new_edges = axis.edges[::ngroup * ngroup_sign][::ngroup_sign]

            # New axis keeping properties
            new_axes += [Axis(new_edges,
                              label = axis.label,
                              scale = axis.scale())]
            
        # === Sum weights square ===
        new_sumw2 = None
        
        if self._sumw2 is not None:
            new_sumw2 = self._sumw2.rebin(ngroup * ngroup_sign)

        # === New histogram ===
        return Histogram(new_axes, new_contents, new_sumw2)

    def draw(self, ax = None, errorbars = True, **kwargs):
        """
        Quick plot of the histogram contents. 

        Under/overflow bins are not included. Only 1D and 2D histograms 
        are supported.

        Args:
            ax (matplotlib.axes): Axes on where to draw the histogram. A new 
                one will be created by default.
            errorbars (bool or None): Include errorbar for 1D histograms. If 
                sumw2 is not available, then sqrt(contents) will be used:
            **kwargs: Passed to `matplotlib.errorbar()` (1D) or 
                `matplotlib.pcolormesh` (2D)
        """

        # Create axes if needed (with labels)
        if ax is None:
            fig,ax = plt.subplots()
            ax.set_xlabel(self.axes[0].label)

            if self.ndim == 2:
                ax.set_ylabel(self.axes[1].label)
            
        # Plot, depending on number of dimensions
        if self.ndim == 1:

            # We have two points per bin (lower edge+center), and 2 extra
            # point for under/overflow (these currently don't have errorbar,
            # they looked bad)
            xdata = np.empty(2*self.nbins + 2)
            xdata[0] = self.axis.edges[0] # For underflow, first edge
            xdata[1::2] = self.axis.edges # In between edges. Last edge for overflow
            xdata[2::2] = self.axis.centers # For markers

            ydata = np.concatenate(([self[-1]],
                                    np.repeat(self.contents, 2),
                                    [self[self.nbins]]))
            
            # Style
            drawstyle = kwargs.pop('drawstyle', 'steps-post')

            # Error bars
            yerr = None

            if errorbars:
                yerr = np.empty(2*self.nbins + 2)
                yerr[2::2] = self.bin_error.contents
                yerr[0] = None # No underflow errorbar, looked bad
                yerr[1::2] = None # No overflow errorbar, looked bad
                
            # Plot
            plot = ax.errorbar(xdata,
                               ydata,
                               yerr = yerr,
                               drawstyle = drawstyle,
                               **kwargs)

        elif self.ndim == 2:

            # No under/overflow
            plot = ax.pcolormesh(self.axes[0].edges,
                                 self.axes[1].edges,
                                 np.transpose(self.contents),
                                 **kwargs)

        else:

            raise ValueError("Plotting only available for 1D and 2D histograms")
            
        return ax,plot
            
    def fit(self, f, lims = None, **kwargs):

        if lims is None:
            lims_bins = slice()
        else:
            lims_bins = slice(*self.find_bin(lims))
            
        x = self.axis.centers[lims_bins]
        y = self[lims_bins]

        sigma = self.bin_error[lims_bins]
        
        return curve_fit(f,x,y, sigma = sigma, **kwargs)
    
