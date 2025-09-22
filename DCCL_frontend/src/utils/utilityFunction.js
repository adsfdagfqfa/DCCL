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

export function saveStateToJson(store) {
  // 构建要保存的完整数据
  const dataToSave = {
    modelList:store.threeInstance.modelList.map((mesh) => mesh.toJSON()),
    distance: store.distance,
    angle: store.angle,
    resonatorParam: store.resonatorParam,
    fastFourierTransformParam: store.fastFourierTransformParam,
  };

  // 序列化为 JSON
  const jsonString = JSON.stringify(dataToSave);
  console.log(jsonString)
  return jsonString
}
// export function saveDataFromJson(jsonObject,store){
//   store.selectedComponent=""
//   store.$patch({
//     angle: jsonObject.angle,
//     distance: jsonObject.distance,
//     resonatorParam: jsonObject.resonatorParam,
//     fastFourierTransformParam: jsonObject.fastFourierTransformParam
//   });
//   store.threeInstance.addGroupFromJson(jsonObject.modelList)
// }
