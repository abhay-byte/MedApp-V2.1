import pandas as pd

read_file = pd.read_excel (r'D:\Projects\Medical diagnosis\Medical_Diagnostic_App\Symptoms X Diseases.xlsx')
read_file.to_csv (r'D:\Projects\Medical diagnosis\Medical_Diagnostic_App\Symptoms X Diseases.csv', index = None, header=True)
