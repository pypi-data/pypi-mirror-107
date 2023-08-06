# Copyright CNRS/Inria/UCA
# Contributor(s): Eric Debreuve (since 2021)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

from typing import Iterator, Sequence

import numpy as nmpy
import scipy.spatial.distance as dstc
from type.cell import cell_t
from type.tracks import tracks_t


array_t = nmpy.ndarray


def CellsTracks(
    cells_per_time_point: Iterator[Sequence[cell_t]],
    bidirectional: bool = True,
    max_distance: float = nmpy.inf,
) -> tracks_t:
    """"""
    output = tracks_t()

    previous_cells = None
    previous_centroids = None
    for t_idx, cells in enumerate(cells_per_time_point):
        if cells.__len__() == 0:
            raise ValueError(f"No cells at time point {t_idx}")

        if previous_cells is None:
            previous_cells = cells
            previous_centroids = _CellsCentroids(cells)
            continue

        centroids = _CellsCentroids(cells)
        pairwise_distances = dstc.cdist(previous_centroids, centroids)

        for c_idx, cell in cells:
            previous_c_idx = nmpy.argmin(pairwise_distances[:, c_idx])
            distance = pairwise_distances[previous_c_idx, c_idx]
            if distance <= max_distance:
                if bidirectional:
                    symmetric_c_idx = nmpy.argmin(pairwise_distances[previous_c_idx, :])
                    should_add_segment = symmetric_c_idx == c_idx
                else:
                    should_add_segment = True

                if should_add_segment:
                    output.AddTrackSegment(previous_cells[previous_c_idx], cell, t_idx - 1)

        previous_cells = cells

    return output


def _CellsCentroids(cells: Sequence[cell_t]) -> array_t:
    """"""
    return nmpy.fromiter((_cll.centroid for _cll in cells), dtype=nmpy.float64)
