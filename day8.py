# https://adventofcode.com/
# 8/12/2019
# Day 8
#
# Image data manipulation and decoding. I got stuck over the rendering of the image and was 
# rendering the reverse which was not readable. Also interpreted a U in the output as a V 
# which was my mistake.
#
# Did a lot of the data array manipulation using brute force offset calculations. Feel there
# is probably a more elegant solution in Python but it got the job done.
#
# Learned: string.count(), string.join() and string.strip().
# Started with a class from the outset due to experience of day 7 but probably not necessary 
# in hindsight.

import unittest

class image:
    def __init__(self, width, height, data ):
        self.width = width
        self.height = height
        self.data = data
        self.layer_size = width * height
        self.layers = int(len(self.data) / self.layer_size)

    def get_layer_size(self):
        return self.layer_size

    def get_layers(self):
        return int(len(self.data) / self.layer_size)

    def count_digits(self,layer,digit):
        row = self.data[layer*self.layer_size:layer*self.layer_size+self.layer_size]
        
        return row.count(digit)

    def find_layer_with_least(self):
        # find layer with fewest 0 digits
        l = self.layer_size
        layer_number = 0
        for i in range(0, len(self.data), self.layer_size):
            row = self.data[i:i+self.layer_size]
            n = row.count("0")

            #print(int(i / self.layer_size),row,n,l,layer_number)
            if n < l:
                l = n
                layer_number = int(i / self.layer_size)

        return layer_number

    def decode_message(self):
        message = []
        for x in range(self.layer_size):
            for layer in range(self.layers):
                cell = self.data[layer * self.layer_size + x]

                # 0 is black
                # 1 is white
                # 2 is transparent (ignore)

                if cell == "0":
                    message.append(" ")
                    break
                elif cell == "1":
                    message.append( "#")
                    break

        return "".join(message)

    # Split into lines and separate with spaces to make it more readable
    def format_message_for_display(self,message):
        output = ""
        for x in range(0,self.layer_size,self.width):
            for y in range(self.width):
                output += message[x+y:x+y+1]  + " "
            output += "\n"

        return output

#
# test cases
#
class AdventTestCase(unittest.TestCase):
    def test_layers(self):
        img = image(3,2,"123456789012")
        self.assertEqual( img.get_layer_size(), 6 )
        self.assertEqual( img.get_layers(), 2 )
        self.assertEqual( img.find_layer_with_least(), 0 )

        img = image(3,2,"100456789012002332")
        self.assertEqual( img.find_layer_with_least(), 1 )
        self.assertEqual( img.count_digits(0,"0"), 2 )
        self.assertEqual( img.count_digits(2,"3"), 2 )

    def test_message(self):
        img = image(2,2,"0222112222120000")
        self.assertEqual( img.decode_message()," ## " )

if __name__ == '__main__':

    fp = open( '8.input.txt' )
    line = fp.readline()
    img = image(25,6,line.strip())
    fp.close()

    n = img.find_layer_with_least()
    one_digits = img.count_digits(n,"1")
    two_digits = img.count_digits(n,"2")
    print("part 1 product",one_digits * two_digits)

    message = img.decode_message()
    print("part 2 code")
    print(img.format_message_for_display(message))
