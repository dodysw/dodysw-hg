SIS_VERSION = '2.03.00'
DEFAULT_VERSION = '2.00.00'
#   PyNetMony Netmonitor for S60 3rd Edition phones
#
#   Copyright (C) 2008  Carsten Knuetter, Georg Lukas, Daniel Perna
#
#   e_m_a-i-l: pynetmony (at) arcor . de
#
#   This program is free software; you can redistribute it and/or modify it
#   under the terms of the GNU General Public License as published by the
#   Free Software Foundation; either version 3 of the License, or (at your
#   option) any later version.  This program is distributed in the hope that
#   it will be useful, but WITHOUT ANY WARRANTY; without even the implied
#   warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#   GNU General Public License for more details.  You should have received a
#   copy of the GNU General Public License along with this program; if not,
#   see <http://www.gnu.org/licenses/>.


import appuifw
#import e32
import location
import sysinfo
import time
import sys
import audio
import thread
import math
#import e32db
import string
#import graphics
import topWindow
#from dialog import Progress
   
try:
   import envy
except:
   pass

try:
   import elocation
   eloc = True
except:
   eloc = False

try:
   import httplib
   skyhookmod = True
   conn = None
except:
   skyhookmod = False
   conn = None

try:
   import miso
   miso_ok = True
except:
   miso_ok = False

try:
   import lightblue
   #import blues
   bt = True
except:
   bt = False
try:
   #import camera
   #import camtest
   cam = False
except:
   cam = False
try:
   import wlantools
   wlan = True
except:
   wlan = False
from key_codes import *
from graphics import *
try:
   import locationrequestor
   locreq = True
   gpsdata = [0, 'GPS disabled']
except:
   gpsdata = [0, 'Module locationrequestor not installed']
   locreq = False

# Meta data section for SIS generation
# unprotected UID
SYMBIAN_UID = 0xE000D81D

TITLE=u'PyNetMony'
VERSION=TITLE + ' ' + SIS_VERSION

CENTER = -1

# temp variables
running=True
light=True
tab=0
tab_max=0
draw_rnc = False
s = None
finder = False
starttime = 0
key_repeat = 0
scroll_wlan = 0
scroll_bt = 0
wlan_radar_zoom = 0.21
heading_north = False
imsi = u''
imei = 0
userid = 0
maxspeed = 0.0

#Encoding scheme
#reload(sys) #dsw: must have this line in python 2.5
#sys.setdefaultencoding('iso-8859-1')
sys.setdefaultencoding('utf-8')
#sys.setdefaultencoding('latin-1')

#yahoo maps
APP_ID = "PoKyoYjV34Hzt6xVEbtLhZXG6N6S4o5X1AhHjxgfxTnkCbg1XNbQhX4GTbpevQ--"
MAP_URL = "http://local.yahooapis.com/MapsService/V1/mapImage?"
MAP_FILE = u"E:\\Images\\pynetmonymap.png"
map_x = map_y = 0
mapimg = status = None

gsm_url = 'http://www.google.com/glm/mmap'

if not os.path.exists("E:\\Images"):
   os.makedirs("E:\\Images")

# XXX: use absolute path for mp3 etc.
# os.path.join(os.getcwd(), u'default_settings.xml')
datadir = "E:\\Data\\Others\\PyNetMony\\"
if not os.path.isdir(datadir):
   os.makedirs(datadir)
pic_path = "E:\\Data\\Others\\PyNetMony\\pics\\"
if not os.path.isdir(pic_path):
   os.makedirs(pic_path)
log_path = "e:\\Data\\Others\\PyNetMony\\logs\\"
if not os.path.isdir(log_path):
   os.makedirs(log_path)

# program config
configfile = "E:\\Data\\Others\\PyNetMony\\pynetmony.cfg"
configfile2 = "E:\\Data\\Others\\PyNetMony\\pynetmony2.cfg"
configfile3 = "E:\\Data\\Others\\PyNetMony\\pynetmony3.cfg"
def_apn_file = "E:\\Data\\Others\\PyNetMony\\apn.cfg"
# XXX configfile =  os.path.join(os.getcwd(), u'pynetmony.cfg')
defconfig = {
   'CellNotify': 0,
   'Light': 0,
   'Refresh': 10,
   'Volume': 5,
   'Voice': 0,
   'GPS': 2,
   'Neighbour Radius': 3.0,
   'WLANInter': 10,
   'CLF': 0,
   'WLAN_STORE': 0,
   'WLAN_NOTIFY': 0,
   'MAPZOOM': 6,
   'BT_SCAN': 0,
   'BT_STORE': 0,
   'BT_NOTIFY': 0,
   'BT_Autosave': 10,
   'BT_SCAN_TIMEOUT': 500,
   'CLF_AUTOSAVE': 30,
   'COLOR_THEME': 0,
   'FONT_SIZE': 1}

config = defconfig.copy()

defconfig2 = {
   'WPS': 2,
   'RADAR_MODE': 0,
   'GEO_LAT': 50.096,
   'GEO_LON': 8.690,
   'WLAN_SORT': 0,
   'BSSID_NOTIFY': u'00:00:00:00:00:00',
   'LAC_CHECK': 0,
   'GSM_LOG_EVENT': 1,
   'POSUPDATE': 0}

config2 = defconfig2.copy()
   
defconfig3 = {
   'OPEN': u'Offenes Weh Lahn in Reichweite',
   'ADHOC': u'Ad-hock Weh Lahn in Reichweite',
   'NEWBT': u'Neues bluh tuhs in Reichweite',
   'LANGUAGE': 0,
   'BSSID': u'Gesuchtes Weh Lahn in Reichweite'}

config3 = defconfig3.copy()

# TODO: move these to theme[xxx]
font=u"normal"
myfont=(None,14,None)
headfont=(None,14,None)
rxl_line_font=(None,13,None)
color=(255,255,255)
linecol=(255,128,128)
bg=(0,0,60)
border=bg
#border=(255,0,0)
headcol=(255,255,255)
headbg=(255,255,255)
grid=(127,127,127)

# table for RX level history
rxl_log = []
rxl_last = 0

# table for Cell history
loc_log = []
logger = None
logname = None
toggle = 2
gpsmodule = 0
gpson = 0

# wps globals
wps_coords = ['NaN','NaN']
wps_list = []
wps_list_radar = []
wps_fix = 0
wps_count = 0
maxaps = 0

# global GSM state variables
t_last = 0
rxl = None
gsmloc = gsmloc_real = None

#WLAN globals
wlani = 0
newwlans = 0
wlangpsupdate = 0
wlanwpsupdate = 0
wlancpsupdate = 0
wlanssidupdate = 0
maxaprxl = -113
wscan = []
wlan_list = []
wlanquery_list = []
wlan_name = "E:\\Data\\Others\\PyNetMony\\pynetmony_wlan.txt"
wlan_name_e = "E:\\Data\\Others\\PyNetMony\\pynetmony_wlan.txt"
wlan_name_c = "C:\\Data\\Others\\PyNetMony\\pynetmony_wlan.txt"
kismet_name = "E:\\Data\\Others\\PyNetMony\\logs\\"
wlogger = None
wlogname = None
show_ssid = True
wlan_saving = False
wlan_scanning = False

save_error = False

#BT globals
invalid_bt = ""
bt_save_error = 0
bt_scan_time = 0
bt_err = 0
bti = 0
newbt = 0
btgpsupdate = 0
bt_busy = False
bt_saving = False
btscan = []
bt_list = []
oui_list = []
btquery_list = []
bt_name = "E:\\Data\\Others\\PyNetMony\\pynetmony_bt.txt"
bt_name_e = "E:\\Data\\Others\\PyNetMony\\pynetmony_bt.txt"
bt_name_c = "C:\\Data\\Others\\PyNetMony\\pynetmony_bt.txt"

#clf globals
new_cells_list = []
new_cells_updated = False
cellselect = -1
lacselect = -1
net_counter = -1
netmode_counter = -1
clf = []
new_cells_lb = None
newcells = 0
clf_saving = False
clf_name = ""
clf_path_c = "C:\\Data\\Others\\PyNetMony\\clf\\"

if not os.path.isdir(clf_path_c):
   os.makedirs(clf_path_c)
clf_path_e = "E:\\Data\\Others\\PyNetMony\\clf\\"
if not os.path.isdir(clf_path_e):
   os.makedirs(clf_path_e)
clf_found = False
cell_searching = False
cell_description = ''
cell_lat = u'999.99999'
cell_lon = u'999.99999'
band = {0:"gsm", 1:"umts"}
oldumts = -1
oldqnet = 99999
neighbour_list = []
neighbour_updated = False
clf_form=appuifw.Form([(u'Cell ID: ','text'),(u'LAC: ','text'),(u'RNC: ','text'),(u'Description: ','text'),(u'LAT: ','text'),(u'LON: ','text')])


s60_ver = e32.s60_version_info
API = s60_ver[0]*10 + s60_ver[1]
del s60_ver

if API <= 12:
   MAXSIZE = (176,208)
   LINEHEIGHT = 16
   HEADHEIGHT = 32
   TABHEIGHT = 13
   TABSPACE = 4
   # Hack for S60 1stEd devices:
   # just add all the required API calls
   appuifw.app.layout = lambda lid: ((176, 208-lid*68), (0, 0))
   appuifw.EScreen = 0
   appuifw.EMainPane = 1
   sysinfo.signal_dbm = lambda: 666
   sysinfo.signal_bars = lambda: 0
   e32.reset_inactivity = lambda: None
else:
   MAXSIZE = (800,352)
   LINEHEIGHT = 20
   HEADHEIGHT = 44
   TABHEIGHT = 16
   TABSPACE = 6
gl_size = (240,320)
# Spelling for network providers
class Voice:
   offline = u"Offline"
   band = [u"G S M", u"U M T S"]

   provider = {
      262: { 1: "Timo Beil",
            2: "Wo da phon",
            3: "E plus",
            7: "Oh tuh"}
      }

class KML_File:
   #"For creating KML files used for Google Earth"
   def __init__(self, filepath):
      self.filepath = filepath
      #"adds the kml header to a file (includes a default style)"
      file = open(filepath,"w")
      file.write(
      "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"\
      "<kml xmlns=\"http://earth.google.com/kml/2.1\">\n"\
      "<Document>\n"\
      "<Style id='Open'>\n"\
      "  <IconStyle>\n"\
      "  <color>ff00ff00</color>\n"\
      "   <scale>0.5</scale>\n"\
      "   <Icon>\n"\
      "     <href>http://maps.google.com/mapfiles/kml/pal4/icon57.png</href>\n"\
      "   </Icon>\n"\
      "  </IconStyle>\n"\
      "</Style>\n"\
      "<Style id='WEP'>\n"\
      "  <IconStyle>\n"\
      "  <color>ff00ffff</color>\n"\
      "   <scale>0.5</scale>\n"\
      "   <Icon>\n"\
      "     <href>http://maps.google.com/mapfiles/kml/pal4/icon57.png</href>\n"\
      "   </Icon>\n"\
      "  </IconStyle>\n"\
      "</Style>\n"\
            "<Style id='WPA'>\n"\
      "  <IconStyle>\n"\
      "  <color>ff0000ff</color>\n"\
      "   <scale>0.5</scale>\n"\
      "   <Icon>\n"\
      "     <href>http://maps.google.com/mapfiles/kml/pal4/icon57.png</href>\n"\
      "   </Icon>\n"\
      "  </IconStyle>\n"\
      "</Style>\n")
      file.close()

   def close(self):
      file = open(self.filepath,"a")
      file.write(
      "</Document>\n"\
      "</kml>")
      file.close()

   def open_folder(self, name):
      file = open(self.filepath,"a")
      file.write(
      "<Folder>\n"\
      "  <name>" + name + "</name>\n")
      file.close()

   def close_folder(self):
      file = open(self.filepath,"a")
      file.write(
      "</Folder>\n")
      file.close()
      
   def open(self):
      file = open(self.filepath,"a")

   def add_placemarker(self, latitude, longitude, altitude = 0.0, description = " ", style = "WEP", range = 6000, tilt = 45, heading = 0):
      #"adds the point to a kml file"
      file = open(self.filepath,"a")
      file.write(
      "  <Placemark>\n"\
      "   <description>" + description + "</description>\n"\
      "   <styleUrl>#"+ style +" </styleUrl>\n" 
      "   <visibility>0</visibility>\n"\
      "    <Point>\n"\
      "     <extrude>1</extrude>\n"\
      "     <altitudeMode>relativeToGround</altitudeMode>\n"\
      "     <coordinates>" + str(longitude) + "," + str(latitude) +", " +  str(altitude) + "</coordinates>\n"\
      "    </Point>\n"\
      "  </Placemark>\n")
      file.close()


class Logger:
   def __init__(self, log_name):
      self.logfile = log_name
   def write(self, obj):
      try:
         log_file = open(self.logfile, 'a')
         log_file.write(obj)
         log_file.close()
      except IOError, err:
         appuifw.note(u"Logger: " + unicode(err), "error")
   def writelines(self, obj):
      self.write(''.join(list))
   def logtab(self, list):
      # Convert list to unicode and add tabs
      txt = ';'.join(map(unicode, list)) + chr(13)+chr(10)
      self.write(txt)
   def flush(self):
      pass

class Setup( object ):
   # Config constants
   SOUND_OFF = 0
   SOUND_SOUND = 1
   SOUND_VOICE = 2
   SOUND_VOICE_NEW = 3

   LIGHT_OFF = 0
   LIGHT_CELL = 1
   LIGHT_ALWAYS = 2
   LIGHT_NEW_CELL = 3

   VOICE_CELL = 0
   VOICE_BAND = 1
   VOICE_BAND_LAC = 2
   VOICE_BAND_LAC_NET = 3
   VOICE_BAND_CLF = 4

   GPS_INTERNAL = 0
   GPS_EXTERNAL = 1
   GPS_ASSISTED = 2
   
   CLF_DEVICE = 0
   CLF_CARD = 1
   
   WLAN_DEVICE = 0
   WLAN_CARD = 1

   WLAN_NOTIFY_OFF = 0
   WLAN_NOTIFY_ADHOC = 1
   WLAN_NOTIFY_OPEN = 2
   WLAN_NOTIFY_BSSID = 3
   WLAN_NOTIFY_OPEN_VIBRATE = 4
   
   BT_DEVICE = 0
   BT_CARD = 1
   
   BT_NOTIFY_OFF = 0
   BT_NOTIFY_NEW_VOICE = 1
   BT_NOTIFY_NEW_LIGHT = 2
   BT_NOTIFY_NEW_VOICE_LIGHT = 3
   
   COLOR_THEME_BLUE = 0
   COLOR_THEME_BLACK = 1
   COLOR_THEME_RED = 2
   COLOR_THEME_GREEN = 3
   COLOR_THEME_MAGENTA = 4
   COLOR_THEME_WHITE = 5
   
   FONT_SIZE_SMALL = 0
   FONT_SIZE_MEDIUM = 1
   FONT_SIZE_LARGE = 2
   FONT_SIZE_XLARGE = 3

   ## The constructor.
   def __init__( self ):
      global config
      ## Config options
      self._iSound = [u'OFF', u'Sound', u'Voice', u'Only new']
      self._iLight = [u'OFF', u'Cell change on', u'Always on', u'New cells only']
      self._iVoice = [u'Cell only',
                  u'Band & Cell',
                  u'Band & Cell & LAC',
                  u'Band & Cell & LAC & NET',
                  u'Band & CLF']
      self._iGPS = [u'Internal', u'External', u'Assisted']
      self._iCLF = [u'Device', u'Memory Card']
      self._iWLAN_Store = [u'Device', u'Memory Card']
      self._iWLAN_Notify = [u'OFF', u'AD-HOC', u'Open', u'BSSID', u'Open (Vibrate)']
      self._iBT_Store = [u'Device', u'Memory Card']
      self._iBT_Notify = [u'OFF', u'Voice', u'Light', u'Voice & Light']
      self._iCOLOR_THEME = [u'Blue', u'Black', u'Red', u'Green', u'Magenta', u'White']
      self._iFONT_SIZE = [u'Small', u'Medium', u'Large', u'XL']
      ## Setup Menu
      self._iMenu = [(u'Defaults', self.defaultConfig),
                  (u'Reload Config File', self.loadConfig)]
      ## Form fields
      self.configToForm()
      #flags = appuifw.FFormEditModeOnly
      flags = appuifw.FFormEditModeOnly + appuifw.FFormDoubleSpaced
      self._iForm = appuifw.Form(self._iFields, flags)
      self._iForm.save_hook = self.saveForm
      #self._iForm.flags = appuifw.FFormEditModeOnly
      self._iForm.menu = self._iMenu

   def configToForm(self):
      global config
      _iFields = [( u'Cellselection Notifier', 'combo', ( self._iSound, config['CellNotify'] ) ),
               ( u'Light', 'combo', ( self._iLight, config['Light'] ) ),
               ( u'WLAN Scan [s] (off=0 / on>8)','number', config['Refresh'] ),
               ( u'Volume','number', config['Volume'] ),
               ( u'Voice Text','combo', (self._iVoice, config['Voice']) ),
               ( u'GPS', 'combo', ( self._iGPS, config['GPS'] ) ),
               ( u'Neighbour Radius [km]', 'float', config['Neighbour Radius']),
               ( u'WLAN Autosave Interval [min]','number', config['WLANInter']),
               ( u'CLF stored on','combo', (self._iCLF, config['CLF'])),
               ( u'WLAN Database stored on','combo', (self._iWLAN_Store, config['WLAN_STORE'])),
               ( u'WLAN Notifier','combo', (self._iWLAN_Notify, config['WLAN_NOTIFY'])),
               ( u'Map Zoom Level (1-12)','number', config['MAPZOOM']),
               ( u'Sec between BT Scans 0=off','number', config['BT_SCAN']),
               ( u'BT Database stored on','combo', (self._iBT_Store, config['BT_STORE'])),
               ( u'BT Notifier','combo', (self._iBT_Notify, config['BT_NOTIFY'])),
               ( u'BT Autosave Interval [min]','number', config['BT_Autosave']),
               ( u'BT Scan Timeout [s]','number', config['BT_SCAN_TIMEOUT']),
               ( u'CLF Autosave Interval [min]','number', config['CLF_AUTOSAVE']),
               ( u'Color Theme','combo', (self._iCOLOR_THEME, config['COLOR_THEME'])),
               ( u'Font Size','combo', (self._iFONT_SIZE, config['FONT_SIZE']))]   
      ## XXX: live update doesn't work yet. Need fixing
      if hasattr(self, '_iFields'):
         for i in range(len(_iFields)):
            self._iFields[i] = _iFields[i]
      else:
         self._iFields = _iFields

   def formToConfig(self):
      global config
      ## XXX: must find elegant way for conversion Form <-> config
      config = {
         'CellNotify': self._iFields[0][2][1],
         'Light': self._iFields[1][2][1],
         'Refresh': self._iFields[2][2],
         'Volume': self._iFields[3][2],
         'Voice': self._iFields[4][2][1],
         'GPS': self._iFields[5][2][1],
         'Neighbour Radius': self._iFields[6][2],
         'WLANInter': self._iFields[7][2],
         'CLF': self._iFields[8][2][1],
         'WLAN_STORE': self._iFields[9][2][1],
         'WLAN_NOTIFY': self._iFields[10][2][1],
         'MAPZOOM': self._iFields[11][2],
         'BT_SCAN': self._iFields[12][2],
         'BT_STORE': self._iFields[13][2][1],
         'BT_NOTIFY': self._iFields[14][2][1],
         'BT_Autosave': self._iFields[15][2],
         'BT_SCAN_TIMEOUT': self._iFields[16][2],
         'CLF_AUTOSAVE': self._iFields[17][2],
         'COLOR_THEME': self._iFields[18][2][1],
         'FONT_SIZE': self._iFields[19][2][1]}
         
      cfgfile = open(configfile, 'wt')
      cfgfile.write(repr(config))
      cfgfile.close()

   def defaultConfig(self):
      global config, defconfig
      config = defconfig.copy()
      self.configToForm()
      appuifw.note(u"Please reopen the Setup dialog.")

   def loadConfig(self, silent=False):
      global config
      config = defconfig.copy()
      try:
         cfgfile = open(configfile, 'rt')
         content = cfgfile.read()
         cfgfile.close()

         config.update(eval(content))
         if not silent:
            appuifw.note(u"Please reopen the Setup dialog.")
      except IOError, error:
         if not silent:
            appuifw.note(unicode(error),'error')
      self.configToForm()

   ## Displays the form.
   def execute( self ):
      self._iForm.execute( )

   ## save_hook send True if the form has been saved.
   def saveForm( self, aConfig ):
      global config
      self._iFields = aConfig
      self.formToConfig()
      
class Setup2( object ):
   # Config constants
   
   WPS_OFF = 0
   WPS_ON = 1
   WPS_ON_AND_LOG = 2
   
   RADAR_MODE_CLF = 0
   RADAR_MODE_GEO = 1
   RADAR_MODE_APS = 2
   RADAR_MODE_FIX = 3
   
   WLAN_SORT_RXL = 0
   WLAN_SORT_CH = 1
   WLAN_SORT_SSID = 2
   
   LAC_CHECK_OFF = 0
   LAC_CHECK_ON = 1
   
   GSM_LOG_EVENT_CHANGE = 0
   GSM_LOG_EVENT_SEC = 1
   
   ## The constructor.
   def __init__( self ):
      global config2
      ## Config options
      self._iWPS = [u'OFF', u'ON', u'Enable WPS/CPS logging']
      self._iRADAR_MODE = [u'CLF', u'Geocache', u"Local AP's"]
      self._iWLAN_SORT = [u'Signalstrength', u'Channel', u'SSID']
      self._iLAC_CHECK = [u'OFF', u'ON']
      self._iGSM_LOG_EVENT = [u'Cellchange only', u'every second']
      ## Setup Menu
      self._iMenu = [(u'Defaults', self.defaultConfig),
                  (u'Reload Config File', self.loadConfig)]
      ## Form fields
      self.configToForm()
      #flags = appuifw.FFormEditModeOnly
      flags = appuifw.FFormEditModeOnly + appuifw.FFormDoubleSpaced
      self._iForm = appuifw.Form(self._iFields, flags)
      self._iForm.save_hook = self.saveForm
      #self._iForm.flags = appuifw.FFormEditModeOnly
      self._iForm.menu = self._iMenu

   def configToForm(self):
      global config2
      _iFields = [( u'WLAN Positioning System', 'combo', (self._iWPS, config2['WPS'])),
               ( u'Radar Mode', 'combo', (self._iRADAR_MODE, config2['RADAR_MODE'])),
               ( u'Geocache LAT', 'float', config2['GEO_LAT']),
               ( u'Geocache LON', 'float', config2['GEO_LON']),
               ( u'WLAN Sorted by', 'combo', (self._iWLAN_SORT, config2['WLAN_SORT'])),
               ( u'BSSID Notifier', 'text', config2['BSSID_NOTIFY']),
               ( u'LAC Check for CLF search', 'combo', (self._iLAC_CHECK, config2['LAC_CHECK'])),
               ( u'GSM / 3G Log Event', 'combo', (self._iGSM_LOG_EVENT, config2['GSM_LOG_EVENT'])),
               ( u'POS Upload Interval [min] on>1','number', config2['POSUPDATE'])]
               
      ## XXX: live update doesn't work yet. Need fixing
      if hasattr(self, '_iFields'):
         for i in range(len(_iFields)):
            self._iFields[i] = _iFields[i]
      else:
         self._iFields = _iFields

   def formToConfig(self):
      global config2
      ## XXX: must find elegant way for conversion Form <-> config
      config2 = {
               'WPS': self._iFields[0][2][1],
               'RADAR_MODE': self._iFields[1][2][1],
               'GEO_LAT': self._iFields[2][2],
               'GEO_LON': self._iFields[3][2],
               'WLAN_SORT': self._iFields[4][2][1],
               'BSSID_NOTIFY': self._iFields[5][2],
               'LAC_CHECK': self._iFields[6][2][1],
               'GSM_LOG_EVENT': self._iFields[7][2][1],
               'POSUPDATE': self._iFields[8][2]}
         
      cfgfile = open(configfile2, 'wt')
      cfgfile.write(repr(config2))
      cfgfile.close()

   def defaultConfig(self):
      global config2, defconfig2
      config2 = defconfig2.copy()
      self.configToForm()
      appuifw.note(u"Please reopen the Setup dialog.")

   def loadConfig(self, silent=False):
      global config2
      config2 = defconfig2.copy()
      try:
         cfgfile = open(configfile2, 'rt')
         content = cfgfile.read()
         cfgfile.close()

         config2.update(eval(content))
         if not silent:
            appuifw.note(u"Please reopen the Setup dialog.")
      except IOError, error:
         if not silent:
            appuifw.note(unicode(error),'error')
      self.configToForm()

   ## Displays the form.
   def execute( self ):
      self._iForm.execute( )

   ## save_hook send True if the form has been saved.
   def saveForm( self, aConfig ):
      global config2
      self._iFields = aConfig
      self.formToConfig()
      
