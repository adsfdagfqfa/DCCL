<template>
  <div>
    <!-- <div v-for="item in modelList" :key="item.userData.name" @click="setSelectedElement(item.userData.name)"> -->

    <div>
      <el-card>
       
          <!-- <div>
            <span>{{item.userData.name}}</span>
          </div> --> 
          
          
          
          
          <el-scrollbar   class="height-full">
            <div class="flex items-center">
              <span class="font-bold whitespace-nowrap min-w-36">模型元素(element)</span>
              <div v-for="item in modelList" :key="item.userData.name" class="flex-item">
                <span>{{ item.userData.name }}</span>
              </div>
            </div>
           
            <div>
              <div class="flex items-center">
                <span class="font-bold whitespace-nowrap min-w-36">距离(distance)</span>
                <div class="w-[100px]"></div><!-- 用于占位 -->
                <div v-for="(d,index) in distance" :key="index" class="flex-item">
                  <span>{{ d }}</span>
                </div>
              </div>
            </div> 
            <div>
              <div class="flex items-center">
                <span class="font-bold whitespace-nowrap min-w-36">角度(angle)</span>
                <div class="w-[100px]"></div>
                <div v-for="(a,index) in angle" :key="index" class="flex-item">
                  <span>{{ a }}</span>
                </div>
              </div>
            </div> 
          </el-scrollbar>
            
         
        
        
        <!-- <div>
          <el-row>
            <el-col :span="12">
              <span>模型类型</span>
            </el-col>
            <el-col :span="12">
              <span>{{item.userData.type}}</span>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="12">
              <span>模型位置</span>
            </el-col>
            <el-col :span="12">
              <span>{{item.position.x}},{{item.position.y}},{{item.position.z}}</span>
            </el-col>
          </el-row>
        </div> -->
      </el-card>
      
    </div>
  </div>
</template>

<script setup>
import { Edit,Delete,Location } from '@element-plus/icons-vue';
import { computed } from 'vue';
import { useThreeInstanceStore } from '@/store';
const store = useThreeInstanceStore();

const modelList = computed(() => store.threeInstance?.modelList);
const distance = computed(() => store.distance);
const angle = computed(() => store.angle);
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