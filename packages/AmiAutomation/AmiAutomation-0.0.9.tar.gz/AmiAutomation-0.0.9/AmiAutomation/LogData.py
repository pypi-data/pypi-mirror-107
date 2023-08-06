import zlib, struct, time, os, io
import datetime as dt
import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET

class Properties:
    def Unserialize(bytesStream):
        
        properties = dict()
        
        version = bytesStream.read(1)[0]
            
        if version != 0:
            print ("Error unserializing properties, version " + str.from_bytes(version) + " is not supported")
            
        itemsCount = bytesStream.read(4)
        intItemsCount = int.from_bytes(itemsCount, "little")
        
        for items in range(intItemsCount): 
            
            strLen = bytesStream.read(1)[0]
            
            key = bytesStream.read(strLen).decode()
            
            dataTypeEnum = bytesStream.read(1)[0]
            
            dataType, size = _getDatatype(dataTypeEnum)
            if dataType == "s":#string
                value = _readString(bytesStream)
            elif dataType == "D":#Datetime
                value = _readString(bytesStream)
                value = value.rstrip('0') #Remove trailing 0s
                value = dt.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
            else:    
                value = struct.unpack(dataType, bytesStream.read(size))[0]
            
            properties[key] = value
            
        if 'Increment' in properties:
            properties['Increment'] = dt.timedelta(milliseconds = properties['Increment'] )
                
        return properties

class Binary:
    def __init__(self):
        self._header = FrameHeader("BLOB")
        self._buffer = []
        self._properties = dict()
    
    def Unserialize(self,bytesStream):
        #Properties  
        self._properties = Properties.Unserialize(bytesStream)
        #Inner
        innerLength = struct.unpack('i', bytesStream.read(4))[0]            
        self._buffer = bytesStream.read(innerLength)

class Composite:
    def __init__(self):
        self._header = FrameHeader("CPST")
        self._frames = []
        self._hash = dict()
        self._properties = dict()
        
    def Unserialize(self,bytesStream):
        #Properties  
        self._properties = Properties.Unserialize(bytesStream)
        #Inner
        count = struct.unpack("h", bytesStream.read(2))[0]         
        for element in range(count):
            
            bag = Bag()
            
            contains = struct.unpack("?", bytesStream.read(1))[0]
            if contains:
                strLen = bytesStream.read(1)[0]
                bag.Key= bytesStream.read(strLen).decode()
                self._hash[bag.Key] = bag
                
            frameHeader = FrameHeader(None)
            frameHeader._tag = bytesStream.read(4)
            frameHeader._version = bytesStream.read(1)[0]
            
            if frameHeader._version == b'\xFF':
                print("Corrupt header, invalid version.")
                
            frameHeader._flags = bytesStream.read(1)[0] & 0xF0 #Only read what I understand
            frameHeader._rawSize = struct.unpack("i", bytesStream.read(4))[0]
            
            if frameHeader._rawSize == 0:
                print("Corrupt header, tag size can't be zero.")
                
            frameBase = FrameBase(frameHeader._tag) 
            frameBase._header = frameHeader
            frameBase._baseframe.Unserialize(bytesStream)
      
            bag._frame = frameBase
            self._frames.append(bag)   
        
class Bag:
    def __init__(self):
        self.Key = str()
        self._frame = None

class FrameHeader:
    def __init__(self,tag):
        self._version = 0;
        self._flags = 0;
        self._rawSize = 0;
        self._tag = tag; 
    
class FrameBase:
    def __init__(self,tagName):
        self._header = FrameHeader(tagName)
        if tagName == b'BLOB':
            self._baseframe = Binary()
        elif tagName == b'CPST':
            self._baseframe = Composite()
        else:
            raise Exception("Invalid tag", tagName, "for FrameBase")

class LogData:
    def __init__(self):
        self._fileName = str()
        self._data = None
        self._mainTrendsNames = None
        self._mainDivisors = None
        self.dataFrame = pd.DataFrame()
        self.properties = None