class Setup3( object ):
   # Config constants
   SINGLE = 0
   GERMAN = 1
   ENGLISH = 2
   ## The constructor.
   def __init__( self ):
      global config3
      ## Config options
      #self._iWPS = [u'OFF', u'ON', u'Enable WPS/CPS logging']
      #self._iRADAR_MODE = [u'CLF', u'Geocache']
      self._iWLAN_LANGUAGE = [u'Single digits', u'Words in german', u'Words in english']
      ## Setup Menu
      self._iMenu = [(u'Defaults', self.defaultConfig),
                  (u'Reload Config File', self.loadConfig)]
      ## Form fields
      self.configToForm()
      flags = appuifw.FFormEditModeOnly + appuifw.FFormDoubleSpaced
      self._iForm = appuifw.Form(self._iFields, flags)
      self._iForm.save_hook = self.saveForm
      self._iForm.menu = self._iMenu

   def configToForm(self):
      global config3
      _iFields = [( u'New open WLAN notifier', 'text', config3['OPEN']),
               ( u'New ad-hoc WLAN notifier', 'text', config3['ADHOC']),
               ( u'New BT notifier', 'text', config3['NEWBT']),
               ( u'Numbers read as', 'combo', (self._iWLAN_LANGUAGE, config3['LANGUAGE'])),
               ( u'BSSID notifier', 'text', config3['BSSID'])]

               
      ## XXX: live update doesn't work yet. Need fixing
      if hasattr(self, '_iFields'):
         for i in range(len(_iFields)):
            self._iFields[i] = _iFields[i]
      else:
         self._iFields = _iFields

   def formToConfig(self):
      global config3
      ## XXX: must find elegant way for conversion Form <-> config
      config3 = {
               'OPEN': self._iFields[0][2],
               'ADHOC': self._iFields[1][2],
               'NEWBT': self._iFields[2][2],
               'LANGUAGE': self._iFields[3][2][1],
               'BSSID': self._iFields[4][2]}
         
      cfgfile = open(configfile3, 'wt')
      cfgfile.write(repr(config3))
      cfgfile.close()

   def defaultConfig(self):
      global config3, defconfig3
      config3 = defconfig3.copy()
      self.configToForm()
      appuifw.note(u"Please reopen the Setup dialog.")

   def loadConfig(self, silent=False):
      global config3
      config3 = defconfig3.copy()
      try:
         cfgfile = open(configfile3, 'rt')
         content = cfgfile.read()
         cfgfile.close()

         config3.update(eval(content))
         if not silent:
            appuifw.note(u"Please reopen the Setup dialog.")
      except IOError, error:
         if not silent:
            appuifw.note(unicode(error),'error')
      self.configToForm()

   ## Displays the form.
   def execute( self ):
      self._iForm.execute( )

   ## save_hook send True if the form has been saved.
   def saveForm( self, aConfig ):
      global config3
      self._iFields = aConfig
      self.formToConfig()
      

class CellCam:
   SIZE = (640,480)

   def __init__(self):
      global finder
      self.timeout = 100
      self.lock = e32.Ao_lock()
      finder = True
      self.oldexit = appuifw.app.exit_key_handler
      appuifw.app.exit_key_handler = self.abort
      appuifw.app.body.bind(EKeySelect, self.take_picture)
      camera.start_finder(self.finder_cb)
      self.lock.wait()

   def abort(self):
      camera.stop_finder()
      self.finish()

   def finish(self):
      global finder
      appuifw.app.body.bind(EKeySelect, None)
      appuifw.app.exit_key_handler = self.oldexit
      self.lock.signal()
      finder = False

   def take_picture(self):
      global finder, gsmloc
      fname = rxl_line(gsmloc, fname=True)
      camera.stop_finder()
      img = camera.take_photo(size=CellCam.SIZE)
      appuifw.note(u"Good Shot!",'info')
      w, h = appuifw.app.body.size
      appuifw.app.body.blit(img,target=(0, 0, w, 0.75 * w), scale = 1)
      appuifw.app.body.text((10,20), u"Writing Image:", fill=color)
      appuifw.app.body.text((10,40), fname, fill=color)
      img.save(pic_path + fname)
      self.finish()
      
   def finder_cb(self, im):
      global gsmloc
      info = rxl_line(gsmloc)
      im.text((10,20), info, fill=color)
      #im.text((10,40), u"Feature test: " + unicode(self.timeout), fill=color)
      appuifw.app.body.blit(im)
      

      
img=Image.new(MAXSIZE)
img_dbl=Image.new(MAXSIZE)
window = topWindow.TopWindow()
#image_splash = graphics.Image.open(u'c:\\Data\Others\PyNetMony\\pynetmony.jpg')
#some text measurements
#(box,TLENGTH_199DBM,numb) = img.measure_text(u'-199dDm')
#(box,TLENGTH_RXL,numb) = img.measure_text(u'-199')
#(box,TLENGTH_WPAPSK,numb) = img.measure_text(u'WpaPsk')
#(box,TLENGTH_C,numb) = img.measure_text(u'C')
(box,TLENGTH_TIME,numb) = img.measure_text(u'23:59:59', font=headfont)
#(box,numb,numb) = img.measure_text(u'ABCDEFGHIJKLMNOPQRSTUVWXY09,()')
#TABHEIGHT = box[3] - box[1] + 2
(box,numb,numb) = img.measure_text(u'ABCDEFGHIJKLMNOPQRSTUVWXYabcdefghijklmnopqrstuvwxyz09,;!#()', font=myfont)
TABHEIGHT = LINEHEIGHT = box[3] - box[1] + 0
LINEY = -box[1] + 1

# Headline size: frame; total height; y position for text
HDLFRAME = 2
(HDLBOX,numb,numb) = img.measure_text(u'C: 99999 W: G:', font=headfont)
HDLH = HDLBOX[3] - HDLBOX[1] + 2*HDLFRAME
HDLY = -HDLBOX[1] + HDLFRAME
HEADHEIGHT = 2*HDLH + 2*HDLFRAME
del HDLBOX, box, numb

def mainmenu_setup():
   global logger, gpson, cam
   logmenu = [(u"Start 2G/3G Logging", toggle_log),
            (u"Stop 2G/3G Logging", toggle_log)]
   gpsmenu = [(u"Start GPS", toggle_gps), (u"Stop GPS", toggle_gps)]
   cammenu = [[], [(u"Site Photo...", cellphoto)]]
   wlogmenu = [(u"Start WLAN Logging", toggle_wlog), (u"Stop WLAN Logging", toggle_wlog)]
   appuifw.app.menu = [logmenu[logger != None],
                  wlogmenu[wlogger != None],
                  gpsmenu[gpson]] + \
            [(u"Database", ((u"Edit a cell", cell_edit), (u"Add a cell", cell_add), (u"Calculate Neighbour", neighbour_start), (u"Kismet Export All", kismet_export), (u"Kismet Export Today", kismet_export_today), (u"WLAN to KML",wlan2kml)))] + \
            [(u"Map", ((u"Upload Position", register), (u"Show Cell (clf) Position", cell_map), (u"Show GPS Position", own_map),(u"Show WPS Position", wps_map), (u"Google Cell Coordinates", search_location), (u"Show Google Position", icell_map), (u"Get Skyhook Position", skyhook)))] + \
            cammenu[cam] + \
                  [(u"Settings", ((u"Orientation", rotate), (u"Settings 1...", setup), (u"Settings 2...", setup2), (u"Voice Setup...", setup3), (u"Check for Updates", checkver), (u"Set Default APN", set_accesspoint), (u"Unset Default APN", unset_accesspoint)))]
               

def menus_setup():
   global tab, tab_max
   mainmenu_setup()
   tabs = [u"NetMon", u"Graph", u"History", u"GPS", u"WLAN", u"CellInfo", u"Radar", u"Map", u"BT", u"Stats", u"Neighbour", u"Newclf", u"About"]
   tab_max = len(tabs)
   appuifw.app.set_tabs(tabs, set_tab)
   appuifw.app.activate_tab(tab)
   
   
def unset_accesspoint():
   global apid, apo
   a = open(def_apn_file,'w')
   a.write(repr(None))
   a.close()
   apo = None
   apid = None
   appuifw.note(u"Default access point is unset ", "info")
   
def set_accesspoint():
   global apid, apo
   apid = socket.select_access_point()
   if appuifw.query(u"Set as default access point","query") == True:
      f = open(def_apn_file,'w')
      f.write(repr(apid))
      f.close()
      appuifw.note(u"Saved default access point ", "info")
      apo = socket.access_point(apid)
      socket.set_default_access_point(apo)
   
def is_not_control(input):
   string = ""
   for zeichen in input:
      c = ord(zeichen)
      if not ((c < 32) or (126 < c < 160) or (9116 < c < 9153)):
         string += zeichen
   return string
   
def signal_ok():
   try:
      bars = sysinfo.signal_bars()
      if bars > 0:
         return True
      else:
         return False
   except:
      return False 

def number2word(e_zahl,lang):
   gruppe = []
   text = ''
   if lang == 0:
      return e_zahl
   elif lang == 1:
      kleiner20 = ['ein','zwei','drei','vier','fuenf','sechs','sieben','acht','neun','zehn','elf','zwoelf','dreizehn','vierzehn','fuenfzehn','sechzehn','siebzehn','achtzehn','neunzehn']
      zehner = ['zehn','zwangzig','dreissig','vierzig','fuenfzig','sechszig','siebzig','achtzig','neunzig']
      singular = ['s','tausend','e Million','e Milliarde','e Billion']
      plural = ['','tausend','millionen','milliarden','billionen']
      nulleins = ['s','stausend','s Millionen','s Milliarden','s Billionen']
      huni = ' hundert '
      und = ' und '
      def sprich_dreier(zahl):
         h = zahl/100
         r = zahl%100
         z = r/10
         e = zahl%10
         erg = ''
         ### begin
         if h > 0:
            erg = erg+kleiner20[h-1]+huni
         if r > 0:
            if r < 20:
               erg = erg+kleiner20[r-1]
            else:
               if e > 0:
                  erg = erg+kleiner20[e-1]
               if e > 0 and z > 0:
                  erg = erg + und
               if z > 0:
                  erg = erg+zehner[z-1]
         return erg
   else:
      kleiner20 = ['one','two','three','four','five','six','seven','eight','nine','ten','eleven','twelve','thirteen','fourteen','fifteen','sixteen','seventeen','eighteen','nineteen']
      zehner = ['ten','twenty','thirty','fourty','fifty','sixty','seventy','eighty','ninety']
      singular = ['s','tausend','e Million','e Milliarde','e Billion']
      plural = ['','thousend','million','billion','trillion']
      nulleins = ['',' thousand',' million',' billion',' trillion']
      huni = ' hundred '
      und = 'and'
      def sprich_dreier(zahl):
         h = zahl/100
         r = zahl%100
         z = r/10
         e = zahl%10
         erg = ''
         ### begin
         if h > 0:
            erg = erg+kleiner20[h-1]+huni
         if r > 0:
            if r < 20:
               erg = erg+kleiner20[r-1]
            else:
               if z > 0:
                  erg = erg+zehner[z-1]+' '
               if e > 0:
                  erg = erg+kleiner20[e-1]
               if e > 0 and z > 0:
                  erg = erg
            
         return erg
   
   while e_zahl > 0:
      gruppe.append(e_zahl%1000)
      e_zahl = e_zahl/1000


   t_i = len(gruppe)
   while t_i > 0:
      if gruppe[t_i-1] > 0:
         text = text+sprich_dreier(gruppe[t_i-1])
         if gruppe[t_i-1] == 1:
            text = text+singular[t_i-1] + ' '
         elif str(gruppe[t_i-1]).find('01') == 1:
            text = text+nulleins[t_i-1]+' '      
         else:
            text = text+plural[t_i-1]+' '
      t_i -=1
   return text
   
def binaere_suche(liste, eingabe,width=17):
   maxindex = len(liste) - 1
   suche_erfolgreich = False
   index = 0
   while not suche_erfolgreich and index <= maxindex:
      mitte = index + ((maxindex - index)/2)
      if liste[mitte][:width] == eingabe:
         suche_erfolgreich = True
      elif eingabe < liste[mitte][:width]:
         maxindex = mitte - 1
      else:
         index = mitte + 1
   if suche_erfolgreich:
      return mitte
   else:
      return -1

def uptime(start):
   diff = time.time()-start
   dmin = math.floor(diff/60)
   dday = int(math.floor(diff/86400))
   dhour = int(math.floor((dmin - dday*24*60)/60))
   dmin = int(math.floor(dmin - dhour*60 - dday*24*60))
   dmin = unicode('%02i'%dmin)
   dhour = unicode('%02i'%dhour)
   dday = unicode(dday)
   return (dday,dhour,dmin)

def fetch_latlon(bytestring):
   global gsm_url, apo
   if signal_ok():
      if apo == None:
         set_accesspoint()
      try:
         data = urllib.urlopen(gsm_url,bytestring)
         response = data.read().encode('hex')
      except:
         response = '1'
      apo.stop()
      if len(response) > 14:
         return response
      else:
         return -1
   else:
      return -1

def convert_bytestring(response):
   if response > -1:
      def check(data):
         result = int(data, 16) 
         if result & 2**31: 
            result = -((result ^ (2**32 - 1)) + 1)
         return result
      lat = check(response[14:22])/1000000.
      lon = check(response[22:30])/1000000.
      return (lat,lon)
   else:
      return ('999.99999', '999.99999')
   
def get_cell_location(cid,lac,mnc,mcc):
   b_string = '000E00000000000000000000000000001B0000000000000000000000030000'+ \
   hex(cid)[2:].zfill(8)+ \
   hex(lac)[2:].zfill(8)+ \
   hex(mnc)[2:].zfill(8)+ \
   hex(mcc)[2:].zfill(8)+ \
   'FFFFFFFF00000000'
   bytes = fetch_latlon(b_string.decode('hex'))
   (a,b) = convert_bytestring(bytes)
   #appuifw.note(u"GSM Coordinates: "+unicode(a)+u" "+unicode(b),'info')
   return (a,b)
   
def search_location():
   global gsmloc
   if gsmloc is None:
      appuifw.note(u"Cell  location invalid!",'error')
   else:
      (mcc, mnc, lac, cid) = gsmloc
      #(cid, rnc) = decode_cid(cid)
      (a,b)= get_cell_location(cid,lac,mnc,mcc)
      appuifw.note(u"GSM Coordinates: "+unicode(a)+u" "+unicode(b),'info')
   
def search_location_for_clf():
   global clf_form
   cid = int(clf_form[0][2])
   lac = int(clf_form[1][2])
   mnc = int(clf_form[6][2][-2:])
   mcc = int(clf_form[6][2][:3])
   (a,b)= get_cell_location(cid,lac,mnc,mcc)
   if (-90 < a < 90) and (-180 < b < 180) and (unicode(clf_form[7][2]) <> u'-1'):
      clf_form[4] = (u'LAT: ','text',unicode("%.6f" % a))
      clf_form[5] = (u'LON: ','text',unicode("%.6f" % b))
      clf_form[7] = (u'POS-RAT: ','text',u"1")
   else:
      appuifw.note(u"No valid coordinates found or position already fixed!",'info')

def take_gps_for_cell():
   global clf_form
   if (len(gpsdata) == 15) and (gpsdata[14] > 2) and (unicode(clf_form[7][2]) <> u'-1'):
      try:
         lat = '%0.6f'%float(gpsdata[1])
         lon = '%0.6f'%float(gpsdata[2])
         clf_form[4] = (u'LAT: ','text',unicode(lat))
         clf_form[5] = (u'LON: ','text',unicode(lon))
         clf_form[7] = (u'POS-RAT: ','text',u"-1")
      except:
         appuifw.note(u"No valid GPS coordinates found!",'info')
   else:
      appuifw.note(u"No GPS coordinates found or position already fixed!",'info')

def rotate():
   if appuifw.app.orientation == 'landscape':
      appuifw.app.orientation = 'portrait'
   else:
      appuifw.app.orientation = 'landscape'
   if tab==6:   
      appuifw.app.body=lb

def setup():
   global btscan, wscan, bg, border, linecol, grid, headcol, color, headbg, headfont, myfont, \
         TABHEIGHT, LINEHEIGHT, LINEY, HDLFRAME, HDLH, HDLY, HEADHEIGHT, TLENGTH_TIME
   # Bug in Form(): manually hide Tabs
   appuifw.app.set_tabs([], None)
   SetupForm.execute( )
   if config['Refresh']<9:
      wscan = []
   if bt and (config['BT_SCAN'] > 0):
      pass
      #if blues.getstate() == 0:
      #   blues.on()
   if config['BT_SCAN'] == 0:
      btscan = []
   if config['COLOR_THEME'] == Setup.COLOR_THEME_BLUE:
      bg=(0,0,60)
      border=bg
      color=(255,255,255)
      linecol=(255,128,128)
      headcol=(255,255,255)
      headbg=(255,255,255)
      grid=(127,127,127)
   elif config['COLOR_THEME'] == Setup.COLOR_THEME_BLACK:
      bg=(0,0,0)
      border=bg
      color=(255,255,255)
      linecol=(255,128,128)
      headcol=(255,255,255)
      headbg=(255,255,255)
      grid=(127,127,127)
   elif config['COLOR_THEME'] == Setup.COLOR_THEME_RED:
      bg=(80,0,0)
      border=bg
      color=(255,255,255)
      linecol=(255,128,128)
      headcol=(255,255,255)
      headbg=(255,255,255)
      grid=(127,127,127)
   elif config['COLOR_THEME'] == Setup.COLOR_THEME_GREEN:
      bg=(0,60,0)
      border=bg
      color=(255,255,255)
      linecol=(255,128,128)
      headcol=(255,255,255)
      headbg=(255,255,255)
      grid=(127,127,127)
   elif config['COLOR_THEME'] == Setup.COLOR_THEME_MAGENTA:
      bg=(226,0,116)
      border=bg
      color=(255,255,255)
      linecol=(60,60,60)
      headcol=(255,255,255)
      headbg=(255,255,255)
      grid=(80,80,80)
   elif config['COLOR_THEME'] == Setup.COLOR_THEME_WHITE:
      bg=(255,255,255)
      border=bg
      color=(0,0,0)
      linecol=(128,0,0)
      headcol=(0,0,0)
      headbg=(0,0,0)
      grid=(127,127,127)
   size,offset = appuifw.app.layout(appuifw.EMainPane)
   if size[0] == 800:
      if config['FONT_SIZE'] == Setup.FONT_SIZE_SMALL:
         myfont = (None,16,0)
         headfont = (None,16,0)
      elif config['FONT_SIZE'] == Setup.FONT_SIZE_MEDIUM:
         myfont = (None,18,FONT_BOLD)
         headfont = (None,18,FONT_BOLD)
      elif config['FONT_SIZE'] == Setup.FONT_SIZE_LARGE:
         myfont = (None,20,FONT_BOLD)
         headfont = (None,20,FONT_BOLD)
      elif config['FONT_SIZE'] == Setup.FONT_SIZE_XLARGE:
         myfont = (None,22,FONT_BOLD)
         headfont = (None,22,FONT_BOLD)
      (box,TLENGTH_TIME,numb) = img.measure_text(u'23:59:59', font=headfont)
      (box,numb,numb) = img.measure_text(u'ABCDEFGHIJKLMNOPQRSTUVWXYabcdefghijklmnopqrstuvwxyz09,;!#()', font=myfont)
      TABHEIGHT = LINEHEIGHT = box[3] - box[1] + 0
      LINEY = -box[1] + 1
      # Headline size: frame; total height; y position for text
      HDLFRAME = 2
      (HDLBOX,numb,numb) = img.measure_text(u'C: 99999 W: G:', font=headfont)
      HDLH = HDLBOX[3] - HDLBOX[1] + 2*HDLFRAME
      HDLY = -HDLBOX[1] + HDLFRAME
      HEADHEIGHT = 2*HDLH + 2*HDLFRAME
      del HDLBOX, box, numb
   elif size[0] < 800:
      if config['FONT_SIZE'] == Setup.FONT_SIZE_SMALL:
         myfont = (None,12,0)
         headfont = (None,12,0)
      elif config['FONT_SIZE'] == Setup.FONT_SIZE_MEDIUM:
         myfont = (None,14,FONT_BOLD)
         headfont = (None,14,FONT_BOLD)
      elif config['FONT_SIZE'] == Setup.FONT_SIZE_LARGE:
         myfont = (None,16,FONT_BOLD)
         headfont = (None,16,FONT_BOLD)
      elif config['FONT_SIZE'] == Setup.FONT_SIZE_XLARGE:
         myfont = (None,18,FONT_BOLD)
         headfont = (None,18,FONT_BOLD)
      (box,TLENGTH_TIME,numb) = img.measure_text(u'23:59:59', font=headfont)
      (box,numb,numb) = img.measure_text(u'ABCDEFGHIJKLMNOPQRSTUVWXYabcdefghijklmnopqrstuvwxyz09,;!#()', font=myfont)
      TABHEIGHT = LINEHEIGHT = box[3] - box[1] + 0
      LINEY = -box[1] + 1
      # Headline size: frame; total height; y position for text
      HDLFRAME = 2
      (HDLBOX,numb,numb) = img.measure_text(u'C: 99999 W: G:', font=headfont)
      HDLH = HDLBOX[3] - HDLBOX[1] + 2*HDLFRAME
      HDLY = -HDLBOX[1] + HDLFRAME
      HEADHEIGHT = 2*HDLH + 2*HDLFRAME
      del HDLBOX, box, numb
      
   menus_setup()
   
