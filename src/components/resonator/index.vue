<template>
    <div style=" width: 900px; height: 300px" class="relative" id="resonator">
      <div style="position: absolute; top: 10px; right: 10px;">
        <el-switch v-model="modelType" size="large" active-text="2D" inactive-text="3D" @click="switchType"/>
      </div>
        
      
    </div>
    
</template>
    
<script setup>
import threeDModel from "@/utils/threejsInstance";
import { onMounted } from 'vue';
import {useStore} from 'vuex'
import { ref } from "vue";
const store = useStore()
const modelType=ref(true);
// 创建 ThreeJs 实例并初始化
const initThreeJs = async () => {
  const app = new threeDModel("resonator");
  app.init();
  app.setupScene()
  app.animate();
  store.dispatch('updateThreeInstance', app);
};

onMounted(initThreeJs);

function switchType () {
  store.dispatch('switchCamera',modelType.value?"2D":"3D")
  
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
