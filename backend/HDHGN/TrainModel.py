import sys
import os

sys.path.append(os.path.dirname(__file__))

from utilities.prepare_source_files import prepare_source_files
from utilities.clear_train_directories import clear_train_directories
from ProcessData import ProccesData
from vocab import make_vocab
from trains.trainHDHGN_c import TrainHDHGN_C
from trains.trainHDHGN import TrainHDHGN

from MyDataset import HDHGData
from vocab import Vocab
from utilities import 
from models.HDHGN import HDHGN 


def TrainModel():
    """
    Train the HDHGN model.
    """
    prepare_source_files()
    clear_train_directories()
    ProccesData()
    make_vocab()
    TrainHDHGN_C()
    TrainHDHGN()
    

if __name__ == '__main__':
    TrainModel()
