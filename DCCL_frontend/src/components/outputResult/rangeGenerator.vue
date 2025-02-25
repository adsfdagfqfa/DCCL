<template>
  <div>
    <div class="flex items-center mb-5" >
      <label class="whitespace-nowrap min-w-20">最小值:</label>
      <el-input
        class="w-10"
        type="number"
        id="minValue"
        v-model.number="minValue"
        placeholder="请输入最小值"
        @blur="generateArray"
        title=""
      />
    </div>
    <div class="flex items-center mb-5">
      <label class="whitespace-nowrap min-w-20">最大值:</label>
      <el-input
        type="number"
        id="maxValue"
        v-model.number="maxValue"
        placeholder="请输入最大值"
        @blur="generateArray"
        title=""
      />
    </div>
    <div class="flex items-center mb-5">
      <label class="whitespace-nowrap min-w-20">步长:</label>
      <el-input
        type="number"
        id="step"
        v-model.number="step"
        placeholder="请输入步长"
        @blur="generateArray"
        title=""
      />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { round } from 'lodash';

    
const minValue=ref(null)
const maxValue=ref(null)
const step=ref(null) 
const emit = defineEmits(['getResultArray']);
   
function generateArray() {
  if (minValue.value === null ||
    maxValue.value === null ||
    step.value === null)
    return;
  if(minValue.value >= maxValue.value || step.value<= 0) {
    alert("请输入有效的最小值、最大值和步长！");
    return;
  }

  
  const resultArray = [];
  for(let i = minValue.value; i <= maxValue.value; i += step.value) {
    let rounded_numbers = round(i, 4) 
    resultArray.push(rounded_numbers);
  }
  
  emit('getResultArray', resultArray);
}


// function sendMessage() {
//   emit('message-sent', 'Hello from Child');
// }
</script>

<style scoped>

</style>