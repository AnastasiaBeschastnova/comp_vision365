import cv2

cs = []  # coords_start
ce = []  # coords_end


def saveCS(x, y):
    cs.clear()
    cs.append(x)
    cs.append(y)


def saveCE(x, y):
    ce.clear()
    ce.append(x)
    ce.append(y)


def findCoords():
    ix = []  # image_x
    iy = []  # image_y
    # координаты выбранного кусочка
    c = ((ce[0] - cs[0]) ** 2. + (ce[1] - cs[1]) ** 2.) ** 0.5
    if (c != 0.):  # если координаты начала и конца области не равны, диагональ не равна 0
        if (ce[0] > cs[0]):
            ix.append(cs[0])
            ix.append(ce[0])
        elif (ce[0] < cs[0]):
            ix.append(ce[0])
            ix.append(cs[0])
        else:
            ix.append(ce[0])
            ix.append(ce[0] + 1)
        if (ce[1] > cs[1]):
            iy.append(cs[1])
            iy.append(ce[1])
        elif (ce[1] < cs[1]):
            iy.append(ce[1])
            iy.append(cs[1])
        else:
            iy.append(ce[1])
            iy.append(ce[1] + 1)
    else:
        ix.append(ce[0])
        ix.append(ce[0] + 1)
        iy.append(ce[1])
        iy.append(ce[1] + 1)
    ii = []
    ii.append(ix)
    ii.append(iy)
    return (ii)


def findGray(pos):
    p = pos / 20.
    image = cv2.imread(r'C:\Users\baugo\Documents\IVT-3kurs_2022-2023\CompVision\pic_1.jpg', cv2.IMREAD_COLOR)
    im_w = image.shape[1]
    im_h = image.shape[0]
    if (len(cs) != 0 and len(ce) != 0):
        ii = findCoords()
    else:
        ii = [[0, im_w], [0, im_h]]
    roi = image[int(ii[1][0]):int(ii[1][1]), int(ii[0][0]):int(ii[0][1])]
    r_w = roi.shape[1]
    r_h = roi.shape[0]
    im_col = image.copy()
    for i in range(r_w):
        for j in range(r_h):
            b,g,r = roi[j][i]
            y = int(0.2126 * r + 0.7152 * g + 0.0722 * b)# ищем серый
            roi[j][i] = (int(b + (y - b) * p), int(g + (y - g) * p), int(r + (y - r) * p))
    im_col[int(ii[1][0]):int(ii[1][1]), int(ii[0][0]):int(ii[0][1])] = roi
    cv2.imshow('New Image', im_col)


def getPic(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        saveCS(x, y)
    if flags == cv2.EVENT_FLAG_LBUTTON or event == cv2.EVENT_LBUTTONUP:
        saveCE(x, y)
    findGray(cv2.getTrackbarPos('Discolor', 'New Image'))



cv2.namedWindow('New Image')
cv2.setMouseCallback('New Image', getPic)
cv2.createTrackbar('Discolor', 'New Image', 10, 20, findGray)
cv2.waitKey(0)
