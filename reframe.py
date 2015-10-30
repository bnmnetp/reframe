import pandas as pd
import warnings
warnings.filterwarnings('ignore')

class Relation(pd.DataFrame):
    """Create a Relation from a csv file of data for use with relational operators

    This module is designed for educational purposes, specifically teaching and experimenting
    with relational algebra.  To that end, you can create a relation from a file of data typically
    a csv file, although you can also specify a separator, for example a vertical bar may be
    better in some cases.

    This module is built on top of the pandas system in in many cases is just a thin shell.

    - **parameters**::

    :param filepath: a string specifying a path to a csv file, OR a Pandas DataFrame to convert to a Relation
    :param sep: specify a separator for the data file.  default is ``|``



    """
    def __init__(self, filepath=None, sep='|'):
        if type(filepath) == str:
            super().__init__(pd.read_csv(filepath,sep=sep))
        elif type(filepath) == pd.DataFrame:
            super().__init__(filepath)
        else:
            print('help')
            
    def project(self, cols):
        """returns a new Relation with only the specified columns

        :param cols: a list of columns to project
        :return: a Relation with duplicate rows dropped

        :Example:

        >>> from reframe import Relation
        >>> country = Relation('country.csv')
        >>> country.project(['region','continent','name']).head(10)
                              region      continent                  name
        0  Southern and Central Asia           Asia           Afghanistan
        1             Western Europe         Europe           Netherlands
        2                  Caribbean  North America  Netherlands Antilles
        3            Southern Europe         Europe               Albania
        4            Northern Africa         Africa               Algeria
        5                  Polynesia        Oceania        American Samoa
        6            Southern Europe         Europe               Andorra
        7             Central Africa         Africa                Angola
        8                  Caribbean  North America              Anguilla
        9                  Caribbean  North America   Antigua and Barbuda
        >>>

        .. note:: Relations have no duplicate rows, so projecting a single column creates a relation with all of the distinct values for that column
        """
        if type(cols) != list:
            raise ValueError("You must provide the attributes to project inside square brackets []")
        return Relation(self[cols].drop_duplicates())
    
    def query(self, q):
        """return a new relation with tuples matching the query condition

        :param q:  a query string
        :return: a Relation

        :Example:

        >>> from reframe import Relation
        >>> country = Relation('country.csv')
        >>> country.query('continent == "Antarctica"').project(['code','name'])
            code                                          name
        232  ATA                                    Antarctica
        233  BVT                                 Bouvet Island
        235  SGS  South Georgia and the South Sandwich Islands
        236  HMD             Heard Island and McDonald Islands
        237  ATF                   French Southern territories
        >>>

        """
        return Relation(super().query(q).drop_duplicates())

    def sort(self, *args):
        return Relation(super().sort(*args))

    def intersect(self, other):
        if sorted(self.columns) != sorted(other.columns):
            raise ValueError("Relations must be Union compatible")
        else:
            print(self.columns)
            return Relation(pd.merge(self,other,how='inner',on=list(self.columns)))

    def rename(self,old,new):
        return Relation(super().rename(columns={old:new}))

    def cartesian_product(self,other):
        self['__cartkey__'] = 1
        other['__cartkey__'] = 1
        res = pd.merge(self,other,on='__cartkey__')
        self.drop('__cartkey__',axis=1,inplace=True)
        other.drop('__cartkey__',axis=1,inplace=True)
        res.drop('__cartkey__',axis=1,inplace=True)
        return Relation(res.drop_duplicates())

    def groupby(self,cols):
        res = super().groupby(cols)
        return GroupWrap(res,cols)


class GroupWrap(pd.core.groupby.DataFrameGroupBy):
    """Wrapper for a DataFrameGroupBy object -- invisible to end user
    """
    def __init__(self, gbo, cols):
        self.gbo = gbo
        self.gb_cols = cols

    def filteragg(self, res, col):
        res = res.reset_index()
        cl = []
        if type(self.gb_cols) == list:
            cl = self.gb_cols
        else:
            cl.append(self.gb_cols)
        cl.append(col)
        res = res[cl].drop_duplicates()
        return res

    def count(self, col):
        """
        Count the number of occurrences of a value in the column for a group.

        :param col:
        :return:  A Relation with the groupby column(s) and count for a single column

        :Example:

        >>> from reframe import Relation
        >>> country = Relation('country.csv')
        >>> country.groupby(['continent']).count('name')

               continent  count_name
        0         Africa          58
        1     Antarctica           5
        2           Asia          51
        3         Europe          46
        5        Oceania          28
        6  South America          14

        """
        res = self.gbo.count()
        return Relation(self.filteragg(res, col).rename(columns={col:"count_"+col}))


    def mean(self, col):
        res = self.gbo.mean()
        return Relation(self.filteragg(res, col))

    def min(self, col):
        res = self.gbo.min()
        return Relation(self.filteragg(res, col))

    def max(self, col):
        res = self.gbo.max()
        return Relation(self.filteragg(res, col))

    def sum(self, col):
        res = self.gbo.sum()
        return Relation(self.filteragg(res, col))

    def median(self, col):
        res = self.gbo.median()
        return Relation(res.filteragg(res, col))

if __name__ == '__main__':
    # country = Relation('/Users/millbr02/Classes/DB/Notebooks/country.csv')
    # print(country.head())
    # print(country.project(['code','name','indepyear']).head())
    # print(country.sort(['indepyear']).query('indepyear < 1200').project(['name','indepyear']))
    # print(country.project(['name','indepyear']).intersect(country.query('indepyear < 1200').project(['name','indepyear'])))
    # print(country.project(['name']).rename('name','countryname'))
    # print(country.groupby(['continent']).count('name'))
    # x = country.query('continent == "Antarctica"').project(['code','name'])
    # y = country.query('continent == "Antarctica"').project(['code','name'])
    # print(x.cartesian_product(y))
    # print(country.groupby('continent').count('name'))
    # print(country.groupby('region').max('population'))
    import doctest
    doctest.testmod()