def setup2():
   # Bug in Form(): manually hide Tabs
   appuifw.app.set_tabs([], None)
   Setup2Form.execute( )
   menus_setup()
   
def setup3():
   # Bug in Form(): manually hide Tabs
   appuifw.app.set_tabs([], None)
   Setup3Form.execute( )
   menus_setup()

def set_tab(newtab):
   global tab, gui
   tab = newtab
   gui.signal()
   
def naive_xml_parser(key, xml):
   key = key.lower()
   for tag in xml.split("<"):
      tokens = tag.split()
      if tokens and tokens[0].lower().startswith(key):
         return tag.split(">")[1].strip()
   return None

def checkver():
   global SIS_VERSION
   ver_url = 'http://www.daniel-perna.de/pynetmony/pnmchk.php'
   cur_ver = SIS_VERSION
   if signal_ok():
      if apo == None:
         set_accesspoint()
      try:
         data = urllib.urlopen(ver_url)
         new_ver = data.readlines()
         apo.stop()
         register(False)
         new_ver[0] = new_ver[0].rstrip()
         new_ver[1] = new_ver[1].rstrip()
         #appuifw.note(unicode(new_ver[1]),'info')
         if DEFAULT_VERSION == new_ver[1]:
            if cur_ver == new_ver[0]:
               appuifw.note(u'PyNetMony is up to date.','info')
            elif cur_ver > new_ver[0]:
               appuifw.note(u'You are using a new beta version.','info')
            elif new_ver[0] == 'error':
               appuifw.note(u'Service currently unavailable.','error')
            else:
               appuifw.query(u'A new version of PyNetMony (' + new_ver[0] + ') is available! See http://pynetmony.googlepages.com for release notes.','query')
               update()
         else:
            appuifw.query(u'Your version is too old! Download and install the new version from http://pynetmony.googlepages.com','query')
      except Exception, error:
         apo.stop()
         appuifw.note(u"Fatal Error: "+unicode(error),'error')
   else:
      appuifw.note(u'No signal!','error')

def update():
   global do_update
   update_possible = 0
   if os.path.exists(file_path+'pynetmony.bak'):
      if appuifw.query(u'pynetmony.bak exists. delete?','query'):
         os.remove(file_path+'pynetmony.bak')
         update_possible = 1
      else:
         update_possible = 0
   else:
      update_possible = 1
   if update_possible == 1:
      if appuifw.query(u'Do you really want to download the update (140kb)?','query'):
         do_update = True
         appuifw.note(u'PyNetMony will shut down now and start updating','info')
         e32.ao_sleep(0.05)
         finish()

def register(MESS=True):
   global SIS_VERSION, wps_coords, userid
   pos_ok = False
   if (gpson == 1) and (len(gpsdata) == 15):
      if gpsdata[14] > 2:
         lat = unicode("%.6f" % gpsdata[1])
         lon = unicode("%.6f" % gpsdata[2])
         pos_ok = True
      elif wps_count > 0:
         lat = wps_coords[0]
         lon = wps_coords[1]
         pos_ok = True
   elif (wps_count > 0):
      lat = wps_coords[0]
      lon = wps_coords[1]
      pos_ok = True
   elif cell_lat != u'999.99999':
      lat = unicode("%.6f" % float(cell_lat))
      lon = unicode("%.6f" % float(cell_lon))
      pos_ok = True
   else:
      if gsmloc is None:
         lat = lon = '0.000000'
      else:
         (mcc, mnc, lac, cid) = gsmloc
         (a,b) = get_cell_location(cid,lac,mnc,mcc)
         if (-90 < a < 90) and (-180 < b < 180):
            lat = unicode("%.6f" % a)
            lon = unicode("%.6f" % b)
         else:
            lat = lon = '0.000000'
      pos_ok = True
   if pos_ok and signal_ok():
      class MyOpener(urllib.FancyURLopener):
         version = 'PyNetMony '+SIS_VERSION+' - '+sysinfo.sw_version()
      myopener = MyOpener()
      identifier = imei
      url = 'http://www.daniel-perna.de/pynetmony/register.php?identifier='+str(identifier)[:15]+'&lat='+lat+'&lon='+lon+'&aps='+str(len(wlan_list)-1)+'&bts='+str(len(bt_list)-1)+'&cells='+str(len(clf)-1)
      if apo == None:
         set_accesspoint()
      try:
         page = myopener.open(url)
         response = page.readlines()
         apo.stop()
      except Exception, error:
         if MESS:
            appuifw.note(u"Fatal Error: "+unicode(error),'error')
         response = ['Could not connect to Server','','','']
         apo.stop()
      if response[0] == 'Operation successful\r\n':
         if MESS:
            appuifw.note(u'Position Upload successful!\nUserID: '+unicode(response[1]),'info')
            userid = unicode(response[1])
         else:
            userid = unicode(response[1])
      else:
         if MESS:
            appuifw.note(u'Error: '+unicode(response[0]),'error')
         else:
            pass
   else:
      if MESS:
         appuifw.note(u'Error: Position unknown or no signal!','error')
      else:
         pass

def cell_map():
   appuifw.app.activate_tab(7)
   set_tab(7)
   if (cell_lat != u'999.99999'):
      new_map(cell_lat, cell_lon, zoom=config['MAPZOOM'], size=gl_size)
   else:
      appuifw.note(u"No valid coordinates found!",'error')
   #thread.start_new_thread(new_map,(cell_lat, cell_lon))
   
def wps_map():
   if config2['WPS']>=Setup2.WPS_ON:
      appuifw.app.activate_tab(7)
      set_tab(7)
      if (wps_coords[0] != u'NaN'):
         new_map(wps_coords[0], wps_coords[1], zoom=config['MAPZOOM'], size=gl_size)
      else:
         appuifw.note(u"No valid coordinates found!",'error')
   else:
      appuifw.note(u"WPS is switched off!",'error')
   
def own_map():
   if (len(gpsdata) == 15) and (gpsdata[14] > 2):
      appuifw.app.activate_tab(7)
      set_tab(7)
      new_map(gpsdata[1], gpsdata[2], zoom=config['MAPZOOM'], size=gl_size)
      
def icell_map():
   global gsmloc
   appuifw.app.activate_tab(7)
   set_tab(7)
   if gsmloc is None:
      appuifw.note(u"Cell location invalid!!",'error')
   else:
      (mcc, mnc, lac, cid) = gsmloc
      (a,b)= get_cell_location(cid,lac,mnc,mcc)
      if (-90 < a < 90) and (-180 < b < 180):
         new_map(a, b, zoom=config['MAPZOOM'], size=gl_size)
      else:
         appuifw.note(u"No valid coordinates found!",'error')
      
def new_cell_map(cid,lac,mnc,mcc):
   appuifw.app.activate_tab(7)
   set_tab(7)
   (a,b)= get_cell_location(cid,lac,mnc,mcc)
   if (-90 < a < 90) and (-180 < b < 180):
      new_map(a, b, zoom=config['MAPZOOM'], size=gl_size)
   else:
      appuifw.note(u"No valid coordinates found!",'error')

def new_map(latitude, longitude, zoom=3, size=(240,320), radius=""):
   global apo, status
   #addr = appuifw.query(u"Address:", "text")
   #if not addr:
   #   return
   if apo == None:
      set_accesspoint()
   (w, h) = size
   params = {"latitude": latitude,
           "longitude": longitude,
           "appid": APP_ID,
           "image_type": "png",
           "image_height": h,
           "image_width": w,
           "zoom": zoom,
           "radius": radius}
   if signal_ok():         
      show_text(u"Loading map...")
      try:
         url = MAP_URL + urllib.urlencode(params)
         res = urllib.urlopen(url).read()
      except Exception, error:
         show_text(u"Network error")
         apo.stop()
         status = None
         appuifw.note(u"Fatal Error: "+unicode(error),'error')
         return

      img_url = naive_xml_parser("result", res)
      if img_url:
         show_text(u"Loading map......")
         load_image(img_url)
         handle_redraw(canvas.size)
         apo.stop()
      else:
         msg = naive_xml_parser("message", res)
         show_text(u"%s" % msg)
         apo.stop()
   else:
      appuifw.note(u'No signal!','error')
      
def load_image(url):
   global mapimg, map_x, map_y, status
   res = urllib.urlopen(url).read()
   f = file(MAP_FILE, "w")
   f.write(res)
   f.close()
   mapimg = graphics.Image.open(MAP_FILE)
   map_x = mapimg.size[0] / 2 - canvas.size[0] / 2
   map_y = mapimg.size[1] / 2 - canvas.size[1] / 2
   status = None
   
def vibration(count):
   if miso_ok:
      try:
         for i in range(count):
            miso.vibrate(800,100)
            e32.ao_sleep(0.5)   
      except:   
         pass

   
def show_text(txt):
   global status
   status = txt
   handle_redraw(canvas.size)
   
def toggle_gps():
   global gpson, locreq, gpsdata
   if not locreq:
      appuifw.note(u"Module Locationrequestor not installed!",'error')
      return
   if not gpson:
      gpsdata = [0, 'Starting GPS...']
      gpson = 1
      mainmenu_setup()
      thread.start_new_thread(gps_worker,())
   else:
      gpson = 0
      mainmenu_setup()
      
def cell_edit():
   global clf_form
   ecid=appuifw.query(u"Enter Cell ID", "number")
   elac=appuifw.query(u"Enter LAC", "number")
   if ecid and elac:
      ecid = '%05i' % (ecid)
      elac = '%05i' % (elac)
      ecell_found = False
      cell=[]
      for i_cell_edit in range(len(clf)):
         if (clf[i_cell_edit][6:11]==ecid) and (clf[i_cell_edit][12:17]==elac):
            cell = clf[i_cell_edit].split(';')
            cell=map(unicode,cell)
            ecell_found = True
            break
      if ecell_found:
         clf_form=appuifw.Form([(u'Cell ID: ','text',cell[1]),(u'LAC: ','text',cell[2]),(u'RNC: ','text',cell[3]),(u'Info: ','text',cell[7]),(u'LAT: ','text',cell[4]),(u'LON: ','text',cell[5]),(u'NET: ','text',cell[0]),(u'POS-RAT: ','text',cell[6])],appuifw.FFormAutoFormEdit)
         clf_form.menu = [(u"Google for coordinates", search_location_for_clf),(u"Take GPS coordinates", take_gps_for_cell)]
         appuifw.app.set_tabs([], None)
         #clf_form.save_hook = save_cell
         clf_form.execute()
         if appuifw.query(u'Do you really want to save?', 'query'):
            cell[1] = unicode(clf_form[0][2])
            cell[2] = unicode(clf_form[1][2])
            cell[3] = unicode(clf_form[2][2])
            cell[7] = unicode(clf_form[3][2])
            cell[4] = unicode(clf_form[4][2])
            cell[5] = unicode(clf_form[5][2])
            cell[0] = unicode(clf_form[6][2])
            cell[6] = unicode(clf_form[7][2])
            clf[i_cell_edit] = ";".join(cell)
            appuifw.note(u"Edited cell saved to clf", "conf")
      else:
         appuifw.note(u"Cell not found", "error")
      menus_setup()
         
def cell_add():
   global clf_form, clf
   cell=[]
   cell.append(u'26207')
   cell.append(u'12345')
   cell.append(u'12345')
   cell.append(u'12345')
   cell.append(u'50.88547')
   cell.append(u'8.88547')
   cell.append(u'2')
   cell.append(u'Site Info')
   cell.append(u'0')
   clf_form=appuifw.Form([(u'Cell ID: ','text',cell[1]),(u'LAC: ','text',cell[2]),(u'RNC: ','text',cell[3]),(u'Info: ','text',cell[7]),(u'LAT: ','text',cell[4]),(u'LON: ','text',cell[5]),(u'NET: ','text',cell[0]),(u'POS-RAT: ','text',cell[6])],appuifw.FFormAutoFormEdit)
   clf_form.menu = [(u"Google for coordinates", search_location_for_clf),(u"Take GPS coordinates", take_gps_for_cell)]
   appuifw.app.set_tabs([], None)
   #clf_form.save_hook = save_cell
   clf_form.execute()
   if appuifw.query(u'Do you really want to add a new cell?', 'query'):
      cell[1] = unicode(clf_form[0][2])
      cell[2] = unicode(clf_form[1][2])
      cell[3] = unicode(clf_form[2][2])
      cell[7] = unicode(clf_form[3][2])
      cell[4] = unicode(clf_form[4][2])
      cell[5] = unicode(clf_form[5][2])
      cell[0] = unicode(clf_form[6][2])
      cell[6] = unicode(clf_form[7][2])
      clf.append(";".join(cell)+chr(13)+chr(10))
      appuifw.note(u"Cell added to clf", "conf")
   menus_setup()
      
   
def save_cell():
   pass

def query_clf(mcc, mnc, cid, lac, rnc, umts):
   global cell_description, cell_lon, cell_lat, oldumts, oldqnet, clf_name, clf_found, clf, cell_searching, \
         newcells, clf_saving, new_cells_list, new_cells_lb, new_cells_updated, net_counter, netmode_counter
   cell_found = False
   cell_searching = True
   new_cells_updated = False
   qnet = '%03i%03i' % (mcc, mnc)
   qcid = '%05i' % (cid)
   qlac = qqlac= '%05i' % (lac)
   if rnc == 'n/a':
      qrnc = '00000'
   else:
      qrnc = '%05i' % (rnc)
   if (umts != oldumts) or (qnet != oldqnet):
      if umts != oldumts:
         netmode_counter += 1
      if qnet != oldqnet:
         net_counter += 1
      oldumts = umts
      oldqnet = qnet
      if len(clf_name) > 3:
         try:
            clf_saving = True
            file = open(clf_name,'w')
            file.writelines(clf)
            file.close()
            clf_saving = False
         except:
            clf_saving = False
      if config['CLF'] == Setup.CLF_DEVICE:
         clf_name = clf_path_c+qnet+"_"+band[umts]+".clf"
      else:
         clf_name = clf_path_e+qnet+"_"+band[umts]+".clf"
      cell_description = unicode('Loading '+clf_name)
      try:
         clf_saving = True
         clf = []
         #eclf = []
         file = open(clf_name)
         clf = file.readlines()
         file.close()
         #for query in eclf:
         #   clf.append(unicode(query))
         #eclf = []
         clf_found = True
         clf_saving = False
      except IOError:
         clf = []
         header = u'//cell list exchange format v3.0//;;;;;;;;'+chr(13)+chr(10)
         clf.append(header)
         cell_description = unicode(clf_name)+u'Started new CLF'
         clf_found = True
         cell_lat = u'999.99999'
         cell_lon = u'999.99999'
         clf_saving = False
   
   if clf_found:
      cell_description = u'searching...'
      if qnet == '262007':
         qlac = qlac[:3]
         for query in clf:
            if (query[:6]==qnet) and (query[7:12]==qcid) and (query[13:16]==qlac):
               splitter = query.split(';')
               if len(splitter[4]) > 1 and len(splitter[5]) > 1 and splitter[4] <> "NaN":
                  cell_lat = unicode(splitter[4])
                  cell_lon = unicode(splitter[5])
               else:
                  cell_lat = u'999.99999'
                  cell_lon = u'999.99999'
               cell_description = unicode(splitter[7])
               cell_found = True
               if config['CellNotify']==Setup.SOUND_VOICE and config['Voice']==Setup.VOICE_BAND_CLF:
                  thread.start_new_thread(reader,(cell_description,))
               break
      elif qnet == '262003':
         qlac = qlac[4:5]
         for query in clf:
            if (query[:6]==qnet) and (query[7:12]==qcid) and (query[17:18]==qlac):
               splitter = query.split(';')
               if len(splitter[4]) > 1 and len(splitter[5]) > 1 and splitter[4] <> "NaN":
                  cell_lat = unicode(splitter[4])
                  cell_lon = unicode(splitter[5])
               else:
                  cell_lat = u'999.99999'
                  cell_lon = u'999.99999'
               cell_description = unicode(splitter[7])
               cell_found = True
               if config['CellNotify']==Setup.SOUND_VOICE and config['Voice']==Setup.VOICE_BAND_CLF:
                  thread.start_new_thread(reader,(cell_description,))
               break
      elif config2['LAC_CHECK']==Setup2.LAC_CHECK_ON:
         for query in clf:
            if (query[:6]==qnet) and (query[7:12]==qcid) and (query[13:18]==qlac):
               splitter = query.split(';')
               if len(splitter[4]) > 1 and len(splitter[5]) > 1 and splitter[4] <> "NaN":
                  cell_lat = unicode(splitter[4])
                  cell_lon = unicode(splitter[5])
               else:
                  cell_lat = u'999.99999'
                  cell_lon = u'999.99999'
               cell_description = unicode(splitter[7])
               cell_found = True
               if config['CellNotify']==Setup.SOUND_VOICE and config['Voice']==Setup.VOICE_BAND_CLF:
                  thread.start_new_thread(reader,(cell_description,))
               break
      else:
         for query in clf:
            if (query[:6]==qnet) and (query[7:12]==qcid):
               splitter = query.split(';')
               if len(splitter[4]) > 1 and len(splitter[5]) > 1 and splitter[4] <> "NaN":
                  cell_lat = unicode(splitter[4])
                  cell_lon = unicode(splitter[5])
               else:
                  cell_lat = u'999.99999'
                  cell_lon = u'999.99999'
               cell_description = unicode(splitter[7])
               cell_found = True
               if config['CellNotify']==Setup.SOUND_VOICE and config['Voice']==Setup.VOICE_BAND_CLF:
                  thread.start_new_thread(reader,(cell_description,))
               break                           
      if not cell_found:
         cell_description = u'New Cell found on '+unicode(time.strftime("%Y/%m/%d"))+u' '+unicode(time.strftime("%H:%M:%S"))
         if (len(gpsdata) == 15) and (gpsdata[14] > 2):
            try:
               cell_lat = '%0.6f'%float(gpsdata[1])
               cell_lon = '%0.6f'%float(gpsdata[2])
               gps = cell_lat+u';'+cell_lon
            except:
               cell_lat = u'999.99999'
               cell_lon = u'999.99999'
               gps = u';'
         else:
            gps = u';'
            cell_lat = u'999.99999'
            cell_lon = u'999.99999'
         line = unicode(qnet)+u';'+unicode(qcid)+u';'+unicode(qqlac)+u';'+unicode(qrnc)+u';'+unicode(gps)+u';0;'+cell_description+u';0'+chr(13)+chr(10)
         clf.append(line)
         new_cells_list.append(line)
         newcells += 1
         new_cells_updated = True
         if config['Light']==Setup.LIGHT_NEW_CELL:
            e32.reset_inactivity()
         if config['CellNotify']==Setup.SOUND_VOICE and config['Voice']==Setup.VOICE_BAND_CLF:
            thread.start_new_thread(reader,(cell_description,))
         if config['CellNotify']==Setup.SOUND_VOICE_NEW:
            thread.start_new_thread(reader,(u'7',))
   cell_searching = False
   #new_cells_updated = True

### WPS

def calculate_wps_lat_lon():
   global wps_list, wps_coords, wps_fix, wps_count, wps_list_radar
   lat_sum = 0
   lon_sum = 0
   devider = 0
   
   for i in range(len(wps_list)):
      if wps_list[i][2] > -70:
         lat_sum += 5*wps_list[i][0]
         lon_sum += 5*wps_list[i][1]
         devider += 5
      elif (wps_list[i][2] <= -70) and (wps_list[i][2] >= -84):
         lat_sum += 3*wps_list[i][0]
         lon_sum += 3*wps_list[i][1]
         devider += 3
      else:
         lat_sum += wps_list[i][0]
         lon_sum += wps_list[i][1]
         devider += 1
   try:
      if devider > 0:
         lat = '%0.6f'%(lat_sum/devider)
         lon = '%0.6f'%(lon_sum/devider)
         #wps_fix = '%0.0f'%(100*devider/(3*len(wps_list)))
      else:
         lat = 'NaN'
         lon = 'NaN'
   except:
      lat = 'NaN'
      lon = 'NaN'
   wps_fix = devider
   wps_count = 5*len(wps_list)
   wps_list_radar = wps_list
   wps_list = []
   wps_coords = [lat, lon]

def query_wps(wlanset):
   global wps_list
   i = -1
   i = binaere_suche(wlan_list, wlanset['BSSID'])
   if i > -1:
      wlist = wlan_list[i].split(';')
      if (wlist[1] <> 'NaN') and (wlist[2] <> 'NaN') and (int(wlist[8]) > -150):
         wps_list.append([float(wlist[1]),float(wlist[2]),int(wlanset['RxLevel']),wlanset['SSID'],wlanset['SecurityMode']])
         ##################################### liste um zwei elemente erweitert

