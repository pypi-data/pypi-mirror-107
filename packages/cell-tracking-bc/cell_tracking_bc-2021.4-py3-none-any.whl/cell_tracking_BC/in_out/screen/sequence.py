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

# import os
# import matplotlib.pyplot as pypl
# from mpl_toolkits.mplot3d import Axes3D as axes_t
#
# def CellLabeling(self,channel,singnal,uid,file, features,track_channel):
#
#     """
#     CellLabeling function allows to identify cells in the original image,
#     by labeling them with their cell unique identifier.
#     """
#
#     if self.cell_channel is not None :
#
#         name="segmentation_map"
#
#         if not os.path.exists("output-SKIP/"+str(file)+"/"+name):
#             os.makedirs("output-SKIP/"+str(file)+"/"+name)
#
#
#     #        for idx,frame in enumerate (self.channel_content[channel]):
#     #
#     #            if idx % 10 == 0 :
#     #                pypl.figure(figsize=(30,30))
#     #                pypl.imshow(frame, cmap="gray")
#     #
#     #                for cell in range(0,len(features["nucl"]["uid"])):
#     #
#     #                    if uid=="root_cell_uid": # the cell is labeled with the same uid over the diferent frames
#     #                        if len(features["nucl"]["uid"][cell])>0 and idx < len(features["nucl"]["position"][cell]):
#     #                            pypl.text(features["nucl"]["position"][cell][idx][0],features["nucl"]["position"][cell][idx][1],
#     #                                         str(features["nucl"]["uid"][cell][0]),color="red", fontsize=40)
#     #
#     #                    elif uid=="cell_uid": # the cell is labeled with the specfic frame uid, if the uid isn't available,
#     #                                       # the cell is labeled with "x"
#     #                       if len(features["nucl"]["position"][cell])-1>= idx:
#     #                           pypl.text(features["nucl"]["position"][cell][0][0],features["nucl"]["position"][cell][0][1],
#     #                                     str(features["nucl"]["uid"][cell][idx]),color="red", fontsize=40)
#     #                       else:
#     #
#     #                           pypl.text(features["nucl"]["position"][cell][0][0],features["nucl"]["position"][cell][0][1],
#     #                                 "x" ,color="red", fontsize= 40 )
#
#     #idx=0
#
#     for idx in range (len(self.channel_content[channel])):
#
#         frame= self.channel_content[channel][idx]
#         pypl.figure(figsize=(30,30))
#         pypl.imshow(frame, cmap="gray")
#
#         if track_channel == "nucl" :
#             for cell in range(0,len(features["cell"]["uid"])):
#                 if len(features["cell"]["uid"][cell])>idx :
# #                        pypl.text(features["cell"]["position"][cell][idx][0],features["cell"]["position"][cell][idx][1],
# #                                     str(features["cell"]["uid"][cell][0]),color="red", fontsize=50)
#
#                     pypl.text(features["cell"]["position"][cell][idx][0],features["cell"]["position"][cell][idx][1],
#                                  str(cell),color="red", fontsize=50)
#
#
#
#         elif track_channel == "cell" :
#
#             for cell in range(0,len(features["cell"]["uid"])):
#                 #print(cell)
#                 if len(features["cell"]["uid"][cell])> idx: #0 :
#                     pypl.text(features["cell"]["position"][cell][idx][0],features["cell"]["position"][cell][idx][1],
#                                  str(features["cell"]["uid"][cell][0]),color="red", fontsize=50)
#
#
#         # save figures
#
#         path= "output-SKIP/"+str(file)+"/"+name+"/frame"+str(idx)+".jpg"
#         pypl.savefig(path)
#         pypl.close()
#
#
# def PlotCellFeatureEvolutions(
#     self,
#     cell_list: Sequence,
#     feature: str,
#     file: str,
#     show_figure: bool = True,
# ) -> None:
#
#     """
#     This function plots the cell feature evolutions
#     calculated by the "CellFeatureEvolution" function
#     """
#
#     figure = pypl.figure()
#     axes = figure.gca() # get the current axes
#     axes.set_title(feature) # set a title
#     axes.set_xlabel("time points") # set the x label
#     axes.set_ylabel("feature value") # set the y label
#     plots = []
#     labels = []
#     colors = "bgrcmyk"
#
#
#     for root_cell in cell_list:
#         color_idx = root_cell.uid % colors.__len__()
#         subplot = None
#
#         for piece in self.CellFeatureEvolution(root_cell, feature): # get the feature evolution
#             if not (isinstance(piece[0][1], int) or isinstance(piece[0][1], float)): # if the feature value isn't "int" or "float" type
#                 break
#
#             time_points = []
#             feature_values = []
#             for time_point, feature_value in piece: # get the time point and the feature value
#                 time_points.append(time_point) # save the time point
#                 feature_values.append(feature_value) # save the feature value
#
#             subplot = axes.plot(
#                 time_points, feature_values, colors[color_idx] + "-x"
#             )[0] # plot f(time_points, feature_values)
#
#         if subplot is not None:
#             plots.append(subplot)
#             labels.append(f"root_cell {root_cell.uid}") # get uid labels
#
#     if plots.__len__() > 0: # if "plots" list isn't empty
#         axes.legend(handles=plots, labels=labels, loc='lower right') # place the legend on the axes
#         # save plot
#         pypl.savefig(str(file)+"/plot_features/"+feature)
#     else:
#         pypl.close(figure)
#
#     if show_figure:
#         pypl.show()
#     def Plot(self, file: str, show_figure: bool = True) -> None:
#         """"""
#         figure = pypl.figure()
#         axes = figure.add_subplot(projection=axes_t.name)
#         axes.set_xlabel("row positions")
#         axes.set_ylabel("column positions")
#         axes.set_zlabel("time points")
#         colors = "bgrcmyk"
#
#         for c_idx, component in enumerate(grph.weakly_connected_components(self)):
#             color_idx = c_idx % colors.__len__()
#             for from_cell, to_cell in self.subgraph(component).edges:
#                 time_points = (
#                     from_cell.time_point,
#                     to_cell.time_point,
#                 )
#                 rows = (
#                     from_cell.position[0],
#                     to_cell.position[0],
#                 )
#                 cols = (
#                     from_cell.position[1],
#                     to_cell.position[1],
#                 )
#                 axes.plot3D(rows, cols, time_points, colors[color_idx])
#
#         if show_figure:
#             pypl.show()
#
#         if not os.path.exists("output-SKIP/" + str(file) + "/tracking"):
#             os.makedirs("output-SKIP/" + str(file) + "/tracking")
#
#         pypl.savefig("output-SKIP/" + str(file) + "/tracking/tracks")
#
# def PlotTracks(self, file: str, show_figure: bool = True) -> None:
#     """"""
#     figure = pypl.figure()
#     axes = figure.add_subplot(projection=axes_t.name)
#     axes.set_xlabel("row positions")
#     axes.set_ylabel("column positions")
#     axes.set_zlabel("time points")
#     colors = "bgrcmyk"
#
#     for c_idx, component in enumerate(grph.weakly_connected_components(self)):
#         color_idx = c_idx % colors.__len__()
#         for from_cell, to_cell in self.subgraph(component).edges:
#             time_points = (
#                 from_cell.time_point,
#                 to_cell.time_point,
#             )
#             rows = (
#                 from_cell.position[0],
#                 to_cell.position[0],
#             )
#             cols = (
#                 from_cell.position[1],
#                 to_cell.position[1],
#             )
#             axes.plot3D(rows, cols, time_points, colors[color_idx])
#
#     if show_figure:
#         pypl.show()
#
#     if not os.path.exists("output-SKIP/" + str(file) + "/tracking"):
#         os.makedirs("output-SKIP/" + str(file) + "/tracking")
#
#     pypl.savefig("output-SKIP/" + str(file) + "/tracking/tracks")
