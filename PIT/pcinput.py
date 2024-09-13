def getFloat( prompt ):
    while True:
        try:
            num = float( input( prompt ) )
        except ValueError:
            print( "Geen getal -- probeer het opnieuw" )
            continue
        return num

def getInteger( prompt ):
    while True:
        try:
            num = int( input( prompt ) )
        except ValueError:
            print( "Geen geheel getal -- probeer het opnieuw" )
            continue
        return num

def getString( prompt ):
    line = input( prompt )
    return line.strip()

def getLetter( prompt ):
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