def query_wlan(wlanset):
   global wlan_list, newwlans, wlangpsupdate, wlanwpsupdate, wlancpsupdate, wlanssidupdate, maxaprxl
   i = -1
   if len(gpsdata) == 15:
      try:
         wlan_lat = '%0.6f'%float(gpsdata[1])
         wlan_lon = '%0.6f'%float(gpsdata[2])
      except:
         wlan_lat = gpsdata[1]
         wlan_lon = gpsdata[2]
      
   if int(wlanset['RxLevel']) > maxaprxl:
      maxaprxl = int(wlanset['RxLevel'])
   i = binaere_suche(wlan_list, wlanset['BSSID'])
   if (config['WLAN_NOTIFY'] == Setup.WLAN_NOTIFY_BSSID) and (config2['BSSID_NOTIFY'] == wlanset['BSSID']):
      thread.start_new_thread(reader,(config3['BSSID'],))
   if i > -1:
      wlist = wlan_list[i].split(';')
      
      if (len(gpsdata) == 15) and (gpsdata[14] > 2) and ((int(wlist[8]) <= int(wlanset['RxLevel'])) or (wlist[1] == u'NaN')):
         rest = u';'+unicode(wlanset['SSID'])+u';'+unicode(wlanset['SecurityMode'])+u';'+unicode(wlanset['BeaconInterval'])+u';'+unicode(wlanset['ConnectionMode'][:5])+u';'+unicode(wlanset['Channel'])+u';'+unicode(-abs(wlanset['RxLevel']))+u';'+unicode(time.strftime("%Y/%m/%d"))+u';'+unicode(time.strftime("%H:%M:%S"))+chr(13)+chr(10)
         wlan_list[i] = unicode(wlanset['BSSID'])+u';'+unicode(wlan_lat)+u';'+unicode(wlan_lon)+rest
         wlangpsupdate += 1
      elif (config2['WPS']==Setup2.WPS_ON_AND_LOG) and (wps_coords[0] <> 'NaN') and ((int(wlist[8]) <= int(wlanset['RxLevel']-200)) or (wlist[1] == u'NaN')):
         rest = u';'+unicode(wlanset['SSID'])+u';'+unicode(wlanset['SecurityMode'])+u';'+unicode(wlanset['BeaconInterval'])+u';'+unicode(wlanset['ConnectionMode'][:5])+u';'+unicode(wlanset['Channel'])+u';'+unicode(-abs(wlanset['RxLevel'])-200)+u';'+unicode(time.strftime("%Y/%m/%d"))+u';'+unicode(time.strftime("%H:%M:%S"))+chr(13)+chr(10)
         wlan_list[i] = unicode(wlanset['BSSID'])+u';'+unicode(wps_coords[0])+u';'+unicode(wps_coords[1])+rest
         wlanwpsupdate += 1
      elif (config2['WPS']==Setup2.WPS_ON_AND_LOG) and (cell_lat != u'999.99999') and ((int(wlist[8]) <= int(wlanset['RxLevel']-400)) or (wlist[1] == u'NaN')):
         rest = u';'+unicode(wlanset['SSID'])+u';'+unicode(wlanset['SecurityMode'])+u';'+unicode(wlanset['BeaconInterval'])+u';'+unicode(wlanset['ConnectionMode'][:5])+u';'+unicode(wlanset['Channel'])+u';'+unicode(-abs(wlanset['RxLevel'])-400)+u';'+unicode(time.strftime("%Y/%m/%d"))+u';'+unicode(time.strftime("%H:%M:%S"))+chr(13)+chr(10)
         wlan_list[i] = unicode(wlanset['BSSID'])+u';'+unicode(cell_lat)+u';'+unicode(cell_lon)+rest
         wlancpsupdate += 1
      elif (config2['WPS']==Setup2.WPS_ON_AND_LOG) and (wlist[2] == u'NaN') and gsmloc:
         (mcc, mnc, lac, cid) = gsmloc
         qnet = '%03i%02i%05i%05i' % (mcc, mnc, lac, cid)
         #(cid, rnc) = decode_cid(cid)
         rest = u';'+unicode(wlanset['SSID'])+u';'+unicode(wlanset['SecurityMode'])+u';'+unicode(wlanset['BeaconInterval'])+u';'+unicode(wlanset['ConnectionMode'][:5])+u';'+unicode(wlanset['Channel'])+u';'+unicode(-abs(wlanset['RxLevel'])-400)+u';'+unicode(time.strftime("%Y/%m/%d"))+u';'+unicode(time.strftime("%H:%M:%S"))+chr(13)+chr(10)
         wlan_list[i] = unicode(wlanset['BSSID'])+u';'+u'NaN'+u';'+unicode(qnet)+rest
         wlancpsupdate += 1
      elif wlanset['SSID'] != wlist[3]:
         rest = u';'+unicode(wlanset['SSID'])+u';'+unicode(wlanset['SecurityMode'])+u';'+unicode(wlanset['BeaconInterval'])+u';'+unicode(wlanset['ConnectionMode'][:5])+u';'+unicode(wlanset['Channel'])+u';'+wlist[8]+u';'+unicode(time.strftime("%Y/%m/%d"))+u';'+unicode(time.strftime("%H:%M:%S"))+chr(13)+chr(10)
         wlan_list[i] = unicode(wlanset['BSSID'])+u';'+wlist[1]+u';'+wlist[2]+rest
         wlanssidupdate += 1
      return False
   else:
      if len(gpsdata) == 15 and (gpsdata[14] > 2):
         rest = u';'+unicode(wlanset['SSID'])+u';'+unicode(wlanset['SecurityMode'])+u';'+unicode(wlanset['BeaconInterval'])+u';'+unicode(wlanset['ConnectionMode'][:5])+u';'+unicode(wlanset['Channel'])+u';'+unicode(-abs(wlanset['RxLevel']))+u';'+unicode(time.strftime("%Y/%m/%d"))+u';'+unicode(time.strftime("%H:%M:%S"))+chr(13)+chr(10)
         wlan_list.append(unicode(wlanset['BSSID'])+u';'+unicode(wlan_lat)+u';'+unicode(wlan_lon)+rest)
      elif config2['WPS']==Setup2.WPS_ON_AND_LOG and (wps_coords[0] <> 'NaN'):
         rest = u';'+unicode(wlanset['SSID'])+u';'+unicode(wlanset['SecurityMode'])+u';'+unicode(wlanset['BeaconInterval'])+u';'+unicode(wlanset['ConnectionMode'][:5])+u';'+unicode(wlanset['Channel'])+u';'+unicode(-abs(wlanset['RxLevel'])-200)+u';'+unicode(time.strftime("%Y/%m/%d"))+u';'+unicode(time.strftime("%H:%M:%S"))+chr(13)+chr(10)
         wlan_list.append(unicode(wlanset['BSSID'])+u';'+unicode(wps_coords[0])+u';'+unicode(wps_coords[1])+rest)
      elif (config2['WPS']==Setup2.WPS_ON_AND_LOG) and (cell_lat != u'999.99999'):
         rest = u';'+unicode(wlanset['SSID'])+u';'+unicode(wlanset['SecurityMode'])+u';'+unicode(wlanset['BeaconInterval'])+u';'+unicode(wlanset['ConnectionMode'][:5])+u';'+unicode(wlanset['Channel'])+u';'+unicode(-abs(wlanset['RxLevel'])-400)+u';'+unicode(time.strftime("%Y/%m/%d"))+u';'+unicode(time.strftime("%H:%M:%S"))+chr(13)+chr(10)
         wlan_list.append(unicode(wlanset['BSSID'])+u';'+unicode(cell_lat)+u';'+unicode(cell_lon)+rest)
      else:
         rest = u';'+unicode(wlanset['SSID'])+u';'+unicode(wlanset['SecurityMode'])+u';'+unicode(wlanset['BeaconInterval'])+u';'+unicode(wlanset['ConnectionMode'][:5])+u';'+unicode(wlanset['Channel'])+u';'+unicode(-abs(wlanset['RxLevel'])-400)+u';'+unicode(time.strftime("%Y/%m/%d"))+u';'+unicode(time.strftime("%H:%M:%S"))+chr(13)+chr(10)
         if gsmloc:
            (mcc, mnc, lac, cid) = gsmloc
            #(cid, rnc) = decode_cid(cid)
            qnet = '%03i%02i%05i%05i' % (mcc, mnc, lac, cid)
            wlan_list.append(unicode(wlanset['BSSID'])+u';'+u'NaN'+u';'+unicode(qnet)+rest)
         else:
            wlan_list.append(unicode(wlanset['BSSID'])+u';'+u'NaN'+u';'+u'NaN'+rest)
      wlan_list.sort()
      newwlans += 1
      if (config['WLAN_NOTIFY'] == Setup.WLAN_NOTIFY_ADHOC) and (wlanset['ConnectionMode'] == 'Adhoc'):
         thread.start_new_thread(reader,(config3['ADHOC'],))
      if (config['WLAN_NOTIFY'] == Setup.WLAN_NOTIFY_OPEN) and (wlanset['SecurityMode'] == 'Open'):
         thread.start_new_thread(reader,(config3['OPEN'],))
      if (config['WLAN_NOTIFY'] == Setup.WLAN_NOTIFY_OPEN_VIBRATE) and (wlanset['SecurityMode'] == 'Open'):
         thread.start_new_thread(vibration,(3,))
      
      return True
   

      
def query_bt(btset):
   global bt_list, newbt, btgpsupdate
   i = -1
   if len(gpsdata) == 15:
      try:
         bt_lat = '%0.6f'%float(gpsdata[1])
         bt_lon = '%0.6f'%float(gpsdata[2])
      except:
         bt_lat = gpsdata[1]
         bt_lon = gpsdata[2]
   i = binaere_suche(bt_list, btset[0])
   if i > -1:
      blist = bt_list[i].split(';')
      if len(btset[1]) > 0:
         rest = u';'+unicode(btset[1])+u';'+unicode(btset[2])+u';'+unicode(time.strftime("%Y/%m/%d"))+u';'+unicode(time.strftime("%H:%M:%S"))+u';'+unicode(btset[3])+chr(13)+chr(10)
      else:
         rest = u';'+unicode(blist[3])+u';'+unicode(btset[2])+u';'+unicode(time.strftime("%Y/%m/%d"))+u';'+unicode(time.strftime("%H:%M:%S"))+u';'+unicode(btset[3])+chr(13)+chr(10)
      if ((len(gpsdata) == 15) and (gpsdata[14] > 2) and (blist[1] == u'NaN')) or ((unicode(blist[3]) <> unicode(btset[1])) and (len(btset[1]) > 0)):
         if (len(gpsdata) == 15) and (gpsdata[14] > 2):
            bt_list[i] = unicode(btset[0])+u';'+unicode(bt_lat)+u';'+unicode(bt_lon)+rest
         else:
            bt_list[i] = unicode(btset[0])+u';'+blist[1]+u';'+blist[2]+rest
         btgpsupdate += 1
      return False
   else:
      rest = u';'+unicode(btset[1])+u';'+unicode(btset[2])+u';'+unicode(time.strftime("%Y/%m/%d"))+u';'+unicode(time.strftime("%H:%M:%S"))+u';'+unicode(btset[3])+chr(13)+chr(10)
      if len(gpsdata) == 15:
         bt_list.append(unicode(btset[0])+u';'+unicode(bt_lat)+u';'+unicode(bt_lon)+rest)
      else:
         bt_list.append(unicode(btset[0])+u';'+u'NaN'+u';'+u'NaN'+rest)
      bt_list.sort()
      newbt += 1
      if (config['BT_NOTIFY'] == Setup.BT_NOTIFY_NEW_VOICE) or (config['BT_NOTIFY'] == Setup.BT_NOTIFY_NEW_VOICE_LIGHT):
         thread.start_new_thread(reader,(config3['NEWBT'],))
      if (config['BT_NOTIFY'] == Setup.BT_NOTIFY_NEW_VOICE_LIGHT) or (config['BT_NOTIFY'] == Setup.BT_NOTIFY_NEW_LIGHT):
         e32.reset_inactivity()
      return True
      

def save_clf():
   global clf, clf_name, clf_saving, save_error
   clf_saving = True
   clf_name_backup = clf_name[:-3]+"bak"
   try:
      statinfob = os.stat(clf_name_backup) #store the info as statinfo
      size_back = statinfob.st_size #size in bytes
   except:
      size_back = 0
   try:
      statinfos = os.stat(clf_name) #store the info as statinfo
      size_org = statinfos.st_size #size in bytes
   except:
      size_org = 0
   #print size_back
   #print size_org
   try:
      if size_org >= 0.8*size_back:
         e32.file_copy(clf_name_backup, clf_name)
      else:
         save_error = True
   except:
      pass
   try:
      file = open(clf_name,'w')
      file.writelines(clf)
      file.close()
   except:
      pass
   clf_saving = False

def save_wlan():
   global wlan_name, save_error, wlan_list, wlan_saving
   wlan_saving = True
   wlan_name_backup = wlan_name[:-3]+"bak"
   try:
      statinfob = os.stat(wlan_name_backup) #store the info as statinfo
      size_back = statinfob.st_size #size in bytes
   except:
      size_back = 0
   try:
      statinfos = os.stat(wlan_name) #store the info as statinfo
      size_org = statinfos.st_size #size in bytes
   except:
      size_org = 0
   try:
      if size_org >= 0.6*size_back:
         e32.file_copy(wlan_name_backup, wlan_name)
      else:
         save_error = True
   except:
      pass
   #header = u'BSSID;LAT;LON;SSID;Crypt;Beacon Interval;Connection Mode;Channel;RXL;Date;Time'+chr(13)+chr(10)
   #wlan_list.insert(0, header)
   try:
      file = open(wlan_name,'w')
      file.writelines(wlan_list)
      file.close()
   except:
      pass
   #if wlan_list[0][:5] == 'BSSID':
   #   del wlan_list[0]
   wlan_saving = False
   
def save_bt():
   global bt_name,  bt_list, bt_save_error, invalid_bt, save_error, bt_saving
   bt_saving = True
   bt_name_backup = bt_name[:-3]+"bak"
   try:
      statinfob = os.stat(bt_name_backup) #store the info as statinfo
      size_back = statinfob.st_size #size in bytes
   except:
      size_back = 0
   try:
      statinfos = os.stat(bt_name) #store the info as statinfo
      size_org = statinfos.st_size #size in bytes
   except:
      size_org = 0
   try:
      if size_org >= 0.6*size_back:
         e32.file_copy(bt_name_backup, bt_name)
      else:
         save_error = True
   except:
      pass
   save_error2 = False
   try:
      #header = u'MAC;LAT;LON;Name;Class ID;Date;Time;Class'+chr(13)+chr(10)
      #bt_list.insert(0, header)
      file = open(bt_name,'w')
      file.writelines(bt_list)
      file.close()
      #if bt_list[0][:3] == 'MAC':
      #   del bt_list[0]
   except:
      save_error2 = True
      file.close()
   
   while save_error2:
      bt_save_error += 1
      try:
         file = open(bt_name,'w')
         for i in range(len(bt_list)):
            file.write(bt_list[i])
         file.close()
         save_error2 = False
      except:
         file.close()
         invalid_bt = bt_list[i]
         del bt_list[i]
         save_error2 = True
   bt_saving = False
      
def kismet_export():
   global kismet_name, wlan_list, status
   kismet_list = []
   file = open(kismet_name+'PyNetMony_Kismet_'+time.strftime("%Y_%m_%d")+'_all.csv','w')
   #pgrs = Progress(u"Exporting to Kismet", len(wlan_list))
   header = u'Network;NetType;ESSID;BSSID;Info;Channel;Cloaked;Encryption;Decrypted;MaxRate;MaxSeenRate;Beacon;LLC;Data;Crypt;Weak;Total;Carrier;Encoding;FirstTime;LastTime;BestQuality;BestSignal;BestNoise;GPSMinLat;GPSMinLon;GPSMinAlt;GPSMinSpd;GPSMaxLat;GPSMaxLon;GPSMaxAlt;GPSMaxSpd;GPSBestLat;GPSBestLon;GPSBestAlt;DataSize;IPType;IP;'+chr(13)+chr(10)
   kismet_list.append(header)
   show_text(u"Exporting...")
   e32.ao_sleep(0.05)
   
   #pgrs.show()
   #e32.ao_sleep(0.5)
   total = len(wlan_list)
   for i in range(1,total):
      wlist = wlan_list[i].split(';')
      #try:
      if (len(wlist) > 9) and (int(wlist[8])> -400):
         if wlist[6] == 'Infra':
            wlist[6] = u'infrastructure'
         if wlist[4] == 'Open':
            wlist[4] = u'None'
         if wlist[1] == 'NaN':
            wlist[1] = wlist[2] = u'0'
         if wlist[3].count('<no ssid>') > 0:
            wlist[3] = u'<no ssid>'
         y = int(wlist[9][:4])
         mo = int(wlist[9][5:7])
         d = int(wlist[9][-2:])
         h = int(wlist[10][:2])
         mi =int(wlist[10][3:5])
         s = int(wlist[10][6:8])
         at = time.asctime((y,mo,d,h,mi,s,0,0,-1))
         at = at[:-1]
         at = at.decode('iso-8859-1')
         line = unicode(i)+u';'+wlist[6]+u';'+wlist[3]+u';'+wlist[0]+u';;'+wlist[7]+u';None;'+wlist[4]+u';No;0;0;'+wlist[5]+u';;;;;;;;'+at+u';'+at+u';0;'+wlist[8]+u';;;;;;;;;;'+wlist[1]+u';'+wlist[2]+u';;;None;0.0.0.0;'+chr(13)+chr(10)
         kismet_list.append(line)
         if i == int(round(total*0.2)):
            show_text(u"Exporting....")
            e32.ao_sleep(0.01)
         elif i == int(round(total*0.4)):
            show_text(u"Exporting.....")
            e32.ao_sleep(0.01)
         elif i == int(round(total*0.6)):
            show_text(u"Exporting......")
            e32.ao_sleep(0.01)
         elif i == int(round(total*0.8)):
            show_text(u"Exporting......")
            e32.ao_sleep(0.01)
      #except Exception, error:
      #   appuifw.note(unicode(error),'error')
      #appuifw.note(u"Bad line no: "+unicode(i),'error')
   file.writelines(kismet_list)
   show_text(u"Exporting.......")
   e32.ao_sleep(0.01)
   file.close()
   kismet_list = []
   status = None
   #pgrs.close()
   appuifw.note(u"Saved to: E:\\Data\\Others\\PyNetMony\\logs\\pynetmony_kismet_yyyy_mm_dd.csv",'info')
   
def kismet_export_today():
   global kismet_name, wlan_list, status
   kismet_list = []
   file = open(kismet_name+'PyNetMony_Kismet_'+time.strftime("%Y_%m_%d")+'.csv','w')
   header = u'Network;NetType;ESSID;BSSID;Info;Channel;Cloaked;Encryption;Decrypted;MaxRate;MaxSeenRate;Beacon;LLC;Data;Crypt;Weak;Total;Carrier;Encoding;FirstTime;LastTime;BestQuality;BestSignal;BestNoise;GPSMinLat;GPSMinLon;GPSMinAlt;GPSMinSpd;GPSMaxLat;GPSMaxLon;GPSMaxAlt;GPSMaxSpd;GPSBestLat;GPSBestLon;GPSBestAlt;DataSize;IPType;IP;'+chr(13)+chr(10)
   kismet_list.append(header)
   show_text(u"Exporting...")
   e32.ao_sleep(0.01)
   total = len(wlan_list)
   for i in range(1,total):
      wlist = wlan_list[i].split(';')
      try:
         if (len(wlist) > 9) and (wlist[9]==unicode(time.strftime("%Y/%m/%d"))) and (int(wlist[8])> -400):
            if wlist[6] == 'Infra':
               wlist[6] = u'infrastructure'
            if wlist[4] == 'Open':
               wlist[4] = u'None'
            if wlist[1] == 'NaN':
               wlist[1] = wlist[2] = u'0'
            if wlist[3].count('<no ssid>') > 0:
               wlist[3] = u'<no ssid>'
            y = int(wlist[9][:4])
            mo = int(wlist[9][5:7])
            d = int(wlist[9][-2:])
            h = int(wlist[10][:2])
            mi =int(wlist[10][3:5])
            s = int(wlist[10][6:8])
            at = time.asctime((y,mo,d,h,mi,s,0,0,-1))
            at = at[:-1]
            at = at.decode('iso-8859-1')
            line = unicode(len(kismet_list))+u';'+wlist[6]+u';'+wlist[3]+u';'+wlist[0]+u';;'+wlist[7]+u';None;'+wlist[4]+u';No;0;0;'+wlist[5]+u';;;;;;;;'+at+u';'+at+u';0;'+wlist[8]+u';;;;;;;;;;'+wlist[1]+u';'+wlist[2]+u';;;None;0.0.0.0;'+chr(13)+chr(10)
            kismet_list.append(line)
         if i == int(round(total*0.2)):
            show_text(u"Exporting....")
            e32.ao_sleep(0.01)
         elif i == int(round(total*0.4)):
            show_text(u"Exporting.....")
            e32.ao_sleep(0.01)
         elif i == int(round(total*0.6)):
            show_text(u"Exporting......")
            e32.ao_sleep(0.01)
         elif i == int(round(total*0.8)):
            show_text(u"Exporting......")
            e32.ao_sleep(0.01)
      except:
         appuifw.note(u"Bad line no: "+unicode(i),'error')
   file.writelines(kismet_list)
   show_text(u"Exporting.......")
   e32.ao_sleep(0.1)
   status = None
   file.close()
   appuifw.note(u"Exported "+unicode(len(kismet_list)-1)+u" WLANs to: E:\\Data\\Others\\PyNetMony\\logs\\",'info')
   kismet_list = []
   
   
def wlan2kml():
   global status
   show_text(u"Open -> KML...")
   e32.ao_sleep(0.01)
   kml = KML_File("C:\\Data\\Others\\PyNetMony\\pynetmony_open_wlan.kml")
   #kml.open()
   total = len(wlan_list)
   for i in range(1,total):
      wlist = wlan_list[i].split(';')
      if (len(wlist) > 9) and (wlist[1] <> 'NaN') and wlist[4] == 'Open':
         wlist[3] = wlist[3].replace('<',"(")
         wlist[3] = wlist[3].replace('>',")")
         wlist[3] = wlist[3].replace('&',"and")
         ssid = is_not_control(wlist[3])
         kml.add_placemarker(wlist[1],wlist[2],0.0,ssid+" "+wlist[0]+" "+wlist[4], "Open")
      if i == int(round(total*0.2)):
         show_text(u"Open -> KML....")
         e32.ao_sleep(0.01)
      elif i == int(round(total*0.4)):
         show_text(u"Open -> KML.....")
         e32.ao_sleep(0.01)
      elif i == int(round(total*0.6)):
         show_text(u"Open -> KML......")
         e32.ao_sleep(0.01)
      elif i == int(round(total*0.8)):
         show_text(u"Open -> KML.......")
         e32.ao_sleep(0.01)
   show_text(u"Open -> KML....done")
   e32.ao_sleep(0.01)
   kml.close()
   #status = None
   #appuifw.note(u"WEP WLAN KML file saved to C:\\Data\\Others\\PyNetMony\\",'info')
   show_text(u"WEP -> KML...")
   e32.ao_sleep(0.01)
   kml = KML_File("C:\\Data\\Others\\PyNetMony\\pynetmony_wep_wlan.kml")
   #kml.open()
   total = len(wlan_list)
   for i in range(1,total):
      wlist = wlan_list[i].split(';')
      if (len(wlist) > 9) and (wlist[1] <> 'NaN') and wlist[4] == 'Wep':
         wlist[3] = wlist[3].replace('<',"(")
         wlist[3] = wlist[3].replace('>',")")
         wlist[3] = wlist[3].replace('&',"and")
         ssid = is_not_control(wlist[3])
         kml.add_placemarker(wlist[1],wlist[2],0.0,ssid+" "+wlist[0]+" "+wlist[4], "WEP")
      if i == int(round(total*0.2)):
         show_text(u"WEP -> KML....")
         e32.ao_sleep(0.01)
      elif i == int(round(total*0.4)):
         show_text(u"WEP -> KML.....")
         e32.ao_sleep(0.01)
      elif i == int(round(total*0.6)):
         show_text(u"WEP -> KML......")
         e32.ao_sleep(0.01)
      elif i == int(round(total*0.8)):
         show_text(u"WEP -> KML.......")
         e32.ao_sleep(0.01)
   show_text(u"WEP -> KML....done")
   e32.ao_sleep(0.01)
   kml.close()
   #status = None
   #appuifw.note(u"WEP WLAN KML file saved to C:\\Data\\Others\\PyNetMony\\",'info')
   show_text(u"WPA -> KML...")
   e32.ao_sleep(0.01)
   kml = KML_File("C:\\Data\\Others\\PyNetMony\\pynetmony_wpa_wlan.kml")
   #kml.open()
   total = len(wlan_list)
   for i in range(1,total):
      wlist = wlan_list[i].split(';')
      if (len(wlist) > 9) and (wlist[1] <> 'NaN') and ((wlist[4] == 'WpaPsk') or (wlist[4] == 'Wpa') or (wlist[4] == '802.1x')):
         wlist[3] = wlist[3].replace('<',"(")
         wlist[3] = wlist[3].replace('>',")")
         wlist[3] = wlist[3].replace('&',"and")
         ssid = is_not_control(wlist[3])
         kml.add_placemarker(wlist[1],wlist[2],0.0,ssid+" "+wlist[0]+" "+wlist[4], "WPA")
      if i == int(round(total*0.2)):
         show_text(u"WPA -> KML....")
         e32.ao_sleep(0.01)
      elif i == int(round(total*0.4)):
         show_text(u"WPA -> KML.....")
         e32.ao_sleep(0.01)
      elif i == int(round(total*0.6)):
         show_text(u"WPA -> KML......")
         e32.ao_sleep(0.01)
      elif i == int(round(total*0.8)):
         show_text(u"WPA -> KML.......")
         e32.ao_sleep(0.01)
   show_text(u"WPA -> KML....done")
   e32.ao_sleep(0.01)
   kml.close()
   status = None
   appuifw.note(u"3 WLAN KML files saved to C:\\Data\\Others\\PyNetMony\\",'info')
   
