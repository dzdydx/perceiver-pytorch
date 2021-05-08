import os, sys, shutil
import pandas as pd

def get_class_names(label):
    clables = []
    label = label.strip('"').split(',')
    try:
        for i in range(len(label)):
            clables.append(class_map[label[i]])
    except:
        print(label)
        sys.exit()

    return clables

def get_file_name(index, class_name):
    files = os.listdir('./audioset-train/' + class_name)
    for name in files:
        if str(index) in name:
            return name
    
    return None


os.chdir('../dataset')
trainset_folders = os.listdir('./audioset-train')
evalset_files = os.listdir('./audioset-eval')

class_map = pd.read_excel('class-map.xlsx')
class_numbers = class_map.iloc[:, 0].tolist()
class_ids = class_map.iloc[:, 1].tolist()
class_labels = class_map.iloc[:, 2].tolist()

class_map = {}

for i in range(len(class_labels)):
    class_labels[i] = class_labels[i].replace(' ', '')
    class_map[class_ids[i]] = class_labels[i]

for split in ['train', 'eval']:
    dataset = pd.read_excel(split + '-labels.xlsx')
    ids = dataset.iloc[:, 0].tolist()
    # start_times = dataset.iloc[:, 1].tolist()
    # end_times = dataset.iloc[:, 2].tolist()
    labels = dataset.iloc[:, 3].tolist()

    if split == 'train':
        for i in range(len(ids)):
            classes = get_class_names(labels[i])
            for j in classes:
                if j in trainset_folders:
                    file_name = get_file_name(i, j)
                    if file_name is not None:
                        file_path = os.path.join('./audioset-train/', j, file_name)
                        new_path = f'./train/{ids[i]}.wav'
                        shutil.copyfile(file_path, new_path)
                        break
                else:
                    print("class not in folders.")
    
    else:
        for i in range(len(ids)):
            for file_name in evalset_files:
                if str(i) in file_name:
                    file_path = os.path.join('./audioset-eval', file_name)
                    new_path = f'./eval/{ids[i]}.wav'
                    shutil.copyfile(file_path, new_path)
            

        


            





