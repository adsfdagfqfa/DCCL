<template>
  <div>
    <div v-for="item in modelList" :key="item.userData.name" @click="setSelectedElement(item.userData.name)">
      <el-card class="box-card">
        <div slot="header" class="clearfix">
          <span>{{item.userData.name}}</span>
          <el-button style="float: right; padding: 3px 0" type="text">
            <el-dropdown @command="handleCommand">
              <span class="el-dropdown-link">
                <el-icon size="20"><Edit /></el-icon>
              </span>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item command="edit">编辑</el-dropdown-item>
                <el-dropdown-item command="delete">删除</el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
          </el-button>
        </div>
        <div>
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
          <el-row>
            <el-col :span="12">
              <span>模型旋转</span>
            </el-col>
            <el-col :span="12">
              <span>{{item.rotation.x}},{{item.rotation.y}},{{item.rotation.z}}</span>
            </el-col>
          </el-row>
        </div>
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
</script>

<style scoped>

</style>