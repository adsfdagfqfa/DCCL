import * as THREE from 'three';
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";
import { ModelFactory } from "@/utils/modelFactory/modelFactory"
import { onlyKey } from './utilityFunction';

export default class threeInstance {
    constructor(id) {
        this.id = id;
        //绑定的元素
        this.dom = document.getElementById(id);
        //相机
        this.camera2D=null;
        this.camera3D=null;
        this.currentCamera=null;
        //相机初始位置
        this.initialCameraPosition=new THREE.Vector3(300,0,50);
        // 控制器
        this.controls=null;
        //场景
        this.scene=null;
        //渲染器
        this.renderer=null;
        // 创建一个组，用于管理模型
        this.group = new THREE.Group();
        this.model=null;
        this.modelList=[]
        this.initialModelPosition=new THREE.Vector3(0,0,0);
        // 坐标轴辅助线
        this.axesHelper=null;
        // 环境光
        this.ambientLight=null;  
        // 鼠标位置
        this.mousePosition = new THREE.Vector2();
        // 碰撞检测
        this.raycaster = new THREE.Raycaster();
        //显示辉光
        this.glowModelList=[];
        // 拖拽模型
        this.dragModel={}
        //模型属性列表
        this.modelAttributeList=[]
    }
    init() {
        this.initScene();
        this.initCamera();
        this.initRender();
        this.initControls();
        
        this.initaxesHelper();
        this.addLight();
        //窗口改变时场景适配
        window.addEventListener('resize', () => {
            this.currentCamera.aspect = this.dom.offsetWidth / this.dom.offsetHeight;
            this.currentCamera.updateProjectionMatrix();
            this.renderer.setSize(this.dom.offsetWidth, this.dom.offsetHeight);
        });     
    }
    // 创建场景
    initScene() {
        this.scene = new THREE.Scene();
        
    }
    // 创建相机
    initCamera() {
        //相机
        //透视相机,各参数含义,视野角度,宽高比,近端面,远端面
        this.camera3D = new THREE.PerspectiveCamera(75, this.dom.offsetWidth / this.dom.offsetHeight, 0.1, 1000);
        //正交相机,各参数含义,左侧面,右侧面,上侧面,下侧面,近端面,远端面
        this.camera2D = new THREE.OrthographicCamera(this.dom.offsetWidth / -2, 
                                                    this.dom.offsetWidth / 2,  
                                                    this.dom.offsetHeight / 2, 
                                                    this.dom.offsetHeight / -2, 0.1, 1000);
        this.currentCamera=this.camera2D
        // this.currentCamera.position = new THREE.Vector3(this.dom.offsetWidth/2-100,0,10)
        this.currentCamera.position.x=this.dom.offsetWidth/2-100
     
        this.currentCamera.position.z=50
        // this.currentCamera.lookAt(new THREE.Vector3(0,0,0))
        console.log(this.currentCamera.position)
        
       
    }
    //创建渲染器
    initRender() {
        this.renderer = new THREE.WebGLRenderer({ antialias: true }); //设置抗锯齿
        //设置屏幕像素比
        this.renderer.setPixelRatio(window.devicePixelRatio);
        //渲染的尺寸大小
        this.renderer.setSize(this.dom.offsetWidth, this.dom.offsetHeight);
        // 设置为浅灰色
        this.renderer.setClearColor(0xcfcfcf); 
        this.dom.appendChild(this.renderer.domElement);
    }
    //创建控制器
    initControls(){
        this.controls = new OrbitControls(this.currentCamera, this.renderer.domElement);
        //this.controls.target.set(0, 0, 0);
    }
    //创建坐标
    initaxesHelper(){
        // 坐标轴辅助线
        this.axesHelper = new THREE.AxesHelper(1000);//100为其长度
        // this.axesHelper.visible = false;
        this.scene.add(this.axesHelper);
    }
    setupScene() {
        // this.addLight();
        // this.addMirrors(-10);
        // this.addLenses(20);
        // this.addGainMedium(30);
    }
    addLight() {
        const ambientLight = new THREE.AmbientLight(0x404040);
        this.scene.add(ambientLight);
        const directionalLight = new THREE.DirectionalLight(0xffffff, 0.5);
        directionalLight.position.set(-1, 2, 4).normalize();
        this.scene.add(directionalLight);
    }
    // 切换相机的函数
    switchCamera(cameraType) {
        console.log (cameraType);
        if ( cameraType === '2D' ) {
            this.currentCamera = this.camera2D;
            
            this.resetCameraToNegativeZ()
            console.log(this.currentCamera.position)
            this.controls.object = this.camera2D;
            this.controls.enableRotate = false; // 禁用旋转
            this.controls.enableZoom = true; // 启用缩放
            //将其左键设计为平移
            this.controls.mouseButtons = { LEFT: THREE.MOUSE.PAN, MIDDLE: THREE.MOUSE.DOLLY, RIGHT: THREE.MOUSE.PAN };
        } 
        else if ( cameraType==='3D' ) {
            this.currentCamera = this.camera3D;
            
            this.resetCameraToNegativeZ();
            this.controls.object = this.camera3D;
            this.controls.enableRotate = true; // 启用旋转
            this.controls.enableZoom = true; // 启用缩放
            this.controls.mouseButtons = { LEFT: THREE.MOUSE.ROTATE, MIDDLE: THREE.MOUSE.DOLLY, RIGHT: THREE.MOUSE.PAN };
        }
        //this.controls.update();
    } 
    //重置相机位置，并使其对准Z轴负半轴
    resetCameraToNegativeZ() {
        
        this.controls.target.set(0, 0, 0);
        this.currentCamera.position.set(this.initialCameraPosition.x,this.initialCameraPosition.y,this.initialCameraPosition.z);
        const direction = new THREE.Vector3(0, 0, -1); // Z轴负半轴方向
        this.currentCamera.lookAt(this.initialCameraPosition.clone().add(direction)); // 相机沿指定方向看
    }
    //保存拖拽的模型的相应参数
    setDragModel(model){
        //实现深拷贝
        this.dragModel=JSON.parse(JSON.stringify(model))
        console.log(this.dragModel)
    }
    setModelList(mesh) {
      mesh.traverse(v => {
        if (!v.isMesh) return;
        this.modelList.push(v);
        this.modelAttributeList.push(v.userData.attribute)
      });
    }
    //放置模型
    setModel(model){
        return new Promise((resolve) => {
            // 创建几何体
            console.log(model)
            const mesh = ModelFactory.createModel(model.type);
            //初始位置
            
            mesh.position.copy(this.initialModelPosition);
            
            // mesh.userData.attribute.model = model.type + "_" + onlyKey(5,10);
            mesh.userData.attribute=model
            mesh.userData.attribute.model=model.type + "_" + onlyKey(4,10)

            this.group.add(mesh);
            this.model = this.group;
            //获取模型的数组
            this.setModelList(mesh);
            // console.log(this.modelAttributeList)
            //储存对应的名字
            this.scene.add(this.model);
            // //计算控制器缩放大小
            // const box = new THREE.Box3().setFromObject(this.model);
            // const size = box.getSize(new THREE.Vector3());
            // this.controls.maxDistance = size.length() * 10;
            console.log(mesh.userData)
            resolve(true);
        });
    }
    
