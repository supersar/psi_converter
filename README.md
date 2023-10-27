The `PressureConverter` class converts a CSV with PSI readings and exports them into a time-series CSV with temperature records.


## Install

1. Run `pip install -r requirements.txt` 

## Run test

1. Run `pytest`

## Run the script as a standalone

1. Add your CSV to the root directory and rename it `input1.csv`
2. Run `python main.py` 
3. Output file will be saved as `test.csv` in root dir
4. Logging and sorted results will be visible in the terminal


## Usage in an application

Refer to `main.py` as an example. Import the class 

```
from Pressure_Converter import Pressure_Converter
```

Instantiate an instance with the `verbose` kwarg as True (False by default) if you wish the class to log verbose messages with progress.
```
converter = Pressure_Converter(verbose=True)
```
call the `convert` method to process your csv. Customize the filenames via the input & output kwargs.
```
converter.convert(input='input1.csv', output='test.csv')
``````
