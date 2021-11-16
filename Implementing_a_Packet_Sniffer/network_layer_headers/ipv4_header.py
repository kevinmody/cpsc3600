from layer_header import LayerHeader
from struct import pack, unpack

class IPv4Header(LayerHeader):
    def __init__(self, pkt):
        # TODO: Replace the value of header_length with the length of an Ethernet header
        header_length = 20
        
        # TODO: If this header can be variable length, you will need to update the contents of 
        #       self.header_bytes once you know the full length of the header in order to ensure
        #       that all of the bytes associated with this header are saved. 
        #       You can leave it as is for now.
        self.header_bytes = pkt[:header_length]
        var_head = unpack("!BBHHHBBHII",self.header_bytes)
        self.version = var_head[0]>>4
        self.IHL = (var_head[0]&0x0F)
        self.TOS = var_head[1]
        self.total_length = var_head[2]
        self.identification = var_head[3]
        self.flags = var_head[4]>>13
        self.fragment_offset = var_head[4]&0x1FFF
        self.TTL = var_head[5]
        self.transport_protocol = var_head[6]
        self.checksum = var_head[7]
        self.source_addr = var_head[8]
        self.dest_addr = var_head[9]
        self.options_bytes = None

        # TODO: Unpack the header and assign the values to the above variables

        # TODO: You do not need to unpack any options, if they are present in the header. However, if options 
        #       are present, store the bytes associated with them in self.options_bytes.
        

    def protocol(self):
        return "IPv4"

    def header_bytes(self):
        return self.header_bytes

    def print_header(self):
        print("")
        print("IPv4 HEADER: ")
        line_width = (96+4)

        ####################################################################
        # Print first line
        print("-"*line_width)
        
        # Compose the contents of the first row of the header
        version_str = "VERSION: " + hex(self.version)
        white_space = (16 - len(version_str))//2
        first_row_str = "|" + " "*white_space + version_str + " "*white_space + "|"

        ihl_str = "IHL: " + hex(self.IHL)
        white_space = (16 - len(ihl_str))//2
        first_row_str += " "*white_space + ihl_str + " "*white_space + "|"

        tos_str = "TOS: " + hex(self.TOS)
        white_space = (16 - len(tos_str))//2
        first_row_str += " "*white_space + tos_str + " "*white_space + "|"

        length_str = "LENGTH: " + hex(self.total_length)
        white_space = (47 - len(length_str))//2
        first_row_str += " "*white_space + length_str + " "*white_space + "|"

        # Print the first row of the header
        print(first_row_str)
        


        ####################################################################
        # Print a line divider
        print("-"*line_width)

        # Compose the contents of the second row of the header
        version_str = "IDENT: " + hex(self.identification)
        white_space = (48 - len(version_str))//2
        second_row_str = "|" + " "*white_space + version_str + " "*white_space + "|"

        tos_str = "FLAGS: " + bin(self.flags)
        white_space = (16 - len(tos_str))//2
        second_row_str += " "*white_space + tos_str + " "*white_space + "|"

        length_str = "FRAG OFFSET: " + str(self.fragment_offset)
        white_space = (32 - len(length_str))//2
        second_row_str += " "*white_space + length_str + " "*white_space + "|"

        # Print the second line of the header
        print(second_row_str)


        ####################################################################
        # Print a line divider
        print("-"*line_width)
      
        # Compose the contents of the second row of the header
        version_str = "TTL: " + str(self.TTL)
        white_space = (24 - len(version_str))//2
        third_row_str = "|" + " "*white_space + version_str + " "*white_space + "|"

        tos_str = "Protocol: " + hex(self.transport_protocol)
        white_space = (24 - len(tos_str))//2
        third_row_str += " "*white_space + tos_str + " "*white_space + "|"

        length_str = "CKSUM: " + hex(self.checksum)
        white_space = (48 - len(length_str))//2
        third_row_str += " "*white_space + length_str + " "*white_space + "|"

        # Print the second line of the header
        print(third_row_str)



        ####################################################################
        # Print a line divider
        print("-"*line_width)
      
        # Compose the contents of the second row of the header
        version_str = "SOURCE ADDR: " + self.format_IPv4_addr(self.source_addr)
        white_space = (98 - len(version_str))//2
        third_row_str = "|" + " "*white_space + version_str + " "*white_space + "|"

        # Print the fourth line of the header
        print(third_row_str)



        ####################################################################
        # Print a line divider
        print("-"*line_width)
      
        # Compose the contents of the second row of the header
        version_str = "DEST ADDR: " + self.format_IPv4_addr(self.dest_addr)
        white_space = (98 - len(version_str))//2
        third_row_str = "|" + " "*white_space + version_str + " "*white_space + "|"

        # Print the fourth line of the header
        print(third_row_str)



        ####################################################################
        # Print a line divider
        print("-"*line_width)

        return super().print_header()