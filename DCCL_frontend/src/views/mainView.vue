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
      <ElementDistancePanel/>
      <el-tabs v-model="activeName" @tab-click="handleClick">
        <el-tab-pane label="常数" name="constant">
          <ConstantPanel/>
        </el-tab-pane>
        <el-tab-pane label="参数" name="parameter">
          <ParameterPanel/>
        </el-tab-pane>
        <el-tab-pane label="仿真" name="simulation">
          <SimulationPanel/>
        </el-tab-pane>
      </el-tabs>
    </div>
    <el-button plain @click="dialogVisible = true">
      Open the event Dialog
    </el-button>

  <el-dialog v-model="dialogVisible" >
    <span>It's a event Dialog</span>
    <template #title>
      <div class="dialog-footer">
        <el-button @click="dialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="dialogVisible = false">Confirm</el-button>
      </div>
    </template>
  </el-dialog>
    <!-- <PyPlot></PyPlot> -->
  </div>
</template>

<script setup>
import Menu from '@/components/menu/index.vue'
import ElementList from '@/components/elementList/index.vue'
import ElementPanel from '@/components/elementPanel/index.vue'
// import OutputResult from '@/components/outputResult/index.vue';
import Resonator from '@/components/resonator/index.vue';
import { onMounted } from 'vue';
import PlotViewer from '@/components/plotViewer/index.vue';
import ElementDistancePanel from '@/components/elementDistancePanel/index.vue';
import ConstantPanel from '@/components/constantPanel/index.vue';
import ParameterPanel from '@/components/parameterPanel/index.vue';
import SimulationPanel from '@/components/simulationPanel/index.vue';
onMounted(async()=>{
  console.log("mainView","挂载")
})
const tabs=[]
function handleClick(tab, event) {
  console.log(tab, event);
}
import { ref } from 'vue'

const dialogVisible = ref(false)
</script>
