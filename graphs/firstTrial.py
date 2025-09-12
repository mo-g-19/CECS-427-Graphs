#Following code lines 2-7 from video https://www.youtube.com/watch?time_continue=37&v=7OdXry0T9Vg&embeds_referring_euri=https%3A%2F%2Fvideo.search.yahoo.com%2Fsearch%2Fvideo%3B_ylt%3DAwrOsH5opMRoPy0Ek0JXNyoA%3B_ylu%3DY29sbwNncTEEcG9zAzIEdnRpZAMEc2VjA3Nj%3Ftype%3DE210US1&embeds_referring_origin=https%3A%2F%2Fvideo.search.yahoo.com&source_ve_path=MzY4NDIsMzY4NDIsMjM4NTE
import xml.etree.ElementTree as etree

#Load the GML file
data = et.parse("HT.gml")
root = data.getroot()
print(root) #this whill print the root element of the GML file

