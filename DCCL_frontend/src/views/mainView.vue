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
        <!-- <router-view/> -->
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
    <el-button plain @click="store.opticalFieldDialogVisible=true">
      Open the optical field Dialog
    </el-button>
    <el-button plain @click="store.plotDialogVisible=true">
      Open the plot Dialog
    </el-button>
  <el-dialog v-model="store.opticalFieldDialogVisible" destroy-on-close>
    <OpticalFieldViewer ref="opticalFieldViewer"/>
    <template #footer>
      <el-button type="primary" @click="downloadData">
        Download<el-icon class="el-icon--right"><Download /></el-icon>
      </el-button>
    </template>
  </el-dialog>
  <el-dialog v-model="store.plotDialogVisible" destroy-on-close> 
    <PLotViewer ref="plotViewer"/>
  </el-dialog>
    <!-- <PyPlot></PyPlot> -->
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Menu from '@/components/menu/index.vue'
import ElementList from '@/components/elementList/index.vue'
import ElementPanel from '@/components/elementPanel/index.vue'
// import OutputResult from '@/components/outputResult/index.vue';
import Resonator from '@/components/resonator/index.vue';
import { onMounted } from 'vue';
import OpticalFieldViewer from '@/components/opticalFieldViewer/index.vue';
import ElementDistancePanel from '@/components/elementDistancePanel/index.vue';
import ConstantPanel from '@/components/constantPanel/index.vue';
import ParameterPanel from '@/components/parameterPanel/index.vue';
import SimulationPanel from '@/components/simulationPanel/index.vue';
import PLotViewer from '@/components/plotViewer/index.vue'
import { Upload,Download } from '@element-plus/icons-vue'
import { useThreeInstanceStore } from '@/store';
const store = useThreeInstanceStore();

onMounted(async()=>{
  console.log("mainView","挂载")
})
const tabs=[]
const activeName=ref("")
function handleClick(tab, event) {
  console.log(tab, event);
}
function downloadData() {
  // 处理下载逻辑
  console.log("下载文件")
  store.downloadData()
}

</script>
