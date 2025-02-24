<template>
  <div class="sub-menu">
    <slot></slot> <!-- 用于插入子菜单项 -->
  </div>
</template>
  
<script setup>

</script>
  
<style scoped>

.sub-menu {
  display: none;
  position: absolute;
  background-color: #fff;
  z-index:1000; /*保证可以渲染到外面,不会被遮挡 */
  box-shadow: 0 2px 5px rgba(0,0,0,0.2);
  top: 0; /* 位于 .menu-item 的底部 */
  left: 100%; /* 与 .menu-item 的左侧对齐 */
}

.menu-item:hover > .sub-menu {
  display: block;
}

.menu-bar:hover > .sub-menu {
  display: block;
}

.menu-bar > .sub-menu {
  top: 100%; /* 位于 .menu-item 的底部 */
  left: 0; /* 与 .menu-item 的左侧对齐 */
}

.menu-item > .sub-menu {
  top: 0; /* 位于 .menu-item 的顶部 */
  left: 100%; /* 与 .menu-item 的右侧对齐 */
}
</style>