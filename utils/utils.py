import calendar
import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from utils.lunar.ulunar import Lunar

width = 800
height = 480
calendar_width = 400
calendar_height = 300
lines = ((0, 300, 800, 300, 2, (200, 0, 0)), (399, 0, 399, 300, 4, 128), (280, 300, 280, 600, 2, (200, 0, 0)),)

# {
#       "size": (800, 600),
#       "calendar": (10, 10),
#       "date": (400, 0),
#       "plan": (0, 300),
#       "lines": ((0, 300, 800, 300, 2, (200, 0, 0)), (399, 0, 399, 300, 4, 128), (280, 300, 280, 600, 2, (200, 0, 0)),)
#     }
img = Image.new('RGB', (width, height), (255, 255, 255))
drawer = ImageDraw.Draw(img)

def draw_lines():
  for (line_startx, line_starty, line_endx, line_endy, width, color) in lines:
    drawer.line((line_startx, line_starty, line_endx, line_endy), fill=color, width=width)

# , photo_path):
def draw_calendar():
  start_x = 10
  start_y = 10
  current_time = datetime.now()
  # 获取月历
  year = current_time.year
  month = current_time.month
  cal = calendar.monthcalendar(year, month)

  # 构建照片日历的画布
  draw = drawer

  # 设置字体
  font = ImageFont.FreeTypeFont(os.path.join(os.getcwd(), 'assets', 'fonts', 'chaoxihuangranrumeng.ttf'), 24)
  font_lunar = ImageFont.FreeTypeFont(os.path.join(os.getcwd(), 'assets', 'fonts', 'chaoxihuangranrumeng.ttf'), 14)
  font_width = 8
  week_height = 40
  week_names = ['一', '二', '三', '四', '五', '六', '日']
  hgap = (calendar_width - start_x * 2 - font_width * 7) / 6
  vgap = (calendar_height - week_height- start_y * 2 - font_width * 5) / 4

  # 根据月历在画布上加入日期
  for week_index, week_name in enumerate(week_names):
    draw.text((start_x + week_index * hgap, 10), week_name, (0, 0, 0), font=font)

  for week_index, week in enumerate(cal):
    for day_index, day in enumerate(week):
      if day == 0:
        continue

      # 获取日期
      date = datetime.strptime('{}-{}-{}'.format(year, month, day), '%Y-%m-%d')

      # 绘制日期
      text_color = (0, 0, 0)
      text_start_x = start_x + day_index * hgap
      text_start_y = week_height + start_y + week_index * vgap
      if current_time.year == year and current_time.month == month and current_time.day == date.day:
        text_color = (255, 0, 0)
        draw.ellipse((text_start_x, text_start_y + 4, text_start_x + 24, text_start_y + 26), fill=None, outline='red', width=1)

      draw.text((text_start_x, text_start_y), f"{date.day:2d}", text_color, font=font)

      lunar = Lunar(year, month, date.day)
      draw.text((text_start_x, week_height + start_y +
            week_index * vgap + 24), lunar.getDate(), (128, 0, 0), font=font_lunar)

def draw_date():
  start_x = 400
  start_y = 0
  current_time = datetime.now()
  month = current_time.month if current_time.month >= 10 else '0{}'.format(current_time.month)
  day = current_time.day if current_time.day >= 10 else '0{}'.format(current_time.day)
  date_str = '{}-{}-{}'.format(current_time.year, month, day)
  font_date = ImageFont.FreeTypeFont(os.path.join(os.getcwd(), 'assets', 'fonts', 'ds-digital.otf'), 70)
  font_date2 = ImageFont.FreeTypeFont(os.path.join(os.getcwd(), 'assets', 'fonts', 'chaoxihuangranrumeng.ttf'), 32)
  font_date_zodiac = ImageFont.FreeTypeFont(os.path.join(os.getcwd(), 'assets', 'fonts', 'chaoxihuangranrumeng.ttf'), 60)
  font_date_zodiac_icon = ImageFont.FreeTypeFont(os.path.join(os.getcwd(), 'assets', 'fonts', 'qweather-icons.ttf'), 130)
  drawer.rectangle((start_x, start_y, start_x + 400, start_y + 300 / 4), fill=(180, 0, 0))
  drawer.text((start_x + 22, start_y), date_str, 'white', font=font_date)
  drawer.rectangle((start_x, start_y + 300 / 4, start_x + 400, start_y + 300), fill='white')
  # 农历日期
  lunar = Lunar(current_time.year, current_time.month, current_time.day)
  lunar_str = '农历{}      年{} {}'.format(lunar.getGanZhi(), lunar.getMonth(),lunar.getDate())
  drawer.text((start_x + 22, start_y + 300 / 4 + 16), lunar_str, 'black', font=font_date2)
  drawer.text((start_x + 150, start_y + 300 / 4 - 4), lunar.getZodiac(), 'red', font=font_date_zodiac)
  drawer.text((start_x + 140, start_y + 300 / 2), lunar.getZodiacIcon(), 'red', font=font_date_zodiac_icon)

def get_bitmap_arr():
  # 生成点阵数组
  # 创建一个新的图像，大小与原图像相同
  output_image = Image.new("RGB", img.size)

  # 循环遍历每个像素
  for x in range(img.width):
    for y in range(img.height):
        # 获取像素值
        pixel = img.getpixel((x, y))

        # 根据像素值设置新图像的颜色
        if pixel[0] < 128 and pixel[1] < 128 and pixel[2] < 128:
            # 黑色
            output_image.putpixel((x, y), (0, 0, 0))
        elif pixel[0] >= 128 and pixel[1] >= 128 and pixel[2] >= 128:
            # 白色
            output_image.putpixel((x, y), (255, 255, 255))
        else:
            # 红色
            output_image.putpixel((x, y), (255, 0, 0))

  # 将图像转换为C语言数组
  return list(output_image.getdata())

def draw_plan():
  start_x = 0
  start_y = 300
  font_title = ImageFont.FreeTypeFont(os.path.join(os.getcwd(), 'assets', 'fonts', 'chaoxihuangranrumeng.ttf'), 28)
  font_date = ImageFont.FreeTypeFont(os.path.join(os.getcwd(), 'assets', 'fonts', 'chaoxihuangranrumeng.ttf'), 20)
  drawer.rectangle((start_x, start_y, start_x + 280, start_y + 40), fill=(180, 0, 0))
  drawer.text((start_x + 4, start_y), '最近日程', 'white', font=font_title)
  plan_list = (('2024-01-23', '休假去旅游'), (('2024-02-02', '休假去睡觉')))
  for (item_index, item) in enumerate(plan_list):
    text_start_x = 10
    text_start_y = start_y + 50 + item_index * 34
    (plan_date, plan_content) = item
    drawer.text((text_start_x, text_start_y), plan_date, 'black', font=font_date)
    drawer.text((text_start_x + 110, text_start_y), plan_content, 'black', font=font_date)

def draw():
  # draw_bg()
  draw_calendar()
  draw_date()
  draw_plan()
  draw_lines()
  bitmap = get_bitmap_arr()
  # 保存图片
  file_path = os.path.abspath(os.path.join(os.getcwd(), 'output', '1.jpg'))
  img.save(file_path)
  return file_path
