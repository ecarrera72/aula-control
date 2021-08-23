from time import sleep, strftime
import json
import os

class daemon:

    def __init__(self) -> None:
        print( "{} Inicia Daemon".format( strftime( '%d-%m-%Y %X' ) ) )

        path = os.path.dirname( __file__ )
        with open( os.path.join( path, 'config.json' ), 'r' ) as file:
            config = json.load( file )

        while True:
            try:
                for process in config['SYSTEM']['PROCESS']:
                    self.checkProcess( os.path.join( path, process ) )

                sleep( 5 )
            except Exception as e:
                print( e )
    
    def checkProcess( self, process ):
        if os.popen( "ps ax | grep -v grep | grep " + process ).read() == "":
            print( "Iniciando " + process )
            os.system( 'gnome-terminal -- python3 ' + process )
        else:
            print( 'Correcto {} {}'.format( strftime( '%d-%m-%Y %X' ), process ) )

daemon()