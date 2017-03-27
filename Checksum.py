import binascii
import pickle

# Assumes last field is the checksum!
def validate_checksum(message):
    try:
        msg = message[0]
        # have to pickle msg here to convert to bytes for generate_checksum
        pickledMsg = pickle.dumps(msg)
        reported_checksum = message[-1]
        return generate_checksum(pickledMsg) == reported_checksum
    except:
        return False

# Assumes message does NOT contain final checksum field.
def generate_checksum(message):
    return str(binascii.crc32(message) & 0xffffffff)
