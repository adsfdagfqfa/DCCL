<template>
  <router-view></router-view>
</template>

<script setup>
import { RouterView, useRoute, useRouter } from 'vue-router';
import { useThreeInstanceStore } from './store/index.js';
import { onMounted } from 'vue';
const store = useThreeInstanceStore();
const router =useRouter()
onMounted(() => {
  store.initToken()
  console.log('App mounted');
})
</script>


<style scoped>

</style>
