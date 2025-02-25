<template>
  <div>
    <Element/>
    <el-tabs v-model="activeName" @tab-click="handleClick">
      <el-tab-pane label="常数" name="constant">
        <Constant/>
      </el-tab-pane>
      <el-tab-pane label="参数" name="parameter">
        <Parameter/>
      </el-tab-pane>
      <el-tab-pane label="仿真" name="simulation">
        <Simulation/>
      </el-tab-pane>
      
    </el-tabs>
  </div>
</template>

<script setup>
import Element from './element.vue';
import Constant from './constant.vue';
import Parameter from './parameter.vue';
import Simulation from './simulation.vue';
const tabs=[]
function handleClick(tab, event) {
  console.log(tab, event);
}
</script>

<style scoped>

</style>