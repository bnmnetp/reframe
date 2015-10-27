import pandas as pd

class Relation(pd.DataFrame):
    def __init__(self, filepath=None, sep='|'):
        if type(filepath) == str:
            super().__init__(pd.read_csv(filepath,sep=sep))
        elif type(filepath) == pd.DataFrame:
            super().__init__(filepath)
        else:
            print('help')
            
    def project(self, cols):
        return Relation(self[cols].drop_duplicates())
    
    def query(self, q):
        return Relation(super().query(q).drop_duplicates())

    def intersect(self, other):
        if sorted(self.columns) != sorted(other.columns):
            raise ValueError("Relations must be Union compatible")
        else:
            print(self.columns)
            return Relation(pd.merge(self,other,how='inner',on=list(self.columns)))



if __name__ == '__main__':
    country = Relation('/Users/bmiller/Classes/DB/Notebooks/country.csv')
    print(country.head())
    print(country.project(['code','name','indepyear']).head())
    print(country.query('indepyear < 1200').project(['name','indepyear']).sort(['indepyear']))
    print(country.project(['name','indepyear']).intersect(country.query('indepyear < 1200').project(['name','indepyear'])))
