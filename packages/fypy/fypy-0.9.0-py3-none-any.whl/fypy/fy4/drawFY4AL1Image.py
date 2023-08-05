# coding:utf-8
import os
import numpy as np
from numpy import uint8, array, arange, uint16
from PIL import Image,ImageDraw,ImageFont
from fypy.utils.hdfpro import readhdf_fileinfo


PATH_PARM = os.path.join(os.path.dirname(__file__), '../parm')
Image.MAX_IMAGE_PIXELS = None

RATE = 4
COLORS = (256 << RATE) - 1
Gamma = lambda x: (np.linspace(0, 1, COLORS + 1) ** (1. / x) * COLORS).astype('u2')

class DrawFY4AL1Image(object):


    def __init__(self, filename=None, geoname=None, outname=None, nightlight=True, title=None):

        self.cir   = np.load(os.path.join(PATH_PARM, 'cir.npy', ))
        self.cib   = np.load(os.path.join(PATH_PARM, 'cib.npy', ))
        self.ck    = np.load(os.path.join(PATH_PARM, 'ck.npy', ))
        self.ckb   = np.load(os.path.join(PATH_PARM, 'ckb.npy', ))
        self.cka   = np.load(os.path.join(PATH_PARM, 'cka.npy', ))
        self.vcA   = np.load(os.path.join(PATH_PARM, 'vcA.npy', ))
        self.V_ARC = np.load(os.path.join(PATH_PARM, 'V_ARC.npy', ))
        self.V_COL = np.load(os.path.join(PATH_PARM, 'V_COL.npy', ))
        self.V1    = np.load(os.path.join(PATH_PARM, 'V1.npy', ))
        self.V2    = np.load(os.path.join(PATH_PARM, 'V2.npy', ))
        self.V3    = np.load(os.path.join(PATH_PARM, 'V3.npy', ))
        self.VB    = np.load(os.path.join(PATH_PARM, 'VB.npy', ))
        self.VK    = np.load(os.path.join(PATH_PARM, 'VK.npy', ))

        if filename is None or geoname is None or outname is None :
            pass
        else:

            refr = self.getdata(filename, 2)
            refg = self.getdata(filename, 3)
            refb = self.getdata(filename, 1)

            bt8 = self.getdata(filename, 8)
            bt12 = self.getdata(filename, 12)
            #
            satz = self.getgeo(geoname, 'NOMSatelliteZenith')
            sunz = self.getgeo(geoname, 'NOMSunZenith')

            self.DrawGeoColor(refr, refg, refb, bt8, bt12, sunz, satz,
                              outname=outname,
                              nightlight=nightlight, title=title)

    def getdata(self, filename, chanid):
        import h5py

        # 转换到区域的行列号（考虑去除图像偏移）
        fileinfo = readhdf_fileinfo(filename)
        Begin_Line_Number = fileinfo['Begin Line Number'][0]
        End_Line_Number = fileinfo['End Line Number'][0]
        Begin_Pixel_Number = fileinfo['Begin Pixel Number'][0]
        End_Pixel_Number = fileinfo['End Pixel Number'][0]

        data = np.zeros(shape=(End_Line_Number+1, End_Pixel_Number+1),dtype=np.float32)

        fp = h5py.File(filename, 'r')
        cal = fp['CALChannel%02d' %(chanid)][:]
        dn = fp['NOMChannel%02d' %(chanid)][:]

        dn[dn>=len(cal)] = 0
        fp.close()

        data[Begin_Line_Number:End_Line_Number+1, Begin_Pixel_Number:End_Pixel_Number+1] = cal[dn]

        return data

    def getgeo(self, filename, sdsname):
        import h5py
        fp = h5py.File(filename, 'r')
        data1 = fp[sdsname][:]
        fp.close()

        # 转换到区域的行列号（考虑去除图像偏移）
        fileinfo = readhdf_fileinfo(filename)
        Begin_Line_Number = fileinfo['Begin Line Number'][0]
        End_Line_Number = fileinfo['End Line Number'][0]
        Begin_Pixel_Number = fileinfo['Begin Pixel Number'][0]
        End_Pixel_Number = fileinfo['End Pixel Number'][0]

        data = np.zeros(shape=(End_Line_Number+1, End_Pixel_Number+1),dtype=np.float32)

        data[Begin_Line_Number:End_Line_Number+1, Begin_Pixel_Number:End_Pixel_Number+1] = data1

        return data


    def spline(self, x, y):
        """
        SPLINE  @ photoshop HEIGH COLOR LEVEL
        :param x:
        :param y:
        :return:
        """
        R = 2 ** RATE
        cb = self._spline(array(x) * R, array(y) * R, arange(COLORS + 1))
        cb[cb < 0] = 0
        cb[cb > COLORS] = COLORS
        cb = cb.astype('u2' if RATE else 'u1')
        return cb



    def Chrange(self, data, minv, maxv, dtype='u2', N=COLORS):
        """
        线性拉伸
        :param data:
        :param minv:
        :param maxv:
        :param dtype: u2
        :param N: 4095
        :return:
        """
        return self.chrange(data - minv, maxv - minv, N).astype(dtype=dtype)

    def T0_255(self, raw):
        return (raw >> RATE).astype(uint8)

    def chrange(self, n, r0, r1):
        n /= r0
        n[n < 0] = 0
        n[n > 1] = 1
        return n * r1

    def Arr2Img(self, arr):
        if arr.dtype == uint8:
            return Image.fromarray(arr, "L")
        if arr.dtype == uint16:
            return Image.fromarray(self.T0_255(arr), "L")
        return Image.fromarray(self.T0_255(arr.astype('u2')), "L")

    def ArcCrl(self, cnl, satZ, RsatZ, sunZ, RsunZ):
        # 色彩增强, 角度修正
        cnl[:] = self.V1[cnl] * sunZ + cnl * RsunZ
        cnl[:] = self.V2[cnl] * satZ + cnl * RsatZ
        cnl[:] = self.V3[cnl]
        return cnl


    def DrawVIS(self, refr, refg, refb, sunz, satz,
                outname, resolution=0.04, nightlight=False): # com_data,

        Z = sunz
        fz = Z > 360

        r = refr.copy()
        g = refg.copy()
        b = refb.copy()

        # 色调校正
        rr = self.chrange(r * 100 + g * 20 - b * 20, 102, COLORS).astype('u2')
        gg = self.chrange(r * 30 + g * 20 + b * 50, 102, COLORS).astype('u2')
        bb = self.chrange(b * 83 + r * 17, 102, COLORS).astype('u2')  #np.uint16
        # img2 = Image.merge('RGB', [self.Arr2Img(i) for i in (rr, gg, bb)])
        # img2.save(outname + '-RAW2.jpg', quality=70)
        # '''
        del r, g, b
        # 对卫星天顶角做归一化处理
        satZ = satz.copy()
        satZ = satZ / 90.0
        satZ[satZ>1] = 1
        satZ[satZ<0] = 0

        RsatZ = 1 - satZ
        sunZ = Z / 90
        sunZ[sunZ > 1] = 1
        sunZ[sunZ < 0] = 0
        RsunZ = 1 - sunZ

        #
        self.ArcCrl(rr, satZ, RsatZ, sunZ, RsunZ)
        self.ArcCrl(gg, satZ, RsatZ, sunZ, RsunZ)
        self.ArcCrl(bb, satZ, RsatZ, sunZ, RsunZ)
        # self.Arr2Img((sunZ * 255).astype('u1')).save(outname + '_sunz.jpg')
        # '''
        # 二次渲染 2019_04_10
        # vm = Image.merge('RGB', [self.Arr2Img(i) for i in (rr, gg, bb)])
        # vm.save(outname + '-RAW3.jpg', quality=70)
        vm = Image.merge('RGB', [self.Arr2Img(i) for i in (rr, gg, bb)])

        # 可见光真彩色图像
        # print(rr.shape, satZ.shape, sunZ.shape)
        # vm = Image.merge('RGB', [self.Arr2Img(
        #     self.ArcCrl(i, satZ, RsatZ, sunZ, RsunZ)
        # ) for i in (rr, gg, bb)])
        # 可见光真彩色图像
        va = self.chrange(90 - Z, 10, COLORS).astype('u2')
        va[fz] = 0
        va = self.Arr2Img(self.vcA[va])

        if nightlight :
            bg = Image.open(os.path.join(PATH_PARM, 'nom_%04dm.jpg' % (int(resolution * 100 * 1000))))
            bg.paste(vm, mask = va)
            bg.save(outname, quality=90)
        else:
            vm.save(outname, quality=100)
        print('draw %s success...' %(outname))

    def DrawIR(self, bt8, bt12, outname, resolution=0.04, nightlight=False):

        i7 = bt8.copy()
        i14 = bt12.copy()

        ika = self.chrange(310 - i7, 130, COLORS).astype('u2')
        ib = self.chrange(i14 - i7 + 10, 20, COLORS).astype('u2')
        i14 = self.chrange(310 - i14, 130, COLORS).astype('u2')

        # 红外通道混色计算
        i14 = self.cir[i14]
        ib = self.cib[ib]
        # bule
        akb = i14.astype('f4')
        akb /= COLORS
        akb = 1 - akb
        i7 = (i14 + akb * ib).astype('u2')
        # i7 = (i14 + akb * cka[ika] * ib).astype('u2')
        del akb, ib, ika
        # 计算红外通道透明度
        iA = np.max([i7, i14], axis=0).astype('u2')
        iA = self.ckb[iA]
        ff = i7 < i14
        i7[ff] = i14[ff]
        # green
        i11 = (i7 * .6 + i14 * .4).astype('u2')
        # red
        i14 = (i7 * .2 + i14 * .8).astype('u2')

        # 增强亮度
        b = self.Arr2Img(self.ck[i7])
        del i7
        g = self.Arr2Img(self.ck[i11])
        del i11
        r = self.Arr2Img(self.ck[i14])
        del i14
        a = self.Arr2Img(iA)
        del iA
        im = Image.merge('RGB', (r, g, b))
        if nightlight :
            bg = Image.open(os.path.join(PATH_PARM, 'nom_%04dm.jpg' % (int(resolution * 100 * 1000))))
            bg.paste(im, mask=a)
            bg.save(outname, quality=90)
        else:
            a.save(outname, quality=90)

        print('draw %s success...' %(outname))


    def DrawGeoColor(self,refr, refg, refb, bt8, bt12, sunz, satz,
                     outname, resolution=0.04, nightlight=False, title=None,
                     arearow=None, areacol=None):
        Z = sunz
        fz = Z > 360

        r = refr.copy()
        g = refg.copy()
        b = refb.copy()

        # 色调校正
        rr = self.chrange(r * 100 + g * 20 - b * 20, 102, COLORS).astype('u2')
        gg = self.chrange(r * 30 + g * 20 + b * 50, 102, COLORS).astype('u2')
        bb = self.chrange(b * 83 + r * 17, 102, COLORS).astype('u2')  #np.uint16
        # img2 = Image.merge('RGB', [self.Arr2Img(i) for i in (rr, gg, bb)])
        # img2.save(outname + '-RAW2.jpg', quality=70)
        # '''
        del r, g, b
        # 对卫星天顶角做归一化处理
        satZ = satz.copy()
        satZ = satZ / 90.0
        satZ[satZ>1] = 1
        satZ[satZ<0] = 0

        RsatZ = 1 - satZ
        sunZ = Z / 90
        sunZ[sunZ > 1] = 1
        sunZ[sunZ < 0] = 0
        RsunZ = 1 - sunZ

        #
        self.ArcCrl(rr, satZ, RsatZ, sunZ, RsunZ)
        self.ArcCrl(gg, satZ, RsatZ, sunZ, RsunZ)
        self.ArcCrl(bb, satZ, RsatZ, sunZ, RsunZ)
        # self.Arr2Img((sunZ * 255).astype('u1')).save(outname + '_sunz.jpg')
        # '''
        # 二次渲染 2019_04_10
        # vm = Image.merge('RGB', [self.Arr2Img(i) for i in (rr, gg, bb)])
        # vm.save(outname + '-RAW3.jpg', quality=70)
        vm = Image.merge('RGB', [self.Arr2Img(i) for i in (rr, gg, bb)])

        # 可见光真彩色图像
        # print(rr.shape, satZ.shape, sunZ.shape)
        # vm = Image.merge('RGB', [self.Arr2Img(
        #     self.ArcCrl(i, satZ, RsatZ, sunZ, RsunZ)
        # ) for i in (rr, gg, bb)])
        # 可见光真彩色图像
        va = self.chrange(90 - Z, 10, COLORS).astype('u2')
        va[fz] = 0
        va = self.Arr2Img(self.vcA[va])

        # if nightlight :
        #     bg = Image.open(os.path.join(PATH_PARM, 'nom_%04dm.jpg' % (int(resolution * 100 * 1000))))
        #     bg.paste(vm, mask = va)
        #     bg.save(outname, quality=90)
        # else:
        #     vm.save(outname, quality=100)
        # print('draw %s success...' %(outname))

        i7 = bt8.copy()
        i14 = bt12.copy()

        ika = self.chrange(310 - i7, 130, COLORS).astype('u2')
        ib = self.chrange(i14 - i7 + 10, 20, COLORS).astype('u2')
        i14 = self.chrange(310 - i14, 130, COLORS).astype('u2')

        # 红外通道混色计算
        i14 = self.cir[i14]
        ib = self.cib[ib]
        # bule
        akb = i14.astype('f4')
        akb /= COLORS
        akb = 1 - akb
        i7 = (i14 + akb * ib).astype('u2')
        # i7 = (i14 + akb * cka[ika] * ib).astype('u2')
        del akb, ib, ika
        # 计算红外通道透明度
        iA = np.max([i7, i14], axis=0).astype('u2')
        iA = self.ckb[iA]
        ff = i7 < i14
        i7[ff] = i14[ff]
        # green
        i11 = (i7 * .6 + i14 * .4).astype('u2')
        # red
        i14 = (i7 * .2 + i14 * .8).astype('u2')

        # 增强亮度
        b = self.Arr2Img(self.ck[i7])
        del i7
        g = self.Arr2Img(self.ck[i11])
        del i11
        r = self.Arr2Img(self.ck[i14])
        del i14
        a = self.Arr2Img(iA)
        del iA
        im = Image.merge('RGB', (r, g, b))
        del r, g, b
        if nightlight :
            bg = Image.open(os.path.join(PATH_PARM, 'nom_%04dm.jpg' % (int(resolution * 100 * 1000))))
            if areacol is not None and arearow is not None :
                bgrgb = np.array(bg)
                r = self.Arr2Img(bgrgb[arearow, areacol, 0])
                g = self.Arr2Img(bgrgb[arearow, areacol, 1])
                b = self.Arr2Img(bgrgb[arearow, areacol, 2])
                bg = Image.merge('RGB', (r, g, b))
                del r, g, b
            bg.paste(im, mask=a)
            bg.paste(vm, mask=va)

            if title is not None:
                bg = self.title(bg, title)

            bg.save(outname, quality=90)
        else:
            vm.paste(im, mask=a)

            vm.save(outname, quality=90)

        print('draw %s success...' %(outname))

    def drawchan(self, data, vmax=None, vmin=None, outname=None, title=None):

        if outname is not None :
            dirname = os.path.dirname(outname)
            if len(dirname) != 0 :
                if not os.path.isdir(dirname) :
                    print('%s is not exist, will create it...' %(dirname))
                    os.makedirs(dirname)

        data[data <0] = np.nan
        if vmin is None or vmax is None:
            vmax = np.nanmax(data)
            vmin = np.nanmin(data)
        print('vmax, vmin:', vmax, vmin)

        data[data > vmax] = vmax
        data[data < vmin] = vmin

        data_norm = np.array((data - vmin) / (vmax - vmin) * 255)
        data_norm[np.isnan(data_norm)] = 255
        data_norm = np.array(data_norm, dtype='uint8')

        if outname is not None:
            img = Image.fromarray(data_norm, mode='L')
            draw = ImageDraw.Draw(img)
            if title is not None:
                font = ImageFont.truetype(
                    font=os.path.join(PATH_PARM,'simsun.ttf'),
                    size=120
                )  # 获得字体
                draw.text((0,0), title, font=font)

            img.save(outname, quality=100)
            print('draw %s success...' %(outname))


    def getfont(self, width, fontsize=None):

        if fontsize is None:
            if width <= 300:
                fontsize = 5
            elif 300 < width <= 1000:
                fontsize = 20
            elif 1000 < width <= 2000:
                left = width * 0.18
                fontsize = 34
            elif 2000 < width <= 4000:
                left = width * 0.25
                fontsize = 80
            elif 4000 < width <= 6000:
                fontsize = 110
            elif 6000 < width <= 9000:
                left = width * 0.22
                fontsize = 130
            elif 9000 < width <= 13000:
                fontsize = 180
            elif 18000 < width <= 23000:
                fontsize = 360
            else:
                fontsize = 80
        fontpath = os.path.join(PATH_PARM, 'simsun.ttf')
        font = ImageFont.truetype(fontpath, fontsize)

        return font

    def title(self, img, title='', fontsize=None):
        picsize = img.size

        # 添加标题
        # colorbar_w = int(picsize[0]) + int(picsize[0] * 0.03)
        # colorbar_h = int(picsize[1] * 0.07)
        # TitleImg = Image.new("RGB", (colorbar_w, colorbar_h), (255, 255, 255))
        # w, h = TitleImg.size
        #
        # left = w * 0.1

        font = self.getfont(picsize[0], fontsize)

        # 获取title的长、宽
        width, height = font.getsize(title)
        left = (picsize[0] - width) / 2

        top = picsize[0] * 0.02
        left = picsize[1] * 0.02
        draw = ImageDraw.Draw(img)
        draw.text((left, top), title, fill=(255, 255, 255), font=font)

        return img
        # # 最后放在一张图上
        # totalImg = Image.new('RGB', (int(picsize[0] + colorbar_w1), int(picsize[1] + colorbar_h + colorbar_h2)))
        # totalImg.paste(TitleImg, (0, 0))
        # totalImg.paste(img, (colorbar_w1, colorbar_h))
        # totalImg.paste(ytickImg, (0, colorbar_h))
        # totalImg.paste(xtickImg, (colorbar_w1, picsize[1] + colorbar_h))
        # totalImg.save(outpicture, quality=75)