def load_wlan():
   global wlan_list, wlan_name
   if config['WLAN_STORE'] == Setup.WLAN_DEVICE:
      wlan_name = wlan_name_c
   else:
      wlan_name = wlan_name_e
   header = u' BSSID;LAT;LON;SSID;Crypt;Beacon Interval;Connection Mode;Channel;RXL;Date;Time'+chr(13)+chr(10)
   try:
      file = open(wlan_name)
      wlan_list = file.readlines()
      file.close()
      if wlan_list[0].find(u"BSSID") == 0 or wlan_list[0].find(u" BSSID") > 0:
         del wlan_list[0]
         wlan_list.insert(0, header)
      wlan_list.sort()
   except IOError:
      wlan_list.append(header)
      
def load_bt():
   global bt_list, bt_name
   if config['BT_STORE'] == Setup.BT_DEVICE:
      bt_name = bt_name_c
   else:
      bt_name = bt_name_e
   header = u' MAC;LAT;LON;Name;Class ID;Date;Time;Class'+chr(13)+chr(10)
   try:
      file = open(bt_name)
      bt_list = file.readlines()
      file.close()
      if bt_list[0].find(u"MAC") == 0 or bt_list[0].find(u" MAC") > 0:
         del bt_list[0]
         bt_list.insert(0, header)
      bt_list.sort()
   except IOError:
      bt_list.append(header)
         

def load_oui():
   global oui_list
   try:
      file = open("E:\\Data\\Others\\PyNetMony\\oui.dat")
      oui_list = file.readlines()
      file.close()
   except IOError:
      pass

def cellphoto():
   appuifw.app.set_tabs([], None)
   c = CellCam()
   menus_setup()

def toggle_log():
   global logger, logname
   if not logger:
      logname = log_path+"NetMonLog_"+time.strftime("%Y%m%d_%H%M%S")+".txt"
      logger = Logger(logname)
      #sys.stderr = sys.stdout = my_log
      logger.logtab((" Date (Y/M/D)", "Time (H:M:S)", "CID", "LCID", "LAC", "MCC", "MNC", "RNC", "RXL", "LON", "LAT", "SPEED", "DISTANCE"))
   else:
      logger = None
   mainmenu_setup()
   
def toggle_wlog():
   global wlogger, wlogname
   if not wlogger:
      wlogname = log_path+"WLAN_Log_"+time.strftime("%Y%m%d_%H%M%S")+".txt"
      wlogger = Logger(wlogname)
      #sys.stderr = sys.stdout = my_log
      wlogger.logtab((" Date (Y/M/D)", "Time (H:M:S)", "BSSID", "SSID", "RXL", "LAT", "LON"))
   else:
      wlogger = None
   mainmenu_setup()

def writelog(list):
   #my_log = Logger(logname)
   #sys.stderr = sys.stdout = my_log
   logger.logtab(list)
   
def writewlog(list):
   #my_log = Logger(logname)
   #sys.stderr = sys.stdout = my_log
   wlogger.logtab(list)


def sound_play():
   global s
   if not s:
      return
   try:
      s.set_volume(config['Volume'])
      s.play()
   except Exception, error:
      pass
      #appuifw.note(u"Sound Error:" + unicode(error),'error')
      


def distance(lat1, lon1, lat2, lon2):
   if (lat1==lat2) and (lon1==lon2):
      return (0, 0)
   else:
      H2 = lat1*math.pi/180
      H3 = lon1*math.pi/180
      H4 = lat2*math.pi/180
      H5 = lon2*math.pi/180
      
      I5 = math.sin(H2)*math.sin(H4)+math.cos(H2)*math.cos(H4)*math.cos(H3-H5)
      if (lon1-lon2) < 0:
         J5 = 0
      else:
         J5 = 360
      try:
         direction = math.fabs(math.acos(math.sin(H4)/math.sin(math.acos(I5))/math.cos(H2)-math.tan(H2)/math.tan(math.acos(I5)))*180/math.pi-J5)
      except:
         if lat1 > lat2:
            direction = 180
         else:
            direction = 0
      dist = 6371.229*math.acos(I5)
      return (dist, direction)
      
def diffangle(head, dir):
   try:
      head = int(round(head))
      dir = int(round(dir))
      x = dir - head
      if x < 0:
         x = 360 + x
      return x
   except:
      x = -999
      return x

def neighbour_start():
   global neighbour_updated, lb
   lb = appuifw.Listbox([u'Calculating . . .'], handle_selection)
   neighbour_updated = False
   thread.start_new_thread(neighbour,())
   
def neighbour_update():
   lb = appuifw.Listbox(neighbour_list, handle_selection)
      
def neighbour():
   global neighbour_list, cell_lat, cell_lon, lb, neighbour_updated, gpsdata
   neighbour_list = []
   ncell_lat = u'999.99999'
   ncell_lon = u'999.99999'
   nstart_lat = u'999.99999'
   nstart_lon = u'999.99999'
   if len(gpsdata) == 15:
      if float(gpsdata[14]) > 2:
         nstart_lat = gpsdata[1]
         nstart_lon = gpsdata[2]
      elif cell_lat != u'999.99999':
         nstart_lat = cell_lat
         nstart_lon = cell_lon
   elif cell_lat != u'999.99999':
         nstart_lat = cell_lat
         nstart_lon = cell_lon
   
   if nstart_lat != u'999.99999':
      for query in clf:
         if query.find("//") == -1:
            splitter = query.split(';')
            ncell_lat = unicode(splitter[4])
            ncell_lon = unicode(splitter[5])
            if (len(ncell_lat) > 1) and (len(ncell_lon) > 1):
               (dx, az) = distance(float(nstart_lat), float(nstart_lon), float(ncell_lat), float(ncell_lon))
               if dx < config['Neighbour Radius']:
                  ncid = splitter[1]
                  cell_description = unicode(splitter[7])
                  neighbour_list.append(unicode('%0.3f km '%dx)+unicode('%0.1f'%az)+u'\u00b0 '+unicode(ncid)+u' '+cell_description)
      neighbour_list.sort()
   else:
      neighbour_list.append(u'Position unknown!')
   if len(neighbour_list) == 0:
      neighbour_list.append(u'No Neighbour found!')
   neighbour_updated = True
      
def handle_selection():
   index = lb.current()
   if len(neighbour_list) > 0:
      notetext = neighbour_list[index]
      appuifw.note(unicode(notetext), 'info')   

def handle_new_cell_selection():
   global new_cells_list, new_cells_updated, clf_form, clf
   index = new_cells_lb.current()
   cell=[]
   ecell_found = False
   if len(new_cells_list) > 0:
      cell = new_cells_list[index].split(';')
      #appuifw.note(unicode(notetext), 'info')
      for i_cell_edit in range(len(clf)):
         if (clf[i_cell_edit][6:11]==cell[1]) and (clf[i_cell_edit][12:17]==cell[2]):
            cell = clf[i_cell_edit].split(';')
            cell=map(unicode,cell)
            ecell_found = True
            break
      if ecell_found:
         clf_form=appuifw.Form([(u'Cell ID: ','text',cell[1]),(u'LAC: ','text',cell[2]),(u'RNC: ','text',cell[3]),(u'Info: ','text',cell[7]),(u'LAT: ','text',cell[4]),(u'LON: ','text',cell[5]),(u'NET: ','text',cell[0]),(u'POS-RAT: ','text',cell[6])],appuifw.FFormAutoFormEdit)
         clf_form.menu = [(u"Google for coordinates", search_location_for_clf),(u"Take GPS coordinates", take_gps_for_cell)]
         appuifw.app.set_tabs([], None)
         clf_form.execute()
         if appuifw.query(u'Do you really want to save?', 'query'):
            cell[1] = unicode(clf_form[0][2])
            cell[2] = unicode(clf_form[1][2])
            cell[3] = unicode(clf_form[2][2])
            cell[7] = unicode(clf_form[3][2])
            cell[4] = unicode(clf_form[4][2])
            cell[5] = unicode(clf_form[5][2])
            cell[0] = unicode(clf_form[6][2])
            cell[6] = unicode(clf_form[7][2])
            clf[i_cell_edit] = ";".join(cell)
            new_cells_list[index] = ";".join(cell)
            appuifw.note(u"Edited cell saved to clf", "conf")
            new_cells_updated = True
      menus_setup()
      #appuifw.note(unicode(new_cells_list[index]), 'info')

      
def decode_cid(cid):
   global draw_rnc
   if cid > 65535:
      cidhex="%X" % cid
      rnc=int(cidhex[:-4],16)
      cid=int(cidhex[-4:],16)
      draw_rnc = True
      return (cid, rnc)
   else:
      return (cid, 'n/a')


def log_rxl(t, rxl):
   global rxl_log, rxl_last
   if not rxl:
      rxl = 0
   if rxl_last == 0:
      rxl_last = t - 1
   while t > rxl_last:
      # rescue last 1000 entries, negate for easier drawing
      rxl_log = rxl_log[-999:] + [-rxl]
      rxl_last += 1

def dbm(rxl):
   if not rxl:
      return u"Offline"
   else:
      return unicode(rxl) + u" dBm"

def log_loc(t, gsmloc):
   global loc_log
   if len(loc_log) > 0 and gsmloc == loc_log[-1:][0][1]:
      return
   loc_log += [[t, gsmloc]]

def draw_setup(ystart=HEADHEIGHT, ydelta=LINEHEIGHT):
   global imgy, deltay
   imgy = ystart
   deltay = ydelta

def draw_space(yspace=5):
   global imgy
   imgy += yspace

def draw_text(x, utext, space=0, width=320, xd = TABSPACE):
   global img, imgy, deltay, myfont
   if x == -1:
      (box,tlength,numb) = img.measure_text(utext, font=myfont, maxwidth=width-xd)
      x = (width-tlength)/2
      while numb < len(utext):
         numb_temp = utext[:numb].rfind(' ')
         if numb_temp > 0:
            numb = numb_temp
         (box,tlength,numb2) = img.measure_text(utext[:numb], font=myfont, maxwidth=width-xd)
         x = (width-tlength)/2
         img.text((x, imgy), utext[:numb], fill=color, font=myfont)
         imgy += deltay + space
         utext = utext[numb:]
         (box,tlength,numb) = img.measure_text(utext, font=myfont, maxwidth=width-xd)
         x = (width-tlength)/2
         
   img.text((x, imgy), utext, fill=color, font=myfont)
   imgy += deltay + space

def measure_table(lformat, rformat=[], tabspace=TABSPACE, xstart=TABSPACE):
   global img, myfont
   x = xstart/2
   #x = tabspace/2
   #x = 0
   xleft = []
   xright = []
   # add the width of all fmtlist entries together
   for fmt in lformat:
      # add current cursor to the xpos list
      xleft += [x]
      rect,width,cursor = img.measure_text(unicode(fmt), font=myfont)
      x += width + tabspace
   leftwidth = x
   x = tabspace/2
   #x = 0
   rf = list(rformat)
   rf.reverse()
   for fmt in rf:
      rect,width,cursor = img.measure_text(unicode(fmt), font=myfont)
      x -= (width + tabspace)
      xright += [x]
   xright.reverse()
   rightwidth = -x
      
   #print xleft, xright
   return xleft + xright, (leftwidth + tabspace + rightwidth)


def draw_table(xlist, textlist, space=0, width=320, highlight=False, italic=False):
   global img, imgy, deltay, myfont
   mytablefont = myfont
   if highlight:
      img.rectangle((0,imgy-(HDLH-2*HDLFRAME)-1,width,imgy+1),headcol,fill=headbg)
   if italic:
      mytablefont = (myfont[0],myfont[1],myfont[2]|FONT_ITALIC)
   for i in range(len(xlist)):
      x = xlist[i]
      if x < 0:
         x += width
      if highlight:
         #img.rectangle((0,imgy-HDLH,width,imgy),headcol,fill=headbg)
         img.text((x, imgy), unicode(textlist[i]), fill=bg, font=mytablefont)
      else:
         img.text((x, imgy), unicode(textlist[i]), fill=color, font=mytablefont)
   imgy += deltay + space
   

def draw_about(imei):
   global img
   size,offset = appuifw.app.layout(appuifw.EMainPane)
   (w, h) = size
   img.rectangle((0,0)+size,outline=border,fill=bg)
   draw_setup(LINEHEIGHT, LINEHEIGHT)
   draw_text(CENTER, VERSION, space=5, width=w)
   draw_text(CENTER, u'\u00a9 2009 by Carsten Kn\u00fctter', space=2, width=w)
   draw_text(CENTER, u'Georg Lukas, Daniel Perna', space=5, width=w)
   draw_text(CENTER, u'pynetmony'+U'@arcor.de', space=10, width=w)
   draw_text(CENTER, u'http://pynetmony.googlepages.com', space=10, width=w)
   GPL = 'This program comes with ABSOLUTELY NO WARRANTY. This is free software, and you are welcome to redistribute it under certain conditions.'
   #for line in GPL:
   draw_text(CENTER, unicode(GPL), space = 2, width=w)
   #draw_space(5)
   #draw_text(CENTER, unicode('IMEI: '+imei), space = 2, width=w)
   

def draw_netmon(lac, mcc, mnc, rnc, rxl, ver, imei, longcid, cidhex, lachex, longcidhex, size, cid):
   global img
   (w, h) = size
   try:
      bars = sysinfo.signal_bars()
   except SystemError:
      bars = u"n/a" 
   batty = sysinfo.battery()
   if eloc:
      try:
         net_reg = elocation.get_registration_status()
         ext_loc = elocation.extended_gsm_location()
         if net_reg == 'RegisteredOnHomeNetwork':
            net_reg = 'Home'
         elif net_reg == 'NotRegisteredSearching':
            net_reg = 'Searching'
         elif net_reg == 'RegisteredRoaming':
            net_reg = 'Roaming'
         elif net_reg == 'NotRegisteredNoService':
            net_reg = 'No Service'
         elif net_reg == 'RegisteredBusy':
            net_reg = 'Busy'
         elif net_reg == 'RegistrationDenied':
            net_reg = 'Denied'
         elif net_reg == 'NotRegisteredEmergencyOnly':
            net_reg = 'Emergency'
         else:
            net_reg = 'Unknown'
      except:
         net_reg = 'eloc error'
         ext_loc = {}
   else:
      net_reg = 'no elocation'
      ext_loc = {}
   if API <= 26:
      # Fix for pre-2ndFP1
      batty = int(batty * 14.3)
   ram = sysinfo.free_ram()/1024
   totram = sysinfo.total_ram()/1024
   x = appuifw.app.layout(appuifw.EScreen)

   draw_setup(HEADHEIGHT, LINEHEIGHT)
   #xpos = (3, 45)
   xpos, tabw = measure_table(('MOD:', 'XXX'))

   if longcid == u'n/a':
      band = 'GSM';
      draw_table(xpos, ('CID:', unicode(cid)+'  ('+unicode(cidhex)+u')'))
   else:
      draw_table(xpos, ('LCID:', unicode(longcid)+' ('+unicode(longcidhex)+u')'))
      draw_table(xpos, ('RNC:', rnc))
      band = 'UMTS';
   draw_table(xpos, ('LAC:', unicode(lac)+u'  ('+unicode(lachex)+u')'))
   if mcc is None or mcc == u'n/a' or mcc == u'busy':
      net = u'n/a-n/a ['+unicode(net_reg)+u']'
   else:
      net = u'%03i-%02i [%s]' % (mcc, mnc, net_reg)
   draw_table(xpos, ('NET:', net))
   draw_table(xpos, ('RXL:', '%s (%s)' % (dbm(rxl), bars)))
   #draw_table(xpos, ('BAT:', '%i %%' % batty))
   if len(ext_loc) > 0:
      draw_table(xpos, ('MOD:', unicode(ext_loc['NetworkMode'])+u' / '+unicode(ext_loc['NetworkAccessTechnology'])))
   else:
      draw_table(xpos, ('MOD:', u'n/a  / n/a'))
   draw_table(xpos, ('RAM:', '%i / %i KB' % (ram, totram)))
   if (cell_lat != u'999.99999') and (gpson == 1) and (len(gpsdata) == 15) and (gpsdata[14] > 2):
      (dx, az) = distance(float(gpsdata[1]), float(gpsdata[2]), float(cell_lat), float(cell_lon))
      draw_table(xpos, ('CDIR:', '%0.3f km    %0.1f' % (dx, az)+u'\u00b0'))
   elif (cell_lat != u'999.99999') and wps_coords[0] <> 'NaN':
      (dx, az) = distance(float(wps_coords[0]), float(wps_coords[1]), float(cell_lat), float(cell_lon))
      draw_table(xpos, ('CDIR:', '%0.3f km    %0.1f' % (dx, az)+u'\u00b0'))
   draw_space(3)
   draw_text(CENTER, cell_description, space=2, width=w)
   #draw_table(xpos, ('IMEI:', imei))
   #draw_table(xpos, ('VER:', ver))
   #draw_table(xpos, ('RES:', x))
   #draw_text(3,  u'APP: '+appuifw.app.full_name())

def draw_rxl_line(size, pos, text):
   global rxl_line_font, color
   if e32.s60_version_info == (1, 2):
      return
   sz = (size[1]-2, 20)
   i = Image.new(sz, '1')
   imask = Image.new(sz, '1')
   i.rectangle((0,0)+sz, fill=0x000000)
   imask.rectangle((0,0)+sz, fill=0x000000)
   i.text((2,11), text, color, font=rxl_line_font)
   imask.text((2,11), text, 0xffffff, font=rxl_line_font)
   irot = i.transpose(ROTATE_90)
   imaskrot = imask.transpose(ROTATE_90)
   img.blit(irot, target=pos, mask=imaskrot)

def headline(size, cid):
   (w, h) = size
   # CLK and CID always on top
   img.rectangle((0,0,w,HDLH),headcol,fill=headbg)
   img.text((w-TLENGTH_TIME-HDLFRAME,HDLY), unicode(time.strftime("%H:%M:%S")),fill=bg, font=headfont)
   if (w > 240):
      img.text((w/2-100,HDLY), u'T'+unicode(bt_scan_time),fill=bg, font=headfont)
      img.text((w/2+50,HDLY),u'e:'+unicode(bt_err),fill=bg, font=headfont)
      
   if logger:
      #img.point((w/2-40,HDLH/2),(255,0,0),width=HDLH-2*HDLFRAME)
      img.text((HDLFRAME,HDLY), unicode(cid),fill=(255,0,0), font=headfont)
   else:
      img.text((HDLFRAME,HDLY), unicode(cid),fill=bg, font=headfont)
   if wlan and (config['Refresh']>8):
      if wlogger:
         img.text((w/2-28,HDLY), u'W'+unicode(len(wscan)),fill=(255,0,0), font=headfont)
      else:
         img.text((w/2-28,HDLY), u'W'+unicode(len(wscan)),fill=bg, font=headfont)
   if config['BT_SCAN']>0:
      if bt_busy:
         img.text((w/2-62,HDLY), u'B'+unicode(len(btscan)),fill=(255,0,0), font=headfont)
      else:
         img.text((w/2-62,HDLY), u'B'+unicode(len(btscan)),fill=bg, font=headfont)
   if (gpson == 1):
      if (len(gpsdata) == 15):
         gpsstat = unicode(gpsdata[14])
      else:
         gpsstat = u"*"
      img.text((w/2+12,HDLY), u'G'+gpsstat,fill=bg, font=headfont)

def rxl_line(log, fname=False):
   (mcc, mnc, lac, cid) = log
   longcid = cid
   (cid, rnc) = decode_cid(cid)
   if mcc is None:
      return u"Offline"
   else:
      if fname:
         return u'%03i-%02i_%05i-%i.jpg' % (mcc, mnc, lac, longcid)
      else:
         return u'%03i-%02i C:%i L:%i' % (mcc, mnc, cid, lac)

def draw_rxlgraph(size):
   global rxl_log, loc_log, t_last
   if len(rxl_log) == 0:
      return
   t = t_last
   (width, height) = size
   sublog = rxl_log[-width:]
   xcoord = range(width-len(sublog)+1, width+1)
   line = zip(xcoord, sublog)
   img.line(line, outline=linecol)
   x = width
   l = len(loc_log)-1
   while x > -20 and l >= 0:
      offset = t - loc_log[l][0]
      x = width - offset
      img.line((x, 0, x ,height),outline=linecol)
      draw_rxl_line(size, (x+1, 1), rxl_line(loc_log[l][1]))
      l-=1
   draw_setup(HEADHEIGHT, LINEHEIGHT)
   draw_text(3, dbm(-rxl_log[-1:][0]))

def draw_history(size):
   global loc_log
   (width, height) = size

   # count is: vertical space starting after headline and table head,
   # divided by height of table lines
   vspace = height - HEADHEIGHT + LINEY - TABHEIGHT - 2
   count = vspace/TABHEIGHT
   #xpos = (3, 81, 136, 194, 244)
   xpos, tabw = measure_table(('99:99:99', '99999', '99999', '99999', '99999'), xstart=0)
   title = ("Time", "CID", "LAC", "RNC", "Net")

   draw_setup(HEADHEIGHT, LINEHEIGHT)
   draw_table(xpos, title, space=2)
   if width >= 500:
      count *= 2
   i = 0
   for v in loc_log[-count:]:
      t = time.strftime("%H:%M:%S ", time.localtime(v[0]))
      (mcc, mnc, lac, cid) = v[1]
      if mcc is None:
         cid = u"Offline"
         net = lac = rnc = u""
      else:
         (cid, rnc) = decode_cid(cid)
         net = '%03i%02i' % (mcc, mnc)
      if (i == (count/2)) and (width >= 500):
         xpos = map(lambda x: x+400, xpos)
         draw_setup(HEADHEIGHT, LINEHEIGHT)
         draw_table(xpos, title, space=2)
      draw_table(xpos, (t, cid, lac, rnc, net))
      i += 1

