

import pandas as pd
import os
import sys
import grpc
from map_reduce_pb2 import *
import map_reduce_pb2_grpc as map_reduce_grpc
from concurrent import futures
import time
from grpc._channel import _InactiveRpcError
import ast

def data_point_format(data):
    data_points = []
    for index, row in data.iterrows():
        data_points.append(data_point(x=row[0], y=row[1]))
    return data_points

def custom_sort_cond(data_point):
    return data_point.key
class Reduce(map_reduce_grpc.ReducerServicer):
    def __init__(self):
        self.fetched_data = []

    def reducer_assign_task(self, request, context):
        self._id  = request.id
        self.partition_index = request.partition_index
        self.M = request.M
        self.R = request.R
        self.k = request.k
        self.mapper_port = request.mapper_port

        # doing fetching data from the mappers (shuffle)
        for i in range(len(self.mapper_port)):
            self.fetch(self.mapper_port[i])
        
        # sorting the fetched data
        # print(self.fetched_data)
        self.fetched_data = sorted(self.fetched_data,key = custom_sort_cond)
        # print(self.fetched_data)
        # calling the reduce
        self.reduce()

        return master_to_reducer_task_assign_response(success=True)
    
    def fetch(self,port):
        channel = grpc.insecure_channel('localhost:'+str(port))
        stub = map_reduce_grpc.MapperStub(channel)
        response = stub.give_partition_data(master_to_reducer_task_assign(partition_index=self.partition_index))
        
        if (response.success):
            self.fetched_data += response.data_points
            # print(f"Data fetched from Mapper {port}")

    def reduce(self):
        # now we have the data in self.fetched_data
        # we will now reduce it
        length = len(self.fetched_data)
        if (length == 0):
            return 
        with open("Data/Reducers/R"+str(self._id)+".txt", "w") as f:
            pass
        idx = 0
        cnt = 0
        point = data_point(x=0, y=0)
        # idx = 1
        # k = self.fetched_data[0].key
        # point = data_point(x=self.fetched_data[0].value.x, y=self.fetched_data[0].value.y)
        # cnt = self.fetched_data[0].count
        while(idx < length):
            k = self.fetched_data[idx].key
            point.x = self.fetched_data[idx].value.x
            point.y = self.fetched_data[idx].value.y
            idx += 1
            cnt = self.fetched_data[idx].count
            if (idx == length):
                break
            while(self.fetched_data[idx].key == k):
                point.x += self.fetched_data[idx].value.x
                point.y += self.fetched_data[idx].value.y
                cnt += self.fetched_data[idx].count
                k = self.fetched_data[idx].key
                idx += 1
                if (idx == length):
                    break
            
            with open("Data/Reducers/R"+str(self._id)+".txt", "a") as f:
                f.write(str(k) + "," + str(point.x/cnt) + "," + str(point.y/cnt) + "\n")
