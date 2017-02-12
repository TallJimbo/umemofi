

class Deblender:
    """Base class for algorithms that separate objects.

    This could do something as simple as masking out neighbors, or as complex
    as simultaneously fitting everything and subtracting them.
    """

    def __init__(self, config):
        self.config = config

    def processMultiExposure(self, data):
        """Given a MultiExposureMultiObjectData, return a new one with objects
        somehow separated.

        May modify image/variance/mask pixels (e.g. subtract or mask
        neighbors) and exposure_regions.

        Must remove objects from ``neighbors`` dicts to reflect changes it has
        made to the images, but it need not remove all neighbors (i.e. partial
        deblenders are allowed).
        """
        raise NotImplementedError()


class SingleExposureDeblender(Deblender):
    """Specialization of Deblender that can work on one exposure at a time.
    """

    def __init__(self, config):
        Deblender.__init__(self, config)

    def processSingleExposure(self, data):
        """Given a SingleExposureMultiObjectData, return a new one with objects
        somehow separated.

        May modify image/variance/mask pixels (e.g. subtract or mask
        neighbors) and exposure_regions.

        Must remove objects from ``neighbors`` dicts to reflect changes it has
        made to the images, but it need not remove all neighbors (i.e. partial
        deblenders are allowed).
        """
        raise NotImplementedError()

    def processMultiExposure(self, data):
        # Reference implementation with a simple loop - but the point is that
        # an external caller could parallelize this loop.
        result = data.copy()
        for exposure_id, exposure_data in data.by_exposure.items():
            result[exposure_id] = self.processSingleExposure(exposure_data)
        return result


class Fitter:

    def __init__(self, config):
        self.config = config

    def processMultiObject(self, data):
        """Measure the properties of multiple objects simultaneously, from
        a given MultiExposureMultiObjectData.

        Return a dict of {object_id: SingleObjectAlgorithmData}.
        """
        raise NotImplementedError()


class SingleObjectFitter(Fitter):

    def __init__(self, config):
        self.config = config

    def processMultiObject(self, data):
        # Reference implementation with a simple loop; harness may parellize
        # this loop.
        result = {}
        for object_id, object_data in data.by_object.items():
            result[object_id] = self.processSingleObject(object_data)
        return result

    def processSingleObject(self, data):
        """Measure the properties of multiple objects simultaneously, from
        a given MultiExposureSingleObjectData.

        Return a single SingleObjectAlgorithmData.
        """
        raise NotImplementedError()
