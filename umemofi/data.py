
class ObjectData:
    """A class that aggregates all the things we know about an Object that don't
    relate to the exposures on whic h it was observed.
    """

    def __init__(self, object_id, sky_region, sky_position):
        self.object_id = object_id
        self.sky_region = sky_region      # maximal (over models) sky area covered by this object: HTM ranges
        self.sky_position = sky_position  # position of the object in sky coords
        # dict of {<algorithm-name>: Model}, to be updated in-place.
        # Should only hold Models that are not specific to a single exposure.
        self._models = dict()


class MultiObjectData:
    """A simple wrapper around a dict of {object_id: ObjectData} that also
    aggregates the object's sky_regions.
    """

    def __init__(self, sky_region, objects):
        self.sky_region = sky_region   # union of all per-object sky_regions
        self.objects = dict(objects)         # dict of {object_id: SingleObjectData}


class Model:
    """Base class for the results of a single algorithm fitting a single object.

    Most algorithm should subclass this to capture their results, multiple
    related algorithms may share the same Model.

    Models may represent three concepts:
    - Objects (not specific to an exposure); these Models are held by
      ObjectData instances.  For example, most shear measurements would fall
      into this category.
    - Sources (an object as it appears in an exposure); these Models are held
      by ObservationMeta instances.  Forced photometry results would fall into
      this category.
    - PSFs (by definition related to a particular point in an exposure); these
      Models are held by PSF objects.

    Note that there is no concept of a model with filter-specific information;
    Models with different parameters in different filters should just treat
    per-filter parameters (such as the flux in a particular band) as distinct
    parameters that are part of an Object model.

    A Model is expected to hold both a best-fit result *and* its uncertainty.
    """

    @classmethod
    def getSchema(cls):
        """Return a nested dict of {name: numpy.dtype} for output records
        (assuming one entry per object).
        """
        raise NotImplementedError()

    def asDict(self):
        """Return a nested dict of values with keys matching the result of
        getSchema() and values coercible to the values of getSchema().
        """
        raise NotImplementedError()

    def render(self, observation, output_image):
        """Create an image of this model corresponding to the image of the
        given observation.
        """
        raise NotImplementedError()

    def mask(self, observation, output_mask, rendered=None):
        """Set a bit in the given mask on pixels heavily influenced by this
        object.

        The result of a call to render() with the same observation may be
        passed to optimize the case where the mask is just a simple threshold
        on the rendered image.
        """
        raise NotImplementedError()

    def computeSkyRegion(self, sky_position):
        """Compute a SkyRegion that includes all pixels covered by this object.

        May include some pixels not covered by this model, if evaluated at
        the given sky position.
        """
        raise NotImplementedError()

    # TODO: how do we save Monte Carlo samples (and describe their schemas)?


class ObservationMeta:

    def __init__(self, object_data, exposure_id, is_coadd, filter_name, wcs,
                 region=None, neighbors=None):
        self.object_data = object_data
        self.exposure_id = exposure_id
        self.is_coadd = is_coadd
        self.filter_name = filter_name
        self.wcs = wcs
        # TODO: if region is None, generate from object_data.sky_region.
        self.region = region
        # neighbors: a dict of {object_id: ObservationMeta} containing all
        # all other objects that may overlap this Observation's postage stamp.
        # (this in turn contains a models dict with objects that can be used
        # to subtract neighbors).
        self.neighbors = dict(neighbors) if neighbors is not None else dict()
        # _models: dict of {<algorithm-name>: Model}, to be updated in-place.
        # Should only hold Models that are specific to this exposure.
        # (those that are should go in self.object_data.models).
        self._models = dict()

    @property
    def object_id(self): return self.object_data.object_id

    def load(self, image=None, mask=None, weight=None):
        """Return the Observation this handle points to.

        If ``image``, ``mask``, and ``weight`` are not None (they all either
        will be or won't be), the Observation's ``image``, ``mask``, and
        ``weight`` should be views of these.
        """
        raise NotImplementedError()


class Observation:

    def __init__(self, image, mask=None, weight=None, psf=None, wcs=None,
                 transmission=None, region=None, neighbors=None, meta=None):
        # TODO: set and document defaults
        self.image = image
        self.mask = mask
        self.weight = weight
        self.psf = psf
        self.wcs = wcs
        self.transmission = transmission
        self.meta = meta


class PSF:

    def __init__(self):
        self.models = {}

    def getObservation(self):
        """Get an image of the PSF as an Observation with trivial ``mask``,
        ``weights``, and ``transmission``, ``psf=None``, and ``wcs`` set to
        define the natural coordinate system of the PSF.
        """
        raise NotImplementedError()


class MultiObjectObservationMeta:

    def __init__(self, exposure_id, multi_object_data, is_coadd, filter_name,
                 observation_meta, region=None):
        self.multi_object_data = multi_object_data  # MultiObjectData
        self.exposure_id = exposure_id
        self.is_coadd = is_coadd
        self.filter_name = filter_name
        self.observation_meta = dict(observation_meta)  # {object_id: ObservationMeta}
        self.region = region  # TODO: generate from union of observations

    def load(self):
        """Return the MultiObjectObservation this handle points to.
        """
        raise NotImplementedError()


class MultiObjectObservation:

    def __init__(self, image, mask, weight, observations, region=None,
                 meta=None):
        self.image = image
        self.mask = mask
        self.weight = weight
        self.observations = dict(observations) if observations is not None else dict()
        self.meta = meta


class ObjectObservationDict:

    def __init__(self, object_data, observation_meta):
        self.object_data = object_data
        self.observation_meta = dict(observation_meta)  # {exposure_id: ObservationMeta}


class MultiObjectObservationDict:

    def __init__(self, multi_object_data, observation_meta):
        self.multi_object_data = multi_object_data
        self.observation_meta = dict(observation_meta)  # {(object_id, exposure_id): ObservationMeta}

    def find_object(self, object_id):
        return ObjectObservationDict(
            self.object_data,
            {exp_id: obs_meta
             for (obj_id, exp_id), obs_meta in self.observation_meta
             if obj_id == object_id}
        )

    def find_exposure(self, exposure_id):
        return MultiObjectObservationMeta(
            self.multi_object_data,
            {obj_id: obs_meta
             for (obj_id, exp_id), obs_meta in self.observation_meta
             if exp_id == exposure_id}
        )
