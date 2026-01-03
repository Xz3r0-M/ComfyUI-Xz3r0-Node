# ComfyUI Xz3r0 Nodes
一些我自己的时尚小垃圾节点(又重复造轮子了)

## 节点列表:
### XSize (分辨率设置节点)
- 设置宽度和高度的值
- 交换宽高值开关。
<img src="Preview/X_Size.png" width="400" alt="XSize">

### XImageSave (图像保存节点)
- 支持文件名标识符
  - `%date%` - 日期 (YYYY-MM-DD格式)
  - `%time%` - 时间 (HH-MM-SS格式)
  - `%Y%`, `%m%`, `%d%` - 年、月、日
  - `%H%`, `%M%`, `%S%` - 时、分、秒
  - `%timestamp%` - Unix时间戳
  - `%seed%` - 生成种子值
- 包含开关可选择是否使用(默认输出目录下)自定义文件夹来保存图像
- 不存在的自定义文件夹将会自动创建（支持同时创建多级子文件夹,如: 默认输出目录/人物/女性）
<img src="Preview/X_Image_Save.png" width="400" alt="XImageSave">

### XLoadLatent (潜变量加载节点)
- 从ComfyUI的Output目录加载`.latent`文件
- 提供下拉列表显示Output目录及其子目录中的潜变量文件

### XSaveLatent (潜变量保存节点)
- 保存潜变量张量到`.latent`文件
- 支持带序号和不带序号的文件名（防止覆盖或直接覆盖）
- 可以指定保存路径(默认为ComfyUI的Output目录)
- 保存Latent让长视频生成工作流更容易分开处理
