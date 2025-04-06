<template>
  <div>
    <!-- 顶端部分 -->
    <header class="flex flex-col">
      <div class="bg-blue-200 text-gray-800 text-center leading-[60px]">分布式耦合腔激光系统仿真软件</div>
      <Menu></Menu>
    </header>
    <div class="grid grid-cols-8">
      <!-- <Steps  @update:router-view="handleClick"/> -->
      <ElementList></ElementList>
      <div class="col-span-5">
        <Resonator></Resonator>
        <router-view/>
      </div>
      <ElementPanel class="col-span-2"/>
      <!-- <test></test> -->
    </div>
    <div>
      <!-- <OutputResult></OutputResult> -->
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
    <!-- <PyPlot></PyPlot> -->
  </div>
</template>

<script setup>
import Menu from '@/components/menu/index.vue'
import ElementList from '@/components/elementList/index.vue'
import ElementPanel from '@/components/elementPanel/index.vue'
import OutputResult from '@/components/outputResult/index.vue';
import Resonator from '@/components/resonator/index.vue';
import { onMounted } from 'vue';
import PyPlot from '@/components/pyPlot/index.vue';
import Element from '@/components/element/index.vue';
import Constant from '@/components/outputResult/constant.vue';
import Parameter from '@/components/outputResult/parameter.vue';
import Simulation from '@/components/outputResult/simulation.vue';
onMounted(async()=>{
  console.log("mainView","挂载")
})
const tabs=[]
function handleClick(tab, event) {
  console.log(tab, event);
}
</script>