def _getDatatype (dataTypeEnum):
    thisdict = {
    3: ("?",1), #bool
    4: ("c",1), #char
    5: ("b",1), #signed char (SByte)
    6: ("B",1), #unsigned char (Byte)
	7: ("h",2), #short (Int16)
	8: ("H",4), #unsigned char (UInt16)
	9: ("i",4), #int (Int32)
	10: ("I",4), #unsigned int (UInt32)
	11: ("q",8), #long long (Int64)
	12: ("Q",8), #unsigned long long (UInt64)
	13: ("f",4), #float (Single)
	14: ("d",8), #double (Double)
	15: ("d",16), #(Decimal) May not work
    16: ("D",8), #(DateTime) May not work
    18: ("s",1), #char[] (String) 
	19: ("Q",16), #(Guid) May not work
	20: ("p",1), #char [] (Binary)
    }
    return thisdict[dataTypeEnum]

def _IntModeDivisor(mode):
    intMode = mode % 100
    switcher = {
        0: 100, #impedance
        1: 100, #current
        2: 100 #resistance
    }
    if intMode in switcher:
        return switcher[intMode]
    else:
        return 1
    
def _ExtModeDivisor(mode):
    extMode =mode / 100 
    switcher = {
        1: 100, #current
        2: 10, #voltage
        3: 10000, #PF
        4: 100, #MW
        5: 10 #RWI
    }
    if extMode in switcher:
        return switcher[extMode]
    else:
        return 1

def _RegModeDivisor(mode):
    div = _ExtModeDivisor(mode)
    if div ==1:
        return _IntModeDivisor(mode)
    else:
        return div

def _getDivisors(divList, RegModeList):
    divColumnReturn = []
    for i,div in enumerate(divList):
        regulationMode = RegModeList[i]
        if div<0:
            if (div == -1): #Int. mode
                divColumnReturn.append(_IntModeDivisor(regulationMode))
            elif (div == -2): #Ext. mode
                divColumnReturn.append(_ExtModeDivisor(regulationMode))
            elif (div== -3): #Int. or Ext. mode
                divColumnReturn.append(_RegModeDivisor(regulationMode))
        else:
            divColumnReturn.append(div)
    return divColumnReturn

def _readString(bytesStream):
    #https://docs.microsoft.com/en-us/openspecs/sharepoint_protocols/ms-spptc/1eeaf7cc-f60b-4144-aa12-4eb9f6e748d1?redirectedfrom=MSDN
    index = 0
    strLen = 0
    while True:
        length = bytesStream.read(1)[0]
        strLen |= (length & 0x7F) << (7*index)
        index += 1

        if length & 0x80 == 0: #Number complete
            break
               
    value = bytesStream.read(strLen).decode()  
    return value

