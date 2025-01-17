<template>
  <div class="menu-bar">
    <MenuBar title="开始" @click="handleClick('开始')"></MenuBar>
    <MenuBar title="文件" @click="handleClick('文件')">
      <SubMenu>
          <MenuItem title="新建" @click="handleClick('新建')">
            <SubMenu>
              <MenuItem title="xx" @click="handleClick('xx')">
                <SubMenu>
                  <MenuItem title="11" @click="handleClick('11')"></MenuItem>
                  <MenuItem title="22" @click="handleClick('22')"></MenuItem>
                <!-- 更多文件菜单项 -->
                </SubMenu>
              </MenuItem>  
              <MenuItem title="aa" @click="handleClick('aa')">
                <SubMenu>
                  <MenuItem title="sss" @click="handleClick('sss')"></MenuItem>
                  <MenuItem title="ss" @click="handleClick('ss')"></MenuItem>
                <!-- 更多文件菜单项 -->
                </SubMenu>
              </MenuItem>
              <!-- 更多文件菜单项 -->
            </SubMenu>
          </MenuItem>
          <MenuItem title="打开" @click="handleClick('打开')">
            <SubMenu>
              <MenuItem title="11" @click="handleClick('11')"></MenuItem>
              <MenuItem title="22" @click="handleClick('22')"></MenuItem>
              <!-- 更多文件菜单项 -->
            </SubMenu>
          </MenuItem>
          <!-- 更多文件菜单项 -->
      </SubMenu>
    </MenuBar>
    <MenuBar title="编辑" @click="handleClick('编辑')">
      <SubMenu>
          <MenuItem title="撤销" @click="handleClick('撤销')"></MenuItem>
          <MenuItem title="重做" @click="handleClick('重做')"></MenuItem>
          
          <!-- 更多编辑菜单项 -->
      </SubMenu>
    </MenuBar>
    <!-- 更多菜单项 -->
  </div>
</template>

<script setup>

import MenuBar from '@/components/menu/menuBar.vue';
import MenuItem from '@/components/menu/menuItem.vue';
import SubMenu from '@/components/menu/subMenu.vue';
function handleClick(title) {
  console.log(`Clicked on: ${title}`);
}
   
</script>

<style scoped>
.menu-bar {
  display: flex;
  background-color: #f8f8f8;
  border-bottom: 1px solid #ddd;
}
</style>