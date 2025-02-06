<template>
    <!-- <div>
      
      <h3 style="font-weight: bold;">Inspector</h3>
      <div>
        <Card :item="store.getters.selectedElement" @update:component="updateComponent"></Card>
      </div>
    </div> -->
  <div class="flex flex-col">
    <AttributeCard></AttributeCard>
    <PositionCard></PositionCard>
  </div>
    
</template>

<script setup>
import PositionCard from './positionCard.vue';
import AttributeCard from './attributeCard.vue';


</script>

<style scoped>


</style>