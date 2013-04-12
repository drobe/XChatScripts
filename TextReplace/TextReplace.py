import xchat
import re
import os

__module_name__ = "Text Replace" 
__module_version__ = "0.1" 
__module_description__ = "Replaces text strings with other text strings."

path = os.path.abspath( __file__ ).replace('.py','.txt')
TextReplaceCache = dict()

####################################################################

# Called automatically on start.
def Start():
    Read()

# Reads from file into the Text Replace Cache
def Read():
    count = 0;
    key = ""
    value = ""
    TextReplaceCache.clear()
    try:
        with open(path, 'r') as file:
            for line in file:
                line = line.replace('\n','')
                if (count % 2 == 0):
                    key = line
                else:
                    value = line
                    TextReplaceCache[key] = value
                count += 1
    except IOError as e:
        xchat.prnt("I/O error({0}): {1} : {2}".format(e.errno, e.strerror, path))

# Writes to file from the Text Replace Cache
def Write():
    count = 0
    with open(path, 'w') as file:
        for str in TextReplaceCache.keys():
            file.write(str + '\n' + TextReplaceCache[str])
            if (count != len(TextReplaceCache)):
                file.write('\n')
            count += 1



####################################################################

def textReplace(strOriginal):
    for str in TextReplaceCache.keys():
        strOriginal = strOriginal.replace(str, TextReplaceCache[str])
    return strOriginal

####################################################################

# Called whenever the /TR command is sent
def onSend(word, word_eol, userdata):
    if len(word) < 2:
        xchat.prnt ("Hauu~ There's nothing here!")
    else:
        xchat.command("msg %s %s" %(xchat.get_info("channel"), textReplace(word_eol[1])))
    return xchat.EAT_ALL


# Called on /TReload. Reloads Text Replace cache
def onReload(word, word_eol, userdata):
    Read()
    xchat.prnt('Reloaded Text Replace Cache: ' + str(len(TextReplaceCache)) + ' items.')
    return xchat.EAT_ALL

# Called on /TRA
def onAdd(word, word_eol, userdata):
    if len(word) < 3:
        xchat.prnt('/TRA <Token> <String Replacement>')
        return xchat.EAT_ALL
    TextReplaceCache[word[1]] = word_eol[2]
    Write()
    xchat.prnt('Added to Text Replace Cache: ' + str(len(TextReplaceCache)) + ' items: + ' + word[1] + ' = ' + word_eol[2])
    return xchat.EAT_ALL

# Called on /TRL
def onList(word, word_eol, userdata):
    xchat.prnt('4Text Replace Listing\n--------------------')
    for str in TextReplaceCache.keys():
        xchat.prnt(str + ' = ' + TextReplaceCache[str])
    xchat.prnt('--------------------')
    return xchat.EAT_ALL

####################################################################

xchat.hook_command("TRA", onAdd, help="/TRAdds <Token> <String Replacement> to the Text Replace cache.")
xchat.hook_command("TRL", onList, help="/TRLists the Text Replace cache.")
xchat.hook_command("TReload", onReload, help="/TReload Reloads the Text Replace cache.")
xchat.hook_command("TR", onSend, help="/TR <message> Sends a message to the channel. Replaces tokens with predefined strings.")

Start()
xchat.prnt(__module_name__ + " Ver. " + __module_version__ + " loaded.")
