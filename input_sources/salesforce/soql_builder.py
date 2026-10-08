def build_query(object_name, field_name, sorting, record_limit, keep_missing_values):
    print(f"Object:   {object_name}")
    query = 'SELECT Id,' + field_name + ' FROM ' + object_name
    
    if not keep_missing_values:
        query = query + " WHERE " + field_name + " != null"
    query = query + ' ORDER BY ' + sorting
    if record_limit != 'all':
        query += ' LIMIT ' + record_limit
    
    return query
