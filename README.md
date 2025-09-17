# 图片添加文字工具

一个功能强大的Python脚本，可以给图片添加自定义文字，支持多种字体、颜色和位置选项。

## ✨ 功能特点

- 🖼️ 支持多种图片格式（JPG、PNG、GIF等）
- 🔤 多种免费字体选择
- 🎨 丰富的颜色定制选项
- 📍 灵活的文字位置设置
- 🖌️ 支持文字描边效果
- 💻 命令行和Python API两种使用方式

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 基本使用

```bash
# 基本用法
python imgaddtext.py your_image.jpg -t "Hello World!"

# 指定输出文件
python imgaddtext.py your_image.jpg -t "标题" -o output.jpg

# 自定义字体大小和颜色
python imgaddtext.py your_image.jpg -t "大标题" -s 80 -c red
```

### 3. 运行示例

```bash
python 使用示例.py
```

## 📋 命令行参数

| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| `--text` | `-t` | 要添加的文字 | 必需 |
| `--output` | `-o` | 输出图片路径 | 自动生成 |
| `--font` | `-f` | 字体名称 | arial |
| `--size` | `-s` | 字体大小 | 40 |
| `--color` | `-c` | 文字颜色 | black |
| `--position` | `-p` | 文字位置 | top-left |
| `--outline-color` | | 描边颜色 | 无 |
| `--outline-width` | | 描边宽度 | 0 |
| `--list-fonts` | | 列出可用字体 | - |
| `--show-colors` | | 显示颜色示例 | - |
| `--show-positions` | | 显示位置示例 | - |

## 🎨 颜色格式

支持多种颜色格式：

- **命名颜色**: `black`, `white`, `red`, `green`, `blue`, `yellow`, `cyan`, `magenta`, `gray`, `orange`, `purple`, `pink`, `brown`, `lime`, `navy`, `teal`
- **十六进制**: `#FF0000`, `#00FF00`, `#0000FF`
- **RGB值**: `255,0,0` 或 `(255,0,0)`

## 📍 位置格式

支持多种位置格式：

### 预定义位置
- `top-left`, `top-center`, `top-right`
- `center-left`, `center`, `center-right`
- `bottom-left`, `bottom-center`, `bottom-right`

### 自定义坐标
- `100,200` 或 `(100,200)`
- `100,vcenter` - 水平坐标100，垂直居中
- `center,200` - 水平居中，垂直坐标200
- `center,center` 或 `vcenter` - 完全居中

### 文件名自动解析位置和字体大小
如果不指定 `-p` 参数，脚本会自动尝试从图片文件名解析位置和字体大小：
- 文件名格式：`顺序-x坐标x y坐标-字体大小.jpg`
- 示例：`1-200x300.jpg` → 位置 (200, 300)，使用默认字体大小
- 示例：`1-200xvcenter-120.jpg` → 位置 (200, vcenter)，字体大小 120
- 示例：`2-100xcenter-80.jpg` → 位置 (100, center)，字体大小 80
- 支持的坐标格式：数字、`center`、`vcenter`
- **位置说明**：所有位置都是文字区域**顶部**距离图片顶部的距离
- **居中说明**：`center`/`vcenter` 表示整个文字区域在图片垂直中心
- 如果文件名不符合格式，使用默认位置 `top-left` 和默认字体大小

### 批量处理排序
批量处理时，图片按照文件名用 `-` 分割后的第一个数值进行排序：
- `1-200x300.jpg` → 排序值：1
- `10-100xcenter.jpg` → 排序值：10
- `2-200x300.jpg` → 排序值：2
- 排序结果：1, 2, 10...

## 🔤 字体支持

### 系统字体
脚本会自动检测系统可用的字体：
- Arial
- Calibri
- Times New Roman
- Verdana
- Comic Sans MS
- Impact
- Trebuchet MS

### 自定义字体
1. 将字体文件（.ttf或.otf）放入 `fonts` 文件夹
2. 使用字体文件名（不含扩展名）作为字体参数

