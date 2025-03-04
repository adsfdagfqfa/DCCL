<template>
  <div>
    <div>
      <el-card>
          <el-scrollbar   class="height-full">
            <div class="flex items-center">
              <span class="font-bold whitespace-nowrap min-w-36">模型元素</span>
              <div v-for="item in store.threeInstance?.modelAttributeList" :key="item.model" class="flex-item">
                <span>{{ item.model }}</span>
              </div>
            </div>
           
            <div>
              <div class="flex items-center">
                <span class="font-bold whitespace-nowrap min-w-36">距离(m)</span>
                <div class="min-w-[100px]"></div><!-- 用于占位 -->
                <div v-for="(d,index) in store.distance" :key="index" class="flex-item">
                  <!-- <span>{{ d }}</span> -->
                  <el-input  type="number" title="" style="width: 80px;" :input-style="{ textAlign: 'center' }" 
                   v-model.number="store.distance[index]" ></el-input>
                </div>
              </div>
            </div> 
            <div>
              <div class="flex items-center">
                <span class="font-bold whitespace-nowrap min-w-36">角度(deg)</span>
                <div class="min-w-[100px]"></div>
                <div v-for="(a,index) in store.angle" :key="index" class="flex-item">
                  <!-- <span>{{ a }}</span> -->
                  <el-input  type="number" title="" style="width: 80px;" :input-style="{ textAlign: 'center' }" 
                   v-model.number="store.angle[index]" ></el-input>
                </div>
              </div>
            </div> 
          </el-scrollbar>
      </el-card>
      
    </div>
  </div>
</template>

<script setup>
import { Edit,Delete,Location } from '@element-plus/icons-vue';
import { computed } from 'vue';
import { useThreeInstanceStore } from '@/store';
const store = useThreeInstanceStore();

// const modelAttributeList = computed(() => store.threeInstance?.modelAttributeList);

</script>

<style scoped>
.flex-item {
  display: inline-block; /* 内联块元素 */
  min-width: 200px; /* 设置每个项目的最小宽度 */
  text-align: center; /* 水平居中 */
}

.el-scrollbar .el-scrollbar__wrap {
  overflow-x: auto; /* 允许横向滚动 */
  height: calc(100% + 20px); /* 额外高度用于显示横向滚动条 */
}

.el-scrollbar .el-scrollbar__view {
  white-space: nowrap; /* 确保内容在一行内显示 */
  display: inline-block; /* 防止内容换行 */
} 

</style>