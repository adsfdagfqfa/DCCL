<template>
    <div class="min-w-[500px]">
        <!-- <el-scrollbar >
          
        </el-scrollbar> -->
        <DynamicScroller
          ref="virtualScroller"
          class="list"
          :items="visibleItems"
          :min-item-size="150">
          <template v-slot="{ item }">
            <!-- <div class="list-item">
              <ResultItem :item="item" ></ResultItem>
            </div> -->
            <DynamicScrollerItem :item="item" :active="true" :size-dependencies="[item.content]">
              <div class="list-item" :key="item.id">
                <ResultItem :item="item.content" :only_final_result="store.onlyFinalResult" />
              </div>
            </DynamicScrollerItem>
          </template>
        </DynamicScroller>
        <!-- <div v-for="(item,index) in resultList" :key="index" >
          <div class="list-item">
            <ResultItem :item="item" ></ResultItem>
          </div>
          
        </div> -->
        <div class="flex justify-between items-center p-4">
          <el-checkbox v-model="store.onlyFinalResult" label="只显示结果" size="large" />
          <div class="flex items-center space-x-2">
            <el-button :type="isPaused?'success':'warning'" @click="onTogglePauseTask">{{ isPaused ? '继续' : '暂停' }}</el-button>
            <el-button type="danger" @click="onCancelTask">取消</el-button>
            <!-- <el-button type="primary" @click="store.plotDialogVisible=true">分析结果</el-button> -->
          </div>
        </div>
      </div>
</template>
<script setup>
import ResultItem from './resultItem.vue';
import { ref ,getCurrentInstance ,computed, watch, nextTick} from 'vue'
import { DynamicScroller, DynamicScrollerItem } from 'vue-virtual-scroller'
import { useThreeInstanceStore } from '@/store';
import { onMounted } from 'vue';
const store = useThreeInstanceStore();
const isPaused = ref(false)
const pageInstance = getCurrentInstance();
const resultList = computed(() => {
    return store.simulationResult;
});
const currentTaskID = computed(() => {
    return store.currentTaskID;
});
const visibleItems = computed(() =>
    store.onlyFinalResult
        ? resultList.value.filter(({ content }) => {
            try {
            return JSON.parse(content).isEnd
            } catch {
            return false
            }
        }): resultList.value
)
watch(
  () => store.simulationResult,
  async () => {
    await nextTick() // 等 DOM 更新完
    console.log("滚动到底部")
    pageInstance.refs.virtualScroller.scrollToBottom()
  },
  { deep: true }
)
function onTogglePauseTask(){
    //清除rangeGenerator里面的输入
    if(isPaused.value){
        isPaused.value=false;
        store.continueTask(currentTaskID.value);
    }
    else{
        isPaused.value=true;
        store.pauseTask(currentTaskID.value);
    }
}
function onCancelTask(){
    //清除rangeGenerator里面的输入
    store.cancelTask(currentTaskID.value);
    isPaused.value=false;
    console.log("取消任务")
    //清空结果列表
    store.simulationResult=[];
    //清空rangeGenerator里面的输入
    if (rangeGenerator.value) {
        rangeGenerator.value.clearInput();
    }
}
onMounted(() => { 
});
</script>
<style scoped>
/* Your component-specific styles go here */
.list {
  height: 500px;
  border: 5px solid #eeeeeee9;
  border-radius: 8px;
}

.list-item {
  height:150px;
  padding: 12px;
  border-bottom: 1px dashed #020817;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
</style>