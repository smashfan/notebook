### 读写图片



```python
#读图片

image_path = '/data/weichai/0817_choice_frame/8.4_sortheast/1.jpg'
image = cv2.imread(image_path) 
# image是一个矩阵。shape: (hight, weight, channel)



#保存图片

output_path = '/home/liulihao/test/demo.jpg'
save_image = np.zeros([200,100,3])
cv2.imwrite(output_path, save_image)


#展示图片
cv2.imshow("image",face)
cv2.waitKey() 

```

