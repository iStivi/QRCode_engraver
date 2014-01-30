import qrcode

######################################
#input address to be made into Qr code
######################################
qrstring = "133Gf5WZEJpNN77upypUGGHZU8pW3oui1c"

#########################
##Machining parameters
#########################

#coin logo type to be engraved
coin_type = "bitcoin"
#coin_type = "doge"
#coin_type = "litecoin"

#name of G-code file to be output
output_file = coin_type + "_qr_engrave.nc"


#parameters for the engraving process
feed_rate = 200 #mm per second, must be type string
mill_width = 0.15  #engraver/end mill width in mm at top of cut
engrave_depth = 0.2 #depth of engrave cut in mm
depth_per_pass = 0.2 #depth to cut at a time in mm
stock_thickness = 3 #thickness of stock in mm
clearance_height = 2 #height above stock to make quick moves between cuts in mm
pixel_size = 0.8 #in mm. Version 3 qr code is 29 pixels all sides
border_size = 4 #number of pixels clearance either side of code area, 4 is standard

square_size = pixel_size*(29+(border_size*2))
print(square_size, "mm dimensions")


##############################
## Function for pixel cutting
##############################

'''individual pixels will be cut in alternating horizontal and vertical stroke patterns'''

def cut_pixel( location_list ):
    print("pixel cutting routine at " , location_list)
    x_start = (location_list[0] * pixel_size) + mill_width/2
    y_start = square_size - (location_list[1] * pixel_size) - mill_width/2
    x_end = (location_list[0]*pixel_size) + pixel_size - mill_width/2
    y_end = square_size - (location_list[1] * pixel_size) - pixel_size + mill_width/2
    gcode_out.write("G0 X%(x)0.4f Y%(y)0.4f \n" % {'x': x_start, 'y': y_start})
    #cut square
    cut_passes = int(engrave_depth / depth_per_pass)
    for cut_pass in range(0, cut_passes):
        pass_depth = (1 + cut_pass) * depth_per_pass
        gcode_out.write("G1 Z-%0.4f \n" % pass_depth)
        gcode_out.write("G1 X%(x)0.4f Y%(y)0.4f \n" % {'x': x_end, 'y': y_start})
        gcode_out.write("G1 X%(x)0.4f Y%(y)0.4f \n" % {'x': x_end, 'y': y_end})
        gcode_out.write("G1 X%(x)0.4f Y%(y)0.4f \n" % {'x': x_start, 'y': y_end})
        gcode_out.write("G1 X%(x)0.4f Y%(y)0.4f \n" % {'x': x_start, 'y': y_start})
    if(engrave_depth%depth_per_pass==0):
        pass
    else:
        gcode_out.write("G1 Z-%0.4f \n" % engrave_depth)
        gcode_out.write("G1 X%(x)0.4f Y%(y)0.4f \n" % {'x': x_end, 'y': y_start})
        gcode_out.write("G1 X%(x)0.4f Y%(y)0.4f \n" % {'x': x_end, 'y': y_end})
        gcode_out.write("G1 X%(x)0.4f Y%(y)0.4f \n" % {'x': x_start, 'y': y_end})
        gcode_out.write("G1 X%(x)0.4f Y%(y)0.4f \n" % {'x': x_start, 'y': y_start})  

    #lift cutter and go to start corner
    gcode_out.write("G1 Z0 \n")
    gcode_out.write("G0 X%(x)0.4f Y%(y)0.4f \n" % {'x': x_start, 'y': y_start})

    #cut horizontal strips if pixel even, vertical strips of odd
    strips = int((pixel_size - ( mill_width * 2)) / mill_width)
    
    if (line_no+point_no)%2==0:
        #horizontal strips
        for cut_pass in range(0, cut_passes): 
            for strip_pass in range(0, strips):
                pass_depth = (1 + cut_pass) * depth_per_pass
                y_strip = y_start - ( mill_width ) - ( strip_pass * mill_width) 
                gcode_out.write("G1 Z%0.4f \n" % ((-1 * pass_depth ) + depth_per_pass * 2))
                gcode_out.write("G0 X%(x)0.4f Y%(y)0.4f \n" % {'x': (x_start + mill_width/2), 'y': y_strip})
                gcode_out.write("G1 Z%0.4f \n" % (-1 * pass_depth ))                
                gcode_out.write("G1 X%(x)0.4f Y%(y)0.4f \n" % {'x': (x_end - mill_width/2), 'y': y_strip})
        if(engrave_depth%depth_per_pass==0):
            pass
        else:
            for strip_pass in range(0, strips):
                pass_depth = engrave_depth
                y_strip = y_start - ( mill_width ) - ( strip_pass * mill_width) 
                gcode_out.write("G1 Z%0.4f \n" % ((-1 * pass_depth ) + depth_per_pass * 2))
                gcode_out.write("G0 X%(x)0.4f Y%(y)0.4f \n" % {'x': (x_start + mill_width/2), 'y': y_strip})
                gcode_out.write("G1 Z%0.4f \n" % (-1 * pass_depth ))                
                gcode_out.write("G1 X%(x)0.4f Y%(y)0.4f \n" % {'x': (x_end - mill_width/2), 'y': y_strip})      
        gcode_out.write("G1 Z%0.4f \n" % clearance_height)
    else:
        #vertical strips
        for cut_pass in range(0, cut_passes): 
            for strip_pass in range(0, strips):
                pass_depth = (1 + cut_pass) * depth_per_pass
                x_strip = x_start + ( mill_width ) + ( strip_pass * mill_width)
                gcode_out.write("G1 Z%0.4f \n" % ((-1 * pass_depth ) + depth_per_pass * 2))
                gcode_out.write("G0 X%(x)0.4f Y%(y)0.4f \n" % {'x': x_strip, 'y': (y_start - mill_width/2)})
                gcode_out.write("G1 Z%0.4f \n" % (-1 * pass_depth ))                
                gcode_out.write("G1 X%(x)0.4f Y%(y)0.4f \n" % {'x': x_strip, 'y': (y_end + mill_width/2)})
        if(engrave_depth%depth_per_pass==0):
            pass
        else:
            for strip_pass in range(0, strips):
                pass_depth = engrave_depth
                x_strip = x_start + ( mill_width ) + ( strip_pass * mill_width)
                gcode_out.write("G1 Z%0.4f \n" % ((-1 * pass_depth ) + depth_per_pass * 2))
                gcode_out.write("G0 X%(x)0.4f Y%(y)0.4f \n" % {'x': x_strip, 'y': (y_start - mill_width/2)})
                gcode_out.write("G1 Z%0.4f \n" % (-1 * pass_depth ))                
                gcode_out.write("G1 X%(x)0.4f Y%(y)0.4f \n" % {'x': x_strip, 'y': (y_end + mill_width/2)})      
        gcode_out.write("G1 Z%0.4f \n" % clearance_height)

    return
    

