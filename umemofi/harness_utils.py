

class PrepHelper:
    """Base class for harnesses that build the data structures for fitting.
    """

    @staticmethod
    def find_object_groups(single_object_input_data):
        """Given a list of SingleObjectInputData, return a list of
        non-overlapping MultiObjectInputData.
        """
        raise NotImplementedError()

    def add_exposure(self, exposure_id, sky_region, filter, is_coadd):
        """Add an exposure to the index.
        """
        # to be implemented here
        pass

    def find_exposures(self, sky_region, filter=None, is_coadd=None):
        """Return a list of exposure_ids overlapping the given sky_region.

        If filter is not None, only return exposure_ids with that filter.

        If is_coadd is True or False, only return exposure_ids with the same
        setting.
        """
        # to be implemented here
        pass

    def make_local_wcs(self, exposure_id, position):
        """Return a local WCS (AffineTransform that maps image coordinates to
        sky coordinates) for the given exposure_id and sky position.
        """
        raise NotImplementedError()

    def make_single_object_data(self, exposure_id, filter, is_coadd, local_wcs, region, neighbors):
        """Return a SingleExposureSingleObjectData for the given exposure_id and other quantities.

        Implementers should install the local_psf attribute directly in a subclass that implements
        realize() for this harness.
        """
        raise NotImplementedError()

    def make_multi_object_data(self, multi_object_input_data):
        """Given a MultiObjectInputData representing a group of objects to be fit together,
        create a MultiExposureMultiObjectData containing all the information needed to fit them.
        """
        # to be implemented here
        pass

