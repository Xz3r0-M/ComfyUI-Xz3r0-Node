# ComfyUI Xz3r0 Nodes
一些我自己的时尚小垃圾节点(又重复造轮子了)

## 节点列表:
### X Size (分辨率设置节点)
- 设置宽度和高度的值
- 交换宽高值开关。
![X Size](Preview/X_Size.png)

### X Image Save (图像保存节点)
- 支持文件名标识符
  - `%date%` - 日期 (YYYY-MM-DD格式)
  - `%time%` - 时间 (HH-MM-SS格式)
  - `%Y%`, `%m%`, `%d%` - 年、月、日
  - `%H%`, `%M%`, `%S%` - 时、分、秒
  - `%timestamp%` - Unix时间戳
  - `%seed%` - 生成种子值
- 包含开关可选择是否使用(默认输出目录下)自定义文件夹来保存图像
- 不存在的自定义文件夹将会自动创建（支持同时创建多级子文件夹,如: 默认输出目录/人物/女性）
 ![X Image Save](Preview/X_Image_Save.png)
