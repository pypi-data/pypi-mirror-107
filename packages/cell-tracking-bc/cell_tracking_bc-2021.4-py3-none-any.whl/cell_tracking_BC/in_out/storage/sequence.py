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

from pathlib import Path as path_t

import cell_tracking_BC.in_out.storage.frame as frame
import numpy as nmpy
# import csv
# import os


array_t = nmpy.ndarray


# TODO: check the output format of the different functions. In particular, do they all output the time dimension as the
# last one?
# TODO: Probably add (generic) parameters to specify eventual required hints for reading function such as number of
# channels...


def SequenceByITK(
    path: path_t,
) -> array_t:
    """"""
    return frame.FrameByITK(path)


def SequenceByIMAGEIO(
    path: path_t,
) -> array_t:
    """"""
    return frame.FrameFromIMAGEIO(path)


# def WriteCellSignalEvolution(self, signal_list,file,channel,type_,idx) :
#
#
#     # save features in csv file
#
#     if not os.path.exists("output-SKIP/"+str(file)+"/signal/total_intencity/"+str(type_)+"/"+str(channel)):
#         os.makedirs("output-SKIP/"+str(file)+"/signal/total_intencity/"+str(type_)+"/"+str(channel))
#
#     fname= "output-SKIP/"+str(file)+"/signal/total_intencity/"+str(type_)+"/"+str(channel)+"/Track_Signal_"+str(idx+1)+".csv"
#
#
#     np_.savetxt(fname, signal_list, delimiter=",", fmt='%s')
#
#
# def WriteFeatureEvolution(self, features_dict,file,type_, to_frame):
#
#
#     header1=["time_points", "uid", "position_X", "position_Y","area", "shift", "edge", "convex_area",
#             "maj_axis_len","min_axis_len","perimeter" ]
#
#     header2= ["time_points", "uid", "position_X", "position_Y","area"]
#
#     for type_, features in features_dict.items():
#
#         if not os.path.exists("output-SKIP/"+str(file)+"/features/"+str(type_)):
#             os.makedirs("output-SKIP/"+str(file)+"/features/"+str(type_))
#
#         for feature_name, feature_lists in features.items():
#
#
#
#             for cell_idx, list_values in enumerate(feature_lists):
#
#                 len_list= len(list_values)
#                 fname= "output-SKIP/"+str(file)+"/features/"+str(type_)+"/Cell_"+str(cell_idx+1)+".csv"
#
#                 with open(fname,"w", newline='') as f :
#                    if type_ == "cell":
#                        writer = csv.DictWriter(f, fieldnames=header1)
#                        writer.writeheader()
#
#                    else:
#                        writer = csv.DictWriter(f, fieldnames=header2)
#                        writer.writeheader()
#
#                    if len_list>1 :
#
#                        for frame in range(0,len_list)  :
#                            if frame <= to_frame:  # solution provisoire il faut revoir la seg et le tracking
#                                if type_ == "cell":
#                                     if frame < len(list_values):
#
#                                         line={"time_points":features["time_points"][cell_idx][frame], "uid":features["uid"][cell_idx][frame],
#                                                "position_X":features["position"][cell_idx][frame][0],
#                                                "position_Y":features["position"][cell_idx][frame][1],"area":features["area"][cell_idx][frame],
#                                                "shift":features["shift"][cell_idx][frame], "edge":features["edge"][cell_idx][frame],
#                                                "convex_area":features["convex_area"][cell_idx][frame],
#                                                "maj_axis_len":features["major_axis_length"][cell_idx][frame],
#                                                "min_axis_len":features["minor_axis_length"][cell_idx][frame],
#                                                "perimeter":features["perimeter"][cell_idx][frame]}
#
#                                         writer.writerow(line)
#
#                                else:
#                                     if frame < len(list_values):
#                                         line={"time_points":features["time_points"][cell_idx][frame], "uid":features["uid"][cell_idx][frame],
#                                                "position_X":features["position"][cell_idx][frame][0],
#                                                "position_Y":features["position"][cell_idx][frame][1],"area":features["area"][cell_idx][frame]}
#
#
#                                         writer.writerow(line)
