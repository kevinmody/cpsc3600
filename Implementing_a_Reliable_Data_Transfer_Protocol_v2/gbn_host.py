#Author: Kevin Mody

from network_simulator import NetworkSimulator, Packet, EventEntity
from enum import Enum
from struct import pack, unpack

class GBNHost():

    # The __init__ method accepts:
    # - a reference to the simulator object
    # - the value for this entity (EntityType.A or EntityType.B)
    # - the interval for this entity's timer
    # - the size of the window used for the Go-Back-N algorithm
    def __init__(self, simulator, entity, timer_interval, window_size):
        
        # These are important state values that you will need to use in your code
        self.simulator = simulator
        self.entity = entity
        
        # Sender properties
        self.timer_interval = timer_interval        # The duration the timer lasts before triggering
        self.window_size = window_size              # The size of the seq/ack window
        self.window_base = 0                        # The last ACKed packet. This starts at 0 because no packets 
                                                    # have been ACKed
        self.next_seq_num = 0                       # The SEQ number that will be used next
        self.app_layer_buffer = []                  # A buffer was created that stores all data received from the application 
                                                    # layer that hasn't yet been sent
        self.unacked_buffer = [] 
        self.exp_seq_num = 0                                    # The next Sequesnce number expected
        self.last_ack_pkt = self.packet_Create(-1, "ACK")                     # The last ACK current_packet sent. 

    ###########################################################################################################
    ## Core Interface functions that are called by Simulator

    # This function implements the SENDING functionality. It should implement retransmit-on-timeout. 
    # Refer to the GBN sender flowchart for details about how this function should be implemented
    def receive_from_application_layer(self, payload):
        if self.next_seq_num < self.window_base + self.window_size:
            self.unacked_buffer.append(self.packet_Create(self.next_seq_num, payload))
            self.simulator.pass_to_network_layer(self.entity, self.unacked_buffer[self.next_seq_num],self.current_ack(self.unacked_buffer[self.next_seq_num]))
            if self.window_base == self.next_seq_num:
                self.simulator.start_timer(self.entity, self.timer_interval)
            self.next_seq_num += 1
        else:
            self.app_layer_buffer.append(payload)    


    # This function implements the RECEIVING functionality. This function will be more complex that
    # receive_from_application_layer(), it includes functionality from both the GBN Sender and GBN receiver
    # FSM's (both of these have events that trigger on receive_from_network_layer). You will need to handle 
    # data differently depending on if it is a packet containing data, or if it is an ACK.
    # Refer to the GBN receiver flowchart for details about how to implement responding to data pkts, and
    # refer to the GBN sender flowchart for details about how to implement responidng to ACKs
    def receive_from_network_layer(self, byte_data):
        if self.current_ack(byte_data) and not self.is_corrupt(byte_data):
            acknum = self.get_currentAck_num(byte_data)
            if acknum >= self.window_base:
                self.window_base = acknum + 1
                self.simulator.stop_timer(self.entity)
                if self.window_base != self.next_seq_num:
                    self.simulator.start_timer(self.entity, self.timer_interval)
                while len(self.app_layer_buffer) > 0 and self.next_seq_num < self.window_base + self.window_size:
                    payload = self.app_layer_buffer.pop()
                    self.unacked_buffer.append(self.packet_Create(self.next_seq_num, payload))
                    self.simulator.pass_to_network_layer(self.entity, self.unacked_buffer[self.next_seq_num], self.current_ack(self.unacked_buffer[self.next_seq_num]))
                    if self.window_base == self.next_seq_num:
                        self.simulator.start_timer(self.entity, self.timer_interval)
                    self.next_seq_num += 1
        elif self.is_corrupt(byte_data):
            self.simulator.pass_to_network_layer(self.entity, self.last_ack_pkt, self.current_ack(self.last_ack_pkt))   
        elif self.get_currentSeq_num(byte_data) != self.exp_seq_num:
            self.simulator.pass_to_network_layer(self.entity, self.last_ack_pkt, self.current_ack(self.last_ack_pkt)) 
        else:
            try:
                data = self.payload_Extraction(byte_data)
                   
            except Exception as e:
                self.simulator.pass_to_network_layer(self.entity, self.last_ack_pkt, self.current_ack(self.last_ack_pkt))
            self.simulator.pass_to_application_layer(self.entity, data)
            self.last_ack_pkt = self.packet_Create(self.exp_seq_num, "ACK")
            self.simulator.pass_to_network_layer(self.entity, self.last_ack_pkt, self.current_ack(self.last_ack_pkt)) 
            self.exp_seq_num += 1

    # This function is called by the simulator when a timer interrupt is triggered due to an ACK not being 
    # received in the expected time frame. All unACKed data should be resent, and the timer restarted
    def timer_interrupt(self):
        self.simulator.start_timer(self.entity, self.timer_interval)
        for a in range(self.window_base, self.next_seq_num, 1):
            self.simulator.pass_to_network_layer(self.entity, self.unacked_buffer[a], self.current_ack(self.unacked_buffer[a]))
        

    # This function should check to determine if a given packet is corrupt. The packet parameter accepted
    # by this function should contain a byte array
    def is_corrupt(self, packet):
        length = unpack("!HiHI", packet[:12])
        checksum = length[2]
        header = pack("!HiHI", length[0], length[1], 0, length[3])
        current_packet = header + packet[12:]
        if checksum == self.checker(current_packet):
            return False
        else:
            return True

    def checker(self, current_packet):
        if len(current_packet) % 2 != 0:
            current_packet = current_packet + bytes(1)

        # Checksum
        s = 0
        for i in range(0, len(current_packet), 2):
            word = current_packet[i] << 8 | current_packet[i+1]
            s += word
            s = (s & 0xffff) + (s >> 16)
        total = ~s & 0xffff
        return total
 
    def packet_Create(self, seq_num, payload):
        if payload == "ACK":
            current_packet = pack("!HiHI" , 0, seq_num, 0, 0 )
            CS = self.checker(current_packet)
            current_packet = pack("!HiHI" , 0 , seq_num, CS, 0)
        else:
            current_packet = pack("!HiHI%is"%len(payload), 128, seq_num, 0, len(payload), payload.encode())
            CS = self.checker(current_packet)
            current_packet = pack("!HiHI%is"%len(payload), 128, seq_num, CS, len(payload), payload.encode())
        return current_packet

    def current_ack(self, current_packet):
        length = unpack("!HiHI", current_packet[:12])
        if length[0] == 0:
            return True
        else:
            return False

    def get_currentAck_num(self, current_packet):
        length = unpack("!HiHI", current_packet[:12])
        return length[1]

    def get_currentSeq_num(self, current_packet):
        length = unpack("!HiHI", current_packet[:12])
        return length[1]     

    def payload_Extraction(self, current_packet):
        length = unpack("!HiHI", current_packet [:12])
        data = unpack("!%is"%length[3], current_packet[12:])
        data = data[0].decode()
        return data
