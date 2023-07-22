from concurrent import futures
import sys
import glob


import os
from merkletools import MerkleTools
import hashlib
import json
import random
import os
import time

intermediate_results = {}
# hash_of_all_input_images = {}
image_epoch_num = 0
image_epoch = '0'
proof_dict = {}
tmp_hash = '57fcec903428812fe635fb2ba5d30d3d8752099d51ee68dfeff87d04db3643b5'


# def update_hash_of_all_input_images(user_id,image_file_path):
#     image = Image.open(io.BytesIO(image_data))
#     image_data_hash = hashlib.sha256(image.tobytes()).hexdigest()
#     image_data_hash_str = str(image_data_hash)
#     if user_id not in self.hash_of_all_input_images.keys():
#         self.hash_of_all_input_images[user_id] = {}
    
#     if image_epoch not in self.hash_of_all_input_images[user_id].keys():
#         self.hash_of_all_input_images[user_id][image_epoch] = []
#         self.hash_of_all_input_images[user_id][image_epoch].append(image_data_hash_str)
#     else:
#         self.hash_of_all_input_images[user_id][image_epoch].append(image_data_hash_str)


# user id is just a random id is fine in test
def generate_merkle_tree(user_id,result_file_path):  
    result_file_path = glob.glob(result_file_path)[0] #       
    with open(result_file_path, 'r') as f:
        content = f.read()

    clusters = content.split('\n\n')
    # print("clusters: ", clusters)

    for cluster in clusters:
        results = []
        if cluster != '':
            results.append(cluster.strip())
            # print("results: ", results)
            # change the results list to string
            results = results[0] + tmp_hash
            # print("results of one cluster: ", results)

        else:
            continue
        # global intermediate_results
        if user_id not in intermediate_results.keys():
            intermediate_results[user_id] = {}
        
        if image_epoch_num not in intermediate_results[user_id].keys():
            intermediate_results[user_id][image_epoch_num] = []
            intermediate_results[user_id][image_epoch_num].append(results)
            # print("aaa intermediate_results[user_id][image_epoch_num]: ", intermediate_results[user_id][image_epoch_num])
        else:
            intermediate_results[user_id][image_epoch_num].append(results)
            # print("bbb intermediate_results[user_id][image_epoch_num]: ", intermediate_results[user_id][image_epoch_num])

    # print("intermediate_results init: ", intermediate_results)



            

    def process_object_file(file_path):
        with open(file_path, 'r') as file:
            file_content = file.read()

        # Split the content by lines
        lines = file_content.split('\n')

        # Initialize result variables
        num_objects = 0
        # object_categories = {}
        # object_motions = {}

        # Process each line
        for line in lines:
            # Skip empty lines
            if not line.strip():
                continue

            # Split line by spaces
            values = line.strip().split()
            # print("values[1]: ", values[1])

            # Get the object index, category, and motion
            object_index = int(float(values[1]))
            num_objects = max(num_objects, object_index)

        # Generate the final result string
        result = f"Number of objects: {num_objects}\n\n"
        return result

    final_results = process_object_file(result_file_path)


       
    mt = MerkleTools() # mt = MerkleTools(hash_type="md5")  # default is sha256 
    # global intermediate_results
    intermediate_results[user_id][image_epoch_num].append(final_results)
    # print("intermediate_results before add leaf: ", intermediate_results)
    intermediate_results_tmp = intermediate_results[user_id][image_epoch_num]
    # hash_of_input_image = hash_of_all_input_images[user_id][image_epoch]
    # merkle_tree_leaf_string = [x + y for x, y in zip(intermediate_results_tmp, hash_of_input_image)]

    mt.add_leaf(intermediate_results_tmp, True) # add all the intermediate results as the leaf nodes, True means the leaf nodes will be hashed

    mt.make_tree() # construct the merkle tree
    # print("root:", mt.get_merkle_root()) 

    merkle_tree_root = mt.get_merkle_root() # get the root node of the merkle tree
    return merkle_tree_root,mt

