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
      />
    </div>
    <div class="flex items-center mb-5">
      <label class="whitespace-nowrap min-w-20">中间数量:</label>
      <el-input
        type="number"
        id="count"
        v-model.number="count"
        placeholder="介于最小值与最大值之间的取值数量"
        @blur="generateArray"
      />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';


    
const minValue=ref(null)
const maxValue=ref(null)
const count=ref(null) 
const emit = defineEmits(['getResultArray']);
   
function generateArray() {
  if (minValue.value === null ||
    maxValue.value === null ||
    count.value === null)
    return;
  if(minValue.value >= maxValue.value || count.value< 0) {
    alert("请输入有效的最小值、最大值和中间数量！");
    return;
  }

  const step = (maxValue.value - minValue.value) / count.value;
  const resultArray = [];
  for (let i = 0; i < count.value; i++) {
    resultArray.push(minValue.value + i * step);
  }
  
  emit('getResultArray', resultArray);
}


// function sendMessage() {
//   emit('message-sent', 'Hello from Child');
// }
</script>

<style scoped>

</style>