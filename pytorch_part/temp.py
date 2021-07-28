model = 'yolov3_416/yolov3.weights'
config_file = 'yolov3_416/yolov3.cfg'
class_labels = 'yolov3_416coco.names'
#confThreshold = 0.5
nmsThreshold = 0.4

config = []
element_dict = {}
final_list = []
with open(config_file, 'r') as file:
    config = file.read().split('\n')
config = [line for line in config if len(line)>0 and line[0] != '#']
config = [line.strip() for line in config]
for line in config:
    if line[0] == '[':
        if len(element_dict) != 0:
            final_list.append(element_dict)
            element_dict = {}
        element_dict['type'] = ''.join([i for i in line if i != '[' and i != ']'])
    else:
        val = line.split('=')
        element_dict[val[0].rstrip()] = val[1].lstrip()
        
final_list.append(element_dict)

print(final_list[0])
'''
        element_dict['type'] = line.strip('[]')
        final_list.append(element_dict)
        print(line)
'''