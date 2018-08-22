# -*- coding: utf-8 -*-
"""Module implementing a simple hooks system to allow late-binding actions to
PyDOV events."""

import sys


class AbstractHook(object):
    """Abstract base class for custom hook implementations.

    Provides all available methods with a default implementation to do
    nothing. This allows for hook subclasses to only implement the events
    they need.

    """
    def wfs_search_init(self, typename):
        """Called upon starting a WFS search.

        Parameters
        ----------
        typename : str
            The typename (layername) of the WFS service used for searching.

        """
        pass

    def wfs_search_result(self, number_of_results):
        """Called after a WFS search finished.

        Parameters
        ----------
        number_of_results : int
            The number of features returned by the WFS search.

        """
        pass

    def xml_requested(self, pkey_object):
        """Called upon requesting an XML document of an object.

        This is either followed by ``xml_cache_hit`` or ``xml_downloaded``.

        Parameters
        ----------
        pkey_object : str
            Permanent key of the requested object.

        """
        pass

    def xml_cache_hit(self, pkey_object):
        """Called when the XML document of an object is retrieved from the
        cache.

        Parameters
        ----------
        pkey_object : str
            Permanent key of the requested object.

        """
        pass

    def xml_downloaded(self, pkey_object):
        """Called when the XML document of an object is downloaded from the
        DOV services.

        Parameters
        ----------
        pkey_object : str
            Permanent key of the requested object.

        """
        pass


class SimpleStatusHook(AbstractHook):
    """Simple hook implementation to print progress to stdout."""
    def __init__(self):
        """Initialisation.

        Initialise all variables to 0.

        """
        self.result_count = 0
        self.prog_counter = 0

    def _write_progress(self, char):
        """Write progress to standard output.

        Progress is grouped on lines per 50 items, adding ``char`` for every
        item processed.

        Parameters
        ----------
        char : str
            Single character to print.

        """
        if self.prog_counter == 0:
            sys.stdout.write('[%03i/%03i] ' % (self.prog_counter,
                                               self.result_count))
            sys.stdout.flush()
        elif self.prog_counter % 50 == 0:
            sys.stdout.write('\n[%03i/%03i] ' % (self.prog_counter,
                                                 self.result_count))
            sys.stdout.flush()

        sys.stdout.write(char)
        sys.stdout.flush()
        self.prog_counter += 1

        if self.prog_counter == self.result_count:
            sys.stdout.write('\n')
            sys.stdout.flush()

    def wfs_search_init(self, typename):
        """When a new WFS search is started, reset all counters to 0.

        Parameters
        ----------
        typename : str
            The typename (layername) of the WFS service used for searching.

        """
        self.result_count = 0
        self.prog_counter = 0

    def wfs_search_result(self, number_of_results):
        """When the WFS search completes, set the total result count to
        ``number_of_results``.

        Parameters
        ----------
        number_of_results : int
            The number of features returned by the WFS search.

        """
        self.result_count = number_of_results

    def xml_cache_hit(self, pkey_object):
        """When an XML document is retrieved from the cache, print 'c' to
        the progress output.

        Parameters
        ----------
        pkey_object : str
            Permanent key of the requested object.

        """
        self._write_progress('c')

    def xml_downloaded(self, pkey_object):
        """When an XML document is downloaded from the DOV services,
        print '.' to the progress output.

        Parameters
        ----------
        pkey_object : str
            Permanent key of the requested object.

        """
        self._write_progress('.')
