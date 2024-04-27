

import subprocess
import re
import time


file_name = "World_cup.csv"
ip = "4.156.73.167"
#ip = "4.236.248.71"
port = "4200"



def get_frontend_pods():
    command = "kubectl get pods | grep frontend | awk '{print $1}'"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    pod_names = result.stdout.strip().splitlines()
    print(pod_names)
    total_cpu_cores = 0

    for pod_name in pod_names:
        command = f"kubectl top pod {pod_name} | grep {pod_name} | awk '{{print $2}}'"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        cpu_cores = result.stdout.strip().replace('m', '')

        if cpu_cores.isdigit():
            total_cpu_cores += int(cpu_cores)

    if pod_names:
        average_cpu_cores = total_cpu_cores / len(pod_names)
        print(f"Average CPU cores used by frontend pods: {average_cpu_cores}")
        return average_cpu_cores , len(pod_names) 
    
    else:
        print("No frontend pods found.")




# get all frontend pods and their average cpu cores and number of pods

# def get_frontend_pods():
#     pody = []
#     command = "kubectl get pods | grep frontend | awk '{print $1}'"
#     result = subprocess.run(command, shell=True, capture_output=True, text=True)
#     pody.append(result.stdout.splitlines())
#     print(result.stdout.splitlines())
#     sum = 0
#     for i in pody:
#         command = f"kubectl top pod {i} | grep {i} | awk '{{print $2}}'"
#         result = subprocess.run(command, shell=True, capture_output=True, text=True)
#         cpu_cores = result.stdout.strip().replace('m', '')
#         sum = sum + int(cpu_cores)
#     #sum = sum / pody.length()
#     print(sum)
    # return result.stdout.splitlines()
        
    # command = f"kubectl top pod {pod.strip()} | grep {pod.strip()} | awk '{{print $2}}'"
            # result = subprocess.run(command, shell=True, capture_output=True, text=True)
            # cpu_cores = result.stdout.strip().replace('m', '')
            



# Read the file
data = []
with open(file_name, 'r') as file:
    for line in file:
        # Strip newline and whitespace then append
        rate = line.strip()
        if rate.isdigit():  # Ensure the line is a digit (simple validation)
            data.append(rate)
i=1


# Open the file containing the pod names
with open('pods_output.txt') as pods:
    pod_names = [pod.strip() for pod in pods.readlines()]

# File to store the CPU Utilization
output_file = 'CPU_Utilization_Output.csv'

# Write header to the CSV file
with open(output_file, 'w') as f:
    f.write('Pod,CPU Limit(m),CPU_Cores(m),Cpu Utilization(%),connections,connection_rate,request_rate,request_size,reply_time,cpu_time,net_io\n')

# Loop over each pod name and fetch CPU limits
for pod in pod_names:
    if 'frontend' in pod:
        for rate in data:
            time.sleep(2)
            print(f"Running test with rate: {rate}")
            connections = int(rate) 
            rates = 50 
            rate = str(connections)
            httperf_output_file = f"Frontend-request-{rate}.txt"
            command = f"httperf --server {ip} --port {port} --num-conns {rate} --rate {rates} > {httperf_output_file}"
            subprocess.run(command, shell=True, check=True)
            i = i+1
            

            with open(httperf_output_file, 'r') as file:
                file_content = file.read()

                connection_rate = re.search(r"Connection rate: (\d+\.\d+)", file_content)
                request_rate = re.search(r"Request size \[B\]: (\d+\.\d+|\d+)", file_content)
                request_size = re.search(r"Request rate: (\d+\.\d+|\d+) req/s", file_content)
                reply_time = re.search(r"Reply time \[ms\]: response (\d+\.\d+|\d+)", file_content)
                cpu_time = re.search(r"CPU time.*user (\d+\.\d+)", file_content)
                net_io = re.search(r"Net I/O: (\d+\.\d+)", file_content)

            # Extract values using regex groups if matches found
                connection_rate = connection_rate.group(1) if connection_rate else 'N/A'
                request_rate = request_rate.group(1) if request_rate else 'N/A'
                request_size = request_size.group(1) if request_size else 'N/A'
                reply_time = reply_time.group(1) if reply_time else 'N/A'
                cpu_time = cpu_time.group(1) if cpu_time else 'N/A'
                net_io = net_io.group(1) if net_io else 'N/A'

                print(f"Results for {httperf_output_file}: Connection Rate={connection_rate}, Request Rate={request_rate}, Request Size={request_size}, Reply Time={reply_time}, CPU Time={cpu_time}, Net I/O={net_io}")

                                                        
            cpu_utilization = 0
        # Initial command to fetch CPU limit from the first node
            command = f"kubectl describe node aks-agentpool-41424896-vmss000019   | grep {pod} | awk '{{print $5}}'"
       
            # Run the command and capture the output
            result = subprocess.run(command, shell=True, capture_output=True, text=True)

            # Extract CPU limit from the command output
            cpu_limit = result.stdout.strip().replace('m', '')
            print(cpu_limit)

            # If the CPU limit is not found, fetch it from the other node description
            if not cpu_limit:
                command = f"kubectl describe node aks-agentpool-41424896-vmss00001a | grep {pod} | awk '{{print $5}}'"
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
                cpu_limit = result.stdout.strip().replace('m', '')

            average_cpu_cores,total_pods = get_frontend_pods()

            # Get the CPU Cores
            # command = f"kubectl top pod {pod.strip()} | grep {pod.strip()} | awk '{{print $2}}'"
            # result = subprocess.run(command, shell=True, capture_output=True, text=True)
            # cpu_cores = result.stdout.strip().replace('m', '')
            

            # # Calculate the CPU Utilization if valid cpu_limit and cpu_cores are found
            if cpu_limit.isdigit() and int(cpu_limit) != 0:
               cpu_utilization = (float(average_cpu_cores) / float(cpu_limit)) * 100
               cpu_utilization = round(cpu_utilization, 4)
            
            # # Append the pod name, its CPU limit, CPU cores, and CPU utilization to the CSV file
            with open(output_file, 'a') as f:
                 f.write(f"{total_pods},{cpu_limit if cpu_limit.isdigit() else 'N/A'},{average_cpu_cores },{cpu_utilization},{rate},{connection_rate},{request_rate},{request_size},{reply_time},{cpu_time},{net_io}\n")

       