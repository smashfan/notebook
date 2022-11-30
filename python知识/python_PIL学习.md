### 打开图像

通过Image 类中的open （）方法，可以创建一个Image对象。语法格式：

```python
im = Image.open(fp,mode="r")
```

from PIL import Image
#打开图片
img=Image.open(r"./t53.png")

### #显示图像

img.show()

Image子库下[split](https://so.csdn.net/so/search?q=split&spm=1001.2101.3001.7020)()函数常用来分离RGB图片的3个颜色

