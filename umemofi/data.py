
class SingleObjectInputData:

    def __init__(self, object_id, sky_region, position, warm_start_data):
        self.object_id = object_id
        self.sky_region = sky_region     # sky area covered by this object: HTM/HealPix?  Polygon?
        self.position = position         # position of the object in sky coords
        self.warm_start_data = warm_start_data  # dict of {<algorithm-name>: SingleObjectAlgorithmData}


class MultiObjectInputData:

    def __init__(self, sky_region, data):
        self.sky_region = sky_region   # union of all per-object sky_regions
        self.data = dict(data)         # dict of {object_id: SingleObjectInputData}


class SingleObjectAlgorithmData:
    """Base class for algorithm results.

    Each algorithm subclass this to capture its results.
    """

    def __init__(self, object_id, sky_region):
        self.object_id = object_id
        self.sky_region = sky_region

    @classmethod
    def get_schema(cls):
        """Return a nested dict of {name: numpy.dtype} for output records
        (assuming one entry per object).
        """
        raise NotImplementedError()

    def as_dict(self):
        """Return a nested dict of values with keys matching the result of
        get_schema() and values coercible to the values of get_schema().
        """
        raise NotImplementedError()

    # To do: how do we save e.g. Monte Carlo samples (and describe their schemas)


class SingleExposureSingleObjectData:
    """Core object representing data needed to fit a single object.

    Will be subclassed by harness to implement realize().
    """

    def __init__(self, object_input_data, filter, is_coadd, region, neighbors):
        self.object_input_data = object_input_data  # SingleObjectInputData for the object to be fit (shared)
        self.exposure_id
        self.filter = filter                      # string or other identifier for filter name
        self.is_coadd = is_coadd
        self.region = region                      # fine-grained description of pixels to consider (SpanSet)

        # An {object_id: object_input_data} dict of any additional objects
        # that have been determined to overlap this object's exposure_region.
        self.neighbors = neighbors

        # The items below are initialized by realize().
        self.image = None                # (y,x) float array of pixel values
        self.mask = None                 # (y,x) integer array, with bits as mask planes
        self.weight = None               # (y,x) float array of per-pixel weights (1/sigma)
        self.local_wcs = None            # Mapping from exposure coordinates to sky (AffineTransform)
        self.local_psf = None            # PSF as a function of wavelength (LocalPSF)
        self.local_transmission = None   # photometric scaling as a function of wavelength (SED)

    def realize(self):
        """Load additional attributes prior to use in an algorithm.  If
        already loaded, this should be a very fast no-op.
        """
        raise NotImplementedError()


class MultiExposureSingleObjectData:

    def __init__(self, object_input_data, exposure_data):
        self.object_input_data = object_input_data
        self.exposure_data = dict(exposure_data)  # dict of {exposure_id: SingleExposureSingleObjectData}

    # dict-like interface for SingleExposureSingleObjectData, indexed by exposure_id

    # various filtering methods to get e.g. all exposures with a given filter


class SingleExposureMultiObjectData:

    def __init__(self, exposure_id, object_data):
        self.exposure_id = exposure_id
        self.filter = filter
        self.object_data = dict(object_data)      # dict of {object_id: SingleExposureSingleObjectData}

        # The items below are initialized by realize().
        self.image = None                # (y,x) float array of pixel values
        self.mask = None                 # (y,x) integer array, with bits as mask planes
        self.variance = None             # (y,x) float array of per-pixel variances

    # dict-like interface for SingleExposureSingleObjectData

    def realize(self):
        """Load additional attributes prior to use in an algorithm.  If
        already loaded, this should be a very fast no-op.
        """
        raise NotImplementedError()


class MultiExposureMultiObjectData:
    # conceptually a dict of {(exposure_id, object_id): SingleExposureSingleObjectData},
    # viewable as either a dict of {object_id: MultiExposureSingleObjectData}
    # or a dict of {exposure_id: SingleExposureMultiObjectData}

    def __init__(self, data):
        self.data = dict(data)

    @property
    def by_exposure(self):
        raise NotImplementedError()

    @property
    def by_object(self):
        raise NotImplementedError()

    # dict-like interface indexed on (object_id, exposure_id) tuples

