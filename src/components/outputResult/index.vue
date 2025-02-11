<template>
  <Element/>
  <el-tabs v-model="activeName" @tab-click="handleClick">
    <el-tab-pane label="常数" name="constant">
      <Constant/>
    </el-tab-pane>
    <el-tab-pane label="参数" name="parameter">
      参数
    </el-tab-pane>
    <el-tab-pane label="仿真" name="emulation">
      emulation
    </el-tab-pane>
    
  </el-tabs>
</template>

<script setup>
import Element from './element.vue';
import Constant from './constant.vue';
const tabs=[]
function handleClick(tab, event) {
  console.log(tab, event);
}
</script>

<style scoped>

</style>