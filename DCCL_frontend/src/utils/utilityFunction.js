/**
 * 生成唯一标识符
 * @param {Number} len 标识符长度
 * @param {Number} radix 基数,标识符所使用的字符
 * @return {String} 唯一标识符
 */
export function onlyKey(len, radix) {
    const chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
    const uuid = [];
    radix = radix || chars.length;
    if (len) {
        for (let i = 0; i < len; i++) {
            uuid[i] = chars[Math.floor(Math.random() * radix)];
        }
    }
    //将数组转化为字符串返回
    return uuid.join("");
}

export function saveStateToFile(store) {
  //提取 threeInstance 的关键数据
  const threeInstanceData = {
    scene: extractSceneData(store.threeInstance.scene), // 提取场景数据
    camera: extractCameraData(store.threeInstance.camera), // 提取相机数据
    renderer: extractRendererData(store.threeInstance.renderer), // 提取渲染器数据
  };

  // 构建要保存的完整数据
  const dataToSave = {
    threeInstance: threeInstanceData,
    selectedElement: store.selectedElement,
    distance: store.distance,
    angle: store.angle,
    resonatorParam: store.resonatorParam,
    fastFourierTransformParam: store.fastFourierTransformParam,
  };

  // 序列化为 JSON
  const jsonString = JSON.stringify(dataToSave);

  // 创建一个 Blob 对象并保存为文件
  const blob = new Blob([jsonString], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'simulationState.json';
  a.click();
  URL.revokeObjectURL(url);
}