def draw_stats(size):
   (w, h) = size
   draw_setup(HEADHEIGHT, LINEHEIGHT)
   dup = uptime(starttime)
   xpos, tabw = measure_table(('APWPSU', '99999', 'APWPSU', '99999'), xstart=2)
   draw_table(xpos, ('Cell Sel:', unicode(cellselect), 'LAC Sel:', unicode(lacselect)))
   draw_table(xpos, ('NeMode:', unicode(netmode_counter), 'Net Sel:', unicode(net_counter)))
   draw_table(xpos, (unicode(unichr(931))+' CLF :', unicode(len(clf)-1), 'NewCell:', unicode(newcells)))
   draw_table(xpos, (unicode(unichr(931))+' APs :', unicode(len(wlan_list)-1), 'NewAP: ', unicode(newwlans)))
   draw_table(xpos, ('ApGPSu:', unicode(wlangpsupdate), 'ApWPSu:', unicode(wlanwpsupdate)))
   draw_table(xpos, ('ApCPSu:', unicode(wlancpsupdate), 'Max APs:', unicode(maxaps)))
   draw_table(xpos, ('SSID up:', unicode(wlanssidupdate), 'MaxRXL:', unicode(maxaprxl)))
   draw_table(xpos, (unicode(unichr(931))+' BTs :', unicode(len(bt_list)-1), 'NewBT:', unicode(newbt)))
   draw_table(xpos, ('BTGPSu :', unicode(btgpsupdate), 'BT SErr:', unicode(bt_save_error)))
   draw_space(1)
   draw_text(2, unicode('Uptime: '+dup[0]+'d '+dup[1]+'h '+dup[2]+'m '), space = 1, width=w)
   draw_text(2, unicode('IMEI: '+imei), space = 1, width=w)
   #draw_text(2, unicode('IMSI: '+unicode(imsi)), space = 1, width=w)
   draw_text(2, unicode('UserID: '+unicode(userid)), space = 1, width=w)
   draw_text(2, unicode(invalid_bt), space=1, width=w)



def draw_gps(size):
   global gpsdata, gpsmodule, gpson, img, cell_lat, cell_lon, maxspeed
   (w, h) = size
   draw_setup(HEADHEIGHT, LINEHEIGHT)
   draw_fix = False
   #xpos = (3, 75)
   xpos, tabw = measure_table(('Accuracy:', 'XXX'))
   if (gpson == 1) and (len(gpsdata) == 15):
      maxspeed = float(max(maxspeed, gpsdata[8]))
      draw_table(xpos, ('Modul:', gpsdata[6]+u' ('+unicode(gpsmodule)+u')'))
      draw_table(xpos, ('Lat:', '%0.6f'%(gpsdata[1])+u'\u00b0'))
      draw_table(xpos, ('Lon:', '%0.6f'%(gpsdata[2])+u'\u00b0'))
      draw_table(xpos, ('Altitude:', ('%0.1f m'%gpsdata[3])))
      draw_table(xpos, ('Accuracy:', ('H: %0.1f m   V: %0.1f m'%(gpsdata[4], gpsdata[5]))))
      draw_table(xpos, ('Speed:', ("%0.1f km/h" % gpsdata[8])))
      draw_table(xpos, ('MxSpeed:', ("%0.1f km/h" % maxspeed)))
      draw_table(xpos, ('Heading:', ('%0.1f'%gpsdata[10])+u'\u00b0'))
      if (cell_lat != u'999.99999'):
         (dx, az) = distance(float(gpsdata[1]), float(gpsdata[2]), float(cell_lat), float(cell_lon))
         #(dx, az) = distance(50.07, 6.07, 50.07, 6.07)
         draw_table(xpos, ('Direction:', ('%0.1f'%az+u'\u00b0')))
         draw_table(xpos, ('Distance:', ('%0.3f km'%dx)))
      if config2['WPS']>=Setup2.WPS_ON:
         draw_table(xpos, ('SAT (Fix):', unicode(gpsdata[13])+u' ('+unicode(gpsdata[14])+u') WPS:'+unicode(wps_count)+u' ('+unicode(wps_fix)+u')'))
         draw_fix = True
      else:
         draw_table(xpos, ('SAT (Fix):', unicode(gpsdata[13])+u' ('+unicode(gpsdata[14])+u')'))
         draw_fix = True
   elif len(gpsdata) >= 2:
      # Display Error from gpsdata[1]
      draw_text(3, u'No GPS data available:')
      draw_text(3, unicode(gpsdata[1]))
   else:
      draw_setup(h/2)
      draw_text(int(w/2)-30, u'GPS OFF')
   if config2['WPS']>=Setup2.WPS_ON:
      if not draw_fix:
         draw_table(xpos, ('WPS (Fix):', unicode(wps_count)+u' ('+unicode(wps_fix)+u')'))
      draw_table(xpos, ('WPS Lat:', wps_coords[0]+u'\u00b0'))
      draw_table(xpos, ('WPS Lon:', wps_coords[1]+u'\u00b0'))

def circle(x,y,radius=5, outline=(255,255,255), fill=0xffff00, width=1):
   global img
   img.ellipse((x-radius, y-radius, x+radius, y+radius), outline, fill, width)
      
def draw_radar(size):
   global gpsdata, gpsmodule, gpson, img, cell_lat, cell_lon, wps_list_radar, wlan_radar_zoom
   (w, h) = size
   (dx, dir) = (-1, -1)
   draw_setup(HEADHEIGHT, LINEHEIGHT)
   zerox = w/2
   zeroy = (h-HDLH)/2+HDLH
   if (h-HDLH) < w:
      maxr = (h-HDLH)/2
   else:
      maxr = w/2
   teiler = maxr/3   
   
   img.line((zerox-10,zeroy,zerox+10,zeroy),grid,width=1)
   img.line((zerox,zeroy-10,zerox,zeroy+10),grid,width=1)
   circle(zerox,zeroy,maxr,outline=grid,fill=None)
   circle(zerox,zeroy,maxr-teiler,outline=grid,fill=None)
   circle(zerox,zeroy,maxr-2*teiler,outline=grid,fill=None)
   #circle(zerox,zeroy,maxr/3,fill=None)
   #circle(zerox,zeroy,maxr/4,fill=None)
   for i in range(0,360,30):
      alf = (90-i)*math.pi/180
      x = math.cos(alf)*maxr
      y = math.sin(alf)*maxr
      img.line((zerox,zeroy,zerox+x,zeroy-y),grid,width=1)
      img.point((zerox+x,zeroy-y),grid,width=8)
   xpos,width = measure_table([u'5.999km'], [u'A:999\u00b0'])
   if (gpson == 1) and (len(gpsdata) == 15):
      if gpsdata[14] > 2:
         if config2['RADAR_MODE']==Setup2.RADAR_MODE_CLF and (cell_lat != u'999.99999'):
            (dx, dir) = distance(float(gpsdata[1]), float(gpsdata[2]), float(cell_lat), float(cell_lon))
         elif config2['RADAR_MODE']==Setup2.RADAR_MODE_GEO:
            (dx, dir) = distance(float(gpsdata[1]), float(gpsdata[2]), config2['GEO_LAT'], config2['GEO_LON'])
         elif config2['RADAR_MODE']==Setup2.RADAR_MODE_APS:
            if heading_north:
               head = 0
               draw_table(xpos, ('[%0.0fm]'%(1000*wlan_radar_zoom/3),u'H:North'), width=w)
            else:
               head = gpsdata[10]
               draw_table(xpos, ('[%0.0fm]'%(1000*wlan_radar_zoom/3),u'H:'+('%0.0f'%head)+u'\u00b0'), width=w)
            for i in range(len(wps_list_radar)):
               (dx, dir) = distance(float(gpsdata[1]), float(gpsdata[2]), float(wps_list_radar[i][0]), float(wps_list_radar[i][1]))
               angle = diffangle(head,dir)
               if angle > 0:
                  alf = (90-angle)*math.pi/180
               dxr = maxr/wlan_radar_zoom*dx
               if wps_list_radar[i][4] == 'WpaPsk':
                  radarcolor = (255,0,0)
               elif wps_list_radar[i][4] == 'Wep':
                  radarcolor = (255,255,0)
               elif wps_list_radar[i][4] == 'Open':
                  radarcolor = (0,255,0)
               else:
                  radarcolor = (255,255,55)
               x = math.cos(alf)*dxr
               y = math.sin(alf)*dxr
               img.point((zerox+x,zeroy-y),radarcolor,width=10)
               (box,tlength,numb) = img.measure_text(wps_list_radar[i][3]+' 99m', font=rxl_line_font)
               img.text((zerox+x-tlength/2, zeroy-y), wps_list_radar[i][3]+' %0.0fm'%(dx*1000), fill=color, font=rxl_line_font)
         if config2['RADAR_MODE']<>Setup2.RADAR_MODE_APS and (dx, dir)<>(-1, -1):
            if heading_north:
               head = 0
               draw_table(xpos, ('%0.3fkm'%dx,u'H:North'), width=w)
            else:
               head = gpsdata[10]
               draw_table(xpos, ('%0.3fkm'%dx,u'H:'+('%0.0f'%head)+u'\u00b0'), width=w)
            angle = diffangle(head,dir)
            if angle > 0:
               alf = (90-angle)*math.pi/180
            if dx > 30:
               dxr = maxr/75*dx
               draw_table(xpos, (u'[25km]',u''), width=w)
               radarcolor = (255,255,255)
            elif dx > 9:
               dxr = maxr/30*dx
               draw_table(xpos, (u'[10km]',u''), width=w)
               radarcolor = (0,255,0)
            elif dx > 3:
               dxr = maxr/9*dx
               draw_table(xpos, (u'[3km]',u''), width=w)
               radarcolor = (255,255,0)
            elif dx > 0.9:
               dxr = maxr/3*dx
               draw_table(xpos, (u'[1km]',u''), width=w)
               radarcolor = (255,127,0)
            else:
               dxr = maxr/0.9*dx
               draw_table(xpos, (u'[300m]',u''), width=w)
               radarcolor = (255,0,0)
            x = math.cos(alf)*dxr
            y = math.sin(alf)*dxr
            img.point((zerox+x,zeroy-y),radarcolor,width=15)
            draw_space(h-4.5*HDLH)
            draw_table(xpos, (u'D:'+('%0.0f'%dir)+u'\u00b0',u'A:'+('%0.0f'%angle)+u'\u00b0'), width=w)
            #draw_table(xpos, (u'D:'+('%0.0f'%dir)+u'\u00b0',u'H:'+('%0.0f'%head)+u'\u00b0'), width=w)
   elif (gpson == 0) and (wps_count > 0):
      #if (cell_lat != u'999.99999'):
      if config2['RADAR_MODE']==Setup2.RADAR_MODE_CLF and (cell_lat != u'999.99999'):
         (dx, dir) = distance(float(wps_coords[0]), float(wps_coords[1]), float(cell_lat), float(cell_lon))
      elif config2['RADAR_MODE']==Setup2.RADAR_MODE_GEO:
         (dx, dir) = distance(float(wps_coords[0]), float(wps_coords[1]), config2['GEO_LAT'], config2['GEO_LON'])
      elif config2['RADAR_MODE']==Setup2.RADAR_MODE_APS:
         draw_table(xpos, ('[%0.0fm]'%(1000*wlan_radar_zoom/3),u'H:North'), width=w)
         for i in range(len(wps_list_radar)):
            (dx, dir) = distance(float(wps_coords[0]), float(wps_coords[1]), float(wps_list_radar[i][0]), float(wps_list_radar[i][1]))
            head = 0
            angle = diffangle(head,dir)
            if angle > 0:
               alf = (90-angle)*math.pi/180
            #draw_table(xpos, (u'SSID:'+wps_list_radar[i][3],'%0.1fm'%(dx*1000)), width=w)
            #draw_table(xpos, (u'Crypt:'+wps_list_radar[i][4],u'[75m]'), width=w)
            dxr = maxr/wlan_radar_zoom*dx
            if wps_list_radar[i][4] == 'WpaPsk':
               radarcolor = (255,0,0)
            elif wps_list_radar[i][4] == 'Wep':
               radarcolor = (255,255,0)
            elif wps_list_radar[i][4] == 'Open':
               radarcolor = (0,255,0)
            else:
               radarcolor = (255,255,55)
            x = math.cos(alf)*dxr
            y = math.sin(alf)*dxr
            img.point((zerox+x,zeroy-y),radarcolor,width=10)
            (box,tlength,numb) = img.measure_text(wps_list_radar[i][3]+' 99m', font=rxl_line_font)
            img.text((zerox+x-tlength/2, zeroy-y), wps_list_radar[i][3]+' %0.0fm'%(dx*1000), fill=color, font=rxl_line_font)
      if config2['RADAR_MODE']<>Setup2.RADAR_MODE_APS and (dx, dir)<>(-1, -1):
         head = 0
         angle = diffangle(head,dir)
         if angle > 0:
            alf = (90-angle)*math.pi/180
         #draw_table(xpos, ('%0.3fkm'%dx,u'A:'+('%0.0f'%angle)+u'\u00b0'), width=w)
         draw_table(xpos, ('%0.3fkm'%dx,u'H:'+u'North'), width=w)
         if dx > 30:
            dxr = maxr/75*dx
            draw_table(xpos, (u'[25km]',u''), width=w)
            radarcolor = (255,255,255)
         elif dx > 9:
            dxr = maxr/30*dx
            draw_table(xpos, (u'[10km]',u''), width=w)
            radarcolor = (0,255,0)
         elif dx > 3:
            dxr = maxr/9*dx
            draw_table(xpos, (u'[3km]',u''), width=w)
            radarcolor = (255,255,0)
         elif dx > 0.9:
            dxr = maxr/3*dx
            draw_table(xpos, (u'[1km]',u''), width=w)
            radarcolor = (255,127,0)
         else:
            dxr = maxr/0.9*dx
            draw_table(xpos, (u'[300m]',u''), width=w)
            radarcolor = (255,0,0)
         x = math.cos(alf)*dxr
         y = math.sin(alf)*dxr
         img.point((zerox+x,zeroy-y),radarcolor,width=15)
         draw_space(h-4.5*HDLH)
         draw_table(xpos, (u'D:'+('%0.0f'%dir)+u'\u00b0',u'A:'+('%0.0f'%angle)+u'\u00b0'), width=w)
         #draw_table(xpos, (u'',u'H:'+u'North'), width=w)

def skyhook():
   global skyhookmod, wscan, conn
   req_template = "<?xml version='1.0'?>\n<LocationRQ xmlns='http://skyhookwireless.com/wps/2005' version='2.6' street-address-lookup='full'>\n<authentication version='2.0'>\n<simple>\n\t<username>beta</username>\n\t<realm>js.loki.com</realm>\n</simple>\n</authentication>%s\n</LocationRQ>"
   ap_template  = "\n<access-point>\n\t<mac>%s</mac>\n\t<signal-strength>%s</signal-strength>\n</access-point>"
   if signal_ok():
      try:
         accesspoints = wscan
         if len(accesspoints) == 0:
            appuifw.note(u'No WiFi Networks found','error')
            return
         req = ""
         ap_list = ""
         try:
            for ap in accesspoints:
               bssid = ap["BSSID"].replace(":","")
               rxlevel = str(ap["RxLevel"])
               ap_list += ap_template % (bssid, rxlevel)
         except:
            pass
         req += req_template % ap_list
         headers = {"Content-type": "text/xml", "Connection": "close"}
         conn = httplib.HTTPSConnection("api.skyhookwireless.com", 443)
         conn.request("POST", "/wps2/location", req, headers)
         resp = conn.getresponse()
         answer = resp.read()
         conn.close()
         apo.stop()
         conn = None
         if resp.status == 200:
            #print answer
            if answer.find("<error>") != -1:
               err = answer[answer.find("<error>")+len("<error>"):answer.find("</error>")]
               appuifw.note(unicode(err),'error')
            else:
               if answer.find("<latitude>") != -1:
                  lat = answer[answer.find("<latitude>")+len("<latitude>"):answer.find("</latitude>")]
                  lon = answer[answer.find("<longitude>")+len("<longitude>"):answer.find("</longitude>")]
                  hpe = answer[answer.find("<hpe>")+len("<hpe>"):answer.find("</hpe>")]
                  display = [
                     (u'Latitude', 'text', u"%s" % lat),
                     (u'Longitude', 'text', u"%s" % lon),
                     (u'Positioning Error (HPE)', 'text', u"%s m" % hpe),
                  ]
                  appuifw.note(u'Lat: '+unicode(lat)+'\nLon: '+unicode(lon)+'\nAccuracy: '+unicode(hpe)+' Meters','info')
         else:
            raise "HTTP Error "+str(resp.status)
      except:
         if conn != None:
            conn.close()
            apo.stop()
   else:
      appuifw.note(u'No signal!','error')

def wlan_scan():
   global wscan, wlanquery_list, wlan_scanning, maxaps, oui_list
   wlan_scanning = True
   wlanquery_list = []
   try:
      wscan = wlantools.scan(False)
      try:
         if config2['WLAN_SORT']==Setup2.WLAN_SORT_RXL:
            decorated_list = [(x['RxLevel'],x) for x in wscan]
            decorated_list.sort()
            decorated_list.reverse()
         elif config2['WLAN_SORT']==Setup2.WLAN_SORT_CH:
            decorated_list = [(x['Channel'],x) for x in wscan]
            decorated_list.sort()
         elif config2['WLAN_SORT']==Setup2.WLAN_SORT_SSID:
            decorated_list = [(x['SSID'],x) for x in wscan]
            decorated_list.sort()
            decorated_list.reverse()
         wscan = [y for (x,y) in decorated_list]
      except:
         sorted = wscan

   except:
      wscan = []
   # for hidden ssid
   lenwscan = len(wscan)
   if lenwscan > maxaps:
      maxaps = lenwscan
   for i in range(lenwscan):
      ssid = wscan[i]['SSID']
      if (ssid.count(chr(0)) == len(ssid)) and (len(ssid) > 0):
         wscan[i]['SSID'] = unicode(len(ssid))+u'c' 
      else:
         ssid = ssid.replace(chr(59),",")
         ssid = ssid.replace(chr(34),"``")
         ssid = is_not_control(ssid)
         wscan[i]['SSID'] = ssid
      ouiline = binaere_suche(oui_list, wscan[i]['BSSID'][0:8], 8)
      if ouiline > -1:
         wscan[i]['SSID'] += ('^' + oui_list[ouiline][8:21].strip())
         


   if config2['WPS']>=Setup2.WPS_ON:
      for i in range(lenwscan):
         query_wps(wscan[i])
      calculate_wps_lat_lon()   
   for i in range(lenwscan):
      wlanquery_list.append(query_wlan(wscan[i]))
      if wlogger:
         if (gpson == 1) and (len(gpsdata) == 15) and str(gpsdata[1]) != 'NaN':
            # Convert lat, lon to formatted strings
            (lat, lon) = map(lambda x: "%2.6f" % x, gpsdata[1:3])
         else:
            lon = lat = 'n/a'
         writewlog((time.strftime("%Y/%m/%d"), time.strftime("%H:%M:%S"), wscan[i]['BSSID'], wscan[i]['SSID'], wscan[i]['RxLevel'], lat, lon))
   wlan_scanning = False

def bt_mainthread():
   global bt_busy, bt_err
   thread.start_new_thread(bt_scan,())
   time.sleep(1)
   while bt_busy and (bt_scan_time < config['BT_SCAN_TIMEOUT']):
      time.sleep(1)
   if bt_scan_time > (config['BT_SCAN_TIMEOUT']-1):
      bt_err += 1
      #thread.start_new_thread(reader,(u'ein Fehler',))
      #blues.off()
      time.sleep(5)
      #blues.on()
      time.sleep(5)
      bt_busy = False

def dec2bin(number):
   result = ''
   while number:
      result = str(number % 2) + result
      number /= 2
   return result

      
