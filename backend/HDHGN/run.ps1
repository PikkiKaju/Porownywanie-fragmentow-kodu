.venv\Scripts\activate
python utilities\prepare_source_files.py

python utilities\clear_train_directories.py
python ProcessData.py -p -c
python vocab.py -p -c
Set-location trains
python trainHDHGN.py
python trainHDHGN_c.py
Set-location ..
