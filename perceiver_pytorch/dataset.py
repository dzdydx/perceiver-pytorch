import soundfile
import os
import pandas as pd
from torch.utils.data import Dataset

class Audioset(Dataset):
    def __init__(self, wav_dir, annotations_file, transform=None, target_transform=None):
        self.wav_dir = wav_dir
        self.wav_labels = pd.read_csv(annotations_file)
        self.transform = transform
        self.target_transform = target_transform
        # TODO
        # wav_labels[idx] = ['id.wav', start_time, end_time, 'class_1, ...']
        
        # wav_labels = []
        # for wav in os.listdir(wav_dir):
        #     # file_name = snipped{id}_{start_time}_{end_time}_labels_{class1}-{class2}.wav
        #     file = file_name.split('_')
        #     file[4] = file[4].split('-')
        #     wav_labels.append(file)
        # self.wav_labels = wav_labels 

    def __len__(self):
        return len(self.wav_labels)

    def __getitem__(self, idx):
        wav_path = os.path.join(self.wav_dir, self.wav_labels.iloc[idx, 0])
        wav = soundfile.SoundFile(str(wav_path))
        label = self.wav_labels.iloc[idx, 1]
        if self.transform:
            wav = self.transform(image)
        if self.target_transform:
            label = self.target_transform(label)
        sample = {"wav": wav, "label": label}    

        return sample