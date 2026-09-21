def get_float( prompt ):
    while True:
        try:
            num = float( input( prompt ) )
        except ValueError:
            print( "Geen getal -- probeer het opnieuw" )
            continue
        return num

getFloat = get_float

def get_integer( prompt ):
    while True:
        try:
            num = int( input( prompt ) )
        except ValueError:
            print( "Geen geheel getal -- probeer het opnieuw" )
            continue
        return num
getInteger = get_integer

def get_string( prompt ):
    line = input( prompt )
    return line.strip()
getString = get_string

def get_letter( prompt ):
    while True:
        line = input( prompt )
        line = line.strip()
        line = line.upper()
        if len( line ) != 1:
            print( "Geef precies een letter in" )
            continue
        if line < 'A' or line > 'Z':
            print( "Geef een letter van het alfabet in" )
            continue
        return line
getLetter = get_letter