    //添加模型
    addModel(model){
        return new Promise(async (resolve, reject) => {
            try {
                // 加载模型
                if (model.type) {
                    console.log(model.type)
                    await this.setModel(model);
                    //this.outlinePass.renderScene = this.geometryGroup;
                    resolve();
                } 
            } catch (err) {
                console.log("Error:" ,err);
                reject();
            }
        });
    }
    deleteModel(name){
      //移除对应模型
      let model = this.modelList.find(v => v.userData.attribute.model === name);
      if (model.geometry) {
        console.log("model.geometry")
        model.geometry.dispose();
      }
      // 清理材质
      if (model.material) {
        console.log("model.material")
        if (Array.isArray(model.material)) {
          model.material.forEach(mat => {
            mat.dispose();
            if (mat.map) mat.map.dispose();
          });
        } else {
          model.material.dispose();
          if (model.material.map) model.material.map.dispose();
        }
      }
      this.group.remove(model);
      // this.modelList=this.modelList.filter(v => v.userData.attribute.model !== name);
      // this.modelAttributeList=this.modelAttributeList.filter(v => v.model !== name);
      //使用filter删除数组中的元素，会生成一个新的数组，进而导致代码中其他引用该数组的地方出现问题，不能及时更新
      //使用splice删除数组中的元素，会直接删除数组中的元素，不会生成新的数组，不会导致其他引用该数组的地方出现问题
      // 删除 modelList 中 userData.attribute.model 等于 name 的元素
      for (let i = this.modelList.length - 1; i >= 0; i--) {
        if (this.modelList[i].userData.attribute.model === name) {
          this.modelList.splice(i, 1); // 删除当前索引的元素
          break;
        }
      }
      for (let i = this.modelAttributeList.length - 1; i >= 0; i--) {
        if (this.modelAttributeList[i].model === name) {
          this.modelAttributeList.splice(i, 1); // 删除当前索引的元素
          break;
        }
      }
      console.log("删除元素",this.modelList)
      console.log("删除元素",this.modelAttributeList)
    }
    clearAllModel(){
        //清除所有模型
        this.modelList.forEach(model => {
            if (model.geometry) {
                model.geometry.dispose();
            }
            if (model.material) {
                if (Array.isArray(model.material)) {
                    model.material.forEach(mat => {
                        mat.dispose();
                        if (mat.map) mat.map.dispose();
                    });
                } else {
                    model.material.dispose();
                    if (model.material.map) model.material.map.dispose();
                }
            }
            this.group.remove(model);
        });
        //直接赋值[]不会被响应式更新
        this.modelList.splice(0, this.modelList.length); // 清空数组
        this.modelAttributeList.splice(0, this.modelAttributeList.length); // 清空数组
        //this.scene.remove(this.group);
    }
    // 动画循环
    animate = () => {
        requestAnimationFrame(this.animate);
        if (this.controls.enabled) {
            this.controls.update(); // 更新轨道控制器
        }
        if(this.currentCamera===this.camera2D){
            // console.log(this.currentCamera.position)
            var  direction = new THREE.Vector3(0, 0, -100); // Z轴负半轴方向
            this.currentCamera.lookAt(this.currentCamera.position.clone().add(direction)); // 相机沿指定方向看
        }
        this.renderer.render(this.scene, this.currentCamera);
    }
}

