<template>
    <div  style="height:400px" class="relative" id="resonator" 
        @drop="onDragDrop" @dragover="onDragOver">
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
function onDragOver(e){
  e.preventDefault(); // 阻止默认行为，允许元素接收拖拽内容
}
const onDragDrop= (e) => {
  const  dragModel  = store.threeInstance.dragModel;
  // console.log(clientX)
  // console.log(clientY)
  // console.log(dragModel)
  //模型
  if (dragModel.type) {
    store.threeInstance.addModel(dragModel);
    //结束后设置dragModel为空
    store.threeInstance.dragModel=null;
    if(store.threeInstance.modelList.length>1){
      store.distance.push(0)
      store.angle.push(0)
    }
  }
}
</script>
    
<style>
</style>
