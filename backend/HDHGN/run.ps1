# .venv\Scripts\activate
# python utilities\prepare_source_files.py

python utilities\clear_train_directories.py
python ProcessData.py -p  # only python files  
python vocab.py -p
Set-location trains
python trainHDHGN.py
# python trainHDHGN_c.py
Set-location ..