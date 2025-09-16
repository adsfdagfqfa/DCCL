<template>
  <div>
    <Guide :steps="tourSteps" :modelValue="tourVisible"
      @update:modelValue="val => tourVisible = val"/>
    <!-- 添加Tour组件 -->
    
    <!-- 顶端部分 -->
    <header class="flex flex-col">
      <div class="bg-blue-200 text-gray-800 text-center leading-[60px]">分布式耦合腔激光系统仿真软件</div>
      <Menu></Menu>
    </header>
    <div class="grid grid-cols-8">
      <!-- <Steps  @update:router-view="handleClick"/> -->
      <ComponentLibrary></ComponentLibrary>
      <div class="col-span-5">
        <Resonator></Resonator>
        <!-- <router-view/> -->
      </div>
      <ComponentWorkbench class="col-span-2"/>
      <!-- <test></test> -->
    </div>
    <div>
      <!-- <OutputResult></OutputResult> -->
      <ComponentDistancePanel/>
      <el-tabs ref="tabsRef" v-model="activeName" @tab-click="handleClick" class="tour-parameter-panel  tour-output-panel">
        <!-- <el-tab-pane label="常数" name="constant">
          <ConstantPanel/>
        </el-tab-pane> -->
        <el-tab-pane label="参数" name="parameter">
          <div class='flex'>
            <ParameterPanel/>
            <SimulationPanel/>
          </div>
        </el-tab-pane>
        <el-tab-pane label="输出" name="output">
          <!-- <SimulationPanel/> -->
          <div class="flex">
          <OutputResultPanel/>
          <el-card  class="flex-1">
            <OpticalFieldViewer ref="opticalFieldViewer"/>
            <div class="mt-2 text-right">
              <el-button type="primary" @click="downloadData">
                Download<el-icon class="el-icon--right"><Download /></el-icon>
              </el-button>
            </div>
          </el-card>

          <!-- 曲线分析 -->
          <el-card  class="flex-1">
            <PLotViewer ref="plotViewer"/>
          </el-card>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script setup>
import { computed, ref ,provide} from 'vue'
import Menu from '@/components/menu/index.vue'
import ComponentLibrary from '@/components/componentLibrary/index.vue'
import ComponentWorkbench from '@/components/componentWorkbench/index.vue'
// import OutputResult from '@/components/outputResult/index.vue';
import Resonator from '@/components/resonator/index.vue';
import { onMounted } from 'vue';
import OpticalFieldViewer from '@/components/opticalFieldViewer/index.vue';
import ComponentDistancePanel from '@/components/componentDistancePanel/index.vue';
import ConstantPanel from '@/components/constantPanel/index.vue';
import ParameterPanel from '@/components/parameterPanel/index.vue';
import SimulationPanel from '@/components/simulationPanel/index.vue';
import OutputResultPanel from '@/components/outputResultPanel/index.vue';
import PLotViewer from '@/components/plotViewer/index.vue'
import { Upload,Download } from '@element-plus/icons-vue'
import { useThreeInstanceStore } from '@/store';
import { ElTour} from 'element-plus';
import Guide from '@/components/guide/index.vue';
import { tourSteps } from '@/js/tourConfig.js';
const store = useThreeInstanceStore();

// 在 setup 中添加 tour 相关数据
const tourVisible = computed({
  get: () => store.tourVisible,
  set: (val) => store.tourVisible = val
});

onMounted(async()=>{
  console.log("mainView","挂载")
  // 首次访问时自动显示引导
})
const activeName=ref("parameter")
const tabsRef=ref(null)
provide('tabsRef',tabsRef)
function handleClick(tab, event) {
  console.log(tab, event);
}
function downloadData() {
  // 处理下载逻辑
  console.log("下载文件")
  store.downloadData()
}

</script>
