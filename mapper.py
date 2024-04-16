
import pandas as pd
import os
import sys
import grpc
from map_reduce_pb2 import *
import map_reduce_pb2_grpc as map_reduce_grpc
from concurrent import futures
import time
# PORT = int(sys.argv[1])
END_SERVER = False
def data_point_format(data):
    data_points = []
    for index, row in data.iterrows():
        data_points.append(data_point(x=row[0], y=row[1]))
    return data_points
def convert_to_mapper_to_reducer_data_point(data):
    data_points = []
    for index, row in data.iterrows():
        data_points.append(mapper_to_reducer_data_point(key = row[0], value = data_point(x=row[1], y=row[2]), count=row[3]))
    return data_points
class Mapper(map_reduce_grpc.MapperServicer):
    def __init__(self):
        pass

    def assign_task(self, request, context):
        self.start = request.start_index
        self.end = request.end_index
        self.k_clusters = request.k_clusters
        self.data_points = request.data_points
        self._id = request.id
        self.M = request.M
        self.R = request.R
        self.k = request.k
        

        # now creating corresponding directory for this mapper
        try:
            os.mkdir(f"Data/Mappers/M{self._id}")
        except FileExistsError:
            pass    

        for i in range(self.R):
            with open(f"Data/Mappers/M{self._id}/Partition_{i}.txt", "w") as f:
                pass

        self.map(self.data_points, self.k_clusters)
        

        # creating R partition files
        # for i in range(self.R):
        #     with open(f"Data/Mappers/M{self._id}/Partition_{i}.txt", "w") as f:
        #         pass

        # self.map(self.data_points, self.k_clusters)

        return master_to_mapper_task_assign_response(success=True)
    
    def euclidean_distance(self, data_point, k_cluster):
        return ((data_point.x - k_cluster.x) ** 2 + (data_point.y - k_cluster.y) ** 2) ** 0.5
    
    def map(self, data_points, k_clusters):
        for i in range(len(data_points)):
            min_dist = float('inf')
            cluster = None
            for j in range(len(k_clusters)):
                dist = self.euclidean_distance(data_points[i], k_clusters[j])
                if dist < min_dist:
                    min_dist = dist
                    cluster = j
            self.emit(cluster, data_points[i])

    def partition_function(self,key):
        return key % self.R
    
    def emit(self, cluster, data_point):
        partition = self.partition_function(cluster)
        with open(f"Data/Mappers/M{self._id}/Partition_{partition}.txt", "a") as f:
            f.write(f"{cluster+1},{data_point.x}, {data_point.y},{1}\n")

    def give_partition_data(self,request,context):
        partition_index = request.partition_index
        data_ = pd.read_csv(f"Data/Mappers/M{self._id}/Partition_{partition_index}.txt", header=None)
        data_points = convert_to_mapper_to_reducer_data_point(data_)
        return reducer_to_mapper_file_read_response(data_points = data_points, success=True)
