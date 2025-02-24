<template>
 
    <el-scrollbar  max-height="300px" class="h-full">
      <el-card >
        <div class="flex flex-col">
          <span class="font-bold whitespace-nowrap min-w-36 text-xl">谐振腔参数</span>
          <div class="h-3"></div><!-- 用于占位 -->
          <div v-for="(value, key) in resonatorParam" :key="key" >
            <div class="flex"> 
              <label class="no-wrap font-bold min-w-40"  :for="key">{{keyMappings[key] }} </label>
              <el-input type='number' 
                        style="width:240px"  
                        v-model.number="resonatorParam[key]" 
                        placeholder="请输入" 
                        @change="handleChange"
                        title=""/>
            </div>
          </div>
        </div>
      </el-card>
      <br>
      <el-card >
        <div class="flex flex-col">
          <span class="font-bold whitespace-nowrap min-w-36 text-xl">快速傅里叶变换(FFT)参数</span>
          <div class="h-3"></div><!-- 用于占位 -->
          <div v-for="(value, key) in fastFTParam" :key="key" >
            <div class="flex"> 
              <label class="no-wrap font-bold min-w-40"  :for="key">{{keyMappings[key] }} </label>
              <el-input type='number' 
                        style="width:240px"  
                        v-model.number="fastFTParam[key]"  
                        placeholder="请输入" 
                        @change="handleChange"
                        title=""/>
            </div>
          </div>
        </div>
      </el-card>
    </el-scrollbar>
  
</template>

<script setup>
// import { constant } from '@/utils/constant/constant';
import { keyMappings } from '@/utils/constant/model';
import { useThreeInstanceStore } from '@/store';
import { computed, handleError } from 'vue';
const store = useThreeInstanceStore();
const resonatorParam = computed(()=>store.resonatorParam);
const fastFTParam = computed(()=>store.fastFourierTransformParam);
function handleChange(){
  console.log(resonatorParam.value)
  console.log(fastFTParam.value)
}

</script>

<style scoped>

</style>