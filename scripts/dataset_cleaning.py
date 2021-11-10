import os, sys, shutil
import pandas as pd
import xlsxwriter

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

def write_line(worksheet, idx):
    worksheet.write('A%s' % (str(i+2)), ids[i])
    worksheet.write('B%s' % (str(i+2)), start_times[i])
    worksheet.write('C%s' % (str(i+2)), end_times[i])
    worksheet.write('D%s' % (str(i+2)), labels[i])

def get_xlsx(split):
    workbook_label = xlsxwriter.Workbook(f'./labels/{split}_labels.xlsx')
    worksheet_label = workbook_label.add_worksheet()
    workbook_miss = xlsxwriter.Workbook(f'./labels/{split}_missing_files.xlsx')
    worksheet_miss = workbook_miss.add_worksheet()

    for sheet in [worksheet_label, worksheet_miss]:
        sheet.write('A1', 'Ids')
        sheet.write('B1', 'Start')
        sheet.write('C1', 'End')
        sheet.write('D1', 'Classes')

    return worksheet_label, worksheet_miss, workbook_label, workbook_miss


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
    start_times = dataset.iloc[:, 1].tolist()
    end_times = dataset.iloc[:, 2].tolist()
    labels = dataset.iloc[:, 3].tolist()
    existing_files_sheet, missing_files_sheet, book_exist, book_miss = get_xlsx(split)

    if split == 'train':
        for i in range(len(ids)):
            classes = get_class_names(labels[i])
            if classes[0] in trainset_folders:
                file_name = get_file_name(i, classes[0])
                if file_name is not None:
                    file_path = os.path.join('./audioset-train/', classes[0], file_name)
                    new_path = f'./train/{ids[i]}.wav'
                    shutil.copyfile(file_path, new_path)
                    write_line(existing_files_sheet, i)
                    break
                else:
                    # Missing file found
                    write_line(missing_files_sheet, i)
    
    else:
        for i in range(len(ids)):
            file_exist = False
            for file_name in evalset_files:
                if str(i) in file_name:
                    file_path = os.path.join('./audioset-eval', file_name)
                    new_path = f'./eval/{ids[i]}.wav'
                    shutil.copyfile(file_path, new_path)
                    write_line(existing_files_sheet, i)
                    file_exist = True
                    break
            if not file_exist:
                write_line(missing_files_sheet, i)

    book_exist.close()
    book_miss.close()
