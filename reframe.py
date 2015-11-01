import pandas as pd
import warnings
warnings.filterwarnings('ignore')

__all__ = ['Relation','GroupWrap']

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
        for name in cols:
            if name not in self.columns:
                raise ValueError("'{}' is not a valid attribute name in relation".format(name))
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

    def sort(self, *args, **kwargs):
        """sort the relation on the given columns

        :param cols:  A list of columns to sort on
        :param ascending:  Boolean, ascending=False implies a sort in reverse order

        :Example:

        >>> from reframe import Relation
        >>> country = Relation('country.csv')
        >>> country.sort(['indepyear'], ascending=False).query('indepyear < 1200').project(['name','indepyear'])
                       name  indepyear
        159        Portugal       1143
        29   United Kingdom       1066
        180      San Marino        885
        164          France        843
        170          Sweden        836
        200         Denmark        800
        81            Japan       -660
        48         Ethiopia      -1000
        93            China      -1523

        """

        return Relation(super().sort(*args, **kwargs))

    def intersect(self, other):
        """Create a new relation that is the intersection of the two given relations

        In order to compute the intersection the relations must be union compatible.  That is they must
        have exactly the same columns.  This may require some projecting and renaming.

        :param other:  The relation to compute the intersection with.
        :return:

        :Example:

        >>> from reframe import Relation
        >>> country = Relation('country.csv')
        >>> country.query('continent == "Africa"').project(['name', 'region']).intersect(country.query('region == "Western Africa"').project(['name', 'region']))
                     name          region
        0           Benin  Western Africa
        1    Burkina Faso  Western Africa
        2          Gambia  Western Africa
        3           Ghana  Western Africa
        4          Guinea  Western Africa
        5   Guinea-Bissau  Western Africa
        6      Cape Verde  Western Africa
        7         Liberia  Western Africa
        8            Mali  Western Africa
        9      Mauritania  Western Africa
        10          Niger  Western Africa
        11        Nigeria  Western Africa
        12  Côte d'Ivoire  Western Africa
        13   Saint Helena  Western Africa
        14        Senegal  Western Africa
        15   Sierra Leone  Western Africa
        16           Togo  Western Africa
        >>>
        """
        if sorted(self.columns) != sorted(other.columns):
            raise ValueError("Relations must be Union compatible")
        else:
            return Relation(pd.merge(self,other,how='inner',on=list(self.columns)))

    def njoin(self, other):
        """Create a new relation that is the intersection of the two given relations

        In order to compute the intersection the relations must be union compatible.  That is they must
        have exactly the same columns.  This may require some projecting and renaming.

        :param other:  The relation to compute the intersection with.
        :return:

        :Example:

        >>> from reframe import Relation
        >>> country = Relation('country.csv')
        >>> country.query('continent == "Africa"').project(['name', 'region']).njoin(country.query('region == "Western Africa"').project(['name', 'region']))
                     name          region
        0           Benin  Western Africa
        1    Burkina Faso  Western Africa
        2          Gambia  Western Africa
        3           Ghana  Western Africa
        4          Guinea  Western Africa
        5   Guinea-Bissau  Western Africa
        6      Cape Verde  Western Africa
        7         Liberia  Western Africa
        8            Mali  Western Africa
        9      Mauritania  Western Africa
        10          Niger  Western Africa
        11        Nigeria  Western Africa
        12  Côte d'Ivoire  Western Africa
        13   Saint Helena  Western Africa
        14        Senegal  Western Africa
        15   Sierra Leone  Western Africa
        16           Togo  Western Africa
        >>>
        """
        col_list = [x for x in self.columns if x in other.columns]
        if not col_list:
            raise ValueError("The two relations must have some columns in common")
        return Relation(pd.merge(self,other,how='inner',on=list(col_list)))



    def union(self,other):
        """ Take two Relations with the same columns and put them together top to bottom

        :param other:
        :return:

        :Example:

        >>> from reframe import Relation
        >>> country = Relation('country.csv')
        >>> country.query('region == "Western Africa"').union(country.query('region == "Polynesia"')).project(['name','region'])
                          name          region
        22               Benin  Western Africa
        33        Burkina Faso  Western Africa
        54              Gambia  Western Africa
        56               Ghana  Western Africa
        63              Guinea  Western Africa
        64       Guinea-Bissau  Western Africa
        89          Cape Verde  Western Africa
        112            Liberia  Western Africa
        124               Mali  Western Africa
        129         Mauritania  Western Africa
        144              Niger  Western Africa
        145            Nigeria  Western Africa
        149      Côte d'Ivoire  Western Africa
        171       Saint Helena  Western Africa
        183            Senegal  Western Africa
        185       Sierra Leone  Western Africa
        202               Togo  Western Africa
        5       American Samoa       Polynesia
        37        Cook Islands       Polynesia
        146               Niue       Polynesia
        157           Pitcairn       Polynesia
        166   French Polynesia       Polynesia
        179              Samoa       Polynesia
        203            Tokelau       Polynesia
        204              Tonga       Polynesia
        212             Tuvalu       Polynesia
        221  Wallis and Futuna       Polynesia
        >>>
        """
        if sorted(self.columns) != sorted(other.columns):
            raise ValueError("Relations must be Union compatible")
        else:
            return Relation(pd.concat([pd.DataFrame(self),pd.DataFrame(other)]))

    def minus(self,other):
        """return a relation containing the rows in self 'but not' in other

        :param other:
        :return:

        :Example:

        >>> from reframe import Relation
        >>> country = Relation('country.csv')
        >>> country.query('continent == "Africa"').minus(country.query('region == "Western Africa"')).project(['name','region','continent'])
                                              name           region continent
        4                                  Algeria  Northern Africa    Africa
        7                                   Angola   Central Africa    Africa
        27                                Botswana  Southern Africa    Africa
        34                                 Burundi   Eastern Africa    Africa
        39                                Djibouti   Eastern Africa    Africa
        43                                   Egypt  Northern Africa    Africa
        45                                 Eritrea   Eastern Africa    Africa
        47                            South Africa  Southern Africa    Africa
        48                                Ethiopia   Eastern Africa    Africa
        53                                   Gabon   Central Africa    Africa
        87                                Cameroon   Central Africa    Africa
        91                                   Kenya   Eastern Africa    Africa
        92                Central African Republic   Central Africa    Africa
        97                                 Comoros   Eastern Africa    Africa
        98                                   Congo   Central Africa    Africa
        99   Congo, The Democratic Republic of the   Central Africa    Africa
        110                                Lesotho  Southern Africa    Africa
        112                                Liberia   Western Africa    Africa
        113                 Libyan Arab Jamahiriya  Northern Africa    Africa
        117                         Western Sahara  Northern Africa    Africa
        119                             Madagascar   Eastern Africa    Africa
        121                                 Malawi   Eastern Africa    Africa
        126                                Morocco  Northern Africa    Africa
        130                              Mauritius   Eastern Africa    Africa
        131                                Mayotte   Eastern Africa    Africa
        138                             Mozambique   Eastern Africa    Africa
        140                                Namibia  Southern Africa    Africa
        162                      Equatorial Guinea   Central Africa    Africa
        167                                Réunion   Eastern Africa    Africa
        169                                 Rwanda   Eastern Africa    Africa
        171                           Saint Helena   Western Africa    Africa
        178                                 Zambia   Eastern Africa    Africa
        181                  Sao Tome and Principe   Central Africa    Africa
        184                             Seychelles   Eastern Africa    Africa
        189                                Somalia   Eastern Africa    Africa
        191                                  Sudan  Northern Africa    Africa
        194                              Swaziland  Southern Africa    Africa
        199                               Tanzania   Eastern Africa    Africa
        206                                   Chad   Central Africa    Africa
        208                                Tunisia  Northern Africa    Africa
        213                                 Uganda   Eastern Africa    Africa
        230                               Zimbabwe   Eastern Africa    Africa
        234         British Indian Ocean Territory   Eastern Africa    Africa
        """
        return Relation(self[~self.isin(other).all(1)])


    def rename(self,old,new):
        """Rename old attribute to new

        :param old: string, name of old attribute
        :param new: string, name to change old to
        :return: Relation

        :Example:

        >>> from reframe import Relation
        >>> country = Relation('country.csv')
        >>> country.project(['name']).rename('name','countryname').head()
                    countryname
        0           Afghanistan
        1           Netherlands
        2  Netherlands Antilles
        3               Albania
        4               Algeria
        >>>
        """
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

    def extend(self,newcol,series):
        """Create a new attribute by combining or modifying one or more existing attributes

        :param newcol:  Name of the new column to create
        :param series:  An expression involving one or more other attributes
        :return:

        :Example:

        >>> from reframe import Relation
        >>> country = Relation('country.csv')
        >>> country.extend('gnpdiff',country.gnp - country.gnpold).project(['name','gnpdiff']).head(10)
                           name  gnpdiff
        0           Afghanistan      NaN
        1           Netherlands    10884
        2  Netherlands Antilles      NaN
        3               Albania      705
        4               Algeria     3016
        5        American Samoa      NaN
        6               Andorra      NaN
        7                Angola    -1336
        8              Anguilla      NaN
        9   Antigua and Barbuda       28
        >>>

        """
        self[newcol] = series
        return self


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
        >>>

        """
        res = self.gbo.count()
        return Relation(self.filteragg(res, col).rename(columns={col:"count_"+col}))


    def mean(self, col):
        """
        Count the number of occurrences of a value in the column for a group.

        :param col:
        :return:  A Relation with the groupby column(s) and count for a single column

        :Example:

        >>> from reframe import Relation
        >>> country = Relation('country.csv')
        >>> country.groupby(['continent']).mean('gnp')
               continent       mean_gnp
        0         Africa   10006.465517
        1     Antarctica       0.000000
        2           Asia  150105.725490
        3         Europe  206497.065217
        4  North America  261854.789189
        5        Oceania   14991.953571
        6  South America  107991.000000

        >>>

        """
        res = self.gbo.mean()
        return Relation(self.filteragg(res, col).rename(columns={col:"mean_"+col}))

    def min(self, col):
        """
        Count the number of occurrences of a value in the column for a group.

        :param col:
        :return:  A Relation with the groupby column(s) and count for a single column

        :Example:

        >>> from reframe import Relation
        >>> country = Relation('country.csv')
        >>> country.groupby(['continent']).min('lifeexpectancy')
               continent  min_lifeexpectancy
        0         Africa                37.2
        1     Antarctica                 NaN
        2           Asia                45.9
        3         Europe                64.5
        4  North America                49.2
        5        Oceania                59.8
        6  South America                62.9

        >>>

        """
        res = self.gbo.min()
        return Relation(self.filteragg(res, col).rename(columns={col:"min_"+col}))

    def max(self, col):
        """
        Count the number of occurrences of a value in the column for a group.

        :param col:
        :return:  A Relation with the groupby column(s) and count for a single column

        :Example:

        >>> from reframe import Relation
        >>> country = Relation('country.csv')
        >>> country.groupby(['continent']).max('gnp')
               continent  max_gnp
        0         Africa   116729
        1     Antarctica        0
        2           Asia  3787042
        3         Europe  2133367
        4  North America  8510700
        5        Oceania   351182
        6  South America   776739
        >>>

        """
        res = self.gbo.max()
        return Relation(self.filteragg(res, col).rename(columns={col:"max_"+col}))

    def sum(self, col):
        """
        Count the number of occurrences of a value in the column for a group.

        :param col:
        :return:  A Relation with the groupby column(s) and count for a single column

        :Example:

        >>> from reframe import Relation
        >>> country = Relation('country.csv')
        >>> country.groupby(['continent']).sum('surfacearea')
               continent  sum_surfacearea
        0         Africa       30250377.0
        1     Antarctica       13132101.0
        2           Asia       31881008.0
        3         Europe       23049133.9
        4  North America       24214469.0
        5        Oceania        8564294.0
        6  South America       17864922.0
        >>>

        """
        res = self.gbo.sum()
        return Relation(self.filteragg(res, col).rename(columns={col:"sum_"+col}))

    def median(self, col):
        """
        Count the number of occurrences of a value in the column for a group.

        :param col:
        :return:  A Relation with the groupby column(s) and count for a single column

        :Example:

        >>> from reframe import Relation
        >>> country = Relation('country.csv')
        >>> country.groupby(['continent']).median('gnp')
               continent  median_gnp
        0         Africa      2533.5
        1     Antarctica         0.0
        2           Asia     15706.0
        3         Europe     20401.0
        4  North America      2223.0
        5        Oceania       123.0
        6  South America     20300.5
        >>>

        """
        res = self.gbo.median()
        return Relation(self.filteragg(res, col).rename(columns={col:"median_"+col}))

if __name__ == '__main__':
    #country = Relation('country.csv')
    import doctest
    doctest.testmod()
