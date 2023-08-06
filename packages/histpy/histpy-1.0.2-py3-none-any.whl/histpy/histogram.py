import logging
logger = logging.getLogger(__name__)

import numpy as np

import operator

from copy import copy,deepcopy

import matplotlib.pyplot as plt

from scipy.optimize import curve_fit

from inspect import signature

import h5py as h5

from .axes import Axes,Axis

class Histogram(object):
    """
    This is a wrapper of a numpy array with axes and a fill method.
    
    Like an array, the histogram can have an arbitrary number of dimensions.

    Standard numpy array indexing is supported to get the contents 
    --i.e. :code:`h[:]`, :code:`h[4]`, :code:`h[[1,3,4]]`, :code:`h[:,5:50:2]]`,
    etc.--. However, the meaning of the :code:`-1` index is different. Instead of 
    counting from the end, :code:`-1` corresponds to the underflow bin. Similarly,
    an index equal to the number of bins corresponds to the overflow bin. 

    You can however give relative position with respect to :code:`h.end` 
    --e.g. :code:`h[0:h.end]` result in all regular bins, :code:`h[-1:h.end+1]` 
    includes also the underflow/overflow bins and :code:`h[h.end]` gives you the 
    contents of the overflow bin. The convenient aliases :code:`h.uf = -1`,
    :code:`h.of = e.end` and :code:`h.all = slice(-1,h.end+1)` are provided.
    
    You can also use an :code:`Ellipsis` object (:code:`...`) at the end to specify that the
    contents from the rest of the dimension are to have the under and overflow
    bins included. e.g. for a 3D histogram :code:`h[1,-1:h.end+1,-1:h.end+1]
    = h[1,...]`. :code:`h[:]` returns all contents without under/overflow bins and
    h[...] returns everything, including those special bins.

    If :code:`sumw2` is not :code:`None`, then the histogram will keep track of 
    the sum of the weights squared --i.e. you better use this if you are using 
    weighted data and are concern about error bars--. You can access these with
    :code:`h.sumw2[item]`, where `item` is interpreted the same was a in :code:`h[item]`.
    :code:`h.bin_error[item]` return the :code:`sqrt(sumw2)` (or :code:`sqrt(contents)` is :code:`sumw2
    was not specified`).

    The operators :code:`+`, :code:`-`, :code:`*` and :code:`-` are available.
    Both other operand can be a histograms, a scalar or an array of appropiate size.
    Note that :code:`h += h0` is more efficient than 
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
        axis_scale (str or array): Bin center mode e.g. `"linear"` or `"log"`. 
            See ``Axis.axis_scale``. 

    """
            
    def __init__(self, edges, contents = None, sumw2 = None,
                 labels=None, axis_scale = None):

        self._axes = Axes(edges, labels=labels, axis_scale = axis_scale)

        # Standarize contents (with under/overflow) or initialize them to zero.
        if contents is not None:
            if np.array_equal(self.axes.nbins+2, np.shape(contents)):
                # Includes under and overflow
                self._contents = np.array(contents) 
            elif np.array_equal(self.axes.nbins, np.shape(contents)):
                # Missing under and overflow, but right shape.
                # Adding empty under/overflow bins
                self._contents = np.pad(contents, 1)
            else:
                raise ValueError("Bins ({}) - contents {} size mismatch".format(self.axes.nbins,np.shape(contents)))
        else:
            self._contents = np.zeros([n+2 for n in self.axes.nbins])

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
        self.slice = self._slice(self)
        
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

    def __array__(self):
        return self.contents
    
    class _NBINS():        
        '''
        Convenience class that will expand to the number of bins of a 
        given dimension. 

        The trick is to overload the -/+ operators such than 
        h.end +/- offset (h being an instance of Histogram and 'end' an 
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
        
    end = _NBINS()

    # Convenient aliases
    uf = -1
    of = end
    all = slice(-1, end+1)
    
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
                              self.axes[dim].nbins + index.start.offset + 1
                              if isinstance(index.start, self._NBINS)
                              else
                              index.start+1,
                              
                              self.axes[dim].nbins+1
                              if index.stop is None
                              else
                              self.axes[dim].nbins + index.stop.offset + 1
                              if isinstance(index.stop, self._NBINS)
                              else
                              index.stop+1,
                              
                              index.step)
                
                # Check bounds. Note index is the _contents index at this point
                if index.start < 0 or index.stop > self.axes[dim].nbins + 2:
                    raise IndexError("Bin index out of bounds")
                
                return index
            
            elif isinstance(index, (np.integer, int)):
                if index < -1 or index > self.axes[dim].nbins:
                    raise IndexError("Bin index out of bounds")

                return index+1

            elif isinstance(index, self._NBINS):

                # Referece with respect to nbins
                return _prepare_index(self.axes[dim].nbins + index.offset, dim)
            
            elif isinstance(index, (np.ndarray, list, tuple, range)):

                # Note: this will return a copy, not a view

                # Handle references with respecto to nbins
                index = np.array(index)

                if index.dtype == bool:
                    # Mask. Pad under/overflow

                    return np.pad(index, 1, constant_values = False)
                    
                else:
                    # Indices

                    index_shape = index.shape

                    index = index.flatten()
                    
                    index =  [self.axes[dim].nbins + i.offset + 1
                              if isinstance(i,self._NBINS) else
                              i + 1
                              for i in index]

                    index = np.reshape(index, index_shape)
                    
                    # Check bounds. Note index is the _contents index at this point/
                    if (np.any(index < 0) or
                         np.any(index > self.axes[dim].nbins + 1)):
                        raise IndexError("Bin index out of bounds")
                        
                    return index
                    
            else:
                raise TypeError("Index can only be an int, slice, list or array")
        
        if isinstance(indices, tuple):

            # Get the rest of the dimensions with under/overflow user used ...
            if indices[-1] is Ellipsis:
                extra_indices = tuple(slice(-1, self.axes[dim].nbins+1)
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

            if self._hist._sumw2 is None:
                raise ValueError("Histogram does not have sumw2")

            indices = self._hist._prepare_indices(indices)
            
            self._hist._sumw2._contents[indices] = new_sumw2
            
    class _get_bin_error(_special_getitem):
        """
        Return the sqrt of sumw2
        """
        
        def __getitem__(self, item):
            return np.sqrt(self._hist.sumw2[item])
                        
        def __setitem__(self, indices, new_bin_error):

            if self._hist._sumw2 is None:
                raise ValueError("Histogram does not have sumw2")

            indices = self._hist._prepare_indices(indices)
            
            self._hist._sumw2._contents[indices] = np.power(new_bin_error, 2)

        def __array__(self):

            return self._hist._contents

    @property
    def contents(self):
        """
        Equivalent to :code:`h[:]`. Use :code:`h[...]` to get under/overflow bins.
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
        Equivalent to :code:`self.axes[0]`, but fails if :code:`ndim > 1`
        """

        if self.ndim > 1:
            raise ValueError("Property 'axis' can only be used with 1D "
                            "histograms. Use `axes` for multidimensional "
                            "histograms")

        return self.axes[0]

    @axis.setter
    def axis(self, new):

        self.axes[0] = new
            
    @property
    def nbins(self):

        if self.ndim == 1:
            return self.axes[0].nbins
        else:
            return self.axes.nbins
            
    def find_bin(self, *values):
        """
        Return one or more indices corresponding to the bin this value or 
        set of values correspond to.

        You can pass either an array, or specified the values as different 
        arguments. i.e. :code:`h.find_bin(x,y,z)` = :code:`h.find_bin([x,y,z])`

        Multiple entries can be passed at once. e.g. 
        :code:`h.find_bin([x0, x1, x2])`, 
        :code:`h.find_bin([x0, x1],[y0, y1],[z0, z1])`,
        :code:`h.find_bin([[x0, x1],[y0, y1],[z0, z1]])`
        
        Args:
            values (float or array): Vaule or list of values. Either shape N or
               ndim x N, where N is the number of entries.

        Return:
            int or tuple: Bin index
        """
        
        # Handle 1D
        if self.ndim == 1:

            # 1D hist, any shape of values works. The output has the same shape
            
            if len(values) != 1:
                raise ValueError("Mismatch between values shape and number of axes")

            return self.axis.find_bin(values[0])

        # >=2D case

        # Sanitize and standarize
        if len(values) == 1:
            # e.g. ([x,y]) or ([[x0,x1], [y0,y1]]), NOT (x,y,z), [[x0,x1], [y0,y1]]
            values = tuple(values[0])
            
        if len(values) != self.ndim:
            raise ValueError("Mismatch between values shape and number of axes")

        return tuple(axis.find_bin(val)
                     for val,axis in zip(values, self.axes))

    def interp(self, *values):
        """
        Get a linearly interpolated content for a given set of values
        along each axes. The bin contents are assigned to the center of the bin.
        
        Args:
            values (float or array): Coordinates within the axes to interpolate.
                 Must have the same size as `ndim`. Input values as
                 `(1,2,3)` or `([1,2,3])`

        Return:
            float
        """

        bins,weights = self._axes.interp_weights(*values)

        content = 0

        if bins.ndim == 1:
            # Single point case
            
            for bin,weight in zip(bins, weights):
                content += weight*self[bin]

        else:

            # Multi
            
            for bin,weight in zip(bins, weights):

                # Each b can be a tuple
                bin = np.array(bin, ndmin = 1)
                
                bin_values = np.reshape([self[b] for b in bin.flatten()],
                                        bin.shape)

                content += weight*bin_values

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

        indices = self.find_bin(*values)

        # Allow for some values with different shape but broadcastable
        indices = self._prepare_indices(indices)
        indices = np.broadcast_arrays(*indices)

        # Flatten all
        indices = tuple([i.flatten() for i in indices])
        weight = np.array(weight).flatten()
        
        # Make it work with multiple entries at one
        new_axes = tuple(np.arange(np.ndim(indices), 2))
        indices = np.expand_dims(indices, new_axes).transpose()
        weight = np.broadcast_to(weight, indices.shape[0])

        for i,w in zip(indices, weight):
            self._contents[tuple(i)] += w

        if self._sumw2 is not None:
            for i,w in zip(indices, weight):
                self._sumw2._contents[tuple(i)] += w*w

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
        
        axis = self._axes.label_to_index(axis)
        
        if len(np.unique(axis)) != len(axis):
            raise ValueError("An axis can't repeat")

        # Project
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

    def clear_overflow(self, axes = None):
        """
        Set all overflow bins to 0, including sumw2

        Args:
            axes (None or array): Axes number or labels. All by default
        """
        if axes is None:
            axes = range(self.ndim)
        elif np.isscalar(axes):
            axes = [axes]
        
        for n in axes:
            indices = self.expand_dict({n:self.of}, self.all)
            self[indices] = 0

        if self._sumw2 is not None:
            self._sumw2.clear_overflow(axes)
        
    def clear_underflow(self, axes = None):
        """
        Set all overflow bins to 0, including sumw2

        Args:
            axes (None or array): Axes number or labels. All by default
        """
        if axes is None:
            axes = range(self.ndim)
        elif np.isscalar(axes):
            axes = [axes]

        for n in axes:
            indices = self.expand_dict({n:self.uf}, self.all)
            self[indices] = 0

        if self._sumw2 is not None:
            self._sumw2.clear_underflow(axes)        

    def clear_underflow_and_overflow(self, *args, **kwargs):
        """
        Set all underflow and overflow bins to 0, including sumw2

        Args:
            axes (None or array): Axes number or labels. All by default
        """

        self.clear_underflow(*args, **kwargs)
        self.clear_overflow(*args, **kwargs)        
            
    class _slice:
        """
        Return a histogram which is a slice of the current one
        """

        def __init__(self, hist):
            self._hist = hist

        def __getitem__(self, item):

            # Check indices and either pad or use under/overflor
            indices = self._hist._prepare_indices(item)

            # If under/overflow are including, will use them instead of pads
            padding = np.ones([self._hist.ndim, 2], dtype = int)

            axes_indices = np.empty(self._hist.ndim, dtype = 'O')
            new_nbins = np.empty(self._hist.ndim, dtype = int)
            
            for ndim,(index, axis) in enumerate(zip(indices,
                                                    self._hist.axes)):

                # Standarize into slice
                if isinstance(index, int):
                   
                    index = slice(index, index+1)

                # Sanity checks
                if not isinstance(index, slice):

                    raise TypeError("Only slices and integers allows in slice[]")
               
                start,stop,stride = index.indices(axis.nbins+2)

                if stride != 1:
                    raise ValueError("Step must be 1 when getting a slice."
                                     "Alertnatively us rebin().")

                if start == stop:
                    raise ValueError("Slice must have a least one bin in "
                                     "all dimensions. Alternatively use project().")

                if start > stop:
                    raise ValueError("Slices cannot reverse the bin order.")

                # Handle under/overflow

                axis_start = start # Axes don't have under/overflow
                axis_stop = stop
                
                if start == 0:

                    if stop-start == 1:
                        raise ValueError("The slice cannot contain only the "
                                         "underflow bin")

                    axis_start += 1
                    
                    padding[ndim, 0] = 0

                    
                if stop == axis.nbins + 2:

                    if stop-start == 1:
                        raise ValueError("The slice cannot contain only the "
                                         "overflow bin")

                    axis_stop -= 1

                    padding[ndim, 1] = 0                        

                    
                axes_indices[ndim] = slice(axis_start, axis_stop)
                new_nbins[ndim] = stop-start
                
            axes_indices = tuple(axes_indices)

            # Get new contents. Pad is underflow/overflow are not included
            # New to broadcast to avoid singletons messing with padding size
            new_contents = self._hist._contents[indices]
            new_contents = np.broadcast_to(new_contents, new_nbins)
            new_contents = np.pad(new_contents, padding)
            
            # New Axes
            new_axes = [Axis(axis.edges[index.start-1:index.stop],
                             label = axis.label,
                             scale = axis.axis_scale)
                         for axis,index in zip(self._hist.axes,axes_indices)]

            # Sum weights squared
            new_sumw2 = None
            if self._hist._sumw2 is not None:
                new_sumw2 = self._hist._sumw2.slice[item]

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

                if other.ndim != self.ndim:
                    raise ValueError("Operand number of dimensions ({}) does not"
                                     "match number of axes ({})".format(other.ndim,
                                                                        self.ndim))
                
                pad = []

                for n,(length,nbins) in enumerate(zip(other.shape, self.axes.nbins)):

                    if length == 1 or length == nbins+2:
                        # Single element axis can be broadcasted as is
                        # OR array includes under/overflow
                        pad += [(0,)]
                    elif length == nbins:
                        # Missing under and overflow, but right shape.
                        pad += [(1,)]
                    else:
                        raise ValueError("Could not broadcast array of shape {} "
                                         "to histogram with nbins "
                                         "{}".format(other.shape,
                                                     self.axes.nbins))

                other = np.pad(other, pad)
                                    
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

    def __lt__(self, other):
        return self.contents < other
    
    def __le__(self, other):
        return self.contents <= other
    
    def __gt__(self, other):
        return self.contents > other
    
    def __ge__(self, other):
        return self.contents >= other
    
    
    def expand_dims(self, *args, **kwargs):
        """
        Same as h.axes.expand_dims().
        """
        return self._axes.expand_dims(*args, **kwargs)
    
    def expand_dict(self, *args, **kwargs):
        """
        Same as h.axes.expand_dict().
        """
        return self._axes.expand_dict(*args, **kwargs)

    def rebin(self, *ngroup):

        """
        Rebin the histogram by grouping multiple bins into a single one.

        Args:
            ngroup (int or array): Number of bins that will be combined for each 
                bin of the output. Can be a single number or a different number
                per axis. A number <0 indicates that the bins will start to be
                combined starting from the last one.

        Return:
            Histogram
        """

        # === Contents ===

        # New number of bins.
        ngroup = np.squeeze(ngroup)
        ngroup = np.broadcast_to(np.abs(ngroup), (self.ndim))
        ngroup_sign = np.sign(ngroup)
        
        new_nbins = np.floor(self.axes.nbins / ngroup).astype(int)

        if any(ngroup == 0):
            raise ValueError("ngroup cannot be 0")
        
        # Add padding do under/overflow bins match ngroup including "leftover bins"
        padding =  [(ngroup_i - 1,
                    ngroup_i - (1 + nbins_i - new_nbins_i * ngroup_i))
                    for ngroup_i, nbins_i, new_nbins_i
                    in zip(ngroup, self.axes.nbins, new_nbins)]

        # Rever direction if needed
        padding = [pad[::direction]
                   for pad,direction
                   in zip(padding,ngroup_sign)]
        
        new_contents = np.pad(self._contents, padding)

        # Sum every ngroup elements by reshaping first
        new_shape = np.empty(2*self.ndim, dtype = int)
        new_shape[0::2] = new_nbins+2
        new_shape[1::2] = ngroup
        new_shape = tuple(new_shape)
        sum_axis = tuple(np.arange(1,2*self.ndim,2))
        new_contents = np.sum(new_contents.reshape(new_shape), axis = sum_axis)

        # === Adjust edges ===
        new_axes = []
        for axis,ngroup_i,ngroup_sign_i in zip(self._axes, ngroup, ngroup_sign):

            # Very ngroup-th edge
            new_edges = axis.edges[::ngroup_i * ngroup_sign_i][::ngroup_sign_i]

            # New axis keeping properties
            new_axes += [Axis(new_edges,
                              label = axis.label,
                              scale = axis.axis_scale)]
            
        # === Sum weights square ===
        new_sumw2 = None
        
        if self._sumw2 is not None:
            new_sumw2 = self._sumw2.rebin(ngroup * ngroup_sign)

        # === New histogram ===
        return Histogram(new_axes, new_contents, new_sumw2)

    def draw(self, ax = None,
             errorbars = True,
             colorbar = True,
             label_axes = True,
             **kwargs):
        """
        Quick plot of the histogram contents. 

        Under/overflow bins are not included. Only 1D and 2D histograms 
        are supported.

        Args:
            ax (matplotlib.axes): Axes on where to draw the histogram. A new 
                one will be created by default.
            errorbars (bool or None): Include errorbar for 1D histograms. If 
                sumw2 is not available, then sqrt(contents) will be used.
            colorbar (bool): Draw colorbar in 2D plots
            label_axes (bool): Label plots axes. Histogram axes must be labeled.
            **kwargs: Passed to `matplotlib.errorbar()` (1D) or 
                `matplotlib.pcolormesh` (2D)
        """

        # Create axes if needed (with labels)
        if ax is None:
            fig,ax = plt.subplots()
            
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

            # Label axes
            if label_axes:
                ax.set_xlabel(self.axes[0].label)                
            
        elif self.ndim == 2:

            # No under/overflow
            plot = ax.pcolormesh(self.axes[0].edges,
                                 self.axes[1].edges,
                                 np.transpose(self.contents),
                                 **kwargs)

            if label_axes:
                ax.set_xlabel(self.axes[0].label)
                ax.set_ylabel(self.axes[1].label)

            if colorbar:
                ax.get_figure().colorbar(plot, ax = ax)
            
        else:

            raise ValueError("Plotting only available for 1D and 2D histograms")
            
        if self.axes[0].axis_scale == 'log':
                ax.set_xscale('log')

        if self.ndim > 1:
            if self.axes[1].axis_scale == 'log':
                ax.set_yscale('log')
                
        return ax,plot
            
    def fit(self, f, lo_lim = None, hi_lim = None, **kwargs):
        """
        Fit histogram data using least squares.

        This is a convenient call to scipy.optimize.curve_fit. Sigma corresponds
        to the output of `h.bin_error`. Empty bins (e.g. error equals 0) are 
        ignored

        Args:
            f (callable): Function f(x),... that takes the independent variable 
                x as first argument, and followed by the parameters to be fitted.
                For a k-dimensional histogram is should handle arrays of shape 
                (k,) or (k,N).
            lo_lim (float or array): Low axis limit to fit. One value per axis.
            lo_lim (float or array): High axis limit to fit. One value per axis.
            **kwargs: Passed to scipy.optimize.curve_fit
        """
        
        # Sanity checks
        for axis,lo,hi in  zip(self.axes,
                          np.broadcast_to(lo_lim, self.ndim),
                          np.broadcast_to(hi_lim, self.ndim)):

            if ((lo is not None and lo < axis.lo_lim) or
                (hi is not None and hi >= axis.hi_lim)):
                raise ValueError("Fit limits out of bounds")

        # Get bins that correspond to the fit limits
        lim_bins = tuple([slice(None if lo is None else axis.find_bin(lo),
                                None if hi is None else axis.find_bin(hi))
                          for axis,lo,hi
                          in zip(self.axes,
                                 np.broadcast_to(lo_lim, self.ndim),
                                 np.broadcast_to(hi_lim, self.ndim))])

        # Get data to fit
        x = [axis.centers[bins] for axis,bins in zip(self.axes,lim_bins)]
        x = np.meshgrid(*x, indexing='ij') # For multi-dimensional histograms
        y = self[lim_bins]
        sigma = self.bin_error[lim_bins]

        # Ignore empty bins
        non_empty = sigma != 0 
        x = [centers[non_empty] for centers in x]
        y = y[non_empty]
        sigma = sigma[non_empty]

        # Flat matrices
        if self.ndim > 1:
            x = [centers.flatten() for centers in x]
            y = y.flatten()
            sigma = sigma.flatten()
        else:
            x = x[0]

        # Sanity checks
        if len(x) < len(signature(f).parameters)-1:
            raise RuntimeError("Less bins within limits than parameters to fit.")
            
        # Actual fit with scipy
        return curve_fit(f, x, y, sigma = sigma, **kwargs)
    
    def write(self, filename, name = "hist", overwrite = False):
        """
        Write histogram to disk.

        It will be save as a group in a HDF5 file. Appended if the file already 
        exists.

        Args:
            filename (str): Path to file
            name (str): Name of group to save histogram (can be any HDF5 path)
            overwrite (str): Delete and overwrite group if already exists.
        """

        with h5.File(filename, 'a') as f:

            # Will fail on existing group by default
            if name in f:
                if overwrite:
                    del f[name]
                else:
                    raise ValueError("Unable to write histogram. Another group "
                                     "with the same name already exists. Choose "
                                     "a different name or use overwrite")

            # Contents
            hist_group = f.create_group(name)

            contents_set = hist_group.create_dataset('contents', data = self._contents)

            if self._sumw2 is not None:
                sumw2_set = hist_group.create_dataset('sumw2', data = self._sumw2._contents)

            # Axes. Each one is a data set with attributes
            axes_group = hist_group.create_group('axes', track_order = True)

            for i,axis in enumerate(self.axes):

                axis_set = axes_group.create_dataset(str(i), data = axis.edges)

                axis_set.attrs['scale'] = axis.axis_scale

                if axis.label is not None:
                    axis_set.attrs['label'] = axis.label

    @classmethod
    def open(cls, filename, name = 'hist'):
        """
        Read histogram from disk.

        Args:
            filename (str): Path to file
            name (str): Name of group where the histogram was saved.
        """

        with h5.File(filename, 'r') as f:

            hist_group = f[name]

            contents = np.array(hist_group['contents'])

            sumw2 = None
            if 'sumw2' in hist_group:
                sumw2 = np.array(hist_group['sumw2'])

            axes_group = hist_group['axes']

            axes = []
            for edges in axes_group.values():

                axes += [Axis(np.array(edges), **edges.attrs)]

        return Histogram(axes, contents = contents, sumw2 = sumw2)
        
