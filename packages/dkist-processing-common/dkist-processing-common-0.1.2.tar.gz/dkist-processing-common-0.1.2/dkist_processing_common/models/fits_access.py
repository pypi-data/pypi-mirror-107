"""
Abstraction layer for accessing fits data via class attributes
"""
from __future__ import annotations

from typing import Optional
from typing import Union

import numpy as np
from astropy.io import fits


class FitsAccessBase:
    def __init__(
        self,
        hdu: Union[fits.ImageHDU, fits.PrimaryHDU, fits.CompImageHDU],
        name: Optional[str] = None,
    ):
        self._hdu = hdu
        self.name = name

    @property
    def data(self) -> np.ndarray:
        return self._hdu.data

    @property
    def header(self) -> fits.Header:
        return self._hdu.header

    @classmethod
    def from_header(
        cls, header: Union[fits.Header, dict], name: Optional[str] = None
    ) -> FitsAccessBase:
        """
        Convert a header to a CommonFitsData (or child) object

        Parameters
        ----------
        header
            A single `astropy.io.fits.header.Header` HDU object.
        name
            A unique name for the fits access instance
        """
        if isinstance(header, dict):
            header = fits.Header(header)
        hdu = fits.PrimaryHDU(header=header)
        return cls(hdu=hdu, name=name)
