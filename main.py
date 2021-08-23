from circuit.circuitSerial import circuitSerial
import pyautogui
import json
import os

class main:

    def __init__(self) -> None:
        path = os.path.dirname( __file__ )
        with open( os.path.join( path, 'config.json' ), 'r' ) as file:
            config = json.load( file )

        instanceCircuit = circuitSerial()
        connection = instanceCircuit.scannerSerial(
            config['CIRCUIT']['MODEL'],
            config['CIRCUIT']['SERIE'],
            config['CIRCUIT']['BAUDIOS'],
            config['CIRCUIT']['TIMEOUT'],
            config['CIRCUIT']['COMMAND'],
            config['CIRCUIT']['PATTERN']
        )

        if connection is not None:
          self.listenControl( instanceCircuit, connection, config['KEYBOARD'] )
    
    def listenControl( self, instanceCircuit, connection, keyboard ):
        print( 'Init Virtual Cam' )
        for key in keyboard['VIRTUAL-CAM']:
            pyautogui.keyDown( key )

        for key in reversed( keyboard['VIRTUAL-CAM'] ):
            pyautogui.keyUp( key )
        print( 'Init Virtual Cam' )

        while True:
            data = instanceCircuit.readSerial( connection ).decode()

            if data != '' and data != False:
                try:
                    print( 'Init Press' )

                    for key in keyboard[ 'CAM-' + data.strip() ]:
                        pyautogui.keyDown( key )
                    
                    for key in reversed( keyboard[ 'CAM-' + data.strip() ] ):
                        pyautogui.keyUp( key )

                    print( 'Fin Press' )
                except Exception as e:
                    print( e )

main()