def generate_proof(user_id,sample_rate,image_index_list,mt):
    proof_result = {} # key: index, value: proof
    image_results = {} # key: index, value: image result
    for index in image_index_list:
        proof = mt.get_proof(int(index))
        proof_result[index] = proof
        # print("type of image_epoch_num: ", type(image_epoch_num))
        # print("type of index: ", type(index))

        # global intermediate_results
        # print("type of intermediate_results[user_id]: ", type(intermediate_results[user_id]))
        # print("type of intermediate_results: ", type(intermediate_results))
        # print("intermediate_results: ", intermediate_results)
        # print("index: ", index)
        image_results[index] = intermediate_results[user_id][image_epoch_num][int(index)]

    proof_result_str = json.dumps(proof_result)
    image_result_str = json.dumps(image_results)
    
    return proof_result_str,image_result_str

def verify_proof(proof_str,image_result_str,merkle_tree_root):
    proof = json.loads(proof_str)
    proof_dict[image_epoch] = proof
    image_results = json.loads(image_result_str)
    # verify the proof
    mt = MerkleTools()
    
    def validate_all_proofs(proof, image_results, merkle_tree_root):
        for key, proof_value in proof.items():
            leaf_node_hex = hashlib.sha256(str(image_results[key]).encode('utf-8')).hexdigest()
            root = merkle_tree_root
            if not mt.validate_proof(proof_value, leaf_node_hex, root):
                return False
        return True
    
    if validate_all_proofs(proof, image_results, merkle_tree_root):
        # print("all the proof is valid!")
        return True
    else:
        print("some proof is invalid!")
        #break the program
        # exit()
        return False





# if __name__ == '__main__':
#     result_file_path = os.path.join('./results', image_epoch, '*.txt')
#     sample_rate = 0.1
#     image_index_list = [0,1,2,3,4,5,6,7,8,9] # based on sample rate to generate the image index list
#     user_id = 'localhost:53097'
#     merkle_tree_root,mt = generate_merkle_tree(user_id,result_file_path)
#     proof_result_str,image_result_str = generate_proof(user_id,sample_rate,image_index_list,mt)
#     verify_result = verify_proof(proof_result_str,image_result_str,merkle_tree_root)
#     print("verify_result: ", verify_result)


# def generate_image_index_list(sample_rate):
#     image_index_list = list(range(10))
#     num_samples = int(sample_rate * 10)
#     image_index_list = image_index_list[:num_samples]
#     return image_index_list

def generate_image_index_list(sample_rate):
    image_index_list = list(range(100))
    num_samples = int(sample_rate * 100)
    image_index_list = random.sample(image_index_list, num_samples)
    return image_index_list

def calculate_verify_time(sample_rate):
    result_file_path = os.path.join('./results', image_epoch, '*.txt')
    image_index_list = generate_image_index_list(sample_rate)
    user_id = 'localhost:53097'
    merkle_tree_root, mt = generate_merkle_tree(user_id, result_file_path)
    proof_result_str, image_result_str = generate_proof(user_id, sample_rate, image_index_list, mt)

    start_time = time.time()
    verify_result = verify_proof(proof_result_str, image_result_str, merkle_tree_root)
    end_time = time.time()
    print("verify_result: ", verify_result)

    verify_time = end_time - start_time
    return verify_time

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--sample_rate', type=float, required=True, help='Sample rate')
    args = parser.parse_args()

    sample_rate = args.sample_rate
    image_index_list = generate_image_index_list(sample_rate)
    print("image_index_list: ", image_index_list)
    verify_time = calculate_verify_time(sample_rate)

    result_filename = f"verify_time_{sample_rate}.txt"
    with open(result_filename, 'a') as file:
        # file.write(f"Sample Rate: {sample_rate}, Verify Time: {verify_time}\n")
        file.write(f"{verify_time}\n")

    # print("verify_result: ", verify_result)
