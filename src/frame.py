"""
DataFrame
---------
An efficient 2D container for potentially mixed-type series of data.
"""
import csv
from typing import OrderedDict
from unidecode import unidecode
from collections import defaultdict
from itertools import zip_longest
import copy

class DataFrame:
    """
    Two-dimensional, size-mutable, potentially heterogeneous tabular data.
    Can be thought of as a dict-like container to store data from csv. 

    Parameters
    ----------
    data : None, Str, or OrderedDict.
        Dict can contain Series, arrays, constants, dataclass or list-like objects. If data is 
        None it initializes an empty DataFrame object. Elif data is type of str (path to csv)
        it parses csv file and stores data in dict-like structure. Finally if data is OrderedDict
        it clones DataFrame object using the deepcopy method. 
    
    kwargs: {
        columns: a list containing the header columns of the csv file to read.
        dtypes: a list containing the data types of each columns. 
    }

    Notes
    ------
    self.print is used to print the dict container to a table like format for easy access from user.

    Examples
    ----------
    >>> customer_df = pd.DataFrame(
                'input/CUSTOMER.csv', 
                columns = [
                            "CUSTOMER_CODE",
                            "FIRSTNAME",
                            "LASTNAME"
                        ],
                dtypes = ["CHAR","CHAR","FLOAT", "DATE" ]
            )
    defaultdict(None, {'CUSTOMER_CODE': ['CUST0000010231', 'CUST0000010235'], 'FIRSTNAME': ['Maria', 'George'], 'LASTNAME': ['Alba', 'Lucas']})

    ...
    >>> customer_df.print()

    CUSTOMER_CODE FIRSTNAME LASTNAME
    CUST0000010231 Maria Alba
    CUST0000010235 George Lucas
    """

    def __init__(self, data = None, **kwargs) -> None:
        
        if data is None: 
            self._data = defaultdict()
        elif isinstance(data, str):
            self._data = self._to_dataframe(data, kwargs)
        elif isinstance(data, OrderedDict):
            self._data = copy.deepcopy(data)

        

    def _to_dataframe(self, path, kwargs):
        """
        Takes as input path and keyword arguments as explained before.
        Read csv file from path and stores data to a dict. This dict is 
        stored to self._data and represents a 2D data-structure.

        Returns
        -------
        defaultdict()
        """
        data = defaultdict()
        columns = kwargs['columns']
        dtypes = kwargs['dtypes']

        #initialize a list for each col to store each values
        values = [[] for _ in range(len(columns))]
        
        
        #read csv
        reader = csv.reader(open(path), delimiter = ',', quotechar='"')

        #iterate rows
        for r_idx, row in enumerate(reader):
            if r_idx ==0: continue #skip first line
            #iterete cols 
            for c_idx,col in enumerate(row): 
                col = unidecode(col).replace('"', '')
                values[c_idx].append(col)

        #convert lists to right data type, as specified
        for idx, dtype in enumerate(dtypes):
            if dtype == 'INTERGER':
                values[idx] = list(map(int, values[idx]))
            elif dtype == 'FLOAT':
                values[idx] = list(map(float, values[idx]))

        #create dict to store data.
        for key, value in zip(columns, values):
            data.update({key:value})
        
        return data

    def to_csv(self, path=None):
        """
        Function that write self._data dictionary to a csv file specified
        with path input variable.

        Returns
        -------
        None
        """

        if path is None:
            raise ValueError("Path cannot be None.")
        
        rows = []
        cols = list(self._data.keys())

        for key in self._data.keys():
            rows.append(self._data[key])
        export_data = zip_longest(*rows, fillvalue = '')

        with open(path, 'w', encoding="ISO-8859-1", newline='') as csv_file:
            wr = csv.writer(csv_file)
            wr.writerow(cols)
            wr.writerows(export_data)

        csv_file.close()
    
    def merge(self, df, key_col):
        """
        Merge columns of another DataFrame.
        Merge columns with `df` DataFrame  on a key column, referenced with 'key_col'
        Efficiently stores the merged data to a new dictionary, creates a new DataFrame Object
        from it and returns it.

        Parameters
        ----------
        df: DataFrame to merge self df with
        key_col: key column name to merge on 

        Returns
        ---------
        DataFrame
        """
        keys = self._data.keys()

        #dictionary to store merged data
        new_dict = OrderedDict()
        new_values = [[] for _ in range(len(keys))]
        
            
        for idx, value in enumerate(self._data[key_col]):
            if value in df[key_col]:
                for j,key in enumerate(self._data.keys()):
                    new_values[j].append(self._data[key][idx])
           
        for key, value in zip(keys, new_values):
            new_dict.update({key:value})
        
        new_df = DataFrame(new_dict)
        return new_df

    @property
    def columns(self):
        return list(self._data.keys())

    def __getitem__(self, item):
        if isinstance(item, str):
            return self._data[item]


    def print(self):
        # Print the names of the columns.
        for row in zip(*([key] + (value) for key, value in (self._data.items()))):
            print(*row)

    