def slurp_file(path):
    """read file given by path and return the contents of the file
       as a single string datatype"""
    try:
        with open(path,'r') as f:
            data = f.read()
        return data
    except IOError:
        return("ERROR: the file cannot be opened or does not exist " + path)
