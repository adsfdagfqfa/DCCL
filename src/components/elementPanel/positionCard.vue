<template>
    <!-- 模型位置 -->
     <div class="flex flex-col">
    <div class="flex items-center">
        <el-icon size="20"><Location /></el-icon>
        <span> 模型位置 </span>
    </div>
    <div>
        <div>
            <el-button type="primary" link>X 轴</el-button>
        </div>
        <div>
            <el-slider  />
        </div>
    </div>
    <div >
        <div >
            <el-button type="primary" link>Y 轴</el-button>
        </div>
        <div>
            <el-slider />
        </div> 
    </div></div>
</template>

<script setup>
import {Location} from '@element-plus/icons-vue'
</script>
<style scoped>

</style>
