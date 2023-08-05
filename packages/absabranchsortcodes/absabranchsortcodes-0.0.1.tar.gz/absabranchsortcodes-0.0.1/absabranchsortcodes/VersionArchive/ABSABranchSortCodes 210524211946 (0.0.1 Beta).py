"""ABSA Branch Sort Codes Generator

Generate a "sort code" file from for ABSA Bank.  The source is a CICS file
which is massaged into a destination file in the correct format for SWIFT
to import."""

import configparser
import argparse
import logging
from pathlib import Path
import sys
import apputils as au


_version = "0.0.1"
_name = None
_path = None


class ABSABranchSortCodes:
    '''Class description
    '''
    def __init__( self, p_cfg, p_ini_pth, p_apputils ):
        '''Method description
        '''
        self.success = True
        self.apputils = p_apputils
        self._cfg = p_cfg
        self.ini_pth = p_ini_pth
        self._log_name = __name__
        self._logger = logging.getLogger( self._log_name )
        self._cfg = configparser.ConfigParser( inline_comment_prefixes = '#')
        self._renew_parameters()
        self._verbose = False
        self.source_fldr = None
        self.history_fldr = None
        self.export_fldr = None
    # end __init__

    def test_func( self ):
        '''Method description
        '''
        print( self.apputils.msg_info('Testing ABSABranchSortCodes...'))
        return True
    # end test_func

    def _renew_parameters( self ):
        '''Method description
        '''
        def create_folders():
            '''Method description
            '''
            if not self.data_folder.exists():
                self.data_folder.mkdir()
            if not self.history_fldr.exists():
                self.history_fldr.mkdir()
            if not self.export_fldr.exists():
                self.export_fldr.mkdir()
            pass
        # end _renew_parameters

        self._cfg.read([ self.ini_pth ])
        self.proj_root_fldr = _path.parents[1]
        self.data_folder = self.proj_root_fldr / self._cfg.get( 'Folders', 'DataSubFolder' )
        create_folders()
        self.test_mode = self._cfg.getboolean( 'Test', 'TestMode' )
        self.verbose = False
        self.source_fldr = Path(self._cfg.get( "Folders", "SourceFolder" ))
        self.history_fldr = Path(self._cfg.get( "Folders", "HistoryFolder" ))
        self.export_fldr = Path(self._cfg.get( "Folders", "ExportFolder" ))
    # end renew_parameters

    def run( self ):
        '''Method description
        '''
        if self.test_mode:
            self._prepare_test()
        print( au.msg_milestone( '==[ Start processing ]===========================================' ))
        self.test_func()
        print( au.msg_milestone( '--[ End processing ]---------------------------------------------' ))
        if self.test_mode:
            self._validate_test()
        pass
    # end run

    def _prepare_test( self ):
        '''Method description
        '''
        print( au.msg_milestone( '==[ Setup testing environment ]==================================' ))
        self.verbose = True
        print( au.msg_milestone( '--[ Setup done ]-------------------------------------------------' ))
    # end _prepare_test

    def _validate_test( self ):
        '''Method description
        '''
        print( au.msg_milestone( '==[ Cleaning up testing environment ]============================' ))
        pass
        print( au.msg_milestone( '--[ Cleaning up done ]-------------------------------------------' ))
    # end _validate_test
# end ABSABranchSortCodes


if __name__ == '__main__':
    argParser = argparse.ArgumentParser( description = 'Get config file name' )
    argParser.add_argument( '-c', '--configPath', help = 'Config file name', default = argParser.prog[ :argParser.prog.find( '.') + 1] + 'ini')
    args = argParser.parse_args()
    ini_pth =  args.configPath
    cfg = configparser.ConfigParser( inline_comment_prefixes = '#')
    cfg.read([ ini_pth ])
    defaultLogLevel = cfg.getint( 'LogLevels', 'Default' )
    consoleLogLevel = cfg.getint( 'LogLevels', 'Console' )
    fileLogLevel = cfg.getint( 'LogLevels', 'File' )

    _path = Path( sys.argv[ 0 ])
    _name = _path.stem
    logger = logging.getLogger( _name )
    logger.setLevel( au.DEF_LOG_LEV )
    file_handle = logging.FileHandler( au.LOG_FILE_NAME, mode = 'w' )
    file_handle.setLevel( au.DEF_LOG_LEV_FILE )
    console_handle = logging.StreamHandler()
    console_handle.setLevel( au.DEF_LOG_LEV_CON )
    file_format = logging.Formatter( au.LOG_FILE_FORMAT, datefmt = au.LOG_DATE_FORMAT )
    console_format = logging.Formatter( au.LOG_CONSOLE_FORMAT )
    file_handle.setFormatter( file_format )
    console_handle.setFormatter( console_format )
    logger.addHandler( file_handle )
    logger.addHandler( console_handle )


    apputils = au.AppUtils( _name, _version, __doc__[0], Path( _path), ini_pth )
    apputils.print_header()
    absa_bsc = ABSABranchSortCodes( cfg, ini_pth, apputils )
    if absa_bsc.success:
        absa_bsc.run()
    apputils.print_footer()
# end __main__
