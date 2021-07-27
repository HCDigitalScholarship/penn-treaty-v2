# importing os module
import os
  
# Function to rename multiple files
def main():
  
    count = 1

    for filename in os.listdir("./static/img/swarthmore/SW_WH1793/"):
        if count < 10:
            dst ="SW_WH1793_Page_00" + str(count) + ".jpg"
        elif count < 100:
            dst ="SW_WH1793_Page_0" + str(count) + ".jpg"
        else:
            dst ="SW_WH1793_Page_" + str(count) + ".jpg"            
        src ='./static/img/swarthmore/SW_WH1793/'+ filename
        dst ='./static/img/swarthmore/SW_WH1793/'+ dst
          
        # rename() function will
        # rename all the files
        os.rename(src, dst)
        count+=1

# Driver Code
if __name__ == '__main__':
      
    # Calling main() function
    main()