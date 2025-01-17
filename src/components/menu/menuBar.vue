<template>
  <div class="menu-bar px-6 py-3 cursor-pointer relative" >
    {{title}}
    <slot></slot> <!-- 用于插入子菜单 -->
  </div>
</template>
  
<script setup>

const props = defineProps(['title'])
const {title} = props;
</script>

<style scoped>

</style>