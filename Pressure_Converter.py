import CoolProp.CoolProp as CP 
import pandas as pd
import os
from math import fsum

class Pressure_Converter():
    '''Initialize class with `verbose=True` for helpful progress logs and a printed summary.
    Call the `.convert` method to convert pressure csv to temp/inrange csv.\n'''

    def __init__(self, verbose = False):
        self.verbose = verbose
        if verbose: 
            print(self.__doc__)
            print('PressureConverter initialized.')

    def _import_csv(self, input):
        return pd.read_csv(input, header=0)

    def _psi_to_fahr(self, psi):
        psi    = max(-13.7, psi)
        pa     = (psi + 14.7) / 0.000145037737730
        temp_k = CP.PropsSI("T", "P", pa, "Q", 1, "Ammonia")
        temp_f = 9 / 5 * (temp_k - 273.15) + 32
        return temp_f

    def _process_input(self, df_in):
        df_out            = df_in.copy().rename(columns={"Time":"t"})
        df_out['tmp']     = df_out['Pressure'].apply(lambda x: self._psi_to_fahr(x))
        df_out['inrange'] = None
        df_out['cooling'] = None

        df_out = df_out.drop('Pressure', axis=1)

        for i in range(len(df_out)):
            inrange: bool or None = 'None'
            cooling: bool or None = 'None'

            if i > 0:
                previousTemp: float = df_out.at[i-1,'tmp']
                currentTemp: float  = df_out.at[i, 'tmp']
                cooling: bool       = previousTemp > currentTemp

                if cooling == True:
                    inrange = 10 <= currentTemp < 20
                else:
                    inrange = currentTemp <= 20 or currentTemp > 40

            df_out.at[i,'cooling'] = cooling
            df_out.at[i,'inrange'] = inrange

        if self.verbose:
            print('Successfully processed output dataframe:')
        return df_out
   
    def _save_to_csv(self, df, output):
        df.to_csv(os.getcwd() + "/" + output, index=False)

    def _print_results(self, df):
        cooler_temps: str = ''
        low_temps: str = ''

        for index, row in df.iterrows():
            formatted = f"{row['t']} : {row['tmp']}\n"
            if row['inrange'] == False and row['cooling'] == True:
                cooler_temps += formatted
            if row['tmp'] < 0:
                low_temps += formatted

        avg_temp_str: str = str(df['tmp'].mean())
        avg_temp: str     = avg_temp_str[0:avg_temp_str.find(".") + 3]

        print("## Results ##")
        print("# Nice Cooler Temp Times #")
        print(cooler_temps if cooler_temps else "None")
        print("# Low Temps #")
        print(low_temps if cooler_temps else "None")
        print("Average Temp: " + avg_temp)

    def convert(self, input, output='output.csv'):
        '''required kwargs:
        input (string): relative path to input csv.
        output (string): relative path where output csv will be saved (default='output.csv')'''
        try:
            df_in             = self._import_csv(input)
            df_in['Pressure'] = df_in['Pressure'].astype(float)
            if self.verbose: 
                print(f"Successfully imported csv.")
                # print(df_in)
        except Exception as e:
            print(f"Failed to import csv: {e}")
            return

        try:
            df_out = self._process_input(df_in)
        except Exception as e:
            print(f"Failed to process input: {e}")
            return

        try:
            self._save_to_csv(df_out, output)
            if self.verbose: print(f"Successfully saved to: {output}.\n")
        except Exception as e:
            print(f"Writing to CSV failed: {e}")

        if self.verbose:
            self._print_results(df_out)
