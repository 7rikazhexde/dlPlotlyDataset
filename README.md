# dlPlotlyDataset
This application selects [plotly / datasets](https://github.com/plotly/datasets) from the Dropdown component and displays it in the DataTable component.The displayed Dataset (DataFrame object) is saved as a csv file by executing the Button component.

## Demo
![Download_Plotly_Dataset_Demo](https://user-images.githubusercontent.com/33836132/210819145-f8fdcd1a-c971-4ecd-bb8f-e4a5385d38b0.gif)

## Usage
1. Get project
```
% git clone https://github.com/7rikazhexde/dlPlotlyDataset.git
```
2. Setup of virtual environment

Run the poetry command.

```
% poetry install
```
* If the package DL fails after installation, there may be a problem with the development environment.  
* See [Switching between environments](https://python-poetry.org/docs/managing-environments/#switching-between-environments).  
* Please run ```poetry env info``` to check your development environment.  
* If your python version is not 3.10 or higher, please run ```poetry env use python3.10``` to recreate your development environment.  

Or create a virtual environment with venv, pyenv, etc. and run the following command.

```
% pip install -r requirements.txt
```

3. Execute the program in a virtual environment
```
% cd app
% poetry shell
% python dl_plotly_datasets.py
```
4. Application Launch

Please access the URL displayed.

```
Dash is running on http://127.0.0.1:8050/

 * Serving Flask app 'dl_plotly_datasets'
 * Debug mode: on
```

5. CSV Download

* If you want to download the CSV file, you can do so by executing the "CSV Download" button.  
* However, the file name is fixed to ```Data.csv``` due to the specification of ```dash_table.DataTable```.  
* This program uses the ```pyperclip``` module to copy the file name selected by ```Dropdown``` to the clipboard.  
* If you are using a Macintosh, a file save dialog will appear and you can paste the file to save it with the name of the data set.
* If you are using Windows, the file save dialog will not appear, so please change the file name after saving the file.

## Note
* datasets are for csv files created directly under the repository.
* Please understand that files stored in folders are not supported.
* If you get an interpreter error using vscode, open and start dlPlotlyDataset with the folder designation.
* Dataset information may differ from the latest information.   
If the expected dataset does not exist, please add it. See the comments in ```plotly_datasets_info.py``` for details.
* If an error occurs after launching the application and you cannot operate it, check the network settings and reload the browser.