def bt_device_class(device_class):
   if len(device_class) >= 3:
      device_class = device_class[-3:]
      major_device_class = device_class[:1]
      major_device_class = int(major_device_class,16)
      minor_device_class = device_class[1:]
      minor_device_class = int(minor_device_class,16)
      if major_device_class == 0:
         return u'Miscellaneous'
      elif major_device_class == 1:
         if minor_device_class == 0:
            return u'Computer Class'
         elif minor_device_class == 4:
            return u'Desktop'
         elif minor_device_class == 8:
            return u'Server'
         elif minor_device_class == 12:
            return u'Laptop'
         elif minor_device_class == 16:
            return u'Handheld PC/PDA'
         elif minor_device_class == 20:
            return u'Palm sized PC/PDA'
         elif minor_device_class == 24:
            return u'Wearable Computer'
         else:
            return u'New Computer Class'
      elif major_device_class == 2:
         if minor_device_class == 0:
            return u'Phone Class'
         elif minor_device_class == 4:
            return u'Cellular'
         elif minor_device_class == 8:
            return u'Cordless'
         elif minor_device_class == 12:
            return u'Smartphone'
         elif minor_device_class == 16:
            return u'Wired modem'
         elif minor_device_class == 20:
            return u'Common ISDN Access'
         else:
            return u'New Phone Class'
      elif major_device_class == 3:
         return u'Access point'
      elif major_device_class == 4:
         if minor_device_class == 0:
            return u'Audio/Video'
         elif minor_device_class == 4:
            return u'Wearable Headset'
         elif minor_device_class == 8:
            return u'Hands-free Device'
         elif minor_device_class == 12:
            return u'New Audio/Video'
         elif minor_device_class == 16:
            return u'Microphone'
         elif minor_device_class == 20:
            return u'Loudspeaker'
         elif minor_device_class == 24:
            return u'Headphones'
         elif minor_device_class == 28:
            return u'Portable Audio'
         elif minor_device_class == 32:
            return u'Car audio'
         elif minor_device_class == 36:
            return u'Set-top box'
         elif minor_device_class == 40:
            return u'HiFi Audio Device'
         elif minor_device_class == 44:
            return u'VCR'
         elif minor_device_class == 48:
            return u'Video Camera'
         elif minor_device_class == 52:
            return u'Camcorder'
         elif minor_device_class == 56:
            return u'Video Monitor'
         elif minor_device_class == 60:
            return u'Vid. Disp. & Speaker'
         elif minor_device_class == 64:
            return u'Video Conferencing'
         elif minor_device_class == 68:
            return u'New Audio/Video'
         elif minor_device_class == 72:
            return u'Gaming/Toy'
         else:
            return u'New Audio/Video'
      elif major_device_class == 5:
         bin_minor_class = int(dec2bin(minor_device_class))
         bin_minor_class = '%08i' % bin_minor_class
         bin_minor_1 = bin_minor_class[:2]
         bin_minor_2 = bin_minor_class[2:5]
         if bin_minor_1 == '01':
            dev1 = u'Keyboard'
         elif bin_minor_1 == '10':
            dev1 = u'Pointing Device'
         elif bin_minor_1 == '11':
            dev1 = u'Combo Key/Pointing'
         else:
            dev1 = u''
         if bin_minor_2 == '0001':
            dev2 = u'Joystick'
         elif bin_minor_2 == '0010':
            dev2 = u'Gamepad'
         elif bin_minor_2 == '0011':
            dev2 = u'Remote Control'
         elif bin_minor_2 == '0100':
            dev2 = u'Sensing Device'
         elif bin_minor_2 == '0101':
            dev2 = u'Digitizer tablet'
         elif bin_minor_2 == '0110':
            dev2 = u'Card Reader'
         else:
            dev2 =u''
         if (len(dev1) == 0) and (len(dev2) == 0):
            return u'Peripheral'
         elif (len(dev1) > 0) and (len(dev2) == 0):
            return dev1
         elif (len(dev1) == 0) and (len(dev2) > 0):
            return dev2
         else:
            return dev1 + u'/' + dev2
      elif major_device_class == 6:
         dev1 = dev2 = dev3 = dev4 = u''
         bin_minor_class = int(dec2bin(minor_device_class))
         bin_minor_class = '%08i' % bin_minor_class
         bin_minor_1 = bin_minor_class[:4]
         if bin_minor_1[0] == '1':
            dev1 = u'Printer'
         if bin_minor_1[1] == '1':
            dev2 = u'Scanner'
         if bin_minor_1[2] == '1':
            dev3 = u'Camera'
         if bin_minor_1[3] == '1':
            dev4 = u'Display'
         dev = dev1+dev2+dev3+dev4
         if len(dev) == 0:
            return u'Imaging'
         else:
            return dev
      elif major_device_class == 7:
         if minor_device_class == 0:
            return u'Wearable Class'
         elif minor_device_class == 4:
            return u'Wrist Watch'
         elif minor_device_class == 8:
            return u'Pager'
         elif minor_device_class == 12:
            return u'Jacket'
         elif minor_device_class == 16:
            return u'Helmet'
         elif minor_device_class == 20:
            return u'Glasses'
         else:
            return u'New Wearable Class'
      elif major_device_class == 8:
         if minor_device_class == 0:
            return u'Toy Class'
         elif minor_device_class == 4:
            return u'Robot'
         elif minor_device_class == 8:
            return u'Vehicle'
         elif minor_device_class == 12:
            return u'Doll / Action Figure'
         elif minor_device_class == 16:
            return u'Controller'
         elif minor_device_class == 20:
            return u'Game'
         else:
            return u'New Toy Class'
      elif major_device_class == 9:
         if minor_device_class == 0:
            return u'Medical Class'
         elif minor_device_class == 4:
            return u'Blood Pressure Monitor'
         elif minor_device_class == 8:
            return u'Thermometer'
         elif minor_device_class == 12:
            return u'Weighing Scale'
         elif minor_device_class == 16:
            return u'Glucose Meter'
         elif minor_device_class == 20:
            return u'Pulse Oximeter'
         elif minor_device_class == 24:
            return u'Heart/Pulse Rate Monitor'
         elif minor_device_class == 28:
            return u'Medical Data Display'
         else:
            return u'New Medical Class'
      else:
         return u'unknown'
   else:
      return u'n/a'
      
def bt_scan():
   global btscan, btquery_list, bt_busy, bt_scan_time, oui_list
   bt_busy = True
   bt_scan_time = 0
   try:
      btscan = lightblue.finddevices()
   except:
      btscan = []
   btquery_list = []
   for i in range(len(btscan)):
      dc = unicode(btscan[i][2])
      if len(dc) > 0:
         dc = unicode("%X"%(int(dc)))
         btscan[i] =[btscan[i][0], btscan[i][1], dc, bt_device_class(dc)]
      else:
         btscan[i] =[btscan[i][0], btscan[i][1], dc, u'']
   for i in range(len(btscan)):
      ssid = btscan[i][1]
      if (ssid.count(chr(0)) == len(ssid)) and (len(ssid) > 0):
         btscan[i] =[btscan[i][0], u'<no ssid> '+unicode(len(ssid))+u' Chrs', btscan[i][2], btscan[i][3]]
      else:
         ssid = ssid.replace(chr(59),",")
         ssid = ssid.replace(chr(34),"``")
         ssid = is_not_control(ssid)
         ouiname = ""
         oui_line_num = binaere_suche(oui_list, btscan[i][0][0:8], 8)
         if oui_line_num > -1:                  
            ssid = "%s^%s" % (ssid, oui_list[oui_line_num][7:27].strip())

         btscan[i] = [btscan[i][0], ssid, btscan[i][2], btscan[i][3]]
      
   for i in range(len(btscan)):
      btquery_list.append(query_bt(btscan[i]))
   bt_busy = False
   
def draw_wlan(size):
   global wlan, wscan, scroll_wlan
   (w, h) = size
   draw_setup(HEADHEIGHT, LINEHEIGHT)
   if not wlan:
      draw_text(3, u'wlantools are missing!')
      return
   if len(wscan) == 0:
      draw_text(3, u'no WLANs found.')
      draw_text(3, unicode(len(wlan_list)-1)+u' WLANs in Database.')
      draw_text(3, unicode(newwlans)+u' new WLANs found.')
      draw_text(3, unicode(wlangpsupdate)+u' WLAN GPS Updates done.')
      scroll_wlan = 0
      return

   if w < 250:
      xpos,width = measure_table(['WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW'], ['#', 'CH', '-99'])
      #xpos = (TABSPACE/2, w-TLENGTH_C-TLENGTH_RXL-2*TABSPACE, w-TLENGTH_RXL-TABSPACE/2)
      if show_ssid:
         if scroll_wlan > 0:
            draw_table(xpos, (chr(94)+u'SSID   '+unicode(len(wlan_list)-1)+u'('+unicode(newwlans)+u'-'+unicode(wlangpsupdate)+u')', u'C', u'CH', u'RXL'), width=w)
         else:
            draw_table(xpos, (u'SSID   '+unicode(len(wlan_list)-1)+u'('+unicode(newwlans)+u'-'+unicode(wlangpsupdate+wlanwpsupdate+wlancpsupdate)+u')', u'C', u'CH', u'RXL'), width=w)
      else:
         if scroll_wlan > 0:
            draw_table(xpos, (chr(94)+u'BSSID  '+unicode(len(wlan_list)-1)+u'('+unicode(newwlans)+u'-'+unicode(wlangpsupdate+wlanwpsupdate+wlancpsupdate)+u')', u'C', u'CH', u'RXL'), width=w)
         else:
            draw_table(xpos, (u'BSSID  '+unicode(len(wlan_list)-1)+u'('+unicode(newwlans)+u'-'+unicode(wlangpsupdate+wlanwpsupdate+wlancpsupdate)+u')', u'C', u'CH', u'RXL'), width=w)
   elif w < 500:
      xpos,width = measure_table(['WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW'], ['WpaPsk', 'CH', '-99'])
      if show_ssid:
         if scroll_wlan > 0:
            draw_table(xpos, (chr(94)+u'SSID       '+unicode(len(wlan_list)-1)+u'('+unicode(newwlans)+u'-'+unicode(wlangpsupdate+wlanwpsupdate+wlancpsupdate)+u')', u'Crypt', u'CH', u'RXL'), width=w)
         else:
            draw_table(xpos, (u'SSID       '+unicode(len(wlan_list)-1)+u'('+unicode(newwlans)+u'-'+unicode(wlangpsupdate+wlanwpsupdate+wlancpsupdate)+u')', u'Crypt', u'CH', u'RXL'), width=w)
      else:
         if scroll_wlan > 0:
            draw_table(xpos, (chr(94)+u'BSSID       '+unicode(len(wlan_list)-1)+u'('+unicode(newwlans)+u'-'+unicode(wlangpsupdate+wlanwpsupdate+wlancpsupdate)+u')', u'Crypt', u'CH', u'RXL'), width=w)
         else:
            draw_table(xpos, (u'BSSID       '+unicode(len(wlan_list)-1)+u'('+unicode(newwlans)+u'-'+unicode(wlangpsupdate+wlanwpsupdate+wlancpsupdate)+u')', u'Crypt', u'CH', u'RXL'), width=w)      
   else:
      #xpos = (3, 350, 500, w-TLENGTH_199DBM-3)
      xpos,width = measure_table(['WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW'], ['99:99:99:99:99:99l', 'Infrastructurel', 'WpaPskW', 'CHl', '-99dBm'])
      if scroll_wlan > 0:
         draw_table(xpos, (chr(94)+u'SSID       '+unicode(len(wlan_list)-1)+u'('+unicode(newwlans)+u'-'+unicode(wlangpsupdate+wlanwpsupdate+wlancpsupdate)+u')', u'BSSID', u'ConnectMode', u'Crypt', u'CH', u'RxLev'), width=w)
      else:
         draw_table(xpos, (u'SSID       '+unicode(len(wlan_list)-1)+u'('+unicode(newwlans)+u'-'+unicode(wlangpsupdate+wlanwpsupdate+wlancpsupdate)+u')', u'BSSID', u'ConnectMode', u'Crypt', u'CH', u'RxLev'), width=w)
   draw_space(2)
   for j in range(len(wscan)):
      if j+scroll_wlan < len(wscan):
         i = j+scroll_wlan      
         if wscan[i]['SecurityMode']==u'Open':
            crypt = u''
         elif wscan[i]['SecurityMode']==u'Wep':
            crypt = u'+'
         else:
            crypt = u'#'
         rxl = -abs(wscan[i]['RxLevel'])
         if len(wscan) == len(wlanquery_list): #to avoid list index out of range errors
            if rxl <= -100:
               rxl = -rxl
            if w < 250:
               if show_ssid:
                  if wscan[i]['ConnectionMode'] == 'Adhoc':
                     draw_table(xpos, (wscan[i]['SSID'], crypt, wscan[i]['Channel'], rxl), width=w, highlight=wlanquery_list[i], italic=True)
                  else:
                     draw_table(xpos, (wscan[i]['SSID'], crypt, wscan[i]['Channel'], rxl), width=w, highlight=wlanquery_list[i])
               else:
                  if wscan[i]['ConnectionMode'] == 'Adhoc':
                     draw_table(xpos, (wscan[i]['BSSID'], crypt, wscan[i]['Channel'], rxl), width=w, highlight=wlanquery_list[i], italic=True)
                  else:
                     draw_table(xpos, (wscan[i]['BSSID'], crypt, wscan[i]['Channel'], rxl), width=w, highlight=wlanquery_list[i])
            elif w < 500:
               if show_ssid:
                  if wscan[i]['ConnectionMode'] == 'Adhoc':
                     draw_table(xpos, (wscan[i]['SSID'], \
                        wscan[i]['SecurityMode'], \
                        wscan[i]['Channel'], \
                        unicode(rxl)), width=w, highlight=wlanquery_list[i], italic=True)
                  else:
                     draw_table(xpos, (wscan[i]['SSID'], \
                        wscan[i]['SecurityMode'], \
                        wscan[i]['Channel'], \
                        unicode(rxl)), width=w, highlight=wlanquery_list[i])
               else:
                  if wscan[i]['ConnectionMode'] == 'Adhoc':
                     draw_table(xpos, (wscan[i]['BSSID'], \
                        wscan[i]['SecurityMode'], \
                        wscan[i]['Channel'], \
                        unicode(rxl)), width=w, highlight=wlanquery_list[i], italic=True)
                  else:
                     draw_table(xpos, (wscan[i]['BSSID'], \
                        wscan[i]['SecurityMode'], \
                        wscan[i]['Channel'], \
                        unicode(rxl)), width=w, highlight=wlanquery_list[i])               
            else:
               draw_table(xpos, (wscan[i]['SSID'], \
                  wscan[i]['BSSID'], \
                  wscan[i]['ConnectionMode'], \
                  wscan[i]['SecurityMode'], \
                  wscan[i]['Channel'], \
                  unicode(rxl)+u'dBm'), width=w, highlight=wlanquery_list[i])

def draw_clf(size):
   #global cell_lon, cell_lat
   (w, h) = size
   draw_setup(HEADHEIGHT, LINEHEIGHT)
   draw_text(CENTER, unicode(len(clf)-1)+u' cells  '+u'New: '+unicode(newcells), space=2, width=w)
   draw_space(20)
   draw_text(CENTER, cell_description, space=2, width=w)
   draw_space(10)
   #dcell_lat = '%0.6f'%float(cell_lat)
   #dcell_lon = '%0.6f'%float(cell_lon)
   draw_text(CENTER, u'LAT: '+ cell_lat, space=2, width=w)
   draw_text(CENTER, u'LON: '+ cell_lon, space=2, width=w)
   draw_space(10)
   #draw_text(CENTER, u'BT Save Error: '+unicode(bt_save_error), space=2, width=w)
   #draw_text(3, unicode(invalid_bt), space=2, width=w)
   
def draw_bt(size):
   global btscan, btlist, scroll_bt
   (w, h) = size
   draw_setup(HEADHEIGHT, LINEHEIGHT)
   if not bt:
      draw_text(3, u'LightBlue or BlueS are missing!')
      return
   if len(btscan) == 0:
      draw_text(3, u'no BT Devices found.')
      draw_text(3, unicode(len(bt_list)-1)+u' BTs in Database.')
      draw_text(3, unicode(newbt)+u' new BTs found.')
      draw_text(3, unicode(btgpsupdate)+u' BT Updates done.')
      scroll_bt = 0
      return
   if w < 250:
      xpos,width = measure_table(['WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW'], ['WWWWW'])
      #xpos = (TABSPACE/2, w-TLENGTH_C-TLENGTH_RXL-2*TABSPACE, w-TLENGTH_RXL-TABSPACE/2)
      if show_ssid:
         if scroll_bt > 0:
            draw_table(xpos, (chr(94)+u'Name   '+unicode(len(bt_list)-1)+u'('+unicode(newbt)+u'-'+unicode(btgpsupdate)+u')', u'Class'), width=w)
         else:
            draw_table(xpos, (u'Name   '+unicode(len(bt_list)-1)+u'('+unicode(newbt)+u'-'+unicode(btgpsupdate)+u')', u'Class'), width=w)
      else:
         if scroll_bt > 0:
            draw_table(xpos, (chr(94)+u'MAC  '+unicode(len(bt_list)-1)+u'('+unicode(newbt)+u'-'+unicode(btgpsupdate)+u')', u'Class ID'), width=w)
         else:
            draw_table(xpos, (u'MAC  '+unicode(len(bt_list)-1)+u'('+unicode(newbt)+u'-'+unicode(btgpsupdate)+u')', u'Class ID'), width=w)
   elif w < 500:
      xpos,width = measure_table(['WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW'], ['WWWWWWWW'])
      if show_ssid:
         if scroll_bt > 0:
            draw_table(xpos, (chr(94)+u'Name       '+unicode(len(bt_list)-1)+u'('+unicode(newbt)+u'-'+unicode(btgpsupdate)+u')', u'Class'), width=w)
         else:
            draw_table(xpos, (u'Name       '+unicode(len(bt_list)-1)+u'('+unicode(newbt)+u'-'+unicode(btgpsupdate)+u')', u'Class'), width=w)
      else:
         if scroll_bt > 0:
            draw_table(xpos, (chr(94)+u'MAC      '+unicode(len(bt_list)-1)+u'('+unicode(newbt)+u'-'+unicode(btgpsupdate)+u')', u'Class ID'), width=w)
         else:
            draw_table(xpos, (u'MAC      '+unicode(len(bt_list)-1)+u'('+unicode(newbt)+u'-'+unicode(btgpsupdate)+u')', u'Class ID'), width=w)      
   else:
      #xpos = (3, 350, 500, w-TLENGTH_199DBM-3)
      xpos,width = measure_table(['WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW'], ['99:99:99:99:99:99l', '2000000', 'Video Display & LoudSpeaker'])
      if scroll_bt > 0:
         draw_table(xpos, (chr(94)+u'Name       '+unicode(len(bt_list)-1)+u'('+unicode(newbt)+u'-'+unicode(btgpsupdate)+u')', u'MAC', u'Class ID', u'Class'), width=w)
      else:
         draw_table(xpos, (u'Name       '+unicode(len(bt_list)-1)+u'('+unicode(newbt)+u'-'+unicode(btgpsupdate)+u')', u'MAC', u'Class ID', u'Class'), width=w)
   draw_space(2)
   for j in range(len(btscan)):
      if j+scroll_bt < len(btscan):
         i = j+scroll_bt      
         if len(btscan) == len(btquery_list): #to avoid list index out of range errors
            if w < 250:
               if show_ssid:
                  draw_table(xpos, (btscan[i][1], btscan[i][3]), width=w, highlight=btquery_list[i])
               else:
                  draw_table(xpos, (btscan[i][0], btscan[i][2]), width=w, highlight=btquery_list[i])
            elif w < 500:
               if show_ssid:
                  draw_table(xpos, (btscan[i][1], btscan[i][3]), width=w, highlight=btquery_list[i])
               else:
                  draw_table(xpos, (btscan[i][0], btscan[i][2]), width=w, highlight=btquery_list[i])                     
            else:
               draw_table(xpos, (btscan[i][1], btscan[i][0], btscan[i][2], btscan[i][3]), width=w, highlight=btquery_list[i])   


def reader(text):
   try:
      audio.say(text)
   except Exception, error:
      # no GUI from sub-thread!
      #appuifw.note(u"Sound Error: "+unicode(error),'error')
      pass

def gps_update(args):
   global gpsdata, gpson
   gpsdata = args
   if (not gpson):
      lockgps.signal()
      gpsdata = [0, 'GPS stopped']

def gps_find_device(lr, type, mode):
   count = lr.GetNumModules()
   if count > 4:
      count = 4
   for i in range(count):
      info = lr.GetModuleInfoByIndex(i)
      if ((info[3] == type) and (info[2] == mode)):
         return info[0]
   return -1

def gps_worker():
   global lockgps, gpsmodule
   lockgps = e32.Ao_lock()
   # create LocationRequestor instance
   lr = locationrequestor.LocationRequestor()
   # show default module
   #print 'Default', lr.GetDefaultModuleId()
   # show number of modules
   #print 'Count', count
   # find internal GPS (if any)
   if config['GPS'] == Setup.GPS_INTERNAL:
      probe = [locationrequestor.EDeviceInternal,
             locationrequestor.EDeviceExternal]
      mode = 1
   elif config['GPS'] == Setup.GPS_ASSISTED:
      probe = [locationrequestor.EDeviceInternal,
             locationrequestor.EDeviceExternal]
      mode = 4
   else:
      probe = [locationrequestor.EDeviceExternal,
             locationrequestor.EDeviceInternal]
      mode = 1
   
   id = gps_find_device(lr, probe[0], mode)
   if id == -1:
      id = gps_find_device(lr, probe[1], 1)

   if id == -1:
      gpsdata = [0, 'Neither internal nor external GPS available']
      return
   gpsmodule = unicode(id)

   # set update options
   lr.SetUpdateOptions(1, 25, 0, 1)
   # connect to position module
   lr.Open(id)
   # install callback
   try:
      lr.InstallPositionCallback(gps_update)
   except Exception, reason:
      #appuifw.note(unicode(reason),'error')
      pass

   lockgps.wait()
   lr.Close()

def log_worker():
   global gsmloc, gsmloc_real, rxl, gui, t_last, running, script_lock
   t_old = 0
   while running:
      t_last = time.time()
      try:
         rxl = -sysinfo.signal_dbm()
         if rxl == 0:
            # Workaround Nokia dumbness:
            rxl = None
      except SystemError:
         rxl = None
      try:
         oldloc = gsmloc
         gsmloc_real = location.gsm_location()
         #if t_last % 10 < 3:
         #   gsmloc_real = None
         # Workaround for "no location during data traffic"
         if gsmloc_real is None and rxl: # and t_old + offlinetimeout < t_last:
            # We are busy, simulate last cell for history
            gsmloc = oldloc
         else:
            # Update state
            gsmloc = gsmloc_real
            t_old = t_last
      except (ValueError, SystemError):
         gsmloc = gsmloc_real = None
      log_rxl(t_last, rxl)
      if gsmloc is None or not rxl:
         log_loc(t_last, (None, None, None, None))
      else:
         log_loc(t_last, gsmloc)
      gui.signal()
      e32.ao_sleep(1)
   # we are finished
   script_lock.signal()

def read_cell(rxl, umts, mcc, mnc, cid, lac, readlac):
   #sound.set_volume(config['Volume'])
   voice = u''
   if not rxl:
      voice = Voice.offline
   elif config['Voice']==Setup.VOICE_CELL:
      voice = unicode(number2word(cid,config3['LANGUAGE']))
   elif config['Voice']==Setup.VOICE_BAND:
      voice = Voice.band[umts] + u"  " + unicode(number2word(cid,config3['LANGUAGE']))
   elif config['Voice']==Setup.VOICE_BAND_LAC:
      voice = Voice.band[umts] + u"  " + unicode(number2word(cid,config3['LANGUAGE']))
      if readlac:
         voice += u'. L A C '+unicode(number2word(lac,config3['LANGUAGE']))
   elif config['Voice']==Setup.VOICE_BAND_LAC_NET:
      voice = Voice.band[umts] + u"  "
      if readlac:
         if mcc in Voice.provider and mnc in Voice.provider[mcc]:
            voice += Voice.provider[mcc][mnc]
         else:
            voice += u'M C C '+unicode(number2word(mcc,config3['LANGUAGE']))+u' M N C '+unicode(number2word(mnc,config3['LANGUAGE']))
         voice += u". " + unicode(number2word(cid,config3['LANGUAGE'])) + u'. L A C '+unicode(number2word(lac,config3['LANGUAGE']))
      else:
         voice += unicode(number2word(cid,config3['LANGUAGE']))
   thread.start_new_thread(reader,(voice,))

