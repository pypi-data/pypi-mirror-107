'''Module for DApi2 error. 

:author: F. Voilat
:date: 2021-03-05 Creation
'''


class DApiComError(Exception):
    '''Base exception class for DAPI communication errors
    
    :param ErrorMessage errmsg: The error message.
        
    '''
    errorno = None
    name    = None
    label   = None
    text    = None
    
        
    @classmethod
    def getErrorClass(cls, errmsg):
        '''Find the class according to the error message.
        
        :param ErrorMessage errmsg: The error message.
        :return: The excepton class found
        '''
        return next(x for x in DApiComError.__subclasses__() if x.errorno[0] <= errmsg.getError() <= x.errorno[1]) 
    
    @classmethod
    def factory(cls, errmsg):
        '''Classmetoh to construct DApiComError according DAPI error code.
        
        :param ErrorMessage errmsg: The error message.
        :param \*exceptions: A list of specific exceptions.
        
        :return: The new exception according DAPI error.
        '''   
        
        assert 0 < errmsg.getError() < 0xc0 or errmsg.getError() >= 0xf0 
        errcls = DApiComError.getErrorClass(errmsg)
        return errcls(errmsg)

    
    def __init__(self, errmsg):
        super(Exception, self).__init__(errmsg)
        return
    
    def __str__(self):
        try:
            return '{0!s} - #0x1:02X} : {2!s}'.format(self.__class__.__name__, self.error, self.label)
        except:
            return Exception.__str__(self)    

    @property 
    def msg(self):
        '''The error message'''
        return self.args[0]
    
    @property
    def error(self):
        '''The error code'''
        return self.msg.getError()

    @property
    def addr(self):
        '''The message address'''
        return self.msg.getAddr()
    
            
    

class DApiComAddrError(DApiComError):
    errorno = (0x01,0x01)
    name    = 'DAPI_COM_WRONG_ADDR'
    label   = 'Wrong address'
    text    = 'Invalid address or command'

class DApiComReadonlyError(DApiComError):
    errorno = (0x02,0x02)
    name    = 'DAPI_COM_READ_ONLY'
    label   = 'Read only'
    text    = 'Try to write in a read only register' 

class DApiComValueError(DApiComError):
    errorno = (0x03,0x03)
    name    = 'DAPI_COM_WRONG_VALUE'
    label   = 'Wrong value'
    text    = 'No allowed value or wrong argument'

class DApiComContextError(DApiComError):
    errorno = (0x04,0x04)
    name    = 'DAPI_COM_WRONG_CONTEXT'
    label   = 'Wrong context'
    text    = 'This change or command is not allowed in this context'

class DApiComFormatError(DApiComError):
    errorno = (0x05,0x05)
    name    = 'DAPI_COM_MALFORMED_MSG'
    label   = 'Malformed message'
    text    = 'Malformed message'

class DApiComAccessError(DApiComError):
    errorno = (0x06,0x06)
    name    = 'DAPI_COM_ACCESS_DENIED'
    label   = 'Access denied'
    text    = 'Read/Write or command is not available with current access level'

class DApiComEepromError(DApiComError):
    errorno = (0x07,0x07)
    name    = 'DAPI_COM_EEPROM_FAILURE'
    label   = 'EEPROM failure'
    text    = 'EEPROM failure'
    

class DApiComAbortedError(DApiComError):
    errorno = (0xfd,0xfd)
    name    = 'DAPI_COM_ABORTED'
    label   = 'Aborted command'
    text    = 'Aborted command'

class DApiComComBrokenError(DApiComError):
    errorno = (0xfe,0xfe)
    name    = 'DAPI_COM_COM_BROKEN'
    label   = 'Borken Communication'
    text    = 'Communication is borken'
    
class DApiComUndefinedError(DApiComError):
    errorno = (0xff,0xff)
    name    = 'DAPI_COM_UDEFNED'
    label   = 'Undefined error'
    text    = 'Undefined error'


class DApiCommandError(DApiComError):
    '''Base exception class for DAPI commands errors
    
    :param ErrorMessage errmsg: The error message.
        
    '''    
    errorno = None
    name    = None
    label   = None
    text    = None    
    
    @classmethod
    def factory(cls, errmsg, *exceptions):
        '''Classmethod to construct DApiCommandError according DAPI error code.
        
        :param ErrorMessage errmsg: The error message.
        :param \*exceptions: A list of specific exceptions.
        
        :return: The new exception according DAPI error.
        :rtype: Child of DApiCommandError.
        '''   
        #assert 0 < errmsg.getError() < 0xc0, "errmsg.getError() => "+str(errmsg.getError()) 
        if errmsg.getError() < 0x80 or errmsg.getError() >= 0xFD:
            return DApiComError.factory(errmsg)
        else:
            for e in exceptions:
                if e.errorno[0] <= errmsg.getError() <= e.errorno[1]:
                    return e(errmsg)
        return DApiCommandError(errmsg)        
    
    
