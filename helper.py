import pandas
from configparser import ConfigParser

def read_csv(path_to_csv):
    return tuple(dict(item[1]) for item in tuple(pandas.read_csv(path_to_csv, sep=';', header=0, index_col = None).iterrows()))

def form_insert_from_dict_tuple(table_name, dict_tuple: [dict])->str:
    return f"INSERT INTO {table_name}({', '.join(dict_tuple[0].keys())}) VALUES {', '.join([str(tuple(i.values())) for i in dict_tuple])}"

#this is parser for config.ini file where credentials to mySQL DB are stored
def read_db_config(filename='config.ini', section='mysql'):
    """ Read database configuration file and return a dictionary object
    :param filename: name of the configuration file
    :param section: section of database configuration
    :return: a dictionary of database parameters
    """
    # create parser and read ini configuration file
    parser = ConfigParser()
    parser.read(filename)

    # get section, default to mysql
    db = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]
    else:
        raise Exception('{0} not found in the {1} file'.format(section, filename))

    return db