def netmonitor():
   global running, toggle, rxl, gsmloc, img, img_dbl, wlan, wlani, wscan, dbsearch, neighbour_updated, lb, \
         gl_size, bt_scan_time, headfont, myfont, TABHEIGHT, LINEHEIGHT, LINEY, HDLFRAME, HDLH, HDLY, \
         HEADHEIGHT, TLENGTH_TIME, new_cells_lb, new_cells_updated, eclf, cellselect, lacselect, imsi, imei
   busytext = ['n/a', 'busy']
   imei=sysinfo.imei()
   #try:
   #imsi=elocation.get_imsi()
   imsi='not yet supported'
   #except:
   #   appuifw.note(u"Update your elocation modul!",'error')
   ver = sysinfo.os_version()
   oldcid = 0
   oldlac = 0
   t_log = 0
   wlan_autosave = 0
   bt_autosave = 0
   clf_autosave = 0
   bti = 0
   bt_block = 0
   pos_update = 0
   while running:
      # Block when Camera is active
      
      while finder:
         e32.ao_sleep(0.5)
      size,offset = appuifw.app.layout(appuifw.EMainPane)
      if (size[0] == 800) and (size <> gl_size):
         if config['FONT_SIZE'] == Setup.FONT_SIZE_SMALL:
            myfont = (None,16,0)
            headfont = (None,16,0)
         elif config['FONT_SIZE'] == Setup.FONT_SIZE_MEDIUM:
            myfont = (None,18,FONT_BOLD)
            headfont = (None,18,FONT_BOLD)
         elif config['FONT_SIZE'] == Setup.FONT_SIZE_LARGE:
            myfont = (None,20,FONT_BOLD)
            headfont = (None,20,FONT_BOLD)
         elif config['FONT_SIZE'] == Setup.FONT_SIZE_XLARGE:
            myfont = (None,22,FONT_BOLD)
            headfont = (None,22,FONT_BOLD)
         (box,TLENGTH_TIME,numb) = img.measure_text(u'23:59:59', font=headfont)
         (box,numb,numb) = img.measure_text(u'ABCDEFGHIJKLMNOPQRSTUVWXYabcdefghijklmnopqrstuvwxyz09,;!#()', font=myfont)
         TABHEIGHT = LINEHEIGHT = box[3] - box[1] + 0
         LINEY = -box[1] + 1
         # Headline size: frame; total height; y position for text
         HDLFRAME = 2
         (HDLBOX,numb,numb) = img.measure_text(u'C: 99999 W: G:', font=headfont)
         HDLH = HDLBOX[3] - HDLBOX[1] + 2*HDLFRAME
         HDLY = -HDLBOX[1] + HDLFRAME
         HEADHEIGHT = 2*HDLH + 2*HDLFRAME
         del HDLBOX, box, numb
      elif (size[0] < 800) and (size <> gl_size):
         if config['FONT_SIZE'] == Setup.FONT_SIZE_SMALL:
            myfont = (None,12,0)
            headfont = (None,12,0)
         elif config['FONT_SIZE'] == Setup.FONT_SIZE_MEDIUM:
            myfont = (None,14,FONT_BOLD)
            headfont = (None,14,FONT_BOLD)
         elif config['FONT_SIZE'] == Setup.FONT_SIZE_LARGE:
            myfont = (None,16,FONT_BOLD)
            headfont = (None,16,FONT_BOLD)
         elif config['FONT_SIZE'] == Setup.FONT_SIZE_XLARGE:
            myfont = (None,18,FONT_BOLD)
            headfont = (None,18,FONT_BOLD)
         (box,TLENGTH_TIME,numb) = img.measure_text(u'23:59:59', font=headfont)
         (box,numb,numb) = img.measure_text(u'ABCDEFGHIJKLMNOPQRSTUVWXYabcdefghijklmnopqrstuvwxyz09,;!#()', font=myfont)
         TABHEIGHT = LINEHEIGHT = box[3] - box[1] + 0
         LINEY = -box[1] + 1
         # Headline size: frame; total height; y position for text
         HDLFRAME = 2
         (HDLBOX,numb,numb) = img.measure_text(u'C: 99999 W: G:', font=headfont)
         HDLH = HDLBOX[3] - HDLBOX[1] + 2*HDLFRAME
         HDLY = -HDLBOX[1] + HDLFRAME
         HEADHEIGHT = 2*HDLH + 2*HDLFRAME
         del HDLBOX, box, numb
         #if len(neighbour_list) > 0:
            #lb.set_list(neighbour_list)
         #   pass
         #else:
         #   #lb.set_list([u'Empty Neighbour List'])
         #   pass
         #if len(new_cells_list) > 0:
         #   new_cells_lb.set_list(new_cells_list)
         #else:
         #   new_cells_lb.set_list([u'No new cells found'])
      gl_size = size
      img.rectangle((0,0)+size,outline=border,fill=bg)
      if gsmloc_real is None and gsmloc is not None:
         busy = True
      else:
         busy = False
      if gsmloc is None or not rxl or busy:
         mcc = mnc = lac = lachex = cid = cidhex = longcid = longcidhex = rnc = cid = busytext[busy]
      else:
         (mcc, mnc, lac, cid) = gsmloc
         if cid > 65535:
            umts = 1
            longcid = cid
            longcidhex = "%X"%(longcid)
         else:
            umts = 0
            longcid = longcidhex = busytext[busy]
         (cid, rnc) = decode_cid(cid)
         try:
            lachex = "%X"%(lac)
         except:
            lachex = busytext[busy]
         try:
            cidhex = "%X"%(cid)
         except:
            cidhex = busytext[busy]
         if config2['GSM_LOG_EVENT']==Setup2.GSM_LOG_EVENT_SEC:
            log_event = True
         else:
            log_event = False
         if (cid != oldcid) and not clf_saving and not cell_searching:
            cellselect += 1
            oldcid = cid
            log_event = True
            thread.start_new_thread(query_clf,(mcc, mnc, cid, lac, rnc, umts))
            #query_clf(mcc, mnc, cid, lac, rnc, umts)
            # Cell changed, notify the user
            if config['Light']==Setup.LIGHT_CELL:
               e32.reset_inactivity()
            if config['CellNotify']==Setup.SOUND_SOUND:
               sound_play()
               #thread.start_new_thread(sound_play,())
            elif config['CellNotify']==Setup.SOUND_VOICE:
               read_cell(rxl, umts, mcc, mnc, cid, lac, oldlac != lac)
            if lac != oldlac:
               lacselect += 1
            oldlac = lac
      if neighbour_updated:
         #lb = appuifw.Listbox(neighbour_list, handle_selection)
         lb.set_list(neighbour_list)
         neighbour_updated = False
         appuifw.note(u'Neighbour List updated! '+unicode(len(neighbour_list))+u' Neighbour cells found within '+unicode(config['Neighbour Radius'])+u' km Radius', 'info')
      if new_cells_updated:
         #eclf=[]
         #map(unicode,eclf)
         #new_cells_lb = appuifw.Listbox(new_cells_list, handle_new_cell_selection)
         new_cells_lb.set_list(new_cells_list)
         new_cells_updated = False
      if tab==0:
         appuifw.app.body=canvas
         draw_netmon(lac, mcc, mnc, rnc, rxl, ver, imei, longcid, cidhex, lachex, longcidhex, size, cid)
      elif tab==1:
         appuifw.app.body=canvas
         draw_rxlgraph(size)
      elif tab==2:
         appuifw.app.body=canvas
         draw_history(size)
      elif tab==3:
         appuifw.app.body=canvas
         draw_gps(size)
      elif tab==4:
         appuifw.app.body=canvas
         draw_wlan(size)
      elif tab==5:
         appuifw.app.body=canvas
         draw_clf(size)
      elif tab==6:
         appuifw.app.body=canvas
         draw_radar(size)
      elif tab==7:
         appuifw.app.body=canvas
      elif tab==8:   
         appuifw.app.body=canvas
         draw_bt(size)
      elif tab==9:   
         appuifw.app.body=canvas
         draw_stats(size)
      elif tab==10:   
         appuifw.app.body=lb
      elif tab==11:   
         appuifw.app.body=new_cells_lb
      elif tab==12:
         appuifw.app.body=canvas
         draw_about(imei)
      # Headline for all but "About" and listboxes
      if tab <= 9:
         headline(size, cid)

      tmp = img_dbl
      img_dbl = img
      img = tmp
      handle_redraw(())
      if logger and log_event:
         if t_log != t_last:
            # Only log coords when GPS is there and values are not NaN
            if (gpson == 1) and (len(gpsdata) == 15) and str(gpsdata[1]) != 'NaN':
               # Convert lat, lon to formatted strings
               (lat, lon) = map(lambda x: "%2.6f" % x, gpsdata[1:3])
               speed = '%0.1f'%gpsdata[8]
               if (cell_lat != u'999.99999'):
                  (ldx, laz) = distance(float(gpsdata[1]), float(gpsdata[2]), float(cell_lat), float(cell_lon))
                  logdx = "%0.3f"%ldx
               else:
                  logdx = 'n/a'
            else:
               lon = lat = speed = logdx = 'n/a'
            if rxl:
               trxl = rxl
            else:
               trxl = 'n/a'
            writelog((time.strftime("%Y/%m/%d"), time.strftime("%H:%M:%S"), cid, longcid, lac, mcc, mnc, rnc, trxl, lon, lat, speed, logdx))
            t_log = t_last
      if config['Light']==Setup.LIGHT_ALWAYS:
         e32.reset_inactivity()
      if wlan and (wlani>=config['Refresh']) and (config['Refresh']>8) and not wlan_saving and not wlan_scanning:
         wlani = 0
         thread.start_new_thread(wlan_scan,())
      if config['Refresh']>8:
         wlani += 1
         wlan_autosave += 1
         if (wlan_autosave > config['WLANInter']*60) and not wlan_saving and not wlan_scanning:
            wlan_autosave = 0
            thread.start_new_thread(save_wlan,())
      if config['BT_SCAN'] > 0 and not bt_busy and bt:
         bti += 1
         bt_autosave += 1
         if (bti > config['BT_SCAN']*1) and not bt_busy and not bt_saving:
            bti = 0
            thread.start_new_thread(bt_mainthread,())
         if (bt_autosave > config['BT_Autosave']*60) and not bt_saving:
            bt_autosave = 0
            thread.start_new_thread(save_bt,())
      if bt_busy:
         bt_scan_time += 1
      if (clf_autosave > config['CLF_AUTOSAVE']*60) and not clf_saving and not cell_searching:
         clf_autosave = 0
         thread.start_new_thread(save_clf,())
      clf_autosave += 1
      if save_error:
         appuifw.note(u"PyNetMony has detected a dataloss!",'error')
         appuifw.query(u"Please watch your backup files and rename them! PyNetmony will be shut down", "query")
         e32.ao_sleep(0.05)
         show_text(u"Shutting down.")
         e32.ao_sleep(0.05)
         finish()
      if config2['POSUPDATE'] > 1:
         pos_update += 1
         if pos_update > config2['POSUPDATE']*60:
            register(False)
            pos_update = 0
      
      gui.wait()


def handle_redraw(rect):
   global img_dbl, canvas
   
   if mapimg and (tab==7):
      canvas.blit(mapimg, target=(0, 0), source=(map_x, map_y))
   else:
      canvas.blit(img_dbl)
   if status:
      canvas.clear(0)
      canvas.text((10, 120), status, fill=(255, 255, 255), font="title")

def handle_event(event):
   global img_dbl, canvas, key_repeat, show_ssid, scroll_wlan, scroll_bt, wlan_radar_zoom, heading_north
   if event['type'] == appuifw.EEventKeyDown:
      sc = event['scancode']
      key_repeat = 0
      #print event
      if (sc > EScancode0) and (sc <= EScancode0 + tab_max):
         newtab = sc - EScancode0 - 1
         appuifw.app.activate_tab(newtab)
         set_tab(newtab)
      elif sc == EScancode0:
         appuifw.app.activate_tab(9)
         set_tab(9)
      if sc == EScancodeSelect:
         if tab == 4 or tab == 8:
            if show_ssid:
               show_ssid = False
            else:
               show_ssid = True
         if tab == 6:
            if heading_north:
               heading_north = False
            else:
               heading_north = True
      if sc == EScancodeDownArrow:
         if tab == 4:
            scroll_wlan += 1
         elif tab == 8:
            scroll_bt += 1
         elif tab == 6:
            wlan_radar_zoom -=0.03
      if sc == EScancodeUpArrow:
         if tab == 4:
            scroll_wlan -= 1
         elif tab == 8:
            scroll_bt -= 1
         elif tab == 6:
            wlan_radar_zoom +=0.03
      if scroll_wlan < 0:
         scroll_wlan = 0
      if scroll_bt < 0:
         scroll_bt = 0
      if wlan_radar_zoom < 0.03:
         wlan_radar_zoom = 0.03
   elif event['type'] == appuifw.EEventKey:
      sc = event['scancode']
      key_repeat += 1
      if key_repeat == 2:
         if sc == EScancodeStar:
            toggle_log()
            gui.signal()
         elif sc == EScancodeHash:
            toggle_gps()
            gui.signal()


def standalone():
   # XXX: use appuifw.app.uid()
   # TITLE in full_name() means standalone
   return appuifw.app.full_name().find(TITLE) != -1

def exit_key_handler():
   global window, image_splash
   if appuifw.query(u'Do you really want to exit?', 'query'):
      #(width, height) = sysinfo.display_pixels()
      size,offset = appuifw.app.layout(appuifw.EMainPane)
      (width, height) = size
      if width == 240:
         height = 320
      elif width == 320:
         height = 240
      elif width == 800:
         height = 352
      e32.ao_sleep(0.05)
      #image_splash.clear()
      #image_splash = graphics.Image.open(u'c:\\Data\Others\PyNetMony\\pynetmony.jpg')
      #image_splash.text((40,50), u'Shutting down...',font=(None,18,FONT_BOLD))
      #window.add_image(image_splash, (0,0,width, height))
      #window.size = (width, height)
      #window.show()
      e32.ao_sleep(0.05)
      finish()

def finish():
   global running, s, clf_umts, clf_gsm, neighbour_list, wlan_list, bt_list, window, image_splash, gwidth, gheight
   # inform the worker threads
   running = False
   size,offset = appuifw.app.layout(appuifw.EMainPane)
   (width, height) = size
   if width == 240:
      height = 320
   elif width == 320:
      height = 240
   elif width == 800:
      height = 352
   gwidth = width
   gheight = height
   #image_splash.clear()
   #image_splash = graphics.Image.open(u'c:\\Data\Others\PyNetMony\\pynetmony.jpg')
   #image_splash.text((3,50), u'Waiting max. 1 min for CLF...',font=(None,18,FONT_BOLD))
   #window.add_image(image_splash, (0,0,width, height))
   #window.size = (width, height)
   #window.show()
   e32.ao_sleep(0.05)
   i = 0
   while cell_searching or clf_saving:
      e32.ao_sleep(1)
      i += 1
      if i > 60:
         break
   #image_splash.clear()
   #image_splash = graphics.Image.open(u'c:\\Data\Others\PyNetMony\\pynetmony.jpg')
   #image_splash.text((40,50), u'Saving CLF...',font=(None,18,FONT_BOLD))
   #window.add_image(image_splash, (0,0,width, height))
   #window.show()
   e32.ao_sleep(0.05)
   save_clf()
   #image_splash.clear()
   #image_splash = graphics.Image.open(u'c:\\Data\Others\PyNetMony\\pynetmony.jpg')
   #image_splash.text((3,50), u'Waiting max. 1 min for WLAN...',font=(None,18,FONT_BOLD))
   #window.add_image(image_splash, (0,0,width, height))
   #window.show()
   e32.ao_sleep(0.05)
   i = 0
   while wlan_saving or wlan_scanning:
      e32.ao_sleep(1)
      i += 1
      if i > 60:
         break
   #image_splash.clear()
   #image_splash = graphics.Image.open(u'c:\\Data\Others\PyNetMony\\pynetmony.jpg')
   #image_splash.text((40,50), u'Saving WLAN...',font=(None,18,FONT_BOLD))
   #window.add_image(image_splash, (0,0,width, height))
   #window.show()
   e32.ao_sleep(0.05)
   save_wlan()
   #image_splash.clear()
   #image_splash = graphics.Image.open(u'c:\\Data\Others\PyNetMony\\pynetmony.jpg')
   #image_splash.text((3,50), u'Waiting max. 1 min for BT...',font=(None,18,FONT_BOLD))
   #window.add_image(image_splash, (0,0,width, height))
   #window.show()
   e32.ao_sleep(0.05)
   i = 0
   while bt_saving or bt_busy:
      e32.ao_sleep(1)
      i += 1
      if i > 60:
         break
   #image_splash.clear()
   #image_splash = graphics.Image.open(u'c:\\Data\Others\PyNetMony\\pynetmony.jpg')
   #image_splash.text((40,50), u'Saving BT...',font=(None,18,FONT_BOLD))
   #window.add_image(image_splash, (0,0,width, height))
   #window.show()
   e32.ao_sleep(0.05)
   save_bt()
   #image_splash.clear()
   #image_splash = graphics.Image.open(u'c:\\Data\Others\PyNetMony\\pynetmony.jpg')
   #image_splash.text((40,50), u'Closing CLF...',font=(None,18,FONT_BOLD))
   #window.add_image(image_splash, (0,0,width, height))
   #window.show()
   e32.ao_sleep(0.05)
   clf = []
   #image_splash.clear()
   #image_splash = graphics.Image.open(u'c:\\Data\Others\PyNetMony\\pynetmony.jpg')
   #image_splash.text((40,50), u'Closing WLAN...',font=(None,18,FONT_BOLD))
   #window.add_image(image_splash, (0,0,width, height))
   #window.show()
   e32.ao_sleep(0.05)
   neighbour_list = []
   wlan_list = []
   #image_splash.clear()
   #image_splash = graphics.Image.open(u'c:\\Data\Others\PyNetMony\\pynetmony.jpg')
   #image_splash.text((40,50), u'Closing BT...',font=(None,18,FONT_BOLD))
   #window.add_image(image_splash, (0,0,width, height))
   #window.show()
   e32.ao_sleep(0.05)
   bt_list = []
   #image_splash.clear()
   #image_splash = graphics.Image.open(u'c:\\Data\Others\PyNetMony\\pynetmony.jpg')
   #image_splash.text((40,50), u'Good Bye...',font=(None,18,FONT_BOLD))
   #window.add_image(image_splash, (0,0,width, height))
   #window.show()
   e32.ao_sleep(0.05)
   #running = False
   # let the GUI exit gracefully
   window.hide()
   #window.remove_image(image_splash)
   gui.signal()
   if s != None:
      s.close()
   appuifw.app.set_tabs([], None)
   if standalone() and not do_update:
      appuifw.app.set_exit()
      

def main():
   global script_lock, gui, s, SetupForm, Setup2Form, Setup3Form, canvas, lb, starttime, bg, \
         border, new_cells_lb, linecol, grid, headcol, headbg, image_splash, window, color, \
         bg, apo, apid
   size,offset = appuifw.app.layout(appuifw.EMainPane)
   (width, height) = size
   if width == 240:
      height = 320
   elif width == 320:
      height = 240
   elif width == 800:
      height = 352
   #(width, height) = sysinfo.display_pixels()
   top = 0
   left = 0
   
   #image.clear()
   #image_splash.text((90,50), unicode(SIS_VERSION),font=(None,18,FONT_BOLD))
   #window.add_image(image_splash, (0,0,width, height))
   #window.size = (width, height)
   #window.corner_type = 'square'
   #window.position = (left,top)
   #window.show()
   e32.ao_sleep(0.05)
   canvas = appuifw.Canvas(event_callback=handle_event, redraw_callback=handle_redraw)
   lb = appuifw.Listbox([u'Empty Neighbour List'], handle_selection)
   new_cells_lb = appuifw.Listbox([u'No new cells found'], handle_new_cell_selection)
   #appuifw.app.screen='large'
   #appuifw.app.screen='normal'
   appuifw.app.title = TITLE
   appuifw.app.body=canvas
   try:
      envy.set_app_system(1) # try to set system your application
   except: 
      print 'exception !'
      appuifw.note(u"Envy Error!",'error')
   script_lock = e32.Ao_lock()
   gui = e32.Ao_lock()
   thread.start_new_thread(log_worker,())
   SetupForm = Setup( )
   SetupForm.loadConfig(silent=True)
   Setup2Form = Setup2( )
   Setup2Form.loadConfig(silent=True)
   Setup3Form = Setup3( )
   Setup3Form.loadConfig(silent=True)
   menus_setup()
   if config['BT_SCAN'] == 0:
      btscan = []
   if config['COLOR_THEME'] == Setup.COLOR_THEME_BLUE:
      bg=(0,0,60)
      border=bg
      color=(255,255,255)
      linecol=(255,128,128)
      headcol=(255,255,255)
      headbg=(255,255,255)
      grid=(127,127,127)
   elif config['COLOR_THEME'] == Setup.COLOR_THEME_BLACK:
      bg=(0,0,0)
      border=bg
      color=(255,255,255)
      linecol=(255,128,128)
      headcol=(255,255,255)
      headbg=(255,255,255)
      grid=(127,127,127)
   elif config['COLOR_THEME'] == Setup.COLOR_THEME_RED:
      bg=(80,0,0)
      border=bg
      color=(255,255,255)
      linecol=(255,128,128)
      headcol=(255,255,255)
      headbg=(255,255,255)
      grid=(127,127,127)
   elif config['COLOR_THEME'] == Setup.COLOR_THEME_GREEN:
      bg=(0,60,0)
      border=bg
      color=(255,255,255)
      linecol=(255,128,128)
      headcol=(255,255,255)
      headbg=(255,255,255)
      grid=(127,127,127)
   elif config['COLOR_THEME'] == Setup.COLOR_THEME_MAGENTA:
      bg=(226,0,116)
      border=bg
      color=(255,255,255)
      linecol=(60,60,60)
      headcol=(255,255,255)
      headbg=(255,255,255)
      grid=(80,80,80)
   elif config['COLOR_THEME'] == Setup.COLOR_THEME_WHITE:
      bg=(255,255,255)
      border=bg
      color=(0,0,0)
      linecol=(128,0,0)
      headcol=(0,0,0)
      headbg=(0,0,0)
      grid=(127,127,127)
   load_wlan()
   load_bt()
   load_oui()
   appuifw.app.exit_key_handler = exit_key_handler
   #appuifw.app.body.bind(EKeyNo, exit_key_handler)
   #if locreq and config['GPS']:
   #   toggle_gps()
   if standalone():
      #path = os.getcwd()
      path = "C:\\Data\\Others\\PyNetMony\\"
   else:
      path = "C:\\Data\\Others\\PyNetMony\\"
   #e32.ao_sleep(1.5)
   #window.hide()
   #window.remove_image(image_splash)
   #try:
      #file = os.path.join(path, u'fanfare3.mp3')
      file = path + "fanfare3.mp3"
      #s = audio.Sound.open(file)
   #except Exception, error:
      #appuifw.note(u"Sound Error: s"+unicode(error),'error')
   if bt and (config['BT_SCAN'] > 0):
      pass
      #if blues.getstate() == 0:
      #   blues.on()
   if not eloc:
      appuifw.note(u"Elocation modul is missing!",'error')
   starttime = time.time()
   if not miso_ok:
      appuifw.note(u"Miso modul is missing!",'error')
   else:
      try:
         miso.vibrate(40,50)
      except:
         pass
         #appuifw.note(u"Vibration is deactivated in current profile!",'error')
   try:
      f=open(def_apn_file,'rb')
      setting = f.read()
      apid = eval(setting)
      f.close()
      if not apid == None :
         apo = socket.access_point(apid)
         socket.set_default_access_point(apo)
      else:
         pass
   except:
      pass
   netmonitor()
   script_lock.wait()

if standalone():
   # Standalone: Display exception as note
   try:
      main()
   except Exception, error:
      appuifw.note(u"Fatal Error: "+unicode(error),'error')
else:
   # Python Script Shell: log exception to stdout
   main()


