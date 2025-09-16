<template>
  <div class="menu-bar">
    <MenuBar title="开始" @click="tourVisible=true"></MenuBar>
    <MenuBar title="文件" @click="handleClick('文件')">
      <SubMenu>
          <MenuItem title="打开" @click="handleClickOpen">
            <input ref="fileInput" style="display: none;" type="file" @change="handleFileChange" />
          </MenuItem>
          <MenuItem title="保存" @click="handleClickSave">
            
          </MenuItem>
          <!-- 更多文件菜单项 -->
      </SubMenu>
    </MenuBar>
    <MenuBar title="编辑" @click="handleClick('编辑')">
      <SubMenu>
          <MenuItem title="撤销" @click="handleClick('撤销')">
            <SubMenu>
              <MenuItem title="xx" @click="handleClick('xx')">
                <SubMenu>
                  <MenuItem title="11" @click="handleClick('11')"></MenuItem>
                  <MenuItem title="22" @click="handleClick('22')"></MenuItem>
                <!-- 更多文件菜单项 -->
                </SubMenu>
              </MenuItem>  
              <MenuItem title="aa" @click="handleClick('aa')">
                <SubMenu>
                  <MenuItem title="sss" @click="handleClick('sss')"></MenuItem>
                  <MenuItem title="ss" @click="handleClick('ss')"></MenuItem>
                <!-- 更多文件菜单项 -->
                </SubMenu>
              </MenuItem>
              <!-- 更多文件菜单项 -->
            </SubMenu>
          </MenuItem>
          <MenuItem title="重做" @click="handleClick('重做')"></MenuItem>
          
          <!-- 更多编辑菜单项 -->
      </SubMenu>
    </MenuBar>
    <!-- 更多菜单项 -->
  </div>
</template>

<script setup>
import {computed, ref} from  'vue';
import MenuBar from '@/components/menu/menuBar.vue';
import MenuItem from '@/components/menu/menuItem.vue';
import SubMenu from '@/components/menu/subMenu.vue';
import { useThreeInstanceStore } from '@/store';
import {saveStateToJson} from '@/utils/utilityFunction'
const store = useThreeInstanceStore();
const tourVisible=computed({
  get: () => store.tourVisible,
  set: (val) => store.tourVisible = val
});
const fileInput=ref(null)
function handleClick(title) {
  console.log(`Clicked on: ${title}`);
}
function handleClickSave(){
  console.log("保存")
  const jsonString=saveStateToJson(store)
  // 创建一个 Blob 对象并保存为文件
  const blob = new Blob([jsonString], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'simulationState.json';
  a.click();
  URL.revokeObjectURL(url);
}
function handleClickOpen(){
  if (fileInput.value) {
    fileInput.value.click();
  }
}
function handleFileChange(event){
  const file = event.target.files[0];// 获取用户选择的文件
  if (file) {
    const reader = new FileReader(); // 创建 FileReader 实例

    // 监听文件读取完成的事件
    reader.onload = function (e) {
      const fileContent = e.target.result; // 获取文件内容（文本格式）
      try {
        const jsonData = JSON.parse(fileContent); // 将文本内容解析为 JSON 对象
        console.log("解析后的 JSON 数据：", jsonData);
        store.selectedElement=""
        store.$patch({
          angle: jsonData.angle,
          distance: jsonData.distance,
          resonatorParam: jsonData.resonatorParam,
          fastFourierTransformParam: jsonData.fastFourierTransformParam
        });
        store.threeInstance.addGroupFromJson(jsonData.modelList)
        fileInput.value.value = null; // 清空文件输入框的值
      } catch (error) {
        console.error("解析 JSON 文件时出错：", error);
        alert("选择的文件不是有效的 JSON 格式！");
      }
    };

    // 监听文件读取失败的事件
    reader.onerror = function (error) {
      console.error("读取文件时出错：", error);
      alert("读取文件时出错！");
    };

    // 开始读取文件内容
    reader.readAsText(file);
  } else {
    console.log("没有选择文件");
  }
}
</script>

<style scoped>
.menu-bar {
  display: flex;
  background-color: #f8f8f8;
  border-bottom: 1px solid #ddd;
}
</style>