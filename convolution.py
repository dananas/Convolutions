from PIL import Image
from IPython.display import display

filepath = ''

# load an image
img = Image.open(filepath)
img = img.convert('L')
w, h = img.size

# create the intensity matrix
img_data = img.getdata()
Img = [[img_data[x + w * y] / 255.0 for x in range(w)] for y in range(h)]

# matrices convolution
def convolution(source, kernel, s_size, k_size):
    def _conv(source, kernel, x, y, s_size, k_size_2):
        if x < k_size_2 or y < k_size_2 or x >= s_size - k_size_2 or y >= s_size - k_size_2:
            return source[x][y]
        S = sum([source[y + y2 - k_size_2][x + x2 - k_size_2] * kernel[y2][x2] for x2 in range(k_size_2 * 2 + 1) for y2 in range(k_size_2 * 2 + 1)])
        return S
    
    k_size_2 = k_size // 2
    C = [[_conv(source, kernel, x, y, s_size, k_size_2) for x in range(s_size)] for y in range(s_size)]
    return C

def convolutiontest(Img, n = 1):
    KSize = 3
    #K = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    K = [[1, 2, 1], [2, 4, 2], [1, 2, 1]]
    #K = [[0, -1, 0], [-1, 5, -1], [0, -1, 0]]
    #K = [[1, 0, -1], [0, 0, 0], [-1, 0, 1]]
    #K = [[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]]
    
    # normalize kernel
    s = sum([sum(K[i]) for i in range(KSize)])
    if (s != 0):
        K = [[K[y][x] / s for x in range(KSize)] for y in range(KSize)]
        
    c = convolution(Img, K, w, KSize)
    showimage(c, w)
    if n > 1:
        convolutiontest(c, n - 1)
        
def showimage(array2d, size):
    cdata = [255 * array2d[x // size][x % size] for x in range(size ** 2)]
    cimage = Image.new("L", (w, h))
    cimage.putdata(cdata)
    cimage = cimage.convert('RGB')
    display(cimage)
    
display(img)
convolutiontest(Img, 1)