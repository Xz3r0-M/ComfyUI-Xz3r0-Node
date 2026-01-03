# ComfyUI Xz3r0 Nodes
一些我自己的时尚小垃圾节点(似乎又重复造轮子了)

```bash
git clone https://github.com/Xz3r0-M/ComfyUI-Xz3r0-Node.git
cd ComfyUI-Xz3r0-Node
pip install -r requirements.txt
```

## 节点列表
### XSize (分辨率设置节点)
- 设置宽度和高度的值
- 交换宽高值开关。
<img src="Preview/XSize.png" width="400" alt="XSize">

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
<img src="Preview/XImageSave.png" width="400" alt="XImageSave">

### XLoadLatent (Latent加载节点)
- 从ComfyUI的Output目录加载`.latent`文件
- 提供下拉列表显示Output目录及其子目录中的Latent文件

### XSaveLatent (Latent保存节点)
- 将`.latent`文件保存到ComfyUI的Output目录
- 支持带序号和不带序号的文件名（防止覆盖或直接覆盖）
- 将已保存的文件名输出为字符串
- 保存Latent让长视频生成工作流更容易分开处理
<img src="Preview\XLoadLatent&XSaveLatent.png" width="400" alt="XLoadLatent&XSaveLatent">