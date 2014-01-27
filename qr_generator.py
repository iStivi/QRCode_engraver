import qrcode
import qrcode.image.svg

######################################
#input address to be made into Qr code
######################################
qrstring = "133Gf5WZEJpNN77upypUGGHZU8pW3oui1c"

#########################
##machining parameters
#########################

#name of G-code file to be output
output_file = "qr_engrave.nc"

#coin logo type to be engraved
coin_type = "bitcoin"
#coin_type = "doge"
#coin_type = "litecoin"

#parameters for the engraving process
feed_rate = "500" #mm per second
mill_width = 0.1  #engraver/end mill width in mm
engrave_depth = 0.5 #depth of engrave cut in mm
stock_thickness = 2 #thickness of stock in mm
clearance_height = 3 #height above stock to make quick moves between cuts in mm
pixel_size = 0.8 #in mm. Version 3 qr code is 29 pixels all sides
border_size = 4 #number of pixels clearance either side of code area, 4 is standard

##############################
##End of user input parameters
##############################

square_size = pixel_size*(29+(border_size*2))
print(square_size, "mm dimensions")


##############################
## Functions for pixel cutting
##############################

def even_cuts( location_list ):
    print("even box cutting routine at ",location_list)
    #cut square starting from (x+mill_width/2), (square_size-y-mill_width) to (x+pixel_size-mill_width), (square_size-(y+pixel_size+mill_width) 
    #cut horizontal strips to bottom, in mill_width increments
    return
    
def odd_cuts( location_list ):
    print("odd box cutting routine at ",location_list)
    #cut square starting from x, square_size-y to x+pixel_size, square_size-(y+pixel_size) 
    #cut vertical strips to bottom, in mill_width increments
    return


qr = qrcode.QRCode(
    version=3,  #version 3 is smallest size bitcoin address will compress to
    error_correction=qrcode.constants.ERROR_CORRECT_M,
    border=border_size,
    #image_factory=qrcode.image.svg.SvgPathImage,
)
qr.add_data(qrstring)
qr.make()
img = qr.make_image()
img.save("qr_view.png")

for line_no, line in enumerate(qr.get_matrix()):
    #print(line_no, line)
    for point_no, point in enumerate(line):
        print(line_no, point_no,point)
        if(point==False):
            continue
        elif (line_no+point_no)%2==0:
            box_type="even"
            even_cuts([line_no,point_no])
        else:
            box_type="odd"
            odd_cuts([line_no,point_no])
        


