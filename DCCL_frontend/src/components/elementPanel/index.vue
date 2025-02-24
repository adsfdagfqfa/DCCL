<template>
    <!-- <div>
      
      <h3 style="font-weight: bold;">Inspector</h3>
      <div>
        <Card :item="store.getters.selectedElement" @update:component="updateComponent"></Card>
      </div>
    </div> -->
  <el-scrollbar max-height="400px">
    <AttributeCard></AttributeCard>
  </el-scrollbar>
    
</template>

<script setup>

import AttributeCard from './attributeCard.vue';


</script>

<style scoped>


</style>