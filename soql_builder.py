def build_query(object_name, field_name, sorting, record_limit):
    print(f"Object:   {object_name}")
    query = 'SELECT Id,' + field_name + ' FROM ' + object_name + ' ORDER BY ' + sorting
    if record_limit != 'all':
        query += ' LIMIT ' + record_limit
    
    return query
