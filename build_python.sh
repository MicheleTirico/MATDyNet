## compile python
pip uninstall matdynet
rm -r /home/mtirico/project/matdynet/build/lib/*
python setup.py pytest
python setup.py bdist_wheel
pip install /home/mtirico/project/matdynet/dist/matdynet-0.2.0-py3-none-any.whl

