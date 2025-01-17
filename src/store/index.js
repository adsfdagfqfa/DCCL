// store.js
import { createStore } from 'vuex';

const store =createStore({
  state: {
    threeInstance: null,
    components:[],
    selectedElement: null//当前选择的元素
  },
  mutations: {//同步
    setThreeInstance(state, instance) {
      state.threeInstance = instance;
    },
    addComponent(state,componentData){
      state.components.push(componentData)
      switch(componentData.type){
        case 'Mirror':
          if (state.threeInstance) {
            state.threeInstance.addMirrors(componentData.position.x,componentData); 
          }
          break;
        case 'Lens':
          if (state.threeInstance) {
            state.threeInstance.addLenses(componentData.position.x,componentData); 
          }
          break;
        case 'Medium':
          if (state.threeInstance) {
            state.threeInstance.addMedium(componentData.position.x,componentData); 
          }
          break;
        
      }
    },
    updateComponent(state, updates ) {
      const component = state.components.find(comp => comp.id === updates.id && comp.type === updates.type);
      if (component) {
        Object.assign(component, updates);//更新内容
      }
      
      if (state.threeInstance) {
        state.threeInstance.updateComponent(updates.type,updates.id,updates.position); 
      }
    },
    removeComponent(state, {id,type}) {
      state.components = state.components.filter(comp => !(comp.id === id && comp.type === type));
      if (state.threeInstance) {
        state.threeInstance.removeComponent(type,id); 
      }
    },
    updateSelected(state, {id, type}){
      const component = state.components.find(comp => comp.id === id && comp.type === type);
      
      if (component) {
        state.selectedElement=component; 
      }
    },
    switchCamera(state,type){
      if (state.threeInstance) {
        state.threeInstance.switchCamera(type); 
      }
    }
    // addMirrors(state,x){
    //     if (state.threeInstance) {
    //         state.threeInstance.addMirrors(x); 
    //     }
    // },
    // addLenses(state,x){
    //     if (state.threeInstance) {
    //         state.threeInstance.addLenses(x); 
    //     }
    // },
    // addGainMedium(state,x){
    //     if (state.threeInstance) {
    //         state.threeInstance.addGainMedium(x); 
    //     }
    // },
    
  },
  actions: {//异步
    updateThreeInstance({ commit }, instance) {
      commit('setThreeInstance', instance);
    },
    addComponent({ commit }, componentData) {
      commit('addComponent', componentData);
    },
    updateComponent({ commit }, updates ) {
      commit('updateComponent', updates );
    },
    removeComponent({ commit }, {id,type}) {
      commit('removeComponent', {id,type});
    },
    updateSelected({commit},{id,type}){
      commit('updateSelected',{ id,type});
    },
    switchCamera({commit},type){
      commit('switchCamera',type);
    }
    
  },
  getters:{
    selectedElement(state){
      if(state.selectedElement){
        return state.selectedElement;
      }
    }
  }
});
export default store;