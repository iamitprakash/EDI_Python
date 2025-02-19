class EDIProcessor:
    def __init__(self):
        self.segments = []
        self.delimiter = '*'
        self.segment_terminator = '~'
    
    def parse_850_purchase_order(self, edi_content):
        """Parse an EDI 850 (Purchase Order) document"""
        lines = edi_content.split(self.segment_terminator)
        purchase_order = {
            'header': {},
            'items': []
        }
        
        for line in lines:
            if not line.strip():
                continue
                
            segments = line.split(self.delimiter)
            
            # Process ST (Transaction Set Header)
            if segments[0] == 'ST':
                purchase_order['header']['transaction_set'] = segments[1]
                purchase_order['header']['control_number'] = segments[2]
            
            # Process BEG (Beginning Segment for PO)
            elif segments[0] == 'BEG':
                purchase_order['header']['po_date'] = segments[5]
                purchase_order['header']['po_number'] = segments[3]
            
            # Process PO1 (Purchase Order Line Item)
            elif segments[0] == 'PO1':
                item = {
                    'line_number': len(purchase_order['items']) + 1,
                    'quantity': segments[2],
                    'unit_price': segments[4],
                    'product_id': segments[7]
                }
                purchase_order['items'].append(item)
        
        return purchase_order

def generate_purchase_order_edi():
    """Generate an EDI 850 Purchase Order"""
    edi_content = []
    
    # Add ISA (Interchange Control Header)
    isa = f"ISA*00*{' '*10}*00*{' '*10}*ZZ*SENDER{' '*9}*ZZ*RECEIVER{' '*8}*200831*1126*U*00401*000000001*0*P*>~"
    edi_content.append(isa)
    
    # Add GS (Functional Group Header)
    gs = "GS*PO*SENDER*RECEIVER*20200831*1126*1*X*004010~"
    edi_content.append(gs)
    
    # Add ST (Transaction Set Header)
    st = "ST*850*0001~"
    edi_content.append(st)
    
    # Add BEG (Beginning Segment for PO)
    beg = "BEG*00*NE*PO12345*20200831~"
    edi_content.append(beg)
    
    # Add PO1 (Line Items)
    po1 = "PO1*1*10*EA*9.99**VP*123456*UP*999999~"
    edi_content.append(po1)
    
    # Add CTT (Transaction Totals)
    ctt = "CTT*1~"
    edi_content.append(ctt)
    
    # Add SE (Transaction Set Trailer)
    se = "SE*6*0001~"
    edi_content.append(se)
    
    # Add GE (Functional Group Trailer)
    ge = "GE*1*1~"
    edi_content.append(ge)
    
    # Add IEA (Interchange Control Trailer)
    iea = "IEA*1*000000001~"
    edi_content.append(iea)
    
    return "\n".join(edi_content)

# Example usage
if __name__ == "__main__":
    # Generate sample EDI document
    edi_content = generate_purchase_order_edi()
    print("Generated EDI Document:")
    print(edi_content)
    
    # Parse the generated document
    processor = EDIProcessor()
    parsed_po = processor.parse_850_purchase_order(edi_content)
    print("\nParsed Purchase Order:")
    print(parsed_po)
