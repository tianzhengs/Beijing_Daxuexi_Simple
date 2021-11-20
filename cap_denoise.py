from io import BytesIO
from PIL import Image

def dn(cap):
    img = Image.open(BytesIO(cap))
    _STEPS_LAYER_1 = ((1,1),(1,0),(1,-1),(0,1),(0,-1),(-1,1),(-1,0),(-1,-1))
    STEPS8  = _STEPS_LAYER_1
    _PX_WHITE=(250,250,250)
    def _denoise(img, steps, threshold, repeat):
        for _ in range(repeat):
            for j in range(img.width):
                for i in range(img.height):
                    px = img.getpixel((j,i))
                    if px == _PX_WHITE: # 自身白
                        continue
                    count = 0
                    if px[0]<px[1]+px[2]:
                        count=2
                    for x, y in steps:
                        j2 = j + y
                        i2 = i + x
                        if 0 <= j2 < img.width and 0 <= i2 < img.height: # 边界内
                            if img.getpixel((j2,i2)) == _PX_WHITE: # 周围白
                                count += 1
                        else: # 边界外全部视为黑
                            count += 1
                    if count >= threshold:
                       img.putpixel((j,i), _PX_WHITE)

        return img

    def denoise8(img, steps=STEPS8, threshold=7, repeat=2):
        """ 考虑外一周的降噪 """
        return _denoise(img, steps, threshold, repeat)

    buf = BytesIO()
    denoise8(img).save(buf, format='PNG')
    byte_im = buf.getvalue()
    return byte_im
