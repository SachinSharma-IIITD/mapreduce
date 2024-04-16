import pandas as pd
import os
import grpc
from map_reduce_pb2 import *
import map_reduce_pb2_grpc as map_reduce_grpc
from concurrent import futures
import time
from hashport import hashport
import multiprocessing
from mapper import Mapper
from reducer import Reduce


def data_point_format(data):
    data_points = []
    for index, row in data.iterrows():
        data_points.append(data_point(x=row[0], y=row[1]))
    return data_points

print("MASTER IS RUNNING ...")
M = int(input("Number of Mappers (M) : "))
R = int(input("Number of Reducers (R) : "))
Centroids = int(input("Number of Centroids (K) : "))
Iterations = int(input("Number of Iterations : "))

print("------------------------------------")

input_file_path = "Data/Input/points.txt"

# reading the input file 
data = pd.read_csv(input_file_path, header=None)

def map(args):
    port = int(args)
    # print(f"Mapper is running on the port : {port}")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    map_reduce_grpc.add_MapperServicer_to_server(Mapper(),server)
    server.add_insecure_port(f"127.0.0.1:{port}")
    try:
        server.start()
        server.wait_for_termination()
    except Exception as e:
        print(e)
    # print("Mapper Terminated")
    return

def reduce(args):
    port = int(args)
    # print(f"Reducer is running on the port : {port}")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    map_reduce_grpc.add_ReducerServicer_to_server(Reduce(),server)
    server.add_insecure_port(f"127.0.0.1:{port}")
    server.start()
    server.wait_for_termination()
    return

class Master():
    def __init__(self,M,R,k,Iterations,data):
        self.M = M
        self.R = R
        self.k = k
        self.Iterations = Iterations
        self.itr = Iterations
        self.data = data

        """randomly selecting k points as centroids"""
        self.centeroids = self.data.sample(n=self.k)
        
        """converting data point to appropriate format"""
        self.data = data_point_format(self.data)
        self.centeroids = data_point_format(self.centeroids)

        self.mapperList = []
        self.mapperPort = []
        self.reducerList = []
        self.reducerPort = []

        #initializing the mappers
        for i in range(self.M):
            
            mapperName = "M"+str(i)
            port = hashport(mapperName)
            self.mapperPort.append(port)
            p = multiprocessing.Process(target = map, args=(str(port),))
            p.start()
            self.mapperList.append(p)
        
        # initializing the reducers
        for i in range(self.R):
            reducer_name = "R"+str(i)
            port = hashport(reducer_name)
            self.reducerPort.append(port)
            p = multiprocessing.Process(target=reduce, args=(port,))
            p.start()
            self.reducerList.append(p)

        self.assign_tasks_to_mappers()
    
    def assign_tasks_to_mappers(self):
        if (self.Iterations==0):
            # writing the final answer in the file
            with open("centroids.txt", "w") as f:
                for index, rows in enumerate(self.centeroids):
                    f.write(f"{index+1},{rows.x},{rows.y}\n")
            print("Training Fininshed")
            return
        for i in range(self.M):
            try:
                start_index = i*(len(self.data)//self.M)
                end_index = (i+1)*(len(self.data)//self.M)
                channel = grpc.insecure_channel(f'127.0.0.1:{self.mapperPort[i]}')
                stub = map_reduce_grpc.MapperStub(channel)
                response = stub.assign_task(master_to_mapper_task_assign(start_index = start_index, end_index= end_index, k_clusters=self.centeroids, data_points=self.data[start_index:end_index], M = self.M, R = self.R, k = self.k, id = i))
                # if (response.success):
                #     # print(f"Task assigned to Mapper {i}")
            except Exception as e:
                print(e)
                print('\Mappemap_reduce_pb2_grpc.py map_reduce_pb2.py map_reduce_pb2.pyir is not working offline\n')
        
        self.assign_task_to_reducer()
    
    def assign_task_to_reducer(self):
        for i in range(self.R):
            try:
                channel = grpc.insecure_channel(f'127.0.0.1:{self.reducerPort[i]}')
                stub = map_reduce_grpc.ReducerStub(channel)
                response = stub.reducer_assign_task(master_to_reducer_task_assign(partition_index = i, mapper_port = self.mapperPort, M = self.M, R = self.R, k = self.k, id = i))
                # if (response.success):
                #     print(f"Task assigned to Reducer {i}")
            except Exception as e:
                print(e)
                print('\nReducer is not working offline\n')
        
        for i in range(self.R):
            reducer_data = pd.read_csv(f"Data/Reducers/R{i}.txt", header=None)
            # print(reducer_data)
            for index, rows in reducer_data.iterrows():
                # print(rows)
                # print(rows[0],rows[1],rows[2])
                self.centeroids[int(rows[0]-1)] = data_point(x=rows[1], y=rows[2])
        
        print("------------------------------------")
        print(f"Iteration {self.itr - self.Iterations}: {self.centeroids}")
        print("------------------------------------")
        self.Iterations -= 1
        self.assign_tasks_to_mappers()
        
            



import sys

if __name__=="__main__":
    try:
        Master(M,R,Centroids,Iterations,data)
    except KeyboardInterrupt as e:
        sys.exit(0)


# python3 -m grpc_tools.protoc -I . --python_out=. --pyi_out=. --grpc_python_out=. map_reduce.proto
# sudo apt clean
# sudo apt autoclean
# sudo apt-get clean
# sudo apt-get autoclean