def _processVersionN(version, composite):
    """
    Unpacks binary file according to its properties

    Parameters
    ----------
    version : int
        binary version  
        
    composite : Composite
        Composite containing properties and frames
    
    Returns
    -------
    LogData
        Structure containing most file data

    """
    # utcStartTime = composite._properties['StartTime']
    # incrementMillisecs = composite._properties['Increment']
    # incrementTicks = incrementMillisecs * 10000.0
    # definition = composite._properties['Definition']
    
    root = ET.fromstring(composite._properties["Definition"])
    
    if version == 3: ##TODO: Use full definition instead of definition
        nodes = root.findall(".//object[@logged='y']/field")
    elif version == 2:
        nodes = root.findall(".//object[@logged='y']/field")
    elif version == 1:
        nodes = root.findall("//object/field")
    else:
        print("Unknown packet version: ", version)
        
    varNames = []
    trendsNames = []
    divisors = []
    fieldTypes = []
    
    listBitMapElement = []
    d_c = []
    
    for index, field in enumerate(nodes):
        fieldType = field.attrib['type']
        fieldTypes.append(fieldType if fieldType == "s" else None)
        if field.attrib['type'] == "s":
                        
            varName = field.text.strip()
            varNames.append(varName)
            if varName != "":
                trendsNames.append(varName)
                option = field.attrib['div']
                try:
                    divisor = float(option)
                    if divisor == 0:
                        divisor = 1
                except:
                    if option == 'I':
                        divisor = -1
                    elif option == "E":
                        divisor = -2
                    elif option == "I|E":
                        divisor = -3
                divisors.append(divisor)
                
        else:
            listBitMapElement.append(index)
            bit = 0
            for bits in field:
                bit += 1
                varNames.append(bits.text)
                if varNames[-1]:
                    trendsNames.append(varNames[-1])
                    divisors.append(1)
    
            d_c.append(bit)

    listOfSamples = []
    
    #Obtain stream data from InnerBuffer
    appendListOfSamples = listOfSamples.append
    
    bytesArray = composite._hash["RawData"]._frame._baseframe._buffer
    bufferSize = len(composite._hash["RawData"]._frame._baseframe._buffer)
    
    dataArray = np.ndarray(shape=(int((bufferSize/2)/len(fieldTypes)),len(fieldTypes)), dtype='h', buffer=bytesArray)
    
    bitMapCount = 0    
    for i in range(len(dataArray[0,:])):
        if (bitMapCount < len(listBitMapElement)):
            if listBitMapElement[bitMapCount] == i:
                for bit in range(d_c[bitMapCount]):
                    series = dataArray[:,i] >> bit & 1
                    appendListOfSamples(series)
                bitMapCount+=1
                continue
        appendListOfSamples(dataArray[:,i])
        
    arraySamples = np.transpose(listOfSamples, axes=None)
    
    logData = LogData()
    logData._data = arraySamples
    logData._mainTrendsNames = trendsNames
    logData._mainDivisors = divisors
    logData.properties = composite._properties
    
    return logData

def binStreamToDF(file):
    """
    Unpacks binary file stream into LogData
    
    Parameters
    ----------
    file : stream
        stream of binary file
        

    Returns
    -------
    LogData
        Structure containing most file data

    """   
    #header
    TAGS = file.read(4)
    if TAGS != b'TAGS':
        print("Error with Tags header")
    versionHeader = file.read(1)
    if versionHeader == b'\xFF':
        print("Corrupt header, version can never reach 255")
    flags = file.read(1)
    if flags.hex() == '40':
        compressed = True
    else:
        compressed = False
    
    composite = Composite()
      
    bytePos = 0    
    if compressed:
        bytesArray = zlib.decompress(file.read())
    else:
        bytesArray = file.read()
    bytesStream = io.BytesIO(bytesArray)
    
    composite.Unserialize(bytesStream)
        
    if 'Version' in composite._properties:
        if composite._properties['Version'] == 1:
            logData = _processVersionN(1, composite)
        elif composite._properties['Version'] == 2:
            logData = _processVersionN(2, composite)
        elif composite._properties['Version'] == 3:
            logData = _processVersionN(3, composite)
        else:
            print("Unknown version")
    
    dFrame = pd.DataFrame(logData._data, columns=logData._mainTrendsNames )
    
    step = np.arange(start = 0, stop=len(logData._data), step=1, dtype=np.int16)
    listOfTimeStamps = logData.properties['StartTime']+logData.properties['Increment']*pd.Series(step)
    
    try:
        divColumns = _getDivisors(logData._mainDivisors,dFrame["RegStatus.RegulationMode"] )
    except:
        divColumns = logData._mainDivisors
        
    logData.dataFrame = dFrame.div(divColumns, axis='columns')
    del logData._data
    
    logData.dataFrame.insert(0,"Timestamp", listOfTimeStamps)
    # logData.dataFrame.set_index("Timestamp",inplace=True)
        
    return logData

def binFileToDF(path):
    """
    Unpacks binary file into LogData
    
    Parameters
    ----------
    path : str
        Complete file path
        
    Returns
    -------
    LogData
        Structure containing most file data

    """
    
    file = open(path, "rb")
    
    logData = binStreamToDF(file)
    logData._fileName = os.path.basename(path)
    
    file.close()
    return logData
