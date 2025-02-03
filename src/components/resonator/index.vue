<template>
    <div style=" width: 900px; height: 300px" class="relative" id="resonator" 
        @drop="onDragDrop">
      <div class="absolute top-2.5 right-1/2">
        <el-tooltip effect="dark" content="重置视角" placement="top">
          <el-icon :size="18" color="#0000ff" @click="resetCamera">
            <Aim/>
          </el-icon>
        </el-tooltip>
      </div>
      <div class ="absolute top-2.5 right-2.5">
        <el-tooltip effect="dark" content="切换视角" placement="top">
          <el-switch v-model="modelType" size="large" active-text="2D" inactive-text="3D" @click="switchType"/>
        </el-tooltip>
      </div>  
    </div>
</template>
    
<script setup>
import {Aim} from '@element-plus/icons-vue'
import threeInstance from "@/utils/threeInstance";
import { onMounted } from 'vue';
import {useThreeInstanceStore} from '@/store/index'
import { ref } from "vue";
const store = useThreeInstanceStore()
const modelType=ref(true);
// 创建 ThreeJs 实例并初始化
// const initThreeJs =  () => {
  
// };

onMounted( async ()=>{
  const app = new threeInstance("resonator");
  app.init();
  app.setupScene()
  app.animate();
  store.setThreeInstance(app)
});

function switchType () {
  //store.dispatch('switchCamera',)
  store.threeInstance.switchCamera(modelType.value?"2D":"3D")
}

function resetCamera(){
  store.threeInstance.resetCameraToNegativeZ()
}

function onDragDrop(){
  // const { dragGeometryModel, dragTag, activeDragManyModel } = store.modelApi;
  // const { clientX, clientY } = e;

  // //更新拖拽位置
  // const updateDragPosition = model => {
  //   model.clientX = clientX;
  //   model.clientY = clientY;
  // };

  // //处理几何体模型
  // if (dragGeometryModel.id && store.modelType === "geometry") {
  //   updateDragPosition(dragGeometryModel);
  //   store.modelApi.onSwitchModel(dragGeometryModel);
  // }
}
</script>
    
<style>
    html, body {
    width: 100%;
    height: 100%;
    margin: 0;
    padding: 0;
    overflow: hidden;
    }
</style>
