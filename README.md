# CSCE_365_PA2

Temporary notes(Ben):
-Need to design 5 packet sending at a time.
  My ideas here include: make send_data recursive or while loop counting to 5 (I prefer looping, state machine will have to be implemented to some degree here). We also need some data structure to hold seq numbers, possibly list of seq# removing numbers as ack is received. When ack is not received or bad ack: we populate the list with 5 numbers starting with the lowest number still in the list. If table count == 0 then add 5 more of the next seq# to the table.
