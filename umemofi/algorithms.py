

class Deblender:
    """Base class for algorithms that separate objects so they can be fit
    independently.

    This could do something as simple as masking out neighbors, or as complex
    as simultaneously fitting everything and subtracting them.
    """

    def __init__(self, config):
        self.config = config

    def processStack(self, blend_obs_ref_stack):
        """Remove neighbors from all ``ObsData`` referenced by a
        ``BlendObsRefStack``.

        The given ``BlendObsRefStack`` should be updated in-place with
        any ``Model``s created by the Deblender (it need not create any).

        Must return a ``BlendObsDataStack`` created by
        ``blend_obs_ref_stack.load()``, with each ``ObsData`` then modified
        in-place.

        Deblenders may modify ``image`` and possibly ``weight`` pixel values to
        subtract neighbors.  They may also indicate pixels that should not be
        used in single-object fitting by setting bits in ``mask``.  Weight
        pixels should not be set to zero to indicate this; donwstream
        algorithms are responsible for doing this themselves (if desired) from
        the mask.

        Deblenders should also update the ``neighbors`` dict in each
        ``ObsRef``, reflecting the objects that are no longer "present" in the
        corresponding ``ObsData``.
        """
        raise NotImplementedError()


class SingleExposureDeblender(Deblender):
    """Specialization of Deblender that can work on one exposure at a time.
    """

    def __init__(self, config):
        Deblender.__init__(self, config)

    def processStack(self, data):
        # TODO: implement here.
        raise NotImplementedError()

    def processExposure(self, blend_obs_ref):
        """Remove neighbors from all ``ObsData`` referenced by a
        ``BlendObsRef``.

        The given ``BlendObsRef`` should be updated in-place with
        any ``Model``s created by the Deblender (it need not create any).

        Must return a ``BlendObsData`` created by
        ``blend_obs_ref.load()``, with each ``ObsData`` then modified
        in-place.

        Deblenders may modify ``image`` and possibly ``weight`` pixel values to
        subtract neighbors.  They may also indicate pixels that should not be
        used in single-object fitting by setting bits in ``mask``.  Weight
        pixels should not be set to zero to indicate this; donwstream
        algorithms are responsible for doing this themselves (if desired) from
        the mask.

        Deblenders should also update the ``neighbors`` dict in each
        ``ObsRef``, reflecting the objects that are no longer "present" in the
        corresponding ``ObsData``.
        """
        raise NotImplementedError()


class Fitter:

    def __init__(self, config):
        self.config = config

    def processBlend(self, blend_obs_ref_stack):
        """Measure the properties of multiple objects simultaneously, from
        a given ``BlendObsRefStack``.

        Results should be returned by adding a ``Model`` to one or more of the
        nested `models` dicts in the ``blend_obs_ref_stack``.
        """
        raise NotImplementedError()


class SingleObjectFitter(Fitter):

    def __init__(self, config):
        self.config = config

    def processBlend(self, blend_obs_ref_stack):
        # TODO: implementhere
        raise NotImplementedError()

    def processObject(self, obs_ref_stack):
        """Measure the properties of a single object, from a given
        ``ObsRefStack``.

        Results should be returned by adding a ``Model`` to one or more of the
        nested `models` dicts in the ``blend_obs_ref_stack``.
        """
        raise NotImplementedError()
