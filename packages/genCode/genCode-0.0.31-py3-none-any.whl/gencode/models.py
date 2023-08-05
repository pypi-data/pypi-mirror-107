class Table:
    comment: str
    xx_table_name: str
    XX_TABLE_NAME: str
    XxTableName: str
    xxTableName: str
    xxtablename: str
    XXTABLENAME: str
    table_name: str
    TABLE_NAME: str
    tablename: str
    TABLENAME: str
    tableName: str
    TableName: str

    columns: []


class Column:
    db_dataType: str
    comment: str
    column_name: str
    Column_Name: str
    COLUMN_NAME: str
    ColumnName: str
    columnname: str
    COLUMNNAME: str
    dataType: str
    data_length: int
    is_pk: bool


class Gcode:
    is_dir = False
    temp_base_name: str
    temp_path: str
    temp_content: str
    target_path: str
    target_content: str
    encode: str
