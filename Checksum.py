import binascii
import pickle

# Assumes last field is the checksum!
def validate_checksum(message):
    try:
        #msg,reported_checksum = message.rsplit('|',1)
        #msg += '|'
        msg = message[0]
        pickledMsg = pickle.dumps(msg)
        reported_checksum = message[-1]
        return generate_checksum(pickledMsg) == reported_checksum
    except:
        return False

# Assumes message does NOT contain final checksum field. Message MUST end
# with a trailing '|' character.
def generate_checksum(message):
    #return str(binascii.crc32(message.encode()) & 0xffffffff) # added encoding here . it may not be needed with pickel
    return str(binascii.crc32(message) & 0xffffffff)
