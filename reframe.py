import pandas as pd
import warnings
warnings.filterwarnings('ignore')

class Relation(pd.DataFrame):
    def __init__(self, filepath=None, sep='|'):
        if type(filepath) == str:
            super().__init__(pd.read_csv(filepath,sep=sep))
        elif type(filepath) == pd.DataFrame:
            super().__init__(filepath)
        else:
            print('help')
            
    def project(self, cols):
        if type(cols) != list:
            raise ValueError("You must provide the attributes to project inside square brackets []")
        return Relation(self[cols].drop_duplicates())
    
    def query(self, q):
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
    def __init__(self, gbo, cols):
        self.gbo = gbo
        self.gb_cols = cols

    def filteragg(self,res, col):
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
        res = self.gbo.count()
        return Relation(self.filteragg(res, col))

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
    country = Relation('/Users/millbr02/Classes/DB/Notebooks/country.csv')
    print(country.head())
    print(country.project(['code','name','indepyear']).head())
    print(country.sort(['indepyear']).query('indepyear < 1200').project(['name','indepyear']))
    print(country.project(['name','indepyear']).intersect(country.query('indepyear < 1200').project(['name','indepyear'])))
    print(country.project(['name']).rename('name','countryname'))
    print(country.groupby(['continent']).count('name'))
    x = country.query('continent == "Antarctica"').project(['code','name'])
    y = country.query('continent == "Antarctica"').project(['code','name'])
    print(x.cartesian_product(y))
    print(country.groupby('continent').count('name'))
    print(country.groupby('region').max('population'))