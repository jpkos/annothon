# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 07:28:08 2022

@author: jankos
"""

from annothon.annotations.bboxes import BBox
import glob
import os

class YOLOfolder(list):
    def __init__(self, path):
        self.path = path
        self.file_paths = glob.glob(os.path.join(path, '*.txt'))
        self.files = self._read(path)

    def count_labels(self):
        count_dict = {}
        for file in self.files:
            for label in file.lbls:
                if label in count_dict.keys():
                    count_dict[label] += 1
                else:
                    count_dict[label] = 1
        return dict(sorted(count_dict.items()))
    
    def __repr__(self):
        return (f'Folder containing yolo-formatted files at {self.path}\n'
                f'Contains {len(self.files)} files')
    
    def __iter__(self):
        for file in self.files:
            yield file
            
    def __getitem__(self, idx):
        return self.files[idx]
    
    def __len__(self):
        return len(self.files)
    
    def _read(self, path):
        file_paths = [YOLOfile(file_path) for file_path
                      in self.file_paths]
        return file_paths
        
class YOLOfile(list):
    def __init__(self, path):
        self.path = path
        self.bboxes = self._read_txt(path)
        self.lbls = [box.lbl for box in self.bboxes]
        
    def contains_label(self, ids, return_list = False):
        ids = [ids] if (isinstance(ids, int)) else ids
        if return_list:
            return [id in self.lbls for id in ids]
        else:
            return any([id in self.lbls for id in ids])
        
    def change_label(self, old, new):
        for bbox in self.bboxes:
            if bbox.lbl == old:
                bbox.lbl = new
                
    def _read_txt(self, path):
        with open(path, 'r') as f:
            flines = [x.split(' ') for x in f.readlines()]
        flines = [f for f in flines if len(f)>=4]
        flines = [list(map(float, x)) for x in flines]
        bboxes = [BBox(*fline) for fline in flines]
        return bboxes
                
    def __iter__(self):
        for bbox in self.bboxes:
            yield bbox
        
    def __getitem__(self, idx):
        return self.bboxes[idx]
    
    def __len__(self):
        return len(self.bboxes)
    
    def __repr__(self):
        return f'File {self.path}\nContains boxes\n{self.bboxes}'
                
#%%
yolo_files = YOLOfolder(r"C:\Users\jankos\tyokansio\projektit\UEF-KUH-HUS\AhIb-annotations\UEFKUHHUS_1_split\labels\validate")

# for i, file in enumerate(yolo_files):
#     print(file.contains_label(1))
# with open('test_data/631.txt', 'r') as f:
#     flines = [x.split(' ') for x in f.readlines()]
#     flines = [list(map(float, x)) for x in flines]

# b = BBox(*flines[0])