###############################################################
##Start Script
###############################################################

#create qrcode data and generate sample png file

qr = qrcode.QRCode(
    version=3,  #version 3 is smallest size bitcoin address will compress to
    error_correction=qrcode.constants.ERROR_CORRECT_M,
    border=border_size,
)

qr.add_data(qrstring)
qr.make()
img = qr.make_image()
img.save("qr_view.png")


#Write header data to Gcode and set up machine

print(output_file)
gcode_out = open(output_file,'w')

gcode_out.write("( QR Code Engraving script for " + coin_type + " )\n")
gcode_out.write("( Code formatted for compatibility with Mach3 )\n")
gcode_out.write("( Generated by qr_generator.py https://github.com/iStivi/QRCode_engraver )\n")
gcode_out.write("( Engraving coded string: " + qrstring + " )\n") 
gcode_out.write("G71 G90\n") #metric, absolute coords

#write Gcode for marking out the QR code pattern

gcode_out.write("( Cutting out QR code )\n")
gcode_out.write("T01 M6 (" + str(mill_width) + "mm engraving tool )\n") 
gcode_out.write("F" + str(feed_rate) + "\n")
gcode_out.write("G1 Z" + str(clearance_height) + "\n")


for line_no, line in enumerate(qr.get_matrix()):
    #print(line_no, line)
    for point_no, point in enumerate(line):
        #print(line_no, point_no,point)
        if(point==False):
            continue
        else:
            cut_pixel([point_no,line_no])
       
        
gcode_out.write("M30 \n")
gcode_out.close()