推荐免费字体资源：
- [Google Fonts](https://fonts.google.com/)
- [Adobe Fonts](https://fonts.adobe.com/)
- [字体天下](https://www.fonts.net.cn/)

## 💡 使用示例

### 单张图片处理

```bash
# 基本用法
python imgaddtext.py photo.jpg -t "生日快乐!"

# 大红色标题，居中显示
python imgaddtext.py photo.jpg -t "重要通知" -s 60 -c red -p center

# 白色文字，黑色描边，底部居中
python imgaddtext.py photo.jpg -t "水印文字" -c white --outline-color black --outline-width 2 -p bottom-center

# 自定义位置和颜色
python imgaddtext.py photo.jpg -t "自定义" -c "#FF6600" -p "300,200"

# 垂直居中，水平坐标100
python imgaddtext.py photo.jpg -t "垂直居中" -p "100,vcenter"

# 水平居中，垂直坐标200
python imgaddtext.py photo.jpg -t "水平居中" -p "center,200"

# 文件名自动解析位置（不需要-p参数）
python imgaddtext.py 1-200x300.jpg -t "自动解析位置"

# 文件名自动解析位置和字体大小
python imgaddtext.py 1-200xvcenter-120.jpg -t "自动解析位置和字体大小"

# 测试垂直距离：文字区域top距离图片顶部200像素
python imgaddtext.py 1-100x200-80.jpg -t "垂直距离测试"

# 批量处理，自动解析每张图片的位置和字体大小，按数值排序
python imgaddtext.py --batch --folder ./images --text-file ./text.txt

# 查看可用选项
python imgaddtext.py --list-fonts
python imgaddtext.py --show-colors
python imgaddtext.py --show-positions
```

### 批量处理功能

```bash
# 基本批量处理
python imgaddtext.py --batch --folder ./images --text-file ./text.txt

# 自定义参数的批量处理
python imgaddtext.py --batch --folder ./images --text-file ./text.txt --font simkai --size 50 --color red --position center

# 带描边效果的批量处理
python imgaddtext.py --batch --folder ./images --text-file ./text.txt --font simhei --size 60 --color white --outline-color black --outline-width 2

# 指定输出文件夹
python imgaddtext.py --batch --folder ./images --text-file ./text.txt --output-folder ./results
```

### Python API 示例

```python
from imgaddtext import ImageTextAdder

# 创建工具实例
adder = ImageTextAdder()

# 单张图片处理
result = adder.add_text_to_image(
    image_path="input.jpg",
    text="Hello World!",
    output_path="output.jpg",
    font_name="simkai",
    font_size=50,
    color="black",
    position="center"
)

print(f"处理完成: {result}")

# 批量处理
batch_result = adder.batch_process_images(
    folder_path="./images",
    text_file_path="./text.txt",
    output_folder="./output",
    font_name="simkai",
    font_size=40,
    color="black",
    position="center"
)

print(f"批量处理完成: {batch_result} 张图片")
```

## 📁 项目结构

```
imgaddtext/
├── imgaddtext.py          # 主脚本
├── requirements.txt       # 依赖文件
├── 使用示例.py            # 使用示例
├── README.md             # 说明文档
└── fonts/                # 字体文件夹
    └── README.md         # 字体说明
```

## 🔧 高级功能

### 批量处理功能

批量处理功能可以自动从文本文件中读取多个段落，并将每个段落添加到对应的图片中。

#### 文本格式要求
- 文本文件使用UTF-8编码
- 段落之间用连续两个换行符分隔
- 每个段落内的换行符会被保留，实现多行文字显示

#### 示例文本格式
```
第一条文案内容
可以包含多行文字
每行都会在图片中换行显示

第二条文案内容
也可以很长
支持多行显示

第三条文案内容
最后一段
```

#### 处理规则
1. 图片按文件名顺序处理
2. 文本按段落顺序处理
3. 每个段落对应一张图片
4. 如果图片不够，剩余文本段落会被忽略
5. 如果文本不够，剩余图片不会被处理

### 多行文字显示
脚本支持在图片中显示多行文字，换行符会被保留，并正确计算垂直居中：

```bash
# 使用 \n 表示换行
python imgaddtext.py image.jpg -t "第一行文字\n第二行文字\n第三行文字" -p center

# 文本文件中的换行符会自动保留
python imgaddtext.py --batch --folder ./images --text-file ./multiline.txt

# 不同字体大小的多行文字垂直居中
python imgaddtext.py image.jpg -t "第一行\n第二行\n第三行" -s 80 -p "100,vcenter"
```

#### 多行文字垂直居中计算
- 行高 = 字体大小 + 5px
- 总高度 = 非空行数 × 行高
- 起始位置 = 居中位置 - 总高度 ÷ 2
- 垂直居中基于实际文字内容计算，不受空行影响
- 整个文字块的中心位置在指定的居中位置

### 文字描边
```bash
python imgaddtext.py image.jpg -t "描边文字" -c white --outline-color black --outline-width 3
```

### 批量处理
```python
import os
from imgaddtext import ImageTextAdder

adder = ImageTextAdder()

# 批量处理文件夹中的图片
for filename in os.listdir("images"):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        input_path = os.path.join("images", filename)
        output_path = os.path.join("output", f"text_{filename}")
        
        adder.add_text_to_image(
            image_path=input_path,
            text="水印文字",
            output_path=output_path,
            position="bottom-right",
            color="white"
        )
```

## ❓ 常见问题

**Q: 为什么有些字体不显示？**
A: 请确保字体文件在 `fonts` 文件夹中，且文件名不包含中文字符。

**Q: 如何调整文字在图片中的精确位置？**
A: 使用自定义坐标格式，如 `-p "100,200"`，其中100是x坐标，200是y坐标。

**Q: 支持哪些图片格式？**
A: 支持PIL库支持的所有格式，包括JPG、PNG、GIF、BMP等。

**Q: 如何批量处理多张图片？**
A: 可以编写Python脚本循环调用API，或使用批处理脚本。

## 📄 许可证

本项目使用MIT许可证。

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个工具！
