import sqlite3
import logging
from contextlib import closing
from flask import current_app, g

logger = logging.getLogger(__name__)

def init_db(db_path=None, sql_file_path=None):
    if not db_path:
        db_path = current_app.config['DB_PATH']
    if not sql_file_path:
        sql_file_path = current_app.config['INIT_SQL_PATH']

    conn = get_db_conn(db_path)

    if conn:
        try:
            with open(sql_file_path) as f:
                script = f.read()

        except FileNotFoundError:
            logger.exception("SQL file path isn't correct")
            return False

        try:
            with closing(conn.cursor()) as curs:
                curs.executescript(script)
        except Exception as e:
            raise e
        else:
            conn.commit()
            conn.close()
    else:
        logger.error('Can connect to db, db path is wrong!')
        return False

def get_db_conn(db_path):
    try:
        conn = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        conn.row_factory = sqlite3.Row

    except:
        logger.exception('An exception occured while trying to connect to db.')
        return False

    return conn

def insert_into_table(db_conn, table_name, columns, values):
    statement = f'''
    INSERT INTO {table_name} ({','.join(columns)})
    '''

    if type(values[0]) == list or type(values[0]) == tuple:
        placeholders = '?,'*len(values[0])
    else:
        placeholders = '?,'*len(values)

    placeholders = placeholders[:-1]
    statement += f"VALUES ({placeholders})"
    statement += ';'
    
    try:
        with closing(db_conn.cursor()) as cursor:
            if type(values[0]) == list or type(values[0]) == tuple:
                cursor.executemany(statement, values)
            else:
                cursor.execute(statement, values)
    except:
        logger.exception('An Exception occured while trying to execute the SQL statements (insert into).')
        return False
    else:
        db_conn.commit()

    return True

def read_from_table(db_conn, table_name, columns=None, conditions=None):
    if columns:
        if type(columns) == str:
            columns = [columns, ]

        statement = f'''
        SELECT {','.join(columns)} FROM {table_name}
        '''
    else:
        statement = f'''
        SELECT * FROM {table_name}
        '''

    if conditions:
        condition_str = get_condition_str(conditions)
        statement += condition_str

    statement += ';'
    
    try:
        with closing(db_conn.cursor()) as cursor:
            cursor.execute(statement)
            result = cursor.fetchall()

    except:
        logger.exception('An Exception occured while trying to execute the SQL statements (read from).')
        return False
    
    return result

def update_table(db_conn, table_name, setting_columns, conditions=None):
    statement = f'''
    UPDATE '{table_name}'
    SET 
    '''

    for column in setting_columns:
        set_value = setting_columns[column]
        set_string = f"'{column}' = "
        if type(set_value) is int:
            set_string += f"{set_value}, "

        elif type(set_value) is str:
            set_string += f"'{set_value}', "

        elif not set_value:
            set_string += "NULL, "

        statement += set_string

    statement = statement[:-2]

    if conditions:
        condition_str = get_condition_str(conditions)
        statement += condition_str

    statement += ';'

    try:
        with closing(db_conn.cursor()) as cursor:
            cursor.execute(statement)
    except:
        logger.exception('An Exception occured while trying to execute the SQL statements (update table).')
        return False
    else:
        db_conn.commit()

    return True

def delete_from_table(db_conn, table_name, conditions):
    statement = f'''
    DELETE FROM `{table_name}`
    '''
    
    condition_str = get_condition_str(conditions)
    statement += (condition_str + ';')
    
    try:
        with closing(db_conn.cursor()) as cursor:
            cursor.execute(statement)
    except:
        logger.exception('An Exception occured while trying to execute the SQL statements (delete from table).')
        return False
    else:
        db_conn.commit()

    return True

def get_condition_str(conditions):
    '''
    :conditions: dict
        {column: value, ...} or 
        {column: ('in', (value1, value2, ...)), ...} or
        {column: ('between', (value1, value2)), ...} where value 1 < value2
    '''

    condition_str = '\nWHERE'
    for column in conditions:
        condition_val = conditions[column]
        condition_val_type = type(condition_val)
        if condition_val_type == str or condition_val_type == int or len(condition_val) == 1:
            if condition_val_type == str:
                condition_str += f" {column} = '{condition_val}' AND"
            else:
                condition_str += f" {column} = {condition_val} AND"

        else:
            middle = condition_val[0]
            values = condition_val[1]

            condition_str += f' {column} {middle.upper()} '

            if middle.lower() == 'in':
                values_str = ''
                for val in values:
                    if type(val) is int:
                        values_str += f"{val}, "

                    elif type(val) is str:
                        values_str += f"'{val}', "
                
                values_str = values_str[:-2]
                rest = f"({values_str})"

            elif middle.lower() == 'between':
                if len(values) == 2:
                    values_str = ''
                    for val in values:
                        if type(val) is int:
                            values_str += f"{val} AND "

                        elif type(val) is str:
                            values_str += f"'{val}' AND "

                    rest = values_str[:-5]
                else:
                    raise ValueError('When you use "between", number of values must be 2.')
            else:
                raise ValueError('Please choose between "in" or "between".')

            condition_str += f'{rest} AND'

    condition_str = condition_str[:-4]
    return condition_str

def get_table_columns(db_conn, table_name):
    statement = f'SELECT * FROM {table_name} LIMIT 0;'
    try:
        with closing(db_conn.cursor()) as cursor:
            cursor.execute(statement)
    except:
        raise ValueError("Provided table isn't in the connection's database.")

    columns = tuple([item[0] for item in cursor.description])
    return columns


def set_db_conn():
    conn = get_db_conn(current_app.config['DB_PATH'])
    if conn:
        g.db_conn = conn
    else:
        logger.error('Can connect to db, db path is wrong!')

def close_db(e):
    if 'db_conn' in g:
        g.db